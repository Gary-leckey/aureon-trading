#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
🔮 PROBABILITY MATRIX SMOKE TEST - HISTORICAL REPLAY 🔮
═══════════════════════════════════════════════════════════════════════════════════════════

    "THE HIGHER SELF IS DIGGING INTO ITS PAST AND PULLING THAT PROBABILITY"

    This simulation replays the last 33 minutes of REAL market data through the
    Probability Nexus + Prime Sentinel Decree to prove the system works.

    We are RELIVING a universe where the system was alive - getting its results.

    Gary Leckey | 02.11.1991 | KEEPER OF THE FLAME

═══════════════════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

# ═══════════════════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════════════════

try:
    from aureon_probability_nexus import AureonProbabilityNexus, Prediction
    NEXUS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Probability Nexus not available: {e}")
    NEXUS_AVAILABLE = False

try:
    from prime_sentinel_decree import (
        PrimeSentinelDecree,
        FlameProtocol,
        THE_DECREE,
        SACRED_NUMBERS,
        DOB_HASH,
    )
    DECREE_AVAILABLE = True
except ImportError:
    DECREE_AVAILABLE = False
    print("⚠️ Prime Sentinel Decree not available")

# ═══════════════════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════════════════

# Simulation parameters
REPLAY_MINUTES = 60  # How far back to look (increased for warmup)
STARTING_CAPITAL = 100.0  # Starting with $100
POSITION_SIZE = 12.0  # $12 per scout (like the live system)
FEE_RATE = 0.0026  # 0.26% Kraken taker fee
WARMUP_CANDLES = 24  # Candles needed for warmup (reduced)

# Pairs to test
TEST_PAIRS = [
    'BTC-USD',
    'ETH-USD',
    'XRP-USD',
    'ADA-USD',
    'SOL-USD',
]

# ═══════════════════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════════════════

@dataclass
class SimulatedTrade:
    """A simulated trade from the replay"""
    timestamp: datetime
    pair: str
    direction: str  # 'LONG' or 'SHORT'
    entry_price: float
    exit_price: float
    size_usd: float
    pnl: float
    pnl_pct: float
    fees: float
    probability: float
    confidence: float
    reason: str
    duration_seconds: int
    outcome: str  # 'WIN' or 'LOSS'


@dataclass
class SimulationResult:
    """Results from the smoke test simulation"""
    start_time: datetime
    end_time: datetime
    duration_minutes: float
    starting_capital: float
    ending_capital: float
    total_pnl: float
    total_pnl_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_fees: float
    largest_win: float
    largest_loss: float
    avg_win: float
    avg_loss: float
    profit_factor: float
    trades: List[SimulatedTrade] = field(default_factory=list)
    pairs_analyzed: Dict[str, int] = field(default_factory=dict)
    signals_generated: int = 0
    signals_acted_on: int = 0


# ═══════════════════════════════════════════════════════════════════════════════════════════
# HISTORICAL DATA FETCHER
# ═══════════════════════════════════════════════════════════════════════════════════════════

class HistoricalDataFetcher:
    """Fetches historical 1-minute candle data from Coinbase"""
    
    BASE_URL = "https://api.exchange.coinbase.com"
    
    def fetch_candles(self, pair: str, minutes: int = 33) -> List[dict]:
        """
        Fetch historical 1-minute candles
        Returns list of candles: [timestamp, low, high, open, close, volume]
        """
        try:
            end = datetime.utcnow()
            start = end - timedelta(minutes=minutes + 5)  # Extra buffer
            
            url = f"{self.BASE_URL}/products/{pair}/candles"
            params = {
                'granularity': 60,  # 1-minute candles
                'start': start.isoformat(),
                'end': end.isoformat(),
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            raw_candles = response.json()
            
            # Convert to our format (API returns newest first)
            candles = []
            for c in reversed(raw_candles[-minutes:]):
                candles.append({
                    'timestamp': datetime.utcfromtimestamp(c[0]),
                    'low': float(c[1]),
                    'high': float(c[2]),
                    'open': float(c[3]),
                    'close': float(c[4]),
                    'volume': float(c[5]),
                })
            
            return candles
            
        except Exception as e:
            print(f"   ⚠️ Error fetching {pair}: {e}")
            return []
    
    def fetch_all_pairs(self, pairs: List[str], minutes: int = 33) -> Dict[str, List[dict]]:
        """Fetch candles for all pairs"""
        all_data = {}
        
        for pair in pairs:
            print(f"   📥 Fetching {pair}...")
            candles = self.fetch_candles(pair, minutes)
            if candles:
                all_data[pair] = candles
                print(f"      ✅ Got {len(candles)} candles")
            else:
                print(f"      ❌ No data")
            time.sleep(0.2)  # Rate limit courtesy
        
        return all_data


# ═══════════════════════════════════════════════════════════════════════════════════════════
# PROBABILITY MATRIX SMOKE TESTER
# ═══════════════════════════════════════════════════════════════════════════════════════════

class ProbabilityMatrixSmokeTester:
    """
    🔮 THE HIGHER SELF LOOKING INTO THE PAST 🔮
    
    Replays historical data through the Probability Nexus to prove
    what trades would have been made and their results.
    """
    
    def __init__(self, starting_capital: float = 100.0, position_size: float = 12.0):
        self.starting_capital = starting_capital
        self.position_size = position_size
        self.fee_rate = FEE_RATE
        
        # Initialize nexus for each pair (separate state)
        self.nexuses: Dict[str, AureonProbabilityNexus] = {}
        
        # Initialize decree if available
        self.decree = PrimeSentinelDecree() if DECREE_AVAILABLE else None
        
        # Track simulation state
        self.capital = starting_capital
        self.trades: List[SimulatedTrade] = []
        self.positions: Dict[str, dict] = {}  # Current open positions
        
        print()
        print("=" * 80)
        print("🔮 PROBABILITY MATRIX SMOKE TESTER INITIALIZED 🔮")
        print("=" * 80)
        print(f"   Starting Capital: ${starting_capital:.2f}")
        print(f"   Position Size: ${position_size:.2f}")
        print(f"   Fee Rate: {self.fee_rate * 100:.2f}%")
        if DECREE_AVAILABLE:
            print(f"   🔱 Prime Sentinel Decree: ACTIVE")
        print("=" * 80)
    
    def _get_nexus(self, pair: str) -> AureonProbabilityNexus:
        """Get or create nexus for pair"""
        if pair not in self.nexuses:
            self.nexuses[pair] = AureonProbabilityNexus()
        return self.nexuses[pair]
    
    def _warm_up_nexus(self, nexus: AureonProbabilityNexus, candles: List[dict], warm_up_count: int = 30):
        """Feed initial candles to warm up indicators"""
        for candle in candles[:warm_up_count]:
            nexus.update_history(candle)
    
    def _simulate_trade(
        self,
        pair: str,
        direction: str,
        entry_candle: dict,
        exit_candle: dict,
        prediction: Prediction
    ) -> SimulatedTrade:
        """
        Simulate a single trade from entry to exit
        """
        entry_price = entry_candle['close']
        exit_price = exit_candle['close']
        
        # Calculate P&L
        if direction == 'LONG':
            pnl_pct = (exit_price - entry_price) / entry_price * 100
        else:  # SHORT
            pnl_pct = (entry_price - exit_price) / entry_price * 100
        
        # Calculate fees (entry + exit)
        fees = self.position_size * self.fee_rate * 2
        
        # Calculate actual P&L in dollars
        gross_pnl = self.position_size * (pnl_pct / 100)
        net_pnl = gross_pnl - fees
        
        # Determine outcome
        outcome = 'WIN' if net_pnl > 0 else 'LOSS'
        
        # Calculate duration
        duration = int((exit_candle['timestamp'] - entry_candle['timestamp']).total_seconds())
        
        return SimulatedTrade(
            timestamp=entry_candle['timestamp'],
            pair=pair,
            direction=direction,
            entry_price=entry_price,
            exit_price=exit_price,
            size_usd=self.position_size,
            pnl=net_pnl,
            pnl_pct=pnl_pct,
            fees=fees,
            probability=prediction.probability,
            confidence=prediction.confidence,
            reason=prediction.reason,
            duration_seconds=duration,
            outcome=outcome
        )
    
    def run_simulation(
        self,
        historical_data: Dict[str, List[dict]],
        min_confidence: float = 0.15,  # Increased: need 15% confidence (7.5% edge)
        hold_candles: int = 5  # Increased: hold longer for bigger moves
    ) -> SimulationResult:
        """
        🔮 RUN THE SMOKE TEST SIMULATION 🔮
        
        Replays all historical data through the probability matrix
        and simulates trades based on signals.
        """
        print()
        print("=" * 80)
        print("🔮 BEGINNING HISTORICAL REPLAY - PULLING FROM THE PAST 🔮")
        print("=" * 80)
        
        all_trades = []
        signals_generated = 0
        signals_acted_on = 0
        pairs_analyzed = {}
        
        start_time = None
        end_time = None
        
        for pair, candles in historical_data.items():
            if len(candles) < WARMUP_CANDLES + 5:
                print(f"\n⚠️ {pair}: Not enough data ({len(candles)} candles, need {WARMUP_CANDLES + 5})")
                continue
            
            print(f"\n{'─' * 60}")
            print(f"📊 ANALYZING {pair}")
            print(f"{'─' * 60}")
            
            nexus = self._get_nexus(pair)
            pairs_analyzed[pair] = 0
            
            # Warm up with first candles
            self._warm_up_nexus(nexus, candles, WARMUP_CANDLES)
            print(f"   ✓ Warmed up with {WARMUP_CANDLES} candles")
            
            # Track start/end times
            if start_time is None or candles[WARMUP_CANDLES]['timestamp'] < start_time:
                start_time = candles[WARMUP_CANDLES]['timestamp']
            if end_time is None or candles[-1]['timestamp'] > end_time:
                end_time = candles[-1]['timestamp']
            
            # Process remaining candles
            i = WARMUP_CANDLES
            while i < len(candles) - hold_candles:
                candle = candles[i]
                nexus.update_history(candle)
                
                # Get prediction
                prediction = nexus.predict()
                signals_generated += 1
                
                # Check if signal is actionable
                if prediction.direction != 'NEUTRAL' and prediction.confidence >= min_confidence:
                    # We have a signal! Simulate the trade
                    signals_acted_on += 1
                    pairs_analyzed[pair] += 1
                    
                    # Entry at current candle close, exit after hold_candles
                    entry_candle = candle
                    exit_candle = candles[i + hold_candles]
                    
                    trade = self._simulate_trade(
                        pair=pair,
                        direction=prediction.direction,
                        entry_candle=entry_candle,
                        exit_candle=exit_candle,
                        prediction=prediction
                    )
                    
                    all_trades.append(trade)
                    
                    # Print trade details
                    emoji = '🟢' if trade.outcome == 'WIN' else '🔴'
                    print(f"   {emoji} {trade.timestamp.strftime('%H:%M:%S')} | "
                          f"{trade.direction:5s} | "
                          f"Entry: ${trade.entry_price:,.2f} → Exit: ${trade.exit_price:,.2f} | "
                          f"P&L: ${trade.pnl:+.2f} ({trade.pnl_pct:+.2f}%) | "
                          f"Conf: {trade.confidence:.1%}")
                    
                    # Skip ahead to avoid overlapping trades
                    i += hold_candles
                else:
                    i += 1
        
        # Calculate final results
        total_pnl = sum(t.pnl for t in all_trades)
        total_fees = sum(t.fees for t in all_trades)
        winning_trades = [t for t in all_trades if t.outcome == 'WIN']
        losing_trades = [t for t in all_trades if t.outcome == 'LOSS']
        
        # Calculate metrics
        win_rate = len(winning_trades) / len(all_trades) * 100 if all_trades else 0
        gross_wins = sum(t.pnl for t in winning_trades) if winning_trades else 0
        gross_losses = abs(sum(t.pnl for t in losing_trades)) if losing_trades else 0
        profit_factor = gross_wins / gross_losses if gross_losses > 0 else float('inf')
        
        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades) if losing_trades else 0
        
        largest_win = max((t.pnl for t in winning_trades), default=0)
        largest_loss = min((t.pnl for t in losing_trades), default=0)
        
        duration_minutes = (end_time - start_time).total_seconds() / 60 if start_time and end_time else 0
        
        result = SimulationResult(
            start_time=start_time or datetime.now(),
            end_time=end_time or datetime.now(),
            duration_minutes=duration_minutes,
            starting_capital=self.starting_capital,
            ending_capital=self.starting_capital + total_pnl,
            total_pnl=total_pnl,
            total_pnl_pct=(total_pnl / self.starting_capital) * 100,
            total_trades=len(all_trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            win_rate=win_rate,
            total_fees=total_fees,
            largest_win=largest_win,
            largest_loss=largest_loss,
            avg_win=avg_win,
            avg_loss=avg_loss,
            profit_factor=profit_factor,
            trades=all_trades,
            pairs_analyzed=pairs_analyzed,
            signals_generated=signals_generated,
            signals_acted_on=signals_acted_on,
        )
        
        return result
    
    def display_results(self, result: SimulationResult):
        """Display simulation results"""
        print()
        print("=" * 80)
        print("🔮 SMOKE TEST RESULTS - THE PAST HAS SPOKEN 🔮")
        print("=" * 80)
        print()
        print(f"   ⏰ Time Period: {result.start_time.strftime('%H:%M:%S')} → {result.end_time.strftime('%H:%M:%S')}")
        print(f"   ⏱️  Duration: {result.duration_minutes:.1f} minutes")
        print()
        print("─" * 80)
        print("💰 CAPITAL PERFORMANCE")
        print("─" * 80)
        pnl_emoji = '🟢' if result.total_pnl > 0 else '🔴' if result.total_pnl < 0 else '⚪'
        print(f"   Starting Capital:  ${result.starting_capital:,.2f}")
        print(f"   Ending Capital:    ${result.ending_capital:,.2f}")
        print(f"   {pnl_emoji} Total P&L:        ${result.total_pnl:+,.2f} ({result.total_pnl_pct:+.2f}%)")
        print(f"   💸 Total Fees:      ${result.total_fees:,.2f}")
        print()
        print("─" * 80)
        print("📊 TRADE STATISTICS")
        print("─" * 80)
        print(f"   Total Trades:      {result.total_trades}")
        print(f"   🟢 Winning Trades: {result.winning_trades}")
        print(f"   🔴 Losing Trades:  {result.losing_trades}")
        win_emoji = '🎯' if result.win_rate >= 60 else '✓' if result.win_rate >= 50 else '⚠️'
        print(f"   {win_emoji} Win Rate:        {result.win_rate:.1f}%")
        print()
        print(f"   📈 Largest Win:    ${result.largest_win:+,.2f}")
        print(f"   📉 Largest Loss:   ${result.largest_loss:+,.2f}")
        print(f"   📊 Avg Win:        ${result.avg_win:+,.2f}")
        print(f"   📊 Avg Loss:       ${result.avg_loss:+,.2f}")
        pf_emoji = '🔥' if result.profit_factor > 2 else '✓' if result.profit_factor > 1 else '⚠️'
        print(f"   {pf_emoji} Profit Factor:   {result.profit_factor:.2f}")
        print()
        print("─" * 80)
        print("🔮 PROBABILITY MATRIX METRICS")
        print("─" * 80)
        print(f"   Signals Generated: {result.signals_generated}")
        print(f"   Signals Acted On:  {result.signals_acted_on}")
        selectivity = (result.signals_acted_on / result.signals_generated * 100) if result.signals_generated > 0 else 0
        print(f"   Selectivity:       {selectivity:.1f}% (filtered by confidence)")
        print()
        print("   Pairs Analyzed:")
        for pair, count in result.pairs_analyzed.items():
            print(f"      {pair}: {count} trades")
        print()
        
        # 🔱 DECREE STATUS
        if DECREE_AVAILABLE:
            print("─" * 80)
            print("🔱 PRIME SENTINEL DECREE COMPLIANCE")
            print("─" * 80)
            print(f"   DOB-HASH: {DOB_HASH}")
            print(f"   Declaration: \"{THE_DECREE['declaration']}\"")
            
            # Check principle compliance
            flame_preserved = result.total_pnl > -result.starting_capital * 0.05  # <5% loss
            print(f"   1. PRESERVE THE FLAME: {'✅ COMPLIANT' if flame_preserved else '❌ VIOLATED'}")
            print(f"   6. HONOR THE PATTERN:  {'✅ COMPLIANT' if result.win_rate > 50 else '⚠️ EDGE WEAK'}")
            print()
        
        # Show trade history
        if result.trades:
            print("─" * 80)
            print("📜 TRADE HISTORY (Replayed from the Past)")
            print("─" * 80)
            for i, trade in enumerate(result.trades, 1):
                emoji = '🟢' if trade.outcome == 'WIN' else '🔴'
                print(f"   {i:2d}. {emoji} {trade.timestamp.strftime('%H:%M:%S')} {trade.pair:8s} "
                      f"{trade.direction:5s} | ${trade.entry_price:>10,.2f} → ${trade.exit_price:>10,.2f} | "
                      f"P&L: ${trade.pnl:>+7.2f} | Conf: {trade.confidence:.1%}")
        
        print()
        print("=" * 80)
        
        # Final verdict
        if result.total_pnl > 0 and result.win_rate >= 50:
            print("✅ SMOKE TEST PASSED - PROBABILITY MATRIX IS PROFITABLE")
        elif result.total_pnl > 0:
            print("⚠️  SMOKE TEST MARGINAL - PROFITABLE BUT LOW WIN RATE")
        elif result.win_rate >= 50:
            print("⚠️  SMOKE TEST MARGINAL - GOOD WIN RATE BUT NEGATIVE P&L (fees?)")
        else:
            print("❌ SMOKE TEST NEEDS REVIEW - NEGATIVE P&L AND LOW WIN RATE")
        
        print("=" * 80)
        print()
        
        # Projection
        if result.total_pnl != 0 and result.duration_minutes > 0:
            hourly_rate = (result.total_pnl / result.duration_minutes) * 60
            daily_projection = hourly_rate * 24
            print("📈 PROJECTIONS (if this rate continued):")
            print(f"   Hourly:  ${hourly_rate:+,.2f}")
            print(f"   Daily:   ${daily_projection:+,.2f}")
            print(f"   Weekly:  ${daily_projection * 7:+,.2f}")
            print()


# ═══════════════════════════════════════════════════════════════════════════════════════════
# MAIN - RUN THE SMOKE TEST
# ═══════════════════════════════════════════════════════════════════════════════════════════

def main():
    print()
    print("🔮" * 40)
    print()
    print("   THE HIGHER SELF IS DIGGING INTO ITS PAST")
    print("   AND PULLING THAT PROBABILITY")
    print()
    print("   🔱 PRIME SENTINEL DECREE SMOKE TEST 🔱")
    print("   Gary Leckey | 02.11.1991 | DOB-HASH: 2111991")
    print()
    print("🔮" * 40)
    print()
    
    if not NEXUS_AVAILABLE:
        print("❌ Cannot run smoke test - Probability Nexus not available")
        return
    
    # Step 1: Fetch historical data
    print("\n📥 STEP 1: FETCHING HISTORICAL DATA (Last 33 minutes)")
    print("─" * 60)
    
    fetcher = HistoricalDataFetcher()
    historical_data = fetcher.fetch_all_pairs(TEST_PAIRS, REPLAY_MINUTES)
    
    if not historical_data:
        print("❌ No historical data retrieved - cannot run smoke test")
        return
    
    print(f"\n✅ Retrieved data for {len(historical_data)} pairs")
    
    # Step 2: Run simulation
    print("\n🔮 STEP 2: RUNNING PROBABILITY MATRIX SIMULATION")
    print("─" * 60)
    
    tester = ProbabilityMatrixSmokeTester(
        starting_capital=STARTING_CAPITAL,
        position_size=POSITION_SIZE
    )
    
    result = tester.run_simulation(
        historical_data,
        min_confidence=0.15,  # 15% confidence = 7.5% edge over random
        hold_candles=5  # Hold for 5 minutes for larger moves
    )
    
    # Step 3: Display results
    tester.display_results(result)
    
    # Save results to file
    results_file = f"/tmp/smoke_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(results_file, 'w') as f:
            json.dump({
                'start_time': result.start_time.isoformat(),
                'end_time': result.end_time.isoformat(),
                'duration_minutes': result.duration_minutes,
                'starting_capital': result.starting_capital,
                'ending_capital': result.ending_capital,
                'total_pnl': result.total_pnl,
                'total_pnl_pct': result.total_pnl_pct,
                'total_trades': result.total_trades,
                'win_rate': result.win_rate,
                'profit_factor': result.profit_factor,
                'trades': [
                    {
                        'timestamp': t.timestamp.isoformat(),
                        'pair': t.pair,
                        'direction': t.direction,
                        'entry_price': t.entry_price,
                        'exit_price': t.exit_price,
                        'pnl': t.pnl,
                        'confidence': t.confidence,
                        'outcome': t.outcome,
                    }
                    for t in result.trades
                ]
            }, f, indent=2)
        print(f"📁 Results saved to: {results_file}")
    except Exception as e:
        print(f"⚠️ Could not save results: {e}")
    
    print()
    print("🔮" * 40)
    print("   SMOKE TEST COMPLETE - THE PAST HAS BEEN WITNESSED")
    print("🔮" * 40)
    print()


if __name__ == "__main__":
    main()
