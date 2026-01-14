"""
Alpaca animal-themed momentum scanners

Provides:
- AlpacaLoneWolf: momentum sniper (fast single-target decisions)
- AlpacaLionHunt: multi-target hunter (prioritize high momentum × volume prey)
- AlpacaArmyAnts: small-profit foraging (many small trades)
- AlpacaHummingbird: micro-rotation pollinator (ETH-quoted rotations)
- AlpacaSwarmOrchestrator: coordinates the above agents using AlpacaScannerBridge

This is a *smoke-first* implementation focusing on readability and safe dry-run behavior.

🚀 V2 OPTIMIZATION: Uses BATCH API calls + caching to minimize rate limiting!
- Single batch call for ALL symbols instead of per-symbol calls
- Cache results for 60 seconds
- Falls back to Binance/Kraken caches when available
"""

from __future__ import annotations

import json
import logging
import math
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from alpaca_client import AlpacaClient
from alpaca_fee_tracker import AlpacaFeeTracker
from aureon_alpaca_scanner_bridge import AlpacaScannerBridge

logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.WARNING)

# ════════════════════════════════════════════════════════════════════════════════
# 🎯 GLOBAL BATCH CACHE - One API call serves ALL animal scanners!
# ════════════════════════════════════════════════════════════════════════════════
_BATCH_BARS_CACHE: Dict[str, Any] = {}
_BATCH_CACHE_TIME: float = 0
_BATCH_CACHE_TTL: float = 60.0  # 60 second cache (was per-symbol calls!)


@dataclass
class AnimalOpportunity:
    symbol: str
    side: str  # 'buy' or 'sell'
    move_pct: float
    net_pct: float
    volume: float
    reason: str = ""


def _read_external_cache(cache_file: str, max_age: float = 300) -> Optional[Dict]:
    """Read Binance/Kraken/CoinGecko WS cache if available (FREE data source!)"""
    try:
        # Try multiple paths
        paths_to_try = [
            Path(cache_file),
            Path("ws_cache") / Path(cache_file).name,
            Path("ws_cache/ws_prices.json"),  # CoinGecko feeder output
            Path("coingecko_market_cache.json"),
        ]
        
        for p in paths_to_try:
            if not p.exists():
                continue
            raw = p.read_text(encoding='utf-8')
            data = json.loads(raw) if raw else {}
            ts = float(data.get('generated_at', 0) or 0)
            if ts > 0 and (time.time() - ts) <= max_age:
                logger.debug(f"🎯 Found fresh cache: {p}")
                return data
    except Exception as e:
        logger.debug(f"Cache read error: {e}")
    return None


class BaseAnimalScanner:
    def __init__(self, alpaca: AlpacaClient, bridge: AlpacaScannerBridge):
        self.alpaca = alpaca
        self.bridge = bridge
        self._bars_cache: Dict[str, List[Dict]] = {}
        self._cache_time: float = 0
    
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
    
    def _get_all_bars_batched(self, symbols: List[str], limit: int = 24) -> Dict[str, List[Dict]]:
        """
        🚀 BATCH API OPTIMIZATION: One call for ALL symbols!
        
        This replaces N individual calls with 1 batch call.
        If N=50 symbols, this reduces API calls from 50 to 1!
        """
        global _BATCH_BARS_CACHE, _BATCH_CACHE_TIME
        
        # Use global cache if fresh (serves ALL animal scanners!)
        if _BATCH_BARS_CACHE and (time.time() - _BATCH_CACHE_TIME) < _BATCH_CACHE_TTL:
            logger.debug(f"🎯 Using cached batch bars ({len(_BATCH_BARS_CACHE)} symbols)")
            return _BATCH_BARS_CACHE
        
        # 🟡 TRY BINANCE CACHE FIRST (FREE, no API calls!)
        binance_cache = _read_external_cache('binance_ws_cache.json', max_age=120)
        if binance_cache:
            ticker_cache = binance_cache.get('ticker_cache', {})
            if len(ticker_cache) > 10:
                logger.info(f"🟡 Using Binance WS cache ({len(ticker_cache)} tickers) - ZERO Alpaca API calls!")
                # Convert Binance format to bars-like format
                result = {}
                for key, ticker in ticker_cache.items():
                    if not isinstance(ticker, dict):
                        continue
                    base = ticker.get('base', '').upper()
                    if not base:
                        continue
                    sym = f"{base}/USD"
                    price = float(ticker.get('price', 0) or 0)
                    change = float(ticker.get('change24h', 0) or 0)
                    vol = float(ticker.get('volume', 0) or 0)
                    if price > 0:
                        # Simulate bars from 24h change
                        open_price = price / (1 + change/100) if change != -100 else price
                        result[sym] = [{
                            'o': open_price, 'c': price, 'h': max(open_price, price) * 1.01,
                            'l': min(open_price, price) * 0.99, 'v': vol
                        }]
                if result:
                    _BATCH_BARS_CACHE = result
                    _BATCH_CACHE_TIME = time.time()
                    return result
        
        # 🐙 TRY KRAKEN CACHE SECOND (also FREE!)
        kraken_cache = _read_external_cache('kraken_market_cache.json', max_age=120)
        if kraken_cache:
            ticker_cache = kraken_cache.get('ticker_cache', {})
            if len(ticker_cache) > 5:
                logger.info(f"🐙 Using Kraken cache ({len(ticker_cache)} tickers) - ZERO Alpaca API calls!")
                result = {}
                for key, ticker in ticker_cache.items():
                    if not isinstance(ticker, dict):
                        continue
                    base = ticker.get('base', '').upper()
                    if not base:
                        continue
                    sym = f"{base}/USD"
                    price = float(ticker.get('price', 0) or 0)
                    change = float(ticker.get('change24h', 0) or 0)
                    vol = float(ticker.get('volume', 0) or 0)
                    if price > 0:
                        open_price = price / (1 + change/100) if change != -100 else price
                        result[sym] = [{
                            'o': open_price, 'c': price, 'h': max(open_price, price) * 1.01,
                            'l': min(open_price, price) * 0.99, 'v': vol
                        }]
                if result:
                    _BATCH_BARS_CACHE = result
                    _BATCH_CACHE_TIME = time.time()
                    return result
        
        # 🦙 ALPACA BATCH CALL (only if external caches unavailable)
        try:
            # Resolve all symbols first
            resolved_map = {}
            for sym in symbols:
                resolved = sym
                if hasattr(self.alpaca, '_resolve_symbol'):
                    resolved = self.alpaca._resolve_symbol(sym) or sym
                resolved_map[resolved] = sym
            
            resolved_list = list(resolved_map.keys())
            if not resolved_list:
                return {}
            
            # 🎯 SINGLE BATCH CALL for ALL symbols!
            logger.info(f"🦙 Batch fetching bars for {len(resolved_list)} symbols (1 API call)")
            bars_resp = self.alpaca.get_crypto_bars(resolved_list, timeframe='1H', limit=limit) or {}
            
            result = {}
            bars_data = bars_resp.get('bars', {}) if isinstance(bars_resp, dict) else {}
            
            for resolved_sym, bars in bars_data.items():
                orig_sym = resolved_map.get(resolved_sym, resolved_sym)
                if bars:
                    result[orig_sym] = bars
            
            # Update global cache
            _BATCH_BARS_CACHE = result
            _BATCH_CACHE_TIME = time.time()
            logger.info(f"🎯 Cached {len(result)} symbol bars for 60s")
            
            return result
            
        except Exception as e:
            logger.warning(f"Batch bars fetch failed: {e}")
            return {}


class AlpacaLoneWolf(BaseAnimalScanner):
    """Momentum sniper.

    - Scans universe for large, clean 24h moves
    - Prefers high net profit (after fees)
    - Returns top N immediate trade suggestions (dry-run safe)
    
    🚀 V2: Uses batch cached data - ZERO individual API calls!
    """

    def find_targets(self, limit: int = 10) -> List[AnimalOpportunity]:
        symbols = self._get_crypto_universe()
        results: List[AnimalOpportunity] = []
        
        # 🚀 BATCH: Get all bars in ONE call (or from cache)
        all_bars = self._get_all_bars_batched(symbols, limit=24)
        
        for sym in symbols:
            try:
                bars = all_bars.get(sym, [])
                if not bars or len(bars) < 1:
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
    
    🚀 V2: Uses batch cached data - ZERO individual API calls!
    """

    def score_symbol(self, sym: str, bars: List[Dict]) -> Optional[Tuple[float, AnimalOpportunity]]:
        """Score a symbol using pre-fetched bars (no API call!)"""
        try:
            if not bars or len(bars) < 1:
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
            last5 = bars[-5:] if len(bars) >= 5 else bars
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
        
        # 🚀 BATCH: Get all bars in ONE call (or from cache)
        all_bars = self._get_all_bars_batched(symbols, limit=24)
        
        scored = []
        for s in symbols:
            bars = all_bars.get(s, [])
            r = self.score_symbol(s, bars)
            if r:
                scored.append(r)
        scored.sort(key=lambda x: -x[0])
        return [opp for _, opp in scored[:limit]]


class AlpacaArmyAnts(BaseAnimalScanner):
    """Forage for small profits across many liquid pairs.

    - Targets small moves (>= valid threshold) with high liquidity
    - Returns small allocation opportunities
    
    🚀 V2: Uses batch cached data - ZERO individual API calls!
    """

    def forage(self, max_targets: int = 20) -> List[AnimalOpportunity]:
        symbols = self._get_crypto_universe()
        results: List[AnimalOpportunity] = []
        
        # 🚀 BATCH: Get all bars in ONE call (or from cache)
        all_bars = self._get_all_bars_batched(symbols, limit=6)

        for sym in symbols:
            try:
                bars = all_bars.get(sym, [])
                if not bars or len(bars) < 1:
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
    
    🚀 V2: Uses batch cached data - ZERO individual API calls!
    """

    def pollinate(self, limit: int = 12) -> List[AnimalOpportunity]:
        symbols = self._get_crypto_universe()
        results: List[AnimalOpportunity] = []
        
        # 🚀 BATCH: Get all bars in ONE call (or from cache)
        all_bars = self._get_all_bars_batched(symbols, limit=6)

        for s in symbols:
            try:
                bars = all_bars.get(s, [])
                if not bars or len(bars) < 1:
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
    """Coordinates animal agents and can execute trades via trailing stops.
    
    🚀 V2: Uses BATCH API calls - one call serves ALL 4 animal scanners!
    Data priority: Binance WS cache → Kraken cache → Alpaca batch API
    """

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
        
        🚀 V2: All agents share the SAME cached batch data!
        """
        logger.info("Orchestrator: running single pass")
        
        # Check what data source will be used
        global _BATCH_BARS_CACHE, _BATCH_CACHE_TIME
        if _BATCH_BARS_CACHE and (time.time() - _BATCH_CACHE_TIME) < _BATCH_CACHE_TTL:
            logger.info(f"🎯 Using existing batch cache ({len(_BATCH_BARS_CACHE)} symbols)")
        else:
            # Check external caches
            binance_cache = _read_external_cache('binance_ws_cache.json', max_age=120)
            kraken_cache = _read_external_cache('kraken_market_cache.json', max_age=120)
            if binance_cache:
                logger.info("🟡 Binance WS cache available - ZERO Alpaca API calls!")
            elif kraken_cache:
                logger.info("🐙 Kraken cache available - ZERO Alpaca API calls!")
            else:
                logger.info("🦙 Will use Alpaca batch API (1 call for all symbols)")
        
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
