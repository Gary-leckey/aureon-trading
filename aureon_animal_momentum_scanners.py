"""
Alpaca animal-themed momentum scanners

Provides:
- AlpacaLoneWolf: momentum sniper (fast single-target decisions)
- AlpacaLionHunt: multi-target hunter (prioritize high momentum × volume prey)
- AlpacaArmyAnts: small-profit foraging (many small trades)
- AlpacaHummingbird: micro-rotation pollinator (ETH-quoted rotations)
- AlpacaSwarmOrchestrator: coordinates the above agents using AlpacaScannerBridge

This is a *smoke-first* implementation focusing on readability and safe dry-run behavior.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from alpaca_client import AlpacaClient
from alpaca_fee_tracker import AlpacaFeeTracker
from aureon_alpaca_scanner_bridge import AlpacaScannerBridge

logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.WARNING)


@dataclass
class AnimalOpportunity:
    symbol: str
    side: str  # 'buy' or 'sell'
    move_pct: float
    net_pct: float
    volume: float
    reason: str = ""


class BaseAnimalScanner:
    def __init__(self, alpaca: AlpacaClient, bridge: AlpacaScannerBridge):
        self.alpaca = alpaca
        self.bridge = bridge

    def _get_crypto_universe(self) -> List[str]:
        # Prefer bridge cached list if available; else query Alpaca
        if self.bridge and self.bridge._crypto_universe:
            return sorted(list(self.bridge._crypto_universe))

        assets = self.alpaca.list_assets(status='active', asset_class='crypto') or []
        syms = []
        for a in assets:
            sym = a.get('symbol') if isinstance(a, dict) else getattr(a, 'symbol', None)
            if sym:
                if '/' not in sym:
                    sym = f"{sym}/USD"
                syms.append(sym)
        return sorted(syms)


class AlpacaLoneWolf(BaseAnimalScanner):
    """Momentum sniper.

    - Scans universe for large, clean 24h moves
    - Prefers high net profit (after fees)
    - Returns top N immediate trade suggestions (dry-run safe)
    """

    def find_targets(self, limit: int = 10) -> List[AnimalOpportunity]:
        symbols = self._get_crypto_universe()
        results: List[AnimalOpportunity] = []

        for sym in symbols:
            try:
                resolved = sym
                if hasattr(self.alpaca, '_resolve_symbol'):
                    resolved = self.alpaca._resolve_symbol(sym)

                bars_resp = self.alpaca.get_crypto_bars([resolved], timeframe='1H', limit=24) or {}
                bars = bars_resp.get('bars', {}).get(resolved, []) if isinstance(bars_resp, dict) else []
                if not bars or len(bars) < 2:
                    continue

                first_price = float(bars[0].get('o', bars[0].get('open', 0)) or 0)
                last_price = float(bars[-1].get('c', bars[-1].get('close', 0)) or 0)
                if first_price <= 0 or last_price <= 0:
                    continue

                move_pct = ((last_price - first_price) / first_price) * 100.0
                vol = sum(float(b.get('v', b.get('volume', 0)) or 0) for b in bars)

                is_profitable, tier = self.bridge.is_move_profitable(abs(move_pct))
                net = self.bridge.calculate_net_profit(abs(move_pct))

                if not is_profitable:
                    continue

                side = 'buy' if move_pct < 0 else 'sell'
                reason = f"Wolf ({tier})"
                results.append(AnimalOpportunity(symbol=sym, side=side, move_pct=move_pct, net_pct=net, volume=vol, reason=reason))

            except Exception:
                continue

        # Sort by net profit then by volume
        results.sort(key=lambda x: (-(x.net_pct), -x.volume))
        return results[:limit]


class AlpacaLionHunt(BaseAnimalScanner):
    """Hunts a pride (subset) and chooses the best prey using composite score.

    Score = |24h move| * log(1 + volume) * coherence_weight
    """

    def score_symbol(self, sym: str) -> Optional[Tuple[float, AnimalOpportunity]]:
        try:
            resolved = sym
            if hasattr(self.alpaca, '_resolve_symbol'):
                resolved = self.alpaca._resolve_symbol(sym)

            bars_resp = self.alpaca.get_crypto_bars([resolved], timeframe='1H', limit=24) or {}
            bars = bars_resp.get('bars', {}).get(resolved, []) if isinstance(bars_resp, dict) else []
            if not bars or len(bars) < 2:
                return None

            first_price = float(bars[0].get('o', bars[0].get('open', 0)) or 0)
            last_price = float(bars[-1].get('c', bars[-1].get('close', 0)) or 0)
            if first_price <= 0 or last_price <= 0:
                return None

            move_pct = ((last_price - first_price) / first_price) * 100.0
            vol = sum(float(b.get('v', b.get('volume', 0)) or 0) for b in bars)
            is_profitable, tier = self.bridge.is_move_profitable(abs(move_pct))
            net = self.bridge.calculate_net_profit(abs(move_pct))

            # Coherence weight from change within last 5 bars (stability)
            last5 = bars[-5:]
            highs = [float(b.get('h', b.get('high', 0)) or 0) for b in last5]
            lows = [float(b.get('l', b.get('low', 0)) or 0) for b in last5]
            if not highs or not lows:
                coherence = 1.0
            else:
                var = (max(highs) - min(lows)) or 1.0
                coherence = 1.0 / (1.0 + var)

            # Only consider profitable opportunities
            if not is_profitable:
                return None

            score = abs(move_pct) * math.log(1 + vol + 1.0) * (coherence * 2.0)
            side = 'buy' if move_pct < 0 else 'sell'
            opp = AnimalOpportunity(symbol=sym, side=side, move_pct=move_pct, net_pct=net, volume=vol, reason=f"Lion ({tier})")
            return score, opp
        except Exception:
            return None

    def hunt(self, limit: int = 10) -> List[AnimalOpportunity]:
        symbols = self._get_crypto_universe()
        scored = []
        for s in symbols:
            r = self.score_symbol(s)
            if r:
                scored.append(r)
        scored.sort(key=lambda x: -x[0])
        return [opp for _, opp in scored[:limit]]


class AlpacaArmyAnts(BaseAnimalScanner):
    """Forage for small profits across many liquid pairs.

    - Targets small moves (>= valid threshold) with high liquidity
    - Returns small allocation opportunities
    """

    def forage(self, max_targets: int = 20) -> List[AnimalOpportunity]:
        symbols = self._get_crypto_universe()
        results: List[AnimalOpportunity] = []

        for sym in symbols:
            try:
                resolved = sym
                if hasattr(self.alpaca, '_resolve_symbol'):
                    resolved = self.alpaca._resolve_symbol(sym)

                bars_resp = self.alpaca.get_crypto_bars([resolved], timeframe='1H', limit=6) or {}
                bars = bars_resp.get('bars', {}).get(resolved, []) if isinstance(bars_resp, dict) else []
                if not bars or len(bars) < 2:
                    continue

                first_price = float(bars[0].get('o', bars[0].get('open', 0)) or 0)
                last_price = float(bars[-1].get('c', bars[-1].get('close', 0)) or 0)
                if first_price <= 0 or last_price <= 0:
                    continue

                move_pct = ((last_price - first_price) / first_price) * 100.0
                vol = sum(float(b.get('v', b.get('volume', 0)) or 0) for b in bars)
                is_profitable, tier = self.bridge.is_move_profitable(abs(move_pct))
                net = self.bridge.calculate_net_profit(abs(move_pct))

                # Ants prefer small valid opportunities with big volume
                if is_profitable and abs(move_pct) <= (self.bridge.get_cost_thresholds().tier_1_hot_threshold * 1.5):
                    side = 'buy' if move_pct < 0 else 'sell'
                    results.append(AnimalOpportunity(symbol=sym, side=side, move_pct=move_pct, net_pct=net, volume=vol, reason=f"Ant (tier={tier})"))

            except Exception:
                continue

        results.sort(key=lambda x: -x.volume)
        return results[:max_targets]


class AlpacaHummingbird(BaseAnimalScanner):
    """Micro-rotation pollinator: rapid scalps on high-frequency momentum.

    Focuses on short-term (6h) momentum with tight profit targets.
    Best for catching quick reversals and micro-swings.
    """

    def pollinate(self, limit: int = 12) -> List[AnimalOpportunity]:
        symbols = self._get_crypto_universe()
        results: List[AnimalOpportunity] = []

        for s in symbols:
            try:
                resolved = s
                if hasattr(self.alpaca, '_resolve_symbol'):
                    resolved = self.alpaca._resolve_symbol(s)

                # Use 6h window for faster momentum detection
                bars_resp = self.alpaca.get_crypto_bars([resolved], timeframe='1H', limit=6) or {}
                bars = bars_resp.get('bars', {}).get(resolved, []) if isinstance(bars_resp, dict) else []
                if not bars or len(bars) < 2:
                    continue

                first_price = float(bars[0].get('o', bars[0].get('open', 0)) or 0)
                last_price = float(bars[-1].get('c', bars[-1].get('close', 0)) or 0)
                if first_price <= 0 or last_price <= 0:
                    continue

                move_pct = ((last_price - first_price) / first_price) * 100.0
                vol = sum(float(b.get('v', b.get('volume', 0)) or 0) for b in bars)

                is_profitable, tier = self.bridge.is_move_profitable(abs(move_pct))
                net = self.bridge.calculate_net_profit(abs(move_pct))

                # Hummingbird prefers quick, moderate moves (not extreme)
                thresholds = self.bridge.get_cost_thresholds()
                max_move = thresholds.tier_1_hot_threshold * 2.0  # Cap at 2x HOT
                if is_profitable and abs(move_pct) <= max_move:
                    side = 'buy' if move_pct < 0 else 'sell'
                    results.append(AnimalOpportunity(
                        symbol=s, side=side, move_pct=move_pct,
                        net_pct=net, volume=vol, reason=f"Hummingbird ({tier})"
                    ))
            except Exception:
                continue

        # Sort by net profit (best micro-trades first)
        results.sort(key=lambda x: -x.net_pct)
        return results[:limit]


class AlpacaSwarmOrchestrator:
    """Coordinates animal agents and can execute trades via trailing stops."""

    def __init__(self, alpaca: AlpacaClient, bridge: AlpacaScannerBridge):
        self.alpaca = alpaca
        self.bridge = bridge
        self.wolf = AlpacaLoneWolf(alpaca, bridge)
        self.lion = AlpacaLionHunt(alpaca, bridge)
        self.ants = AlpacaArmyAnts(alpaca, bridge)
        self.hummingbird = AlpacaHummingbird(alpaca, bridge)
        self.dry_run = True  # Safety default

    def run_once(self) -> Dict[str, List[AnimalOpportunity]]:
        """Run one orchestration cycle (dry-run safe).

        Returns a dict with results from each agent.
        """
        logger.info("Orchestrator: running single pass")
        out = {}
        out['wolf'] = self.wolf.find_targets(limit=8)
        out['lion'] = self.lion.hunt(limit=8)
        out['ants'] = self.ants.forage(max_targets=12)
        out['hummingbird'] = self.hummingbird.pollinate(limit=12)

        # Notify bridge of opportunities detected
        total = sum(len(v) for v in out.values())
        self.bridge._stats['opportunities_detected'] += total
        return out

    def execute_opportunity(self, opp: AnimalOpportunity, qty: float, use_trailing_stop: bool = True) -> Optional[Dict]:
        """Execute a trade for an opportunity with optional trailing stop.

        Args:
            opp: The opportunity to execute
            qty: Quantity to trade
            use_trailing_stop: Whether to use trailing stop (default True)

        Returns:
            Order result dict or None if dry-run / error
        """
        if self.dry_run:
            logger.info(f"[DRY-RUN] Would execute {opp.side} {qty} {opp.symbol} ({opp.reason})")
            return {'dry_run': True, 'symbol': opp.symbol, 'side': opp.side, 'qty': qty}

        try:
            if use_trailing_stop:
                result = self.bridge.execute_with_trailing_stop(
                    symbol=opp.symbol,
                    side=opp.side,
                    qty=qty,
                    trail_percent=2.0  # Default 2% trail
                )
            else:
                result = self.alpaca.place_market_order(opp.symbol, opp.side, qty)

            logger.info(f"Executed {opp.side} {qty} {opp.symbol}: {result}")
            return result
        except Exception as e:
            logger.error(f"Execution failed for {opp.symbol}: {e}")
            return None

    def get_best_opportunity(self) -> Optional[AnimalOpportunity]:
        """Get the single best opportunity across all agents."""
        results = self.run_once()
        all_opps = []
        for agent_opps in results.values():
            all_opps.extend(agent_opps)

        if not all_opps:
            return None

        # Sort by net profit
        all_opps.sort(key=lambda x: -x.net_pct)
        return all_opps[0]


def main(dry_run: bool = True):
    alpaca = AlpacaClient()
    fee_tracker = AlpacaFeeTracker(alpaca)
    bridge = AlpacaScannerBridge(alpaca_client=alpaca, fee_tracker=fee_tracker, enable_sse=False, enable_stocks=False)

    orch = AlpacaSwarmOrchestrator(alpaca, bridge)
    results = orch.run_once()

    print("\n=== SWARM SUMMARY ===")
    for k, v in results.items():
        print(f"\n{k.upper()}: {len(v)} targets")
        for i, opp in enumerate(v[:8], 1):
            print(f" {i:2}. {opp.symbol:12} {opp.side:4} {opp.move_pct:+6.2f}% net {opp.net_pct:+.3f}% {opp.reason}")

    print("\n✅ Swarm pass complete (dry-run: %s)" % str(dry_run))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    main(dry_run=True)
