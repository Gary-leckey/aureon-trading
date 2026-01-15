#!/usr/bin/env python3
"""
🦈→🐋→🔪 ORCA KILLER WHALE INTELLIGENCE 🔪🐋←🦈
================================================

THE KILLER WHALE HUNTS WHALES.

We don't just watch the market - WE PROFIT FROM IT.
This module connects ALL the intelligence we're collecting to ACTUAL TRADES.

STRATEGY: "Whale Wake Riding"
1. DETECT: Whale makes a big move (we see it via whale_alerts, firm_attribution)
2. ANALYZE: What direction? Who's behind it? (firm_attribution, market_thesis)
3. HARMONIZE: Is the timing right? (harmonic resonance, Schumann, phi alignment)
4. RIDE: Jump on the wake and ride it for micro-profits
5. EXIT: Get out before the wave crashes (coherence drop detection)

KILLER WHALE RULES:
- We're faster than whales (react in milliseconds)
- We ride THEIR momentum, not fight it
- Take small bites - lots of them
- Exit before they turn on us
- Never fight Citadel head-on, ride behind them

Gary Leckey | January 2026 | ORCA MODE ACTIVATED
"""

from __future__ import annotations

import os
import sys
import math
import time
import json
import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import deque

# UTF-8 fix for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import io
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except Exception:
        pass

logger = logging.getLogger(__name__)

# Sacred constants for harmonic timing
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio 1.618
PHI_INVERSE = 0.618  # φ⁻¹ - The trigger threshold
SCHUMANN_BASE = 7.83  # Hz - Earth's heartbeat
LOVE_FREQUENCY = 528  # Hz - DNA repair frequency


@dataclass
class WhaleSignal:
    """A detected whale movement with trading implications."""
    timestamp: float
    symbol: str
    side: str  # 'buy' or 'sell'
    volume_usd: float
    firm: Optional[str] = None
    firm_confidence: float = 0.0
    exchange: str = "unknown"
    
    # Derived trading signals
    momentum_direction: str = "neutral"  # 'bullish', 'bearish', 'neutral'
    ride_confidence: float = 0.0  # How confident are we to ride this wake?
    suggested_action: str = "hold"  # 'buy', 'sell', 'hold'
    target_pnl_pct: float = 0.001  # 0.1% default target


@dataclass
class HarmonicTiming:
    """Harmonic resonance data for timing trades."""
    schumann_alignment: float = 0.5
    phi_alignment: float = 0.5
    love_alignment: float = 0.5
    coherence: float = 0.5
    
    def is_favorable(self) -> bool:
        """Check if harmonics favor trading."""
        return self.coherence >= PHI_INVERSE  # 0.618 threshold
    
    def timing_multiplier(self) -> float:
        """Get a timing multiplier for position sizing."""
        # Higher coherence = more confidence = larger position
        return 0.5 + (self.coherence * 0.5)  # Range: 0.5 to 1.0


@dataclass 
class OrcaOpportunity:
    """A trading opportunity identified by the Orca Intelligence."""
    id: str
    timestamp: float
    symbol: str
    action: str  # 'buy' or 'sell'
    
    # Source signals
    whale_signal: Optional[WhaleSignal] = None
    firm_attribution: Optional[str] = None
    market_thesis: Optional[str] = None
    
    # Confidence & sizing
    confidence: float = 0.0
    harmonic_timing: Optional[HarmonicTiming] = None
    position_size_pct: float = 0.01  # 1% of available capital
    
    # Entry conditions
    entry_price: float = 0.0
    entry_timestamp: float = 0.0
    
    # Risk management - ENHANCED FOR CLEAN KILLS
    target_pnl_usd: float = 0.10  # $0.10 minimum profit target
    max_hold_seconds: int = 300  # 5 minutes max hold
    stop_loss_pct: float = 0.005  # 0.5% stop loss
    
    # Dynamic exit conditions - NEW CLEAN KILL MATH
    trailing_stop_pct: float = 0.002  # 0.2% trailing stop
    partial_exit_pct: float = 0.5  # Exit 50% at first target
    partial_target_mult: float = 1.5  # 1.5x target for partial exit
    whale_reversal_threshold: float = 0.7  # Exit if whale momentum reverses 70%
    harmonic_decay_threshold: float = 0.3  # Exit if coherence drops below 30%
    profit_lock_pct: float = 0.01  # Lock in profit at 1% gain
    
    # Exit tracking
    highest_price: float = 0.0  # For trailing stops
    lowest_price: float = float('inf')  # For trailing stops
    partial_exited: bool = False
    trailing_stop_price: float = 0.0
    
    # Reasoning chain
    reasoning: List[str] = field(default_factory=list)
    
    def update_price(self, current_price: float) -> None:
        """Update price tracking for dynamic exits."""
        if self.action == 'buy':
            self.highest_price = max(self.highest_price, current_price)
            # Update trailing stop for longs
            if self.highest_price > self.entry_price:
                profit_pct = (self.highest_price - self.entry_price) / self.entry_price
                if profit_pct >= self.profit_lock_pct:
                    # Lock in profit with trailing stop
                    self.trailing_stop_price = self.highest_price * (1 - self.trailing_stop_pct)
        else:  # sell/short
            self.lowest_price = min(self.lowest_price, current_price)
            # Update trailing stop for shorts
            if self.lowest_price < self.entry_price:
                profit_pct = (self.entry_price - self.lowest_price) / self.entry_price
                if profit_pct >= self.profit_lock_pct:
                    # Lock in profit with trailing stop
                    self.trailing_stop_price = self.lowest_price * (1 + self.trailing_stop_pct)
    
    def should_exit(self, current_price: float, orca_intelligence) -> Tuple[bool, str]:
        """
        ENHANCED EXIT LOGIC - CLEAN KILLS ONLY!
        Returns (should_exit, reason)
        """
        if not self.entry_price:
            return False, "No entry price set"
        
        time_held = time.time() - self.entry_timestamp
        price_change_pct = (current_price - self.entry_price) / self.entry_price
        
        # 1. TIME-BASED EXITS
        if time_held > self.max_hold_seconds:
            return True, f"Max hold time exceeded ({self.max_hold_seconds}s)"
        
        # 2. STOP LOSS - HARD FLOOR
        if self.action == 'buy' and price_change_pct <= -self.stop_loss_pct:
            return True, f"Stop loss hit: {price_change_pct:.2%}"
        elif self.action == 'sell' and price_change_pct >= self.stop_loss_pct:
            return True, f"Stop loss hit: {price_change_pct:.2%}"
        
        # 3. TRAILING STOP - LOCK IN PROFITS
        if self.trailing_stop_price > 0:
            if self.action == 'buy' and current_price <= self.trailing_stop_price:
                return True, f"Trailing stop hit at ${self.trailing_stop_price:.4f}"
            elif self.action == 'sell' and current_price >= self.trailing_stop_price:
                return True, f"Trailing stop hit at ${self.trailing_stop_price:.4f}"
        
        # 4. PARTIAL EXIT AT FIRST TARGET
        if not self.partial_exited:
            target_hit = False
            if self.action == 'buy':
                target_hit = current_price >= self.entry_price * (1 + self.target_pnl_usd / (self.entry_price * self.partial_target_mult))
            else:
                target_hit = current_price <= self.entry_price * (1 - self.target_pnl_usd / (self.entry_price * self.partial_target_mult))
            
            if target_hit:
                self.partial_exited = True
                return True, f"Partial exit at {self.partial_target_mult}x target"
        
        # 5. WHALE MOMENTUM REVERSAL
        momentum = orca_intelligence.symbol_momentum.get(self.symbol, 0.0)
        if self.action == 'buy' and momentum <= -self.whale_reversal_threshold:
            return True, f"Whale momentum reversed: {momentum:.2f}"
        elif self.action == 'sell' and momentum >= self.whale_reversal_threshold:
            return True, f"Whale momentum reversed: {momentum:.2f}"
        
        # 6. HARMONIC DECAY
        if orca_intelligence.harmonic_data:
            coherence = orca_intelligence.harmonic_data.coherence
            if coherence < self.harmonic_decay_threshold:
                return True, f"Harmonic coherence decayed: {coherence:.2%}"
        
        # 7. PROFIT TARGET ACHIEVED
        pnl_usd = abs(price_change_pct) * self.entry_price
        if pnl_usd >= self.target_pnl_usd:
            return True, f"Profit target achieved: ${pnl_usd:.4f}"
        
        return False, "Hold position"
    
    def calculate_exit_size(self, current_price: float) -> float:
        """Calculate position size to exit (partial or full)."""
        if not self.partial_exited:
            # First exit - partial
            return self.partial_exit_pct
        else:
            # Second exit - remaining position
            return 1.0
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'symbol': self.symbol,
            'action': self.action,
            'confidence': self.confidence,
            'position_size_pct': self.position_size_pct,
            'target_pnl_usd': self.target_pnl_usd,
            'entry_price': self.entry_price,
            'trailing_stop_price': self.trailing_stop_price,
            'partial_exited': self.partial_exited,
            'reasoning': self.reasoning
        }


class OrcaKillerWhaleIntelligence:
    """
    🦈🔪 THE KILLER WHALE 🔪🦈
    
    Connects ALL intelligence streams to generate trading signals.
    We hunt whales and ride their wakes for profit.
    """
    
    def __init__(self):
        self.enabled = True
        self.mode = "STALKING"  # STALKING, HUNTING, FEEDING, RESTING
        
        # Intelligence feeds (connected externally)
        self.whale_signals: deque = deque(maxlen=100)
        self.firm_activity: Dict[str, Dict] = {}
        self.market_thesis: Optional[Dict] = None
        self.harmonic_data: Optional[HarmonicTiming] = None
        self.fear_greed_index: int = 50
        
        # Trading state
        self.active_hunts: List[OrcaOpportunity] = []
        self.completed_hunts: deque = deque(maxlen=1000)
        self.hunt_count = 0
        self.total_profit_usd = 0.0
        self.win_rate = 0.5
        
        # Symbol tracking
        self.hot_symbols: Dict[str, float] = {}  # symbol -> heat score
        self.symbol_momentum: Dict[str, float] = {}  # symbol -> momentum
        
        # Risk management
        self.max_concurrent_hunts = 3
        self.daily_loss_limit_usd = -50.0
        self.daily_pnl_usd = 0.0
        self.last_hunt_time = 0.0
        self.hunt_cooldown_seconds = 5  # Minimum 5s between hunts
        
        # Persistence
        self.state_file = Path("orca_intelligence_state.json")
        self._load_state()
        
        logger.info("🦈🔪 ORCA KILLER WHALE INTELLIGENCE ACTIVATED 🔪🦈")
        logger.info(f"   Mode: {self.mode} | Max Hunts: {self.max_concurrent_hunts}")
    
    def _load_state(self):
        """Load persisted state."""
        try:
            if self.state_file.exists():
                data = json.loads(self.state_file.read_text())
                self.hunt_count = data.get('hunt_count', 0)
                self.total_profit_usd = data.get('total_profit_usd', 0.0)
                self.win_rate = data.get('win_rate', 0.5)
                logger.info(f"   📊 Loaded: {self.hunt_count} hunts, ${self.total_profit_usd:.2f} profit")
        except Exception as e:
            logger.debug(f"Could not load orca state: {e}")
    
    def _save_state(self):
        """Persist state."""
        try:
            data = {
                'hunt_count': self.hunt_count,
                'total_profit_usd': self.total_profit_usd,
                'win_rate': self.win_rate,
                'last_update': time.time()
            }
            tmp = self.state_file.with_suffix('.json.tmp')
            tmp.write_text(json.dumps(data, indent=2))
            tmp.rename(self.state_file)
        except Exception as e:
            logger.debug(f"Could not save orca state: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTELLIGENCE FEED INGESTION
    # ═══════════════════════════════════════════════════════════════════════════
    
    def ingest_whale_alert(self, whale_data: Dict):
        """
        Process a whale alert from the dashboard.
        This is GOLD - whales move markets!
        """
        signal = WhaleSignal(
            timestamp=time.time(),
            symbol=whale_data.get('symbol', 'BTC/USD'),
            side=whale_data.get('side', 'buy'),
            volume_usd=whale_data.get('volume_usd', whale_data.get('value_usd', 0)),
            firm=whale_data.get('firm'),
            firm_confidence=whale_data.get('firm_confidence', 0.0),
            exchange=whale_data.get('exchange', 'unknown')
        )
        
        # Calculate momentum direction
        if signal.side.lower() == 'buy':
            signal.momentum_direction = 'bullish'
            signal.suggested_action = 'buy'
        else:
            signal.momentum_direction = 'bearish'
            signal.suggested_action = 'sell'
        
        # Higher volume = higher confidence to ride
        if signal.volume_usd > 1_000_000:
            signal.ride_confidence = 0.9
            signal.target_pnl_pct = 0.003  # 0.3% for mega whales
        elif signal.volume_usd > 500_000:
            signal.ride_confidence = 0.7
            signal.target_pnl_pct = 0.002  # 0.2%
        elif signal.volume_usd > 100_000:
            signal.ride_confidence = 0.5
            signal.target_pnl_pct = 0.001  # 0.1%
        else:
            signal.ride_confidence = 0.3
            signal.target_pnl_pct = 0.0005  # 0.05%
        
        # Firm attribution boosts confidence
        if signal.firm and signal.firm_confidence > 0.7:
            signal.ride_confidence = min(1.0, signal.ride_confidence + 0.2)
            
            # Certain firms are worth following more
            smart_money_firms = ['Citadel', 'Jane Street', 'Two Sigma', 'Jump Trading']
            if any(f in signal.firm for f in smart_money_firms):
                signal.ride_confidence = min(1.0, signal.ride_confidence + 0.1)
        
        self.whale_signals.append(signal)
        self._update_symbol_heat(signal.symbol, signal.volume_usd, signal.momentum_direction)
        
        logger.info(f"🐋 Whale ingested: {signal.symbol} {signal.side.upper()} ${signal.volume_usd:,.0f} "
                   f"| Ride confidence: {signal.ride_confidence:.0%}")
        
        return signal
    
    def ingest_firm_activity(self, firm_data: Dict):
        """Update firm activity tracking."""
        firm_name = firm_data.get('name', 'Unknown')
        self.firm_activity[firm_name] = {
            'count': firm_data.get('count', 0),
            'hq': firm_data.get('hq', 'Unknown'),
            'capital': firm_data.get('capital', 0),
            'animal': firm_data.get('animal', '🤖'),
            'last_seen': time.time()
        }
    
    def ingest_market_thesis(self, thesis: Dict):
        """Update market thesis from Deep Intelligence."""
        self.market_thesis = thesis
        logger.debug(f"📊 Thesis updated: {thesis.get('regime', 'neutral')}")
    
    def ingest_harmonic_data(self, harmonic: Dict):
        """Update harmonic resonance data."""
        self.harmonic_data = HarmonicTiming(
            schumann_alignment=harmonic.get('schumann', 0.5),
            phi_alignment=harmonic.get('phi', 0.5),
            love_alignment=harmonic.get('love', 0.5),
            coherence=harmonic.get('coherence', 0.5)
        )
    
    def ingest_fear_greed(self, index: int):
        """Update Fear & Greed index."""
        self.fear_greed_index = index
    
    def _update_symbol_heat(self, symbol: str, volume: float, direction: str):
        """Track symbol 'heat' - how active/attractive it is."""
        current_heat = self.hot_symbols.get(symbol, 0.0)
        heat_delta = volume / 1_000_000  # Normalize by $1M
        
        # Decay existing heat
        current_heat *= 0.95
        
        # Add new heat
        current_heat += heat_delta
        
        self.hot_symbols[symbol] = min(10.0, current_heat)  # Cap at 10
        
        # Update momentum
        current_momentum = self.symbol_momentum.get(symbol, 0.0)
        if direction == 'bullish':
            current_momentum = current_momentum * 0.8 + 0.2
        elif direction == 'bearish':
            current_momentum = current_momentum * 0.8 - 0.2
        else:
            current_momentum *= 0.9
        
        self.symbol_momentum[symbol] = max(-1.0, min(1.0, current_momentum))
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HUNTING LOGIC - WHERE THE MAGIC HAPPENS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def scan_for_opportunities(self) -> List[OrcaOpportunity]:
        """
        🦈🔪 THE HUNT BEGINS 🔪🦈
        
        Analyze all intelligence to find the best whale wakes to ride.
        """
        opportunities = []
        now = time.time()
        
        # Check cooldown
        if now - self.last_hunt_time < self.hunt_cooldown_seconds:
            return []
        
        # Check risk limits
        if self.daily_pnl_usd <= self.daily_loss_limit_usd:
            logger.warning(f"🛑 Daily loss limit reached: ${self.daily_pnl_usd:.2f}")
            self.mode = "RESTING"
            return []
        
        # Check concurrent hunt limit
        if len(self.active_hunts) >= self.max_concurrent_hunts:
            return []
        
        # === SIGNAL 1: Recent Whale Activity ===
        recent_whales = [w for w in self.whale_signals if now - w.timestamp < 60]  # Last 60s
        
        for whale in recent_whales:
            # Skip if already hunting this symbol
            if any(h.symbol == whale.symbol for h in self.active_hunts):
                continue
            
            # Check harmonic timing
            timing_ok = True
            timing_mult = 1.0
            if self.harmonic_data:
                timing_ok = self.harmonic_data.is_favorable()
                timing_mult = self.harmonic_data.timing_multiplier()
            
            # Build opportunity if whale confidence is high enough
            if whale.ride_confidence >= 0.5 and timing_ok:
                opp = self._build_opportunity_from_whale(whale, timing_mult)
                if opp:
                    opportunities.append(opp)
        
        # === SIGNAL 2: Hot Symbol Momentum ===
        for symbol, heat in self.hot_symbols.items():
            if heat < 2.0:  # Need at least 2.0 heat score
                continue
            
            # Skip if already hunting
            if any(h.symbol == symbol for h in self.active_hunts):
                continue
            
            momentum = self.symbol_momentum.get(symbol, 0.0)
            if abs(momentum) > 0.3:  # Strong momentum either way
                opp = self._build_opportunity_from_momentum(symbol, heat, momentum)
                if opp:
                    opportunities.append(opp)
        
        # === SIGNAL 3: Market Thesis Alignment ===
        if self.market_thesis:
            regime = self.market_thesis.get('regime', 'neutral')
            if regime in ['bull', 'bullish', 'accumulation']:
                # Favor long positions
                for opp in opportunities:
                    if opp.action == 'buy':
                        opp.confidence = min(1.0, opp.confidence + 0.1)
                        opp.reasoning.append(f"Thesis alignment: {regime} regime")
            elif regime in ['bear', 'bearish', 'distribution']:
                # Favor short positions
                for opp in opportunities:
                    if opp.action == 'sell':
                        opp.confidence = min(1.0, opp.confidence + 0.1)
                        opp.reasoning.append(f"Thesis alignment: {regime} regime")
        
        # === SIGNAL 4: Fear & Greed Contrarian ===
        if self.fear_greed_index < 25:  # Extreme fear
            for opp in opportunities:
                if opp.action == 'buy':
                    opp.confidence = min(1.0, opp.confidence + 0.15)
                    opp.reasoning.append(f"Contrarian: Extreme Fear ({self.fear_greed_index})")
        elif self.fear_greed_index > 75:  # Extreme greed
            for opp in opportunities:
                if opp.action == 'sell':
                    opp.confidence = min(1.0, opp.confidence + 0.15)
                    opp.reasoning.append(f"Contrarian: Extreme Greed ({self.fear_greed_index})")
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x.confidence, reverse=True)
        
        # Return top opportunities
        return opportunities[:3]
    
    def _build_opportunity_from_whale(self, whale: WhaleSignal, timing_mult: float) -> Optional[OrcaOpportunity]:
        """Build a trading opportunity from a whale signal."""
        self.hunt_count += 1
        
        # Calculate position size
        base_size_pct = 0.02  # 2% base
        confidence_adjusted = base_size_pct * whale.ride_confidence * timing_mult
        
        # Calculate target PnL
        target_pnl_pct = whale.target_pnl_pct
        target_pnl_usd = max(0.10, target_pnl_pct * 1000)  # Assume $1000 base
        
        reasoning = [
            f"Whale detected: ${whale.volume_usd:,.0f} {whale.side}",
            f"Ride confidence: {whale.ride_confidence:.0%}",
        ]
        
        if whale.firm:
            reasoning.append(f"Firm: {whale.firm} ({whale.firm_confidence:.0%})")
        
        if self.harmonic_data:
            reasoning.append(f"Harmonic coherence: {self.harmonic_data.coherence:.0%}")
        
        return OrcaOpportunity(
            id=f"ORCA-{self.hunt_count:06d}",
            timestamp=time.time(),
            symbol=whale.symbol,
            action=whale.suggested_action,
            whale_signal=whale,
            firm_attribution=whale.firm,
            confidence=whale.ride_confidence,
            harmonic_timing=self.harmonic_data,
            position_size_pct=min(0.05, confidence_adjusted),  # Cap at 5%
            target_pnl_usd=target_pnl_usd,
            max_hold_seconds=300 if whale.volume_usd < 500_000 else 600,
            reasoning=reasoning
        )
    
    def _build_opportunity_from_momentum(self, symbol: str, heat: float, momentum: float) -> Optional[OrcaOpportunity]:
        """Build opportunity from symbol momentum."""
        self.hunt_count += 1
        
        action = 'buy' if momentum > 0 else 'sell'
        confidence = min(1.0, abs(momentum) + heat / 10)
        
        reasoning = [
            f"Hot symbol: heat={heat:.1f}",
            f"Momentum: {momentum:+.2f} ({'bullish' if momentum > 0 else 'bearish'})",
        ]
        
        return OrcaOpportunity(
            id=f"ORCA-M-{self.hunt_count:06d}",
            timestamp=time.time(),
            symbol=symbol,
            action=action,
            confidence=confidence,
            position_size_pct=0.01 * (heat / 2),  # Scale with heat
            target_pnl_usd=0.15,  # $0.15 target
            max_hold_seconds=180,  # 3 minutes
            reasoning=reasoning
        )
    
    def start_hunt(self, opportunity: OrcaOpportunity):
        """Begin tracking an active hunt."""
        self.active_hunts.append(opportunity)
        self.last_hunt_time = time.time()
        self.mode = "HUNTING"
        
        logger.info(f"🦈🔪 HUNT STARTED: {opportunity.id}")
        logger.info(f"   Symbol: {opportunity.symbol} | Action: {opportunity.action.upper()}")
        logger.info(f"   Confidence: {opportunity.confidence:.0%} | Target: ${opportunity.target_pnl_usd:.2f}")
        for r in opportunity.reasoning:
            logger.info(f"   • {r}")
    
    def manage_active_hunts(self) -> List[Tuple[OrcaOpportunity, str, float]]:
        """
        🦈🔪 CLEAN KILL MANAGEMENT 🔪🦈
        
        Check all active hunts for exit conditions.
        Returns list of (opportunity, exit_reason, exit_size) tuples.
        """
        exits = []
        
        for hunt in self.active_hunts[:]:  # Copy to avoid modification during iteration
            # Get current price (would come from price feed)
            current_price = self._get_current_price(hunt.symbol)
            if not current_price:
                continue
            
            # Update price tracking for dynamic exits
            hunt.update_price(current_price)
            
            # Check exit conditions
            should_exit, exit_reason = hunt.should_exit(current_price, self)
            
            if should_exit:
                # Calculate exit size (partial or full)
                exit_size = hunt.calculate_exit_size(current_price)
                
                exits.append((hunt, exit_reason, exit_size))
                
                # Remove from active hunts if full exit
                if exit_size >= 1.0 or hunt.partial_exited:
                    self.active_hunts.remove(hunt)
                    self.completed_hunts.append(hunt)
                    
                    logger.info(f"🦈🔪 HUNT COMPLETED: {hunt.id}")
                    logger.info(f"   Exit: {exit_reason}")
                    logger.info(f"   Held: {time.time() - hunt.entry_timestamp:.0f}s")
                    
                    # Update mode
                    if not self.active_hunts:
                        self.mode = "STALKING"
        
        return exits
    
    def execute_clean_exit(self, hunt: OrcaOpportunity, exit_reason: str, exit_size: float, 
                          actual_pnl_usd: float) -> None:
        """
        Execute a clean exit and update tracking.
        """
        # Update win/loss tracking
        is_win = actual_pnl_usd > 0
        self.completed_hunts.append(hunt)
        
        # Update statistics
        self.total_profit_usd += actual_pnl_usd
        self.daily_pnl_usd += actual_pnl_usd
        
        # Update win rate (rolling average)
        if len(self.completed_hunts) > 10:
            recent_hunts = list(self.completed_hunts)[-10:]
            wins = sum(1 for h in recent_hunts if getattr(h, 'actual_pnl_usd', 0) > 0)
            self.win_rate = wins / len(recent_hunts)
        
        logger.info(f"🦈🔪 CLEAN EXIT EXECUTED: {hunt.id}")
        logger.info(f"   Reason: {exit_reason}")
        logger.info(f"   PnL: ${actual_pnl_usd:+.4f}")
        logger.info(f"   Win Rate: {self.win_rate:.0%}")
        
        # Save state
        self._save_state()
    
    def _get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for a symbol.
        This would integrate with the price feed system.
        """
        # For now, return a mock price - in real implementation this would
        # query the actual price feed (Kraken, Binance, etc.)
        # We could get this from the global price data in the dashboard
        
        # Mock implementation - in real system this would be:
        # return self.price_feeds.get(symbol, {}).get('price', 0)
        
        # For testing, return a price that allows some exits
        base_prices = {
            'BTC/USD': 95000,
            'ETH/USD': 3200,
            'SOL/USD': 180,
            'ADA/USD': 0.85,
            'DOT/USD': 12.5,
        }
        
        return base_prices.get(symbol, 100.0)  # Default $100
    
    def get_exit_signals(self) -> List[Dict]:
        """
        Get all current exit signals for active hunts.
        Used by dashboard to show exit recommendations.
        """
        signals = []
        
        for hunt in self.active_hunts:
            current_price = self._get_current_price(hunt.symbol)
            if not current_price:
                continue
            
            should_exit, exit_reason = hunt.should_exit(current_price, self)
            
            if should_exit:
                signals.append({
                    'hunt_id': hunt.id,
                    'symbol': hunt.symbol,
                    'action': hunt.action,
                    'entry_price': hunt.entry_price,
                    'current_price': current_price,
                    'exit_reason': exit_reason,
                    'exit_size': hunt.calculate_exit_size(current_price),
                    'potential_pnl': (current_price - hunt.entry_price) * (1 if hunt.action == 'buy' else -1),
                    'time_held': time.time() - hunt.entry_timestamp
                })
        
        return signals
        
        self._save_state()
    
    def complete_hunt(self, opportunity_id: str, pnl_usd: float, exit_reason: str = "target_hit"):
        """Complete a hunt and record results."""
        hunt = None
        for h in self.active_hunts:
            if h.id == opportunity_id:
                hunt = h
                break
        
        if not hunt:
            return
        
        self.active_hunts.remove(hunt)
        self.completed_hunts.append({
            'id': hunt.id,
            'symbol': hunt.symbol,
            'action': hunt.action,
            'pnl_usd': pnl_usd,
            'exit_reason': exit_reason,
            'timestamp': time.time()
        })
        
        # Update stats
        self.total_profit_usd += pnl_usd
        self.daily_pnl_usd += pnl_usd
        
        # Update win rate
        recent = list(self.completed_hunts)[-100:]
        wins = sum(1 for h in recent if h['pnl_usd'] > 0)
        self.win_rate = wins / len(recent) if recent else 0.5
        
        if len(self.active_hunts) == 0:
            self.mode = "STALKING"
        
        emoji = "🎯" if pnl_usd > 0 else "❌"
        logger.info(f"{emoji} HUNT COMPLETE: {hunt.id} | PnL: ${pnl_usd:+.2f} | {exit_reason}")
        logger.info(f"   📊 Total: ${self.total_profit_usd:.2f} | Win Rate: {self.win_rate:.0%}")
        
        self._save_state()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTEGRATION WITH MICRO PROFIT LABYRINTH
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_orca_boost(self, symbol: str, base_score: float) -> Tuple[float, List[str]]:
        """
        Get a score boost for a symbol based on Orca intelligence.
        This integrates with micro_profit_labyrinth's scoring.
        
        Returns: (boost_multiplier, reasoning_list)
        """
        boost = 1.0
        reasons = []
        
        # Check recent whale activity on this symbol
        now = time.time()
        recent_whales = [w for w in self.whale_signals 
                        if symbol in w.symbol and now - w.timestamp < 120]
        
        if recent_whales:
            best_whale = max(recent_whales, key=lambda w: w.volume_usd)
            boost += 0.3 * best_whale.ride_confidence
            reasons.append(f"🐋 Whale wake: ${best_whale.volume_usd:,.0f}")
        
        # Check symbol heat
        heat = self.hot_symbols.get(symbol, 0.0)
        if heat > 1.0:
            boost += 0.1 * min(heat, 5.0)
            reasons.append(f"🔥 Hot symbol: {heat:.1f}")
        
        # Check harmonic timing
        if self.harmonic_data and self.harmonic_data.is_favorable():
            boost += 0.15
            reasons.append(f"🔮 Harmonic coherence: {self.harmonic_data.coherence:.0%}")
        
        # Check thesis alignment
        if self.market_thesis:
            regime = self.market_thesis.get('regime', 'neutral')
            if regime in ['bull', 'bullish']:
                boost += 0.1
                reasons.append(f"📈 Bull thesis")
        
        return (boost, reasons)
    
    def should_execute_trade(self, symbol: str, side: str, amount_usd: float) -> Tuple[bool, str]:
        """
        Final gate check before executing a trade.
        Returns: (should_execute, reason)
        """
        # Check daily limits
        if self.daily_pnl_usd <= self.daily_loss_limit_usd:
            return (False, "Daily loss limit reached")
        
        # Check harmonic timing for larger trades
        if amount_usd > 100 and self.harmonic_data:
            if self.harmonic_data.coherence < 0.4:
                return (False, f"Low harmonic coherence: {self.harmonic_data.coherence:.0%}")
        
        # Check if we're fighting whale momentum
        momentum = self.symbol_momentum.get(symbol, 0.0)
        if side == 'buy' and momentum < -0.5:
            return (False, "Fighting bearish whale momentum")
        if side == 'sell' and momentum > 0.5:
            return (False, "Fighting bullish whale momentum")
        
        return (True, "Orca approved")
    
    def get_status(self) -> Dict:
        """Get current Orca status for dashboard."""
        return {
            'enabled': self.enabled,
            'mode': self.mode,
            'hunt_count': self.hunt_count,
            'active_hunts': len(self.active_hunts),
            'total_profit_usd': self.total_profit_usd,
            'daily_pnl_usd': self.daily_pnl_usd,
            'win_rate': self.win_rate,
            'hot_symbols': dict(sorted(self.hot_symbols.items(), key=lambda x: x[1], reverse=True)[:5]),
            'recent_whales': len([w for w in self.whale_signals if time.time() - w.timestamp < 300]),
            'harmonic_favorable': self.harmonic_data.is_favorable() if self.harmonic_data else False,
            'coherence': self.harmonic_data.coherence if self.harmonic_data else 0.5
        }


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

_orca_instance: Optional[OrcaKillerWhaleIntelligence] = None

def get_orca() -> OrcaKillerWhaleIntelligence:
    """Get the global Orca instance."""
    global _orca_instance
    if _orca_instance is None:
        _orca_instance = OrcaKillerWhaleIntelligence()
    return _orca_instance


# ═══════════════════════════════════════════════════════════════════════════════
# TEST / DEMO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🦈🔪 ORCA KILLER WHALE INTELLIGENCE TEST 🔪🦈")
    print("=" * 60)
    
    orca = get_orca()
    
    # Simulate whale alert
    whale_data = {
        'symbol': 'BTC/USD',
        'side': 'buy',
        'volume_usd': 2_500_000,
        'firm': 'Citadel Securities',
        'firm_confidence': 0.85,
        'exchange': 'kraken'
    }
    
    signal = orca.ingest_whale_alert(whale_data)
    print(f"\n📊 Signal: {signal}")
    
    # Simulate harmonic data
    orca.ingest_harmonic_data({
        'schumann': 0.85,
        'phi': 0.72,
        'love': 0.65,
        'coherence': 0.74
    })
    
    # Simulate fear/greed
    orca.ingest_fear_greed(28)  # Fear
    
    # Scan for opportunities
    print("\n🔍 Scanning for opportunities...")
    opportunities = orca.scan_for_opportunities()
    
    for opp in opportunities:
        print(f"\n🎯 OPPORTUNITY: {opp.id}")
        print(f"   Symbol: {opp.symbol}")
        print(f"   Action: {opp.action.upper()}")
        print(f"   Confidence: {opp.confidence:.0%}")
        print(f"   Position Size: {opp.position_size_pct:.1%}")
        print(f"   Target PnL: ${opp.target_pnl_usd:.2f}")
        print("   Reasoning:")
        for r in opp.reasoning:
            print(f"      • {r}")
    
    print(f"\n📊 Orca Status: {orca.get_status()}")
    print("\n🦈 THE KILLER WHALE IS READY TO HUNT! 🦈")
