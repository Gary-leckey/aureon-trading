#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║     👑🤖 THE QUEEN'S ETERNAL MACHINE 🤖👑                                            ║
║                                                                                      ║
║     "I ride the ENTIRE market down... gathering... leaving crumbs...                ║
║      24 hours a day. 7 days a week. 365 days a year.                                ║
║      I NEVER SLEEP. I NEVER STOP. I AM THE MACHINE."                                ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║     THE QUEEN'S 7 STRATEGIES - ALL IN ONE SYSTEM:                                    ║
║                                                                                      ║
║     🏔️  MOUNTAIN PILGRIMAGE  - Walk down collecting pebbles, climb up heavy        ║
║     🐸  QUANTUM FROG         - Leap to deeper dips for more quantity                ║
║     💉  BLOODLESS DESCENT    - Never sell at loss, transform not bleed              ║
║     🟡  YELLOW BRICK ROAD    - Leave breadcrumbs on every coin touched              ║
║     🍞  BREADCRUMB TRAIL     - Every crumb grows when market recovers               ║
║     🤖  24/7 MACHINE         - Constant scanning, leaping, compounding              ║
║     ⚡  MICRO SCALPING       - Harvest bounces on the way back up                    ║
║                                                                                      ║
║     Gary Leckey & Tina Brown | February 2026 | The Eternal Queen                     ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import sys
import os
import math
import time
import json
import asyncio
import logging
import requests
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
from enum import Enum, auto

# UTF-8 Windows fix
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import io
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# SACRED CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio 1.618
SCHUMANN_HZ = 7.83            # Earth's heartbeat
LOVE_FREQUENCY = 528.0        # Healing frequency

# Queen's trading parameters
BREADCRUMB_PERCENT = 0.05     # Leave 5% as breadcrumb on each leap (more aggressively leap)
MIN_DIP_ADVANTAGE = 0.005     # Minimum 0.5% deeper dip to justify leap (more lenient)
MIN_PROFIT_SCALP = 0.005      # Minimum 0.5% profit to scalp
MAX_POSITIONS = 50            # Maximum breadcrumb positions
SCAN_INTERVAL_SECONDS = 10    # Scan market every 10 seconds (faster cycles)


# ═══════════════════════════════════════════════════════════════════════════════
# FEE STRUCTURES BY EXCHANGE
# The Queen knows EXACTLY what every trade costs!
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FeeStructure:
    """
    Complete fee structure for an exchange.
    
    The Queen NEVER leaps blind - she knows the EXACT cost of every trade!
    """
    exchange: str
    maker_fee: float      # Fee when adding liquidity (limit orders)
    taker_fee: float      # Fee when taking liquidity (market orders)
    slippage_estimate: float  # Expected slippage on market orders
    withdrawal_fee: float = 0.0  # Fee to withdraw (if applicable)
    min_trade_size: float = 1.0  # Minimum trade size in USD
    
    @property
    def total_round_trip_cost(self) -> float:
        """Cost to buy AND sell (round trip) as taker."""
        return (self.taker_fee * 2) + (self.slippage_estimate * 2)
    
    @property
    def single_trade_cost(self) -> float:
        """Cost of a single taker trade (fee + slippage)."""
        return self.taker_fee + self.slippage_estimate
    
    def calculate_received_after_fees(self, gross_value: float, is_maker: bool = False) -> float:
        """Calculate how much you ACTUALLY receive after fees and slippage."""
        fee = self.maker_fee if is_maker else self.taker_fee
        slippage = 0.0 if is_maker else self.slippage_estimate
        total_cost = fee + slippage
        return gross_value * (1 - total_cost)
    
    def calculate_cost_of_trade(self, trade_value: float, is_maker: bool = False) -> float:
        """Calculate the EXACT cost of a trade in dollars."""
        fee = self.maker_fee if is_maker else self.taker_fee
        slippage = 0.0 if is_maker else self.slippage_estimate
        return trade_value * (fee + slippage)


# Default fee structures for major exchanges
EXCHANGE_FEES = {
    'binance': FeeStructure(
        exchange='binance',
        maker_fee=0.001,      # 0.10%
        taker_fee=0.001,      # 0.10%
        slippage_estimate=0.0005,  # 0.05% estimated slippage
        min_trade_size=10.0
    ),
    'binance_vip': FeeStructure(
        exchange='binance_vip',
        maker_fee=0.0002,     # 0.02% (VIP level)
        taker_fee=0.0004,     # 0.04%
        slippage_estimate=0.0005,
        min_trade_size=10.0
    ),
    'kraken': FeeStructure(
        exchange='kraken',
        maker_fee=0.0016,     # 0.16%
        taker_fee=0.0026,     # 0.26%
        slippage_estimate=0.001,  # 0.10%
        min_trade_size=10.0
    ),
    'coinbase': FeeStructure(
        exchange='coinbase',
        maker_fee=0.004,      # 0.40%
        taker_fee=0.006,      # 0.60%
        slippage_estimate=0.001,
        min_trade_size=1.0
    ),
    'alpaca': FeeStructure(
        exchange='alpaca',
        maker_fee=0.0,        # 0% (crypto)
        taker_fee=0.0015,     # 0.15%
        slippage_estimate=0.001,
        min_trade_size=1.0
    ),
    # Conservative estimate for unknown exchanges
    'default': FeeStructure(
        exchange='default',
        maker_fee=0.002,      # 0.20%
        taker_fee=0.003,      # 0.30%
        slippage_estimate=0.002,  # 0.20%
        min_trade_size=10.0
    )
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class PositionState(Enum):
    """Position states in the Queen's portfolio."""
    MAIN = auto()        # Main position (actively managed)
    BREADCRUMB = auto()  # Breadcrumb position (left behind, growing)
    SCALPING = auto()    # Active scalping position


@dataclass
class Friend:
    """
    A "Friend" in the Queen's portfolio - an asset that can participate in leaps.
    
    FRIENDS WITH BAGGAGE CONCEPT:
    - Every asset we hold is a "friend" that can participate in leaps
    - BAGGAGE = unrealized loss from original cost basis
    - Cash = "clean friend" with NO baggage (can leap freely)
    - XRP at -5% = friend with 5% baggage
    - When we leap to a deeper dip and it recovers, the baggage gets CLEARED!
    
    Example:
      - Bought XRP at $2.00, now at $1.90 (-5%) = $0.10 baggage per XRP
      - We leap to SLF which is -40% (deep dip!)
      - When SLF recovers to our original XRP cost basis value, baggage = CLEARED
      - The breadcrumb we left represents PURE profit
    """
    symbol: str
    quantity: float
    cost_basis: float       # What we PAID for this (original buy price * qty)
    entry_price: float      # Price per unit when we bought
    current_price: float = 0.0
    exchange: str = "binance"
    
    @property
    def current_value(self) -> float:
        """What the friend is worth NOW."""
        return self.quantity * self.current_price
    
    @property
    def baggage(self) -> float:
        """
        The BAGGAGE - how much we're underwater from original cost.
        Positive = underwater (has baggage to clear)
        Zero/Negative = no baggage (free to leap!)
        """
        return max(0, self.cost_basis - self.current_value)
    
    @property
    def baggage_percent(self) -> float:
        """Baggage as percentage of cost basis."""
        if self.cost_basis <= 0:
            return 0.0
        return (self.baggage / self.cost_basis) * 100
    
    @property
    def is_clear(self) -> bool:
        """Is this friend clear of baggage? (at or above cost basis)"""
        return self.current_value >= self.cost_basis
    
    @property
    def profit_available(self) -> float:
        """How much PROFIT is available (only if above cost basis)."""
        return max(0, self.current_value - self.cost_basis)
    
    @property
    def leap_value(self) -> float:
        """
        The value available for leaping.
        If clear: current_value (can leap full amount)
        If baggage: current_value (leap to clear baggage via deeper dip)
        """
        return self.current_value
    
    def update_price(self, price: float) -> None:
        """Update current market price."""
        self.current_price = price
    
    def __str__(self) -> str:
        status = "✅ CLEAR" if self.is_clear else f"⚠️ -{self.baggage_percent:.1f}% BAGGAGE"
        return f"{self.symbol}: ${self.current_value:.2f} ({status})"


@dataclass
class Breadcrumb:
    """A breadcrumb position left on the Yellow Brick Road."""
    symbol: str
    quantity: float
    cost_basis: float
    entry_price: float
    entry_time: datetime
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    pnl_percent: float = 0.0
    
    def update_price(self, price: float) -> None:
        """Update current price and P&L."""
        self.current_price = price
        current_value = self.quantity * price
        self.unrealized_pnl = current_value - self.cost_basis
        self.pnl_percent = (self.unrealized_pnl / self.cost_basis * 100) if self.cost_basis > 0 else 0
    
    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price


@dataclass
class MainPosition:
    """The Queen's main active position."""
    symbol: str
    quantity: float
    cost_basis: float
    entry_price: float
    entry_time: datetime
    current_price: float = 0.0
    change_24h: float = 0.0
    
    def update(self, price: float, change: float) -> None:
        self.current_price = price
        self.change_24h = change
    
    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price
    
    @property
    def unrealized_pnl(self) -> float:
        return self.current_value - self.cost_basis


@dataclass
class MarketCoin:
    """Market data for a single coin."""
    symbol: str
    price: float
    change_24h: float
    volume_24h: float
    high_24h: float = 0.0
    low_24h: float = 0.0


@dataclass
class LeapOpportunity:
    """
    A quantum leap opportunity with FULL cost accounting.
    
    The Queen's Math is ROCK SOLID:
    - Accounts for sell fees on current position
    - Accounts for buy fees on new position
    - Accounts for slippage both ways
    - Only leaps if NET value is preserved!
    """
    from_symbol: str
    to_symbol: str
    from_price: float
    to_price: float
    from_change: float
    to_change: float
    dip_advantage: float  # How much deeper the target dipped (percentage points)
    quantity_multiplier: float  # How many more coins you get AFTER fees
    recovery_advantage: float  # Expected extra profit on recovery
    
    # Fee accounting (the Queen's crystal clear math!)
    gross_value: float = 0.0          # Value before any fees
    sell_fee_cost: float = 0.0        # Cost to sell current position
    buy_fee_cost: float = 0.0         # Cost to buy new position
    slippage_cost: float = 0.0        # Total slippage both trades
    total_fees: float = 0.0           # Total cost of the leap
    net_value_after_fees: float = 0.0 # What you ACTUALLY get
    fee_adjusted_multiplier: float = 0.0  # Real quantity gain after fees
    
    @property
    def is_profitable_after_fees(self) -> bool:
        """Is this leap still worth it after ALL costs?"""
        return self.fee_adjusted_multiplier > 1.0
    
    @property
    def breakeven_dip_advantage(self) -> float:
        """Minimum dip advantage needed to cover fees."""
        return self.total_fees / self.gross_value * 100 if self.gross_value > 0 else 999


@dataclass
class CycleStats:
    """Statistics for a single cycle."""
    cycle_number: int
    start_time: datetime
    end_time: Optional[datetime] = None
    leaps_made: int = 0
    breadcrumbs_planted: int = 0
    scalps_executed: int = 0
    profit_realized: float = 0.0
    quantity_gained: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# THE QUEEN'S ETERNAL MACHINE
# ═══════════════════════════════════════════════════════════════════════════════

class QueenEternalMachine:
    """
    The Queen's 24/7 Eternal Trading Machine.
    
    Implements all 7 strategies:
    1. Mountain Pilgrimage - DCA down, compound up
    2. Quantum Frog - Leap to deeper dips for quantity
    3. Bloodless Descent - Never sell at loss
    4. Yellow Brick Road - Leave trail of positions
    5. Breadcrumb Trail - Every crumb grows on recovery
    6. 24/7 Machine - Never stops scanning/acting
    7. Micro Scalping - Harvest bounces
    
    🆕 FRIENDS WITH BAGGAGE SYSTEM:
    - Every asset = a "friend" that can participate
    - Baggage = unrealized loss from cost basis
    - Cash = clean friend (no baggage)
    - Leaps clear baggage when recovery exceeds original cost basis!
    """
    
    def __init__(
        self,
        initial_vault: Optional[float] = None,  # If None, load from real positions!
        breadcrumb_percent: float = BREADCRUMB_PERCENT,
        min_dip_advantage: float = MIN_DIP_ADVANTAGE,
        dry_run: bool = True,
        state_file: str = "queen_eternal_state.json",
        exchange: str = "binance",
        fee_structure: Optional[FeeStructure] = None,
        cost_basis_file: str = "cost_basis_history.json"
    ):
        self.breadcrumb_percent = breadcrumb_percent
        self.min_dip_advantage = min_dip_advantage
        self.dry_run = dry_run
        self.state_file = Path(state_file)
        self.exchange = exchange
        self.cost_basis_file = Path(cost_basis_file)
        
        # Fee structure - THE QUEEN KNOWS HER COSTS!
        self.fee_structure = fee_structure or EXCHANGE_FEES.get(exchange, EXCHANGE_FEES['default'])
        
        # Track total fees paid
        self.total_fees_paid: float = 0.0
        self.total_slippage_cost: float = 0.0
        
        # 🆕 FRIENDS WITH BAGGAGE SYSTEM
        self.friends: Dict[str, Friend] = {}  # All our "friends" (assets)
        self.cash_balance: float = 0.0  # Cash is the cleanest friend!
        
        # Portfolio state (legacy)
        self.main_position: Optional[MainPosition] = None
        self.breadcrumbs: Dict[str, Breadcrumb] = {}
        self.available_cash: float = 0.0
        
        # Market data cache
        self.market_data: Dict[str, MarketCoin] = {}
        self.last_scan_time: Optional[datetime] = None
        
        # Statistics
        self.total_cycles: int = 0
        self.total_leaps: int = 0
        self.total_breadcrumbs: int = 0
        self.total_scalps: int = 0
        self.total_profit_realized: float = 0.0
        self.cycle_history: List[CycleStats] = []
        
        # Running state
        self.is_running: bool = False
        self.start_time: Optional[datetime] = None
        
        # Load REAL positions from tracked_positions.json!
        if initial_vault is None:
            self._load_friends_from_real_positions()  # NEW: Load from LIVE positions!
            self.initial_vault = self.total_portfolio_value
        else:
            self.initial_vault = initial_vault
            self.available_cash = initial_vault
            self.cash_balance = initial_vault
        
        # Load existing state if available
        self._load_state()
        
        logger.info("👑 Queen Eternal Machine initialized")
        logger.info(f"   💰 Total vault: ${self.total_portfolio_value:.2f}")
        logger.info(f"   👥 Friends loaded: {len(self.friends)}")
        logger.info(f"   💵 Cash balance: ${self.cash_balance:.2f}")
        logger.info(f"   🍞 Breadcrumb %: {breadcrumb_percent*100:.1f}%")
        logger.info(f"   📉 Min dip advantage: {min_dip_advantage*100:.1f}%")
        logger.info(f"   🧪 Dry run: {dry_run}")
    
    def _load_friends_from_real_positions(self) -> None:
        """
        Load friends from LIVE API balances + cross-reference with cost basis tracker.
        
        THE TRUTH:
        - LIVE API balances = What we ACTUALLY HOLD right now
        - CostBasisTracker = What we PAID for stuff (with FIFO accounting)
        
        We might have bought/sold same coin multiple times!
        Only what we HOLD NOW matters for leaping.
        
        Cost basis comes from remaining lots after FIFO sales.
        """
        # First fetch LIVE balances from all exchanges
        live_balances = self._fetch_live_balances()
        
        if not live_balances:
            logger.warning("⚠️ No live balances available - falling back to cost basis fallback")
            self._load_friends_from_cost_basis_fallback()
            return
        
        # Initialize cost basis tracker for accurate cost basis calculation
        cost_basis_tracker = None
        try:
            from cost_basis_tracker import CostBasisTracker
            cost_basis_tracker = CostBasisTracker()
            logger.info("📊 Cost Basis Tracker: WIRED for accurate baggage calculation")
        except Exception as e:
            logger.warning(f"⚠️ Cost Basis Tracker unavailable: {e}")
        
        # Build friends from LIVE balances
        for asset, (qty, exchange) in live_balances.items():
            if qty <= 0:
                continue
            
            # Skip stablecoins (they're cash, not friends)
            if asset in ['USD', 'USDC', 'USDT', 'BUSD', 'EUR', 'GBP', 'TUSD']:
                self.cash_balance += qty if asset in ['USD', 'USDC', 'USDT', 'BUSD'] else 0
                continue
            
            # Get ACCURATE cost basis using the tracker
            cost_basis = 0.0
            entry_price = 0.0
            
            if cost_basis_tracker:
                # Try different symbol formats to find the position
                # The tracker expects just the base asset name (e.g., "ADA", "BTC")
                pos = cost_basis_tracker.get_cost_basis(asset, exchange)
                if pos:
                    # Use the tracker's accurate cost basis (remaining after FIFO)
                    cost_basis = pos.get('total_cost', 0)
                    entry_price = pos.get('avg_entry_price', 0)
                    logger.info(f"   📊 {asset}: Found cost basis ${cost_basis:.2f} @ ${entry_price:.4f}")
                else:
                    logger.info(f"   📊 {asset}: No cost basis found in tracker")
            else:
                # Fallback: read cost_basis_history.json directly with correct key format
                cost_basis_data = {}
                if self.cost_basis_file.exists():
                    try:
                        with open(self.cost_basis_file, 'r') as f:
                            cb_data = json.load(f)
                            cost_basis_data = cb_data.get('positions', {})
                    except Exception as e:
                        logger.warning(f"⚠️ Could not load cost basis file: {e}")
                
                # Try the correct key format: "exchange:asset"
                fallback_key = f"{exchange}:{asset}"
                if fallback_key in cost_basis_data:
                    cb = cost_basis_data[fallback_key]
                    total_cost = cb.get('total_cost', 0)
                    total_qty = cb.get('total_quantity', 0)
                    if total_qty > 0:
                        # This is still approximate - better than nothing
                        cost_per_unit = total_cost / total_qty
                        cost_basis = qty * cost_per_unit
                        entry_price = cb.get('avg_entry_price', cost_per_unit)
                        logger.info(f"   📊 {asset}: Fallback cost basis ${cost_basis:.2f} @ ${entry_price:.4f}")
                
                # Also try without exchange prefix as backup
                elif asset in cost_basis_data:
                    cb = cost_basis_data[asset]
                    total_cost = cb.get('total_cost', 0)
                    total_qty = cb.get('total_quantity', 0)
                    if total_qty > 0:
                        cost_per_unit = total_cost / total_qty
                        cost_basis = qty * cost_per_unit
                        entry_price = cb.get('avg_entry_price', cost_per_unit)
                        logger.info(f"   📊 {asset}: Fallback cost basis ${cost_basis:.2f} @ ${entry_price:.4f}")
            
            # If no cost basis found, assume current price (no baggage)
            if cost_basis == 0:
                # Try to get current price for initial cost basis
                current_price = 0.0
                # This is approximate - in real usage, market data would be available
                entry_price = current_price or 1.0  # Fallback
                cost_basis = qty * entry_price
                logger.info(f"   📊 {asset}: No cost basis found, assuming ${cost_basis:.2f} @ ${entry_price:.4f}")
            
            self.friends[asset] = Friend(
                symbol=asset,
                quantity=qty,
                cost_basis=cost_basis,
                entry_price=entry_price,
                current_price=entry_price,  # Will be updated with market data
                exchange=exchange
            )
        
        logger.info(f"👥 Loaded {len(self.friends)} friends from LIVE API balances")
        logger.info(f"   💵 Cash balance: ${self.cash_balance:.2f}")
        
        # Log summary with baggage info
        total_value = sum(f.current_value for f in self.friends.values())
        total_baggage = sum(f.baggage for f in self.friends.values())
        clear_friends = sum(1 for f in self.friends.values() if f.is_clear)
        
        logger.info(f"   💰 Total position value: ${total_value:.2f}")
        logger.info(f"   🧳 Total baggage: ${total_baggage:.2f}")
        logger.info(f"   ✅ Clear friends: {clear_friends}/{len(self.friends)}")
        
        # Log by exchange
        by_exchange: Dict[str, int] = {}
        for f in self.friends.values():
            by_exchange[f.exchange] = by_exchange.get(f.exchange, 0) + 1
        for ex, count in by_exchange.items():
            logger.info(f"   📍 {ex}: {count} positions")
    
    def _fetch_live_balances(self) -> Dict[str, Tuple[float, str]]:
        """
        Fetch LIVE balances from all exchange APIs.
        
        Returns: {asset: (quantity, exchange)}
        """
        balances: Dict[str, Tuple[float, str]] = {}
        
        # 1. BINANCE
        try:
            from binance_client import BinanceClient
            binance = BinanceClient()
            binance_bals = binance.get_balance()
            for asset, qty in binance_bals.items():
                if qty > 0:
                    balances[asset] = (qty, 'binance')
            logger.info(f"   📍 Binance: {len([q for q in binance_bals.values() if q > 0])} assets")
        except Exception as e:
            logger.warning(f"   ⚠️ Binance unavailable: {e}")
        
        # 2. ALPACA
        try:
            from alpaca_client import AlpacaClient
            alpaca = AlpacaClient()
            positions = alpaca.get_positions()
            for pos in positions:
                symbol = pos.get('symbol', '')
                qty = float(pos.get('qty', 0))
                if qty > 0 and symbol:
                    # Alpaca uses different symbol format
                    asset = symbol.replace('/USD', '').replace('USD', '')
                    if asset in balances:
                        # Merge with existing
                        old_qty, _ = balances[asset]
                        balances[asset] = (old_qty + qty, 'multi')
                    else:
                        balances[asset] = (qty, 'alpaca')
            logger.info(f"   📍 Alpaca: {len(positions)} positions")
        except Exception as e:
            logger.warning(f"   ⚠️ Alpaca unavailable: {e}")
        
        # 3. KRAKEN - Try live API first, cached snapshot ONLY as emergency fallback
        kraken_success = False
        try:
            from kraken_client import KrakenClient
            kraken = KrakenClient()
            kraken_bals = kraken.get_balance()
            for asset, qty in kraken_bals.items():
                qty = float(qty)
                if qty > 0:
                    # Clean Kraken asset names (remove X/Z prefixes)
                    clean_asset = asset.replace('.B', '').replace('X', '').replace('Z', '')
                    if len(clean_asset) > 1:
                        if clean_asset in balances:
                            old_qty, _ = balances[clean_asset]
                            balances[clean_asset] = (old_qty + qty, 'multi')
                        else:
                            balances[clean_asset] = (qty, 'kraken')
            logger.info(f"   📍 Kraken: {len([q for q in kraken_bals.values() if float(q) > 0])} assets (LIVE API)")
            kraken_success = True
        except Exception as e:
            logger.warning(f"   ⚠️ Kraken LIVE API failed: {e}")
            # ONLY use cached snapshot as emergency fallback
            try:
                kraken_file = Path("kraken_balance_snapshot_2026-02-03.json")
                if kraken_file.exists():
                    with open(kraken_file, 'r') as f:
                        kraken_data = json.load(f)
                    for asset, qty in kraken_data.get('balances', {}).items():
                        qty = float(qty)
                        if qty > 0:
                            # Clean Kraken asset names (remove X/Z prefixes)
                            clean_asset = asset.replace('.B', '').replace('X', '').replace('Z', '')
                            if len(clean_asset) > 1:
                                if clean_asset in balances:
                                    old_qty, _ = balances[clean_asset]
                                    balances[clean_asset] = (old_qty + qty, 'multi')
                                else:
                                    balances[clean_asset] = (qty, 'kraken-cached')
                    logger.info(f"   📍 Kraken: {len(kraken_data.get('balances', {}))} assets (CACHED FALLBACK - OLD DATA)")
                else:
                    logger.warning("   ⚠️ No Kraken cached snapshot available")
            except Exception as cache_e:
                logger.warning(f"   ⚠️ Kraken cached fallback also failed: {cache_e}")
        
        return balances
    
    def _load_friends_from_cost_basis_fallback(self) -> None:
        """Fallback: Load from cost_basis_history.json if tracked_positions.json doesn't exist."""
        try:
            if not self.cost_basis_file.exists():
                logger.warning(f"⚠️ Cost basis file not found: {self.cost_basis_file}")
                return
            
            with open(self.cost_basis_file, 'r') as f:
                data = json.load(f)
            
            positions = data.get('positions', {})
            
            for symbol, pos_data in positions.items():
                if not isinstance(pos_data, dict):
                    continue
                
                qty = pos_data.get('total_quantity', 0)
                cost = pos_data.get('total_cost', 0)
                entry_price = pos_data.get('avg_entry_price', 0)
                exchange = pos_data.get('exchange', 'binance')
                asset = pos_data.get('asset', symbol.replace('USDC', '').replace('USD', '').replace('EUR', ''))
                
                if qty <= 0 or cost <= 0:
                    continue
                
                self.friends[asset] = Friend(
                    symbol=asset,
                    quantity=qty,
                    cost_basis=cost,
                    entry_price=entry_price,
                    current_price=entry_price,
                    exchange=exchange
                )
            
            logger.warning(f"⚠️ Loaded {len(self.friends)} friends from cost_basis FALLBACK (not live positions!)")
            
        except Exception as e:
            logger.error(f"❌ Failed to load from cost_basis fallback: {e}")
    
    def update_friends_prices(self) -> None:
        """Update all friends with current market prices."""
        for symbol, friend in self.friends.items():
            market_coin = self.market_data.get(symbol)
            if market_coin:
                friend.update_price(market_coin.price)
    
    @property
    def total_portfolio_value(self) -> float:
        """Total value of all friends + cash."""
        friends_value = sum(f.current_value for f in self.friends.values())
        return friends_value + self.cash_balance
    
    @property
    def total_baggage(self) -> float:
        """Total baggage (unrealized loss) across all friends."""
        return sum(f.baggage for f in self.friends.values())
    
    @property
    def friends_with_baggage(self) -> List[Friend]:
        """All friends that have baggage (underwater)."""
        return [f for f in self.friends.values() if not f.is_clear]
    
    @property
    def clear_friends(self) -> List[Friend]:
        """All friends that are clear (at or above cost basis)."""
        return [f for f in self.friends.values() if f.is_clear]
    
    def get_best_leaper(self) -> Optional[Friend]:
        """
        Get the best friend to leap from.
        
        Priority:
        1. Cash (cleanest - no baggage)
        2. Friends with profit (can drop breadcrumbs)
        3. Friends with baggage (need to clear via deeper dip)
        """
        # Cash first
        if self.cash_balance > self.fee_structure.min_trade_size:
            return Friend(
                symbol="CASH",
                quantity=self.cash_balance,
                cost_basis=self.cash_balance,
                entry_price=1.0,
                current_price=1.0,
                exchange=self.exchange
            )
        
        # Find friend with most profit (clear + highest gain)
        clear = sorted(self.clear_friends, key=lambda f: f.profit_available, reverse=True)
        if clear and clear[0].leap_value > self.fee_structure.min_trade_size:
            return clear[0]
        
        # Find friend with baggage but enough value to leap
        baggage = sorted(self.friends_with_baggage, key=lambda f: f.leap_value, reverse=True)
        if baggage and baggage[0].leap_value > self.fee_structure.min_trade_size:
            return baggage[0]
        
        return None
    
    def show_friends_situation(self) -> str:
        """
        Display the current situation of all friends.
        
        Shows:
        - Total portfolio value
        - Cash balance (cleanest friend)
        - Friends with profit (ready to leap!)
        - Friends with baggage (need clearing)
        """
        self.update_friends_prices()
        
        lines = []
        lines.append("═" * 70)
        lines.append("👥 FRIENDS SITUATION - Who's Ready to Leap?")
        lines.append("═" * 70)
        
        # Cash
        lines.append(f"\n💵 CASH (Cleanest Friend): ${self.cash_balance:.2f}")
        
        # Portfolio totals
        lines.append(f"\n📊 PORTFOLIO SUMMARY:")
        lines.append(f"   💰 Total Value: ${self.total_portfolio_value:.2f}")
        lines.append(f"   ⚠️ Total Baggage: ${self.total_baggage:.2f}")
        lines.append(f"   👥 Total Friends: {len(self.friends)}")
        
        # Clear friends (ready to leap!)
        clear = self.clear_friends
        if clear:
            lines.append(f"\n✅ CLEAR FRIENDS ({len(clear)}) - Ready to Leap!")
            for f in sorted(clear, key=lambda x: x.profit_available, reverse=True)[:10]:
                profit = f.profit_available
                lines.append(f"   {f.symbol}: ${f.current_value:.2f} (+${profit:.2f} profit)")
        
        # Friends with baggage
        baggage = self.friends_with_baggage
        if baggage:
            lines.append(f"\n⚠️ FRIENDS WITH BAGGAGE ({len(baggage)}) - Need Deeper Dips!")
            for f in sorted(baggage, key=lambda x: x.baggage, reverse=True)[:10]:
                lines.append(f"   {f.symbol}: ${f.current_value:.2f} (-${f.baggage:.2f} baggage, {f.baggage_percent:.1f}%)")
        
        lines.append("\n" + "═" * 70)
        
        return "\n".join(lines)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MARKET DATA FETCHING
    # ═══════════════════════════════════════════════════════════════════════════
    
    def fetch_market_data(self) -> Dict[str, MarketCoin]:
        """Fetch live market data from Binance."""
        try:
            resp = requests.get(
                "https://api.binance.com/api/v3/ticker/24hr",
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            
            self.market_data.clear()
            
            for ticker in data:
                symbol = ticker['symbol']
                # Only USDC pairs with decent volume
                if symbol.endswith('USDC'):
                    volume = float(ticker['quoteVolume'])
                    if volume > 100000:  # Min $100k volume
                        coin_symbol = symbol.replace('USDC', '')
                        price = float(ticker['lastPrice'])
                        if price > 0.0001:  # Filter dust
                            self.market_data[coin_symbol] = MarketCoin(
                                symbol=coin_symbol,
                                price=price,
                                change_24h=float(ticker['priceChangePercent']),
                                volume_24h=volume,
                                high_24h=float(ticker['highPrice']),
                                low_24h=float(ticker['lowPrice'])
                            )
            
            self.last_scan_time = datetime.now()
            logger.info(f"📊 Fetched {len(self.market_data)} coins from market")
            return self.market_data
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch market data: {e}")
            return self.market_data
    
    def get_sorted_by_dip(self) -> List[MarketCoin]:
        """Get coins sorted by 24h loss (biggest losers first)."""
        return sorted(
            self.market_data.values(),
            key=lambda x: x.change_24h
        )
    
    def get_coins_in_red(self) -> List[MarketCoin]:
        """Get all coins currently in the red."""
        return [c for c in self.market_data.values() if c.change_24h < 0]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🐸 QUANTUM FROG - LEAP FOR QUANTITY (WITH ROCK SOLID FEE MATH!)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def find_friend_leap_opportunities(self, friend: Friend) -> List[LeapOpportunity]:
        """
        Find quantum leap opportunities FOR A SPECIFIC FRIEND with baggage accounting!
        
        🆕 FRIENDS WITH BAGGAGE MATH:
        - If friend has baggage, the target dip must be deep enough to:
          1. Cover all fees
          2. CLEAR the baggage (recover to original cost basis)
          3. Still leave profit for breadcrumbs!
        
        Example:
          - XRP bought at $2.00, now $1.90 (-5% = 5% baggage)
          - SLF is -40% (deep dip!)
          - Dip advantage: 35% (40% - 5%)
          - Leap clears baggage because when SLF recovers, we exceed original XRP cost!
        """
        opportunities = []
        
        if friend.symbol == "CASH":
            # Cash has no market change, use 0%
            friend_change = 0.0
            leap_value = friend.current_value
        else:
            market_coin = self.market_data.get(friend.symbol)
            if not market_coin:
                return opportunities
            friend_change = market_coin.change_24h
            friend.update_price(market_coin.price)
            leap_value = friend.leap_value
        
        # Calculate leap amount (keep breadcrumb behind if profitable)
        breadcrumb_value = 0
        if friend.is_clear and friend.profit_available > 0:
            # Friend is clear! Leave breadcrumb of profit
            breadcrumb_value = leap_value * self.breadcrumb_percent
            leap_value = leap_value - breadcrumb_value
        
        # Skip if below minimum trade size
        if leap_value < self.fee_structure.min_trade_size:
            return opportunities
        
        # The BAGGAGE we need to clear (if any)
        baggage_percent = friend.baggage_percent
        
        for symbol, coin in self.market_data.items():
            if symbol == friend.symbol:
                continue
            
            # Skip low volume coins (slippage nightmare)
            if coin.volume_24h < 500000:
                continue
            
            # Calculate dip advantage (how much MORE it fell than our friend)
            dip_advantage = friend_change - coin.change_24h
            
            # ═══════════════════════════════════════════════════════════════
            # THE QUEEN'S BAGGAGE-AWARE FEE MATH
            # ═══════════════════════════════════════════════════════════════
            
            # SELL side
            sell_fee = leap_value * self.fee_structure.taker_fee
            sell_slippage = leap_value * self.fee_structure.slippage_estimate
            value_after_sell = leap_value - sell_fee - sell_slippage
            
            # BUY side
            buy_fee = value_after_sell * self.fee_structure.taker_fee
            buy_slippage = value_after_sell * self.fee_structure.slippage_estimate
            net_value_for_purchase = value_after_sell - buy_fee - buy_slippage
            
            # Total costs
            total_fees = sell_fee + buy_fee
            total_slippage = sell_slippage + buy_slippage
            total_cost = total_fees + total_slippage
            
            # Fee percentage
            fee_percent = (total_cost / leap_value) * 100 if leap_value > 0 else 999
            
            # REQUIRED DIP ADVANTAGE:
            # Must cover: fees + baggage + small profit margin
            min_required_dip = fee_percent + baggage_percent + 0.5  # 0.5% margin
            
            # Calculate quantities
            new_qty = net_value_for_purchase / coin.price if coin.price > 0 else 0
            
            # If friend is NOT cash, calculate equivalent qty for comparison
            if friend.symbol != "CASH":
                # How many we're leaping (not counting breadcrumb)
                old_qty = (leap_value / friend.current_price) if friend.current_price > 0 else 0
                fee_adjusted_multiplier = new_qty / old_qty if old_qty > 0 else 0
            else:
                # Cash: compare value
                old_qty = leap_value
                fee_adjusted_multiplier = net_value_for_purchase / leap_value if leap_value > 0 else 0
            
            # Only consider if dip advantage is sufficient
            if dip_advantage >= min_required_dip and fee_adjusted_multiplier > 1.0:
                recovery_advantage = abs(coin.change_24h) - abs(friend_change)
                
                opportunities.append(LeapOpportunity(
                    from_symbol=friend.symbol,
                    to_symbol=symbol,
                    from_price=friend.current_price,
                    to_price=coin.price,
                    from_change=friend_change,
                    to_change=coin.change_24h,
                    dip_advantage=dip_advantage,
                    quantity_multiplier=new_qty / old_qty if old_qty > 0 else 0,
                    recovery_advantage=recovery_advantage,
                    gross_value=leap_value,
                    sell_fee_cost=sell_fee,
                    buy_fee_cost=buy_fee,
                    slippage_cost=total_slippage,
                    total_fees=total_cost,
                    net_value_after_fees=net_value_for_purchase,
                    fee_adjusted_multiplier=fee_adjusted_multiplier
                ))
        
        # Sort by fee-adjusted multiplier (best real gains first)
        opportunities.sort(key=lambda x: x.fee_adjusted_multiplier, reverse=True)
        return opportunities
    
    def find_leap_opportunities(self) -> List[LeapOpportunity]:
        """
        Find quantum leap opportunities WITH FULL FEE ACCOUNTING.
        
        The Queen's ROCK SOLID math:
        1. Calculate gross value of leap
        2. Subtract SELL fee (exiting current position)
        3. Subtract BUY fee (entering new position)
        4. Subtract SLIPPAGE both ways
        5. ONLY leap if net quantity gain > 1.0 AFTER all costs!
        
        A leap is justified when:
        1. Target coin dipped MORE than current position
        2. Dip advantage EXCEEDS total fee cost
        3. NET quantity multiplier > 1.0 after all fees
        """
        opportunities = []
        
        if not self.main_position:
            return opportunities
        
        current = self.market_data.get(self.main_position.symbol)
        if not current:
            return opportunities
        
        # Calculate the value we're leaping with (90% of main position)
        leap_qty = self.main_position.quantity * (1 - self.breadcrumb_percent)
        gross_value = leap_qty * current.price
        
        # Skip if below minimum trade size
        if gross_value < self.fee_structure.min_trade_size:
            return opportunities
        
        for symbol, coin in self.market_data.items():
            if symbol == self.main_position.symbol:
                continue
            
            # Skip low volume coins (slippage nightmare)
            if coin.volume_24h < 500000:  # Require $500k daily volume
                continue
            
            # Calculate dip advantage (how much MORE it fell)
            dip_advantage = current.change_24h - coin.change_24h
            
            # ═══════════════════════════════════════════════════════════════
            # THE QUEEN'S FEE CALCULATION - CRYSTAL CLEAR MATH
            # ═══════════════════════════════════════════════════════════════
            
            # SELL side: Exiting current position
            sell_fee = gross_value * self.fee_structure.taker_fee
            sell_slippage = gross_value * self.fee_structure.slippage_estimate
            value_after_sell = gross_value - sell_fee - sell_slippage
            
            # BUY side: Entering new position
            buy_fee = value_after_sell * self.fee_structure.taker_fee
            buy_slippage = value_after_sell * self.fee_structure.slippage_estimate
            net_value_for_purchase = value_after_sell - buy_fee - buy_slippage
            
            # Total costs
            total_fees = sell_fee + buy_fee
            total_slippage = sell_slippage + buy_slippage
            total_cost = total_fees + total_slippage
            
            # Calculate quantities
            gross_new_qty = gross_value / coin.price  # If no fees
            actual_new_qty = net_value_for_purchase / coin.price  # After all fees
            
            # The REAL multiplier after fees
            fee_adjusted_multiplier = actual_new_qty / leap_qty if leap_qty > 0 else 0
            
            # Minimum dip advantage required to cover fees
            fee_percent = (total_cost / gross_value) * 100
            
            # Aggressive leap criteria - with relaxed thresholds for demo
            # Accept any leap that doesn't lose money (just need positive fee-adjusted multiplier)
            if fee_adjusted_multiplier > 0.90:  # Only need 90% after fees
                # Calculate recovery advantage
                recovery_advantage = abs(coin.change_24h) - abs(current.change_24h)
                
                opportunities.append(LeapOpportunity(
                    from_symbol=self.main_position.symbol,
                    to_symbol=symbol,
                    from_price=current.price,
                    to_price=coin.price,
                    from_change=current.change_24h,
                    to_change=coin.change_24h,
                    dip_advantage=dip_advantage,
                    quantity_multiplier=gross_new_qty / leap_qty if leap_qty > 0 else 0,
                    recovery_advantage=recovery_advantage,
                    # Fee details - FULL TRANSPARENCY
                    gross_value=gross_value,
                    sell_fee_cost=sell_fee,
                    buy_fee_cost=buy_fee,
                    slippage_cost=total_slippage,
                    total_fees=total_cost,
                    net_value_after_fees=net_value_for_purchase,
                    fee_adjusted_multiplier=fee_adjusted_multiplier
                ))
        
        # Sort by fee-adjusted multiplier (best real gains first)
        opportunities.sort(key=lambda x: x.fee_adjusted_multiplier, reverse=True)
        return opportunities
    
    def execute_quantum_leap(self, opportunity: LeapOpportunity) -> bool:
        """
        Execute a BLOODLESS quantum leap with breadcrumb.
        
        THE GOLDEN RULE: VALUE STAYS THE SAME (minus fees), QUANTITY GROWS!
        
        ROCK SOLID MATH:
        1. Leave BREADCRUMB_PERCENT in current coin (keeps growing there)
        2. Calculate EXACT fees (sell fee + slippage + buy fee + slippage)
        3. Swap remaining VALUE for new coin AFTER deducting all fees
        4. Because target fell MORE, you STILL get MORE QUANTITY even after fees
        5. Track every penny of fees paid
        
        Example with fees:
          - Have: 0.05 ETH @ $2000 = $100 value
          - Leap 90%: $90 gross value
          - Sell fee (0.1%): $0.09
          - Sell slippage (0.05%): $0.045
          - After sell: $89.865
          - Buy fee (0.1%): $0.090
          - Buy slippage (0.05%): $0.045
          - Net value: $89.73 (lost $0.27 to fees/slippage)
          - BUT: Target fell 20% more, so $89.73 buys MORE coins than $90 of old coin!
        """
        if not self.main_position:
            logger.warning("⚠️ No main position to leap from")
            return False
        
        # Verify the leap is still profitable after fees
        if not opportunity.is_profitable_after_fees:
            logger.warning(f"⚠️ Leap rejected - not profitable after fees!")
            logger.warning(f"   Fee-adjusted multiplier: {opportunity.fee_adjusted_multiplier:.4f}x (needs > 1.0)")
            return False
        
        # Current value at CURRENT prices
        current_value = self.main_position.current_value
        breadcrumb_value = current_value * self.breadcrumb_percent
        
        # Use the PRE-CALCULATED net value from the opportunity (already fee-adjusted!)
        net_value_for_purchase = opportunity.net_value_after_fees
        
        # Track fees paid
        self.total_fees_paid += opportunity.total_fees
        self.total_slippage_cost += opportunity.slippage_cost
        
        # Calculate quantities
        old_qty = self.main_position.quantity * (1 - self.breadcrumb_percent)
        new_qty = net_value_for_purchase / opportunity.to_price
        
        # Create breadcrumb from current position (this stays and grows!)
        breadcrumb_qty = self.main_position.quantity * self.breadcrumb_percent
        breadcrumb = Breadcrumb(
            symbol=self.main_position.symbol,
            quantity=breadcrumb_qty,
            cost_basis=breadcrumb_value,
            entry_price=self.main_position.current_price,
            entry_time=datetime.now(),
            current_price=self.main_position.current_price
        )
        self.breadcrumbs[self.main_position.symbol] = breadcrumb
        self.total_breadcrumbs += 1
        
        # Create new main position with FEE-ADJUSTED values
        self.main_position = MainPosition(
            symbol=opportunity.to_symbol,
            quantity=new_qty,
            cost_basis=net_value_for_purchase,  # Real cost after fees
            entry_price=opportunity.to_price,
            entry_time=datetime.now(),
            current_price=opportunity.to_price,
            change_24h=opportunity.to_change
        )
        
        self.total_leaps += 1
        
        # DETAILED LOGGING WITH FULL FEE BREAKDOWN
        logger.info(f"🐸 BLOODLESS QUANTUM LEAP! (Fee-adjusted)")
        logger.info(f"   ════════════════════════════════════════════")
        logger.info(f"   💰 GROSS VALUE: ${opportunity.gross_value:.4f}")
        logger.info(f"   📉 SELL FEE:    -${opportunity.sell_fee_cost:.4f} ({self.fee_structure.taker_fee*100:.2f}%)")
        logger.info(f"   📉 BUY FEE:     -${opportunity.buy_fee_cost:.4f} ({self.fee_structure.taker_fee*100:.2f}%)")
        logger.info(f"   📉 SLIPPAGE:    -${opportunity.slippage_cost:.4f} ({self.fee_structure.slippage_estimate*100:.2f}% x2)")
        logger.info(f"   ────────────────────────────────────────────")
        logger.info(f"   💵 NET VALUE:   ${net_value_for_purchase:.4f}")
        logger.info(f"   💸 TOTAL COST:  ${opportunity.total_fees:.4f} ({opportunity.total_fees/opportunity.gross_value*100:.2f}%)")
        logger.info(f"   ════════════════════════════════════════════")
        logger.info(f"   📦 OLD QTY: {old_qty:.6f} {opportunity.from_symbol}")
        logger.info(f"   📦 NEW QTY: {new_qty:.6f} {opportunity.to_symbol}")
        logger.info(f"   🎯 MULTIPLIER: {opportunity.fee_adjusted_multiplier:.4f}x (AFTER fees!)")
        logger.info(f"   ════════════════════════════════════════════")
        logger.info(f"   🍞 Breadcrumb: {breadcrumb_qty:.6f} {opportunity.from_symbol} (${breadcrumb_value:.2f})")
        logger.info(f"   📊 Dip advantage: {opportunity.dip_advantage:.2f}% (vs {opportunity.total_fees/opportunity.gross_value*100:.2f}% fees)")
        logger.info(f"   💰 Lifetime fees paid: ${self.total_fees_paid:.4f}")
        
        self._save_state()
        return True
    
    def execute_friend_leap(self, friend: Friend, opportunity: LeapOpportunity) -> bool:
        """
        Execute a quantum leap for a FRIEND with cost basis tracking integration.
        
        This updates the cost basis tracker so baggage calculations stay accurate.
        """
        if friend.symbol not in self.friends:
            logger.warning(f"⚠️ Friend {friend.symbol} not found")
            return False
        
        # Verify the leap is still profitable
        if not opportunity.is_profitable_after_fees:
            logger.warning(f"⚠️ Friend leap rejected - not profitable after fees!")
            return False
        
        # Initialize cost basis tracker
        cost_basis_tracker = None
        try:
            from cost_basis_tracker import CostBasisTracker
            cost_basis_tracker = CostBasisTracker()
        except Exception as e:
            logger.warning(f"⚠️ Cost basis tracker unavailable for leap recording: {e}")
        
        # Calculate leap amounts
        leap_value = opportunity.gross_value
        breadcrumb_value = opportunity.gross_value * self.breadcrumb_percent
        net_leap_value = leap_value - breadcrumb_value
        
        # Track fees
        self.total_fees_paid += opportunity.total_fees
        self.total_slippage_cost += opportunity.slippage_cost
        
        # Calculate quantities
        old_qty_leaping = net_leap_value / friend.current_price if friend.current_price > 0 else 0
        new_qty = opportunity.net_value_after_fees / opportunity.to_price if opportunity.to_price > 0 else 0
        
        # Leave breadcrumb if friend is clear
        if friend.is_clear and breadcrumb_value > 0:
            breadcrumb_qty = breadcrumb_value / friend.current_price if friend.current_price > 0 else 0
            breadcrumb = Breadcrumb(
                symbol=friend.symbol,
                quantity=breadcrumb_qty,
                cost_basis=breadcrumb_value,
                entry_price=friend.current_price,
                entry_time=datetime.now(),
                current_price=friend.current_price
            )
            self.breadcrumbs[friend.symbol] = breadcrumb
            self.total_breadcrumbs += 1
            
            # Reduce friend's quantity by breadcrumb amount
            friend.quantity -= breadcrumb_qty
        
        # Reduce friend's quantity by leaping amount
        friend.quantity -= old_qty_leaping
        
        # If friend is now empty, remove them
        if friend.quantity <= 0.000001:
            del self.friends[friend.symbol]
        else:
            # Update friend's cost basis proportionally
            # (This is approximate - cost basis tracker has the real FIFO accounting)
            remaining_ratio = friend.quantity / (friend.quantity + old_qty_leaping)
            friend.cost_basis *= remaining_ratio
        
        # Add new friend or update existing
        if opportunity.to_symbol in self.friends:
            # Merge with existing friend
            existing = self.friends[opportunity.to_symbol]
            total_qty = existing.quantity + new_qty
            total_cost = existing.cost_basis + opportunity.net_value_after_fees
            avg_price = total_cost / total_qty if total_qty > 0 else opportunity.to_price
            
            existing.quantity = total_qty
            existing.cost_basis = total_cost
            existing.entry_price = avg_price
            existing.current_price = opportunity.to_price
        else:
            # Create new friend
            self.friends[opportunity.to_symbol] = Friend(
                symbol=opportunity.to_symbol,
                quantity=new_qty,
                cost_basis=opportunity.net_value_after_fees,
                entry_price=opportunity.to_price,
                current_price=opportunity.to_price,
                exchange=friend.exchange  # Same exchange
            )
        
        # Record the trades in cost basis tracker
        if cost_basis_tracker and not self.dry_run:
            try:
                # Record sell of old position
                cost_basis_tracker.record_trade(
                    symbol=f"{friend.symbol}USDT",  # Assume USDT pair
                    side='sell',
                    quantity=old_qty_leaping,
                    price=friend.current_price,
                    exchange=friend.exchange,
                    fee=opportunity.sell_fee_cost + (opportunity.slippage_cost / 2)
                )
                
                # Record buy of new position
                cost_basis_tracker.record_trade(
                    symbol=f"{opportunity.to_symbol}USDT",  # Assume USDT pair
                    side='buy',
                    quantity=new_qty,
                    price=opportunity.to_price,
                    exchange=friend.exchange,
                    fee=opportunity.buy_fee_cost + (opportunity.slippage_cost / 2)
                )
                
                logger.info(f"📊 Cost basis updated for friend leap")
            except Exception as e:
                logger.warning(f"⚠️ Failed to update cost basis tracker: {e}")
        
        self.total_leaps += 1
        
        # Detailed logging
        logger.info(f"🐸 FRIEND QUANTUM LEAP! {friend.symbol} → {opportunity.to_symbol}")
        logger.info(f"   ═══════════════════════════════════════════════")
        logger.info(f"   💰 GROSS LEAP: ${leap_value:.4f}")
        logger.info(f"   🍞 BREADCRUMB: -${breadcrumb_value:.4f} ({self.breadcrumb_percent*100:.1f}%)")
        logger.info(f"   📉 FEES:       -${opportunity.total_fees:.4f}")
        logger.info(f"   ───────────────────────────────────────────────")
        logger.info(f"   💵 NET VALUE:  ${opportunity.net_value_after_fees:.4f}")
        logger.info(f"   📦 LEAP QTY:   {old_qty_leaping:.6f} {friend.symbol}")
        logger.info(f"   📦 NEW QTY:    {new_qty:.6f} {opportunity.to_symbol}")
        logger.info(f"   📦 MULTIPLIER: {new_qty/old_qty_leaping:.4f}x")
        logger.info(f"   ═══════════════════════════════════════════════")
        
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🟡 YELLOW BRICK ROAD - INITIALIZE JOURNEY
    # ═══════════════════════════════════════════════════════════════════════════
    
    def start_journey(self, start_symbol: str = "ETH") -> bool:
        """
        Start the Yellow Brick Road journey.
        
        Enter the market with the full vault in the starting coin.
        """
        if self.main_position:
            logger.warning("⚠️ Journey already in progress")
            return False
        
        self.fetch_market_data()
        
        if start_symbol not in self.market_data:
            logger.error(f"❌ {start_symbol} not found in market data")
            return False
        
        coin = self.market_data[start_symbol]
        quantity = self.available_cash / coin.price
        
        self.main_position = MainPosition(
            symbol=start_symbol,
            quantity=quantity,
            cost_basis=self.available_cash,
            entry_price=coin.price,
            entry_time=datetime.now(),
            current_price=coin.price,
            change_24h=coin.change_24h
        )
        
        self.available_cash = 0.0
        self.start_time = datetime.now()
        
        logger.info(f"🟡 YELLOW BRICK ROAD JOURNEY STARTED!")
        logger.info(f"   Starting coin: {start_symbol}")
        logger.info(f"   Entry price: ${coin.price:.4f}")
        logger.info(f"   Quantity: {quantity:.6f} {start_symbol}")
        logger.info(f"   Vault deployed: ${self.initial_vault:.2f}")
        
        self._save_state()
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🍞 BREADCRUMB MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def update_breadcrumbs(self) -> Dict[str, float]:
        """Update all breadcrumb positions with current prices."""
        updates = {}
        
        for symbol, crumb in self.breadcrumbs.items():
            if symbol in self.market_data:
                old_value = crumb.current_value
                crumb.update_price(self.market_data[symbol].price)
                updates[symbol] = crumb.unrealized_pnl
        
        return updates
    
    def get_breadcrumb_summary(self) -> Dict[str, Any]:
        """Get summary of all breadcrumb positions."""
        total_cost = sum(c.cost_basis for c in self.breadcrumbs.values())
        total_value = sum(c.current_value for c in self.breadcrumbs.values())
        total_pnl = total_value - total_cost
        
        return {
            "count": len(self.breadcrumbs),
            "total_cost": total_cost,
            "total_value": total_value,
            "total_pnl": total_pnl,
            "pnl_percent": (total_pnl / total_cost * 100) if total_cost > 0 else 0,
            "positions": {
                s: {
                    "quantity": c.quantity,
                    "cost": c.cost_basis,
                    "value": c.current_value,
                    "pnl": c.unrealized_pnl,
                    "pnl_pct": c.pnl_percent
                }
                for s, c in self.breadcrumbs.items()
            }
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ⚡ MICRO SCALPING
    # ═══════════════════════════════════════════════════════════════════════════
    
    def find_scalp_opportunities(self) -> List[Tuple[str, float]]:
        """
        Find breadcrumbs ready for scalping.
        
        A scalp is ready when:
        1. Breadcrumb has gained MIN_PROFIT_SCALP or more
        2. Market shows signs of bounce exhaustion (optional)
        """
        opportunities = []
        
        for symbol, crumb in self.breadcrumbs.items():
            if crumb.pnl_percent >= MIN_PROFIT_SCALP * 100:
                opportunities.append((symbol, crumb.pnl_percent))
        
        # Sort by profit (highest first)
        opportunities.sort(key=lambda x: x[1], reverse=True)
        return opportunities
    
    def execute_scalp(self, symbol: str, percent_to_sell: float = 0.5) -> float:
        """
        Execute a scalp on a breadcrumb position.
        
        Sells a portion of the position to realize profit,
        leaving the rest to continue growing.
        """
        if symbol not in self.breadcrumbs:
            return 0.0
        
        crumb = self.breadcrumbs[symbol]
        sell_qty = crumb.quantity * percent_to_sell
        sell_value = sell_qty * crumb.current_price
        
        # Calculate realized profit
        cost_portion = crumb.cost_basis * percent_to_sell
        profit = sell_value - cost_portion
        
        # Update breadcrumb
        crumb.quantity -= sell_qty
        crumb.cost_basis -= cost_portion
        
        # Add to available cash
        self.available_cash += sell_value
        self.total_profit_realized += profit
        self.total_scalps += 1
        
        # Remove if too small
        if crumb.quantity * crumb.current_price < 1.0:  # Less than $1
            del self.breadcrumbs[symbol]
        
        logger.info(f"⚡ SCALP EXECUTED on {symbol}!")
        logger.info(f"   Sold: {sell_qty:.4f} @ ${crumb.current_price:.4f}")
        logger.info(f"   Realized profit: ${profit:.2f}")
        
        self._save_state()
        return profit
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🔄 MAIN CYCLE - THE 24/7 MACHINE
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def run_cycle(self) -> CycleStats:
        """
        Run a single cycle of the eternal machine.
        
        1. SCAN - Fetch market data
        2. UPDATE - Update all positions
        3. ANALYZE - Find leap opportunities
        4. LEAP - Execute best leap if available
        5. SCALP - Harvest ready breadcrumbs
        6. RECORD - Log statistics
        """
        self.total_cycles += 1
        stats = CycleStats(
            cycle_number=self.total_cycles,
            start_time=datetime.now()
        )
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🔄 CYCLE #{self.total_cycles} - {datetime.now().strftime('%H:%M:%S')}")
        logger.info(f"{'='*60}")
        
        # 1. SCAN
        self.fetch_market_data()
        
        # 2. UPDATE
        if self.main_position and self.main_position.symbol in self.market_data:
            coin = self.market_data[self.main_position.symbol]
            self.main_position.update(coin.price, coin.change_24h)
        
        self.update_breadcrumbs()
        
        # 3. ANALYZE
        opportunities = self.find_leap_opportunities()
        
        # 4. LEAP (if good opportunity)
        if opportunities:
            best = opportunities[0]
            # Execute the best leap opportunity (fee-adjusted multiplier already validated it)
            if self.execute_quantum_leap(best):
                stats.leaps_made += 1
                stats.breadcrumbs_planted += 1
        
        # 5. SCALP
        scalp_opps = self.find_scalp_opportunities()
        for symbol, pnl_pct in scalp_opps[:3]:  # Max 3 scalps per cycle
            profit = self.execute_scalp(symbol)
            if profit > 0:
                stats.scalps_executed += 1
                stats.profit_realized += profit
        
        # 6. RECORD
        stats.end_time = datetime.now()
        self.cycle_history.append(stats)
        
        # Log summary
        self._log_cycle_summary(stats)
        
        self._save_state()
        return stats
    
    async def run_forever(self, interval_seconds: int = SCAN_INTERVAL_SECONDS):
        """
        Run the eternal machine forever.
        
        This is the 24/7 loop that never stops.
        """
        self.is_running = True
        logger.info("👑🤖 QUEEN ETERNAL MACHINE ACTIVATED - 24/7 MODE")
        
        try:
            while self.is_running:
                await self.run_cycle()
                await asyncio.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("👑 Machine stopped by user")
        except Exception as e:
            logger.error(f"❌ Machine error: {e}")
        finally:
            self.is_running = False
            self._save_state()
    
    def stop(self):
        """Stop the eternal machine."""
        self.is_running = False
        logger.info("👑 Machine stopping...")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 📊 REPORTING & LOGGING
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _log_cycle_summary(self, stats: CycleStats):
        """Log summary of a cycle."""
        logger.info(f"\n📊 CYCLE #{stats.cycle_number} SUMMARY:")
        
        # Main position
        if self.main_position:
            mp = self.main_position
            logger.info(f"   Main: {mp.quantity:.4f} {mp.symbol} @ ${mp.current_price:.4f} = ${mp.current_value:.2f}")
            logger.info(f"         24h: {mp.change_24h:+.2f}% | P&L: ${mp.unrealized_pnl:+.2f}")
        
        # Breadcrumbs
        summary = self.get_breadcrumb_summary()
        logger.info(f"   Breadcrumbs: {summary['count']} positions")
        logger.info(f"         Value: ${summary['total_value']:.2f} | P&L: ${summary['total_pnl']:+.2f} ({summary['pnl_percent']:+.2f}%)")
        
        # Totals
        total_value = (self.main_position.current_value if self.main_position else 0) + summary['total_value'] + self.available_cash
        total_pnl = total_value - self.initial_vault
        logger.info(f"   Total Portfolio: ${total_value:.2f}")
        logger.info(f"   Total P&L: ${total_pnl:+.2f} ({total_pnl/self.initial_vault*100:+.2f}%)")
        logger.info(f"   Cash: ${self.available_cash:.2f}")
        
        # Stats
        logger.info(f"   Lifetime: {self.total_leaps} leaps | {self.total_breadcrumbs} breadcrumbs | {self.total_scalps} scalps")
        logger.info(f"   Realized profit: ${self.total_profit_realized:.2f}")
    
    def get_full_report(self) -> Dict[str, Any]:
        """Generate a full portfolio report."""
        self.update_breadcrumbs()
        
        main_value = self.main_position.current_value if self.main_position else 0
        breadcrumb_summary = self.get_breadcrumb_summary()
        total_value = main_value + breadcrumb_summary['total_value'] + self.available_cash
        
        return {
            "timestamp": datetime.now().isoformat(),
            "initial_vault": self.initial_vault,
            "total_value": total_value,
            "total_pnl": total_value - self.initial_vault,
            "total_pnl_percent": (total_value / self.initial_vault - 1) * 100,
            "cash": self.available_cash,
            "main_position": {
                "symbol": self.main_position.symbol if self.main_position else None,
                "quantity": self.main_position.quantity if self.main_position else 0,
                "value": main_value,
                "cost_basis": self.main_position.cost_basis if self.main_position else 0,
                "unrealized_pnl": self.main_position.unrealized_pnl if self.main_position else 0,
                "change_24h": self.main_position.change_24h if self.main_position else 0
            },
            "breadcrumbs": breadcrumb_summary,
            "statistics": {
                "total_cycles": self.total_cycles,
                "total_leaps": self.total_leaps,
                "total_breadcrumbs": self.total_breadcrumbs,
                "total_scalps": self.total_scalps,
                "total_profit_realized": self.total_profit_realized,
                "running_since": self.start_time.isoformat() if self.start_time else None
            }
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 💾 STATE PERSISTENCE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _save_state(self):
        """Save current state to file."""
        try:
            state = {
                "timestamp": datetime.now().isoformat(),
                "initial_vault": self.initial_vault,
                "available_cash": self.available_cash,
                "main_position": {
                    "symbol": self.main_position.symbol,
                    "quantity": self.main_position.quantity,
                    "cost_basis": self.main_position.cost_basis,
                    "entry_price": self.main_position.entry_price,
                    "entry_time": self.main_position.entry_time.isoformat()
                } if self.main_position else None,
                "breadcrumbs": {
                    s: {
                        "quantity": c.quantity,
                        "cost_basis": c.cost_basis,
                        "entry_price": c.entry_price,
                        "entry_time": c.entry_time.isoformat()
                    }
                    for s, c in self.breadcrumbs.items()
                },
                "statistics": {
                    "total_cycles": self.total_cycles,
                    "total_leaps": self.total_leaps,
                    "total_breadcrumbs": self.total_breadcrumbs,
                    "total_scalps": self.total_scalps,
                    "total_profit_realized": self.total_profit_realized,
                    "start_time": self.start_time.isoformat() if self.start_time else None
                }
            }
            
            # Atomic write
            temp_file = self.state_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(state, f, indent=2)
            temp_file.rename(self.state_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to save state: {e}")
    
    def _load_state(self):
        """Load state from file if exists."""
        if not self.state_file.exists():
            return
        
        try:
            with open(self.state_file) as f:
                state = json.load(f)
            
            self.initial_vault = state.get("initial_vault", self.initial_vault)
            self.available_cash = state.get("available_cash", 0)
            
            # Load main position
            mp_data = state.get("main_position")
            if mp_data:
                self.main_position = MainPosition(
                    symbol=mp_data["symbol"],
                    quantity=mp_data["quantity"],
                    cost_basis=mp_data["cost_basis"],
                    entry_price=mp_data["entry_price"],
                    entry_time=datetime.fromisoformat(mp_data["entry_time"])
                )
            
            # Load breadcrumbs
            for symbol, data in state.get("breadcrumbs", {}).items():
                self.breadcrumbs[symbol] = Breadcrumb(
                    symbol=symbol,
                    quantity=data["quantity"],
                    cost_basis=data["cost_basis"],
                    entry_price=data["entry_price"],
                    entry_time=datetime.fromisoformat(data["entry_time"])
                )
            
            # Load statistics
            stats = state.get("statistics", {})
            self.total_cycles = stats.get("total_cycles", 0)
            self.total_leaps = stats.get("total_leaps", 0)
            self.total_breadcrumbs = stats.get("total_breadcrumbs", 0)
            self.total_scalps = stats.get("total_scalps", 0)
            self.total_profit_realized = stats.get("total_profit_realized", 0)
            if stats.get("start_time"):
                self.start_time = datetime.fromisoformat(stats["start_time"])
            
            logger.info(f"📂 Loaded state from {self.state_file}")
            logger.info(f"   Main: {self.main_position.symbol if self.main_position else 'None'}")
            logger.info(f"   Breadcrumbs: {len(self.breadcrumbs)}")
            logger.info(f"   Cycles: {self.total_cycles}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load state: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎮 CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Print the Queen's banner."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║     👑🤖 THE QUEEN'S ETERNAL MACHINE 🤖👑                                            ║
║                                                                                      ║
║     🏔️  Mountain Pilgrimage  │  🐸 Quantum Frog      │  💉 Bloodless Descent        ║
║     🟡  Yellow Brick Road    │  🍞 Breadcrumb Trail  │  🤖 24/7 Machine              ║
║                                                                                      ║
║     "I NEVER SLEEP. I NEVER STOP. I AM THE MACHINE."                                ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
    """)


async def run_demo():
    """Run a demonstration of the Queen's machine."""
    print_banner()
    
    machine = QueenEternalMachine(
        initial_vault=100.0,
        breadcrumb_percent=0.10,
        min_dip_advantage=0.02,
        dry_run=True
    )
    
    # Start the journey
    print("\n🟡 Starting Yellow Brick Road journey...")
    machine.start_journey("ETH")
    
    # Run a few cycles
    print("\n🔄 Running 3 demonstration cycles...")
    for _ in range(3):
        await machine.run_cycle()
        await asyncio.sleep(2)
    
    # Print final report
    print("\n" + "="*60)
    print("📊 FINAL REPORT")
    print("="*60)
    
    report = machine.get_full_report()
    print(json.dumps(report, indent=2, default=str))


async def run_live(vault: float = 100.0, interval: int = 60, start_symbol: str = "ETH"):
    """Run the machine in live mode."""
    print_banner()
    
    machine = QueenEternalMachine(
        initial_vault=vault,
        breadcrumb_percent=0.10,
        min_dip_advantage=0.02,
        dry_run=True  # Start in dry run for safety
    )
    
    # Start journey if not already started
    if not machine.main_position:
        print(f"\n🟡 Starting Yellow Brick Road journey with {start_symbol}...")
        machine.start_journey(start_symbol)
    
    # Run forever
    print(f"\n🤖 Running 24/7 mode (interval: {interval}s)...")
    print("   Press Ctrl+C to stop\n")
    
    await machine.run_forever(interval_seconds=interval)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="The Queen's Eternal Machine")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--live", action="store_true", help="Run live 24/7 mode")
    parser.add_argument("--vault", type=float, default=100.0, help="Initial vault amount")
    parser.add_argument("--interval", type=int, default=60, help="Scan interval in seconds")
    parser.add_argument("--symbol", type=str, default="ETH", help="Starting symbol for the journey")
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    if args.demo:
        asyncio.run(run_demo())
    elif args.live:
        asyncio.run(run_live(args.vault, args.interval, args.symbol))
    else:
        # Default: run demo
        asyncio.run(run_demo())
