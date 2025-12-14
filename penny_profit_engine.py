#!/usr/bin/env python3
"""
🪙 PENNY PROFIT ENGINE
======================
The stupidest AND smartest trading strategy:
"Am I up by the exact amount needed for 1 penny profit? SELL."

Loads validated thresholds from penny_profit_thresholds.json and provides
simple dollar-based exit rules for each exchange.

Gary Leckey & GitHub Copilot | December 2025
"""

import json
import os
import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PennyThreshold:
    """Threshold for a specific trade size on an exchange."""
    trade_size: float
    total_cost: float
    win_gte: float      # Gross P&L >= this = TAKE PROFIT
    stop_lte: float     # Gross P&L <= this = STOP LOSS
    win_pct: float      # Price move % for win
    stop_pct: float     # Price move % for stop


class PennyProfitEngine:
    """
    The Penny Profit Engine.
    
    Usage:
        engine = PennyProfitEngine()
        
        # Check if position should exit
        action = engine.check_exit(
            exchange='binance',
            entry_value=7.50,
            current_value=7.55
        )
        
        if action == 'TAKE_PROFIT':
            sell()
        elif action == 'STOP_LOSS':
            sell()
    """
    
    def __init__(self, thresholds_file: str = 'penny_profit_thresholds.json'):
        self.thresholds: Dict = {}
        self.loaded = False
        self._load_thresholds(thresholds_file)
    
    def _load_thresholds(self, filepath: str):
        """Load thresholds from JSON file."""
        try:
            # Try multiple locations
            locations = [
                filepath,
                os.path.join(os.path.dirname(__file__), filepath),
                os.path.join(os.path.dirname(__file__), '..', filepath),
            ]
            
            for loc in locations:
                if os.path.exists(loc):
                    with open(loc, 'r') as f:
                        data = json.load(f)
                    self._parse_thresholds(data)
                    self.loaded = True
                    logger.info(f"🪙 Penny Profit Engine loaded from {loc}")
                    return
            
            # If no file found, use hardcoded defaults
            logger.warning("🪙 Using hardcoded penny profit thresholds")
            self._use_defaults()
            self.loaded = True
            
        except Exception as e:
            logger.error(f"🪙 Failed to load penny profit thresholds: {e}")
            self._use_defaults()
            self.loaded = True
    
    def _parse_thresholds(self, data: Dict):
        """Parse thresholds from loaded JSON."""
        # Handle both old and new format
        if 'thresholds' in data:
            # Old format with nested taker/maker
            for exchange, sizes in data['thresholds'].items():
                self.thresholds[exchange] = {}
                for size_key, values in sizes.items():
                    # Extract size from key like "$7.50"
                    size = float(size_key.replace('$', ''))
                    
                    # Get taker values (worst case)
                    taker = values.get('taker', values)
                    
                    self.thresholds[exchange][size] = PennyThreshold(
                        trade_size=size,
                        total_cost=taker.get('total_costs', taker.get('cost', 0.03)),
                        win_gte=taker.get('min_gross_profit', taker.get('win_gte', 0.04)),
                        stop_lte=taker.get('max_gross_loss', taker.get('stop_lte', -0.02)),
                        win_pct=taker.get('min_price_move_pct', taker.get('win_pct', 0.5)),
                        stop_pct=taker.get('stop_pct', -0.3),
                    )
        
        elif 'exchanges' in data:
            # New format
            for exchange, info in data['exchanges'].items():
                self.thresholds[exchange] = {}
                for size_key, values in info.get('thresholds', {}).items():
                    size = float(size_key.replace('$', ''))
                    self.thresholds[exchange][size] = PennyThreshold(
                        trade_size=size,
                        total_cost=values.get('cost', 0.03),
                        win_gte=values.get('win_gte', 0.04),
                        stop_lte=values.get('stop_lte', -0.02),
                        win_pct=values.get('win_pct', 0.5),
                        stop_pct=values.get('stop_pct', -0.3),
                    )
    
    def _use_defaults(self):
        """Use hardcoded default thresholds."""
        # Defaults for $7.50 trade size
        self.thresholds = {
            'binance': {
                5.0: PennyThreshold(5.0, 0.020, 0.030, -0.010, 0.60, -0.20),
                7.5: PennyThreshold(7.5, 0.030, 0.040, -0.015, 0.53, -0.20),
                10.0: PennyThreshold(10.0, 0.040, 0.050, -0.020, 0.50, -0.20),
                15.0: PennyThreshold(15.0, 0.060, 0.070, -0.030, 0.47, -0.20),
                20.0: PennyThreshold(20.0, 0.080, 0.090, -0.040, 0.45, -0.20),
            },
            'kraken': {
                5.0: PennyThreshold(5.0, 0.036, 0.046, -0.018, 0.92, -0.36),
                7.5: PennyThreshold(7.5, 0.054, 0.064, -0.027, 0.85, -0.36),
                10.0: PennyThreshold(10.0, 0.072, 0.082, -0.036, 0.82, -0.36),
                15.0: PennyThreshold(15.0, 0.108, 0.118, -0.054, 0.79, -0.36),
                20.0: PennyThreshold(20.0, 0.144, 0.154, -0.072, 0.77, -0.36),
            },
            'capital': {
                10.0: PennyThreshold(10.0, 0.044, 0.054, -0.022, 0.54, -0.22),
                15.0: PennyThreshold(15.0, 0.066, 0.076, -0.033, 0.51, -0.22),
                20.0: PennyThreshold(20.0, 0.088, 0.098, -0.044, 0.49, -0.22),
            },
            'alpaca': {
                5.0: PennyThreshold(5.0, 0.035, 0.045, -0.018, 0.90, -0.35),
                7.5: PennyThreshold(7.5, 0.053, 0.063, -0.026, 0.83, -0.35),
                10.0: PennyThreshold(10.0, 0.070, 0.080, -0.035, 0.80, -0.35),
            },
        }
    
    def get_threshold(self, exchange: str, entry_value: float) -> PennyThreshold:
        """
        Get the threshold for a given exchange and trade size.
        Finds the closest matching size bucket.
        """
        exchange = exchange.lower()
        
        if exchange not in self.thresholds:
            # Default to binance if unknown exchange
            exchange = 'binance'
        
        sizes = self.thresholds[exchange]
        
        # Find closest size bucket
        closest_size = min(sizes.keys(), key=lambda x: abs(x - entry_value))
        
        return sizes[closest_size]
    
    def check_exit(self, exchange: str, entry_value: float, current_value: float) -> Tuple[str, float]:
        """
        Check if position should exit based on penny profit rules.
        
        Args:
            exchange: Exchange name (binance, kraken, etc.)
            entry_value: Entry value in USD
            current_value: Current value in USD
        
        Returns:
            Tuple of (action, gross_pnl) where action is:
            - 'TAKE_PROFIT': Hit penny profit target
            - 'STOP_LOSS': Hit stop loss
            - 'HOLD': Neither threshold hit
        """
        threshold = self.get_threshold(exchange, entry_value)
        gross_pnl = current_value - entry_value
        
        if gross_pnl >= threshold.win_gte:
            return ('TAKE_PROFIT', gross_pnl)
        elif gross_pnl <= threshold.stop_lte:
            return ('STOP_LOSS', gross_pnl)
        else:
            return ('HOLD', gross_pnl)
    
    def get_exit_prices(self, exchange: str, entry_price: float, quantity: float) -> Dict:
        """
        Calculate exact exit prices for TP and SL.
        
        Returns dict with tp_price and sl_price.
        """
        entry_value = entry_price * quantity
        threshold = self.get_threshold(exchange, entry_value)
        
        # TP: entry_value + win_gte = target_exit_value
        tp_value = entry_value + threshold.win_gte
        tp_price = tp_value / quantity if quantity > 0 else entry_price * (1 + threshold.win_pct / 100)
        
        # SL: entry_value + stop_lte = stop_exit_value
        sl_value = entry_value + threshold.stop_lte
        sl_price = sl_value / quantity if quantity > 0 else entry_price * (1 + threshold.stop_pct / 100)
        
        return {
            'entry_price': entry_price,
            'entry_value': entry_value,
            'tp_price': tp_price,
            'tp_value': tp_value,
            'tp_gross_target': threshold.win_gte,
            'sl_price': sl_price,
            'sl_value': sl_value,
            'sl_gross_target': threshold.stop_lte,
            'total_cost': threshold.total_cost,
            'net_profit_if_tp': 0.01,  # The penny!
        }
    
    def print_summary(self):
        """Print a summary of loaded thresholds."""
        print("=" * 60)
        print("🪙 PENNY PROFIT ENGINE - LOADED THRESHOLDS")
        print("=" * 60)
        
        for exchange, sizes in self.thresholds.items():
            print(f"\n🏦 {exchange.upper()}")
            print(f"   {'Size':>8} | {'Cost':>7} | {'TP >=':>8} | {'SL <=':>8} | {'Move%':>6}")
            print(f"   {'-'*8}-+-{'-'*7}-+-{'-'*8}-+-{'-'*8}-+-{'-'*6}")
            
            for size in sorted(sizes.keys()):
                t = sizes[size]
                print(f"   ${size:>7.2f} | ${t.total_cost:>6.3f} | ${t.win_gte:>7.3f} | ${t.stop_lte:>7.3f} | {t.win_pct:>5.2f}%")


# Singleton instance
_engine: Optional[PennyProfitEngine] = None


def get_penny_engine() -> PennyProfitEngine:
    """Get the singleton penny profit engine instance."""
    global _engine
    if _engine is None:
        _engine = PennyProfitEngine()
    return _engine


def check_penny_exit(exchange: str, entry_value: float, current_value: float) -> Tuple[str, float]:
    """
    Quick check for penny profit exit.
    
    Returns: (action, gross_pnl)
    - action: 'TAKE_PROFIT', 'STOP_LOSS', or 'HOLD'
    """
    return get_penny_engine().check_exit(exchange, entry_value, current_value)


if __name__ == '__main__':
    # Test the engine
    engine = PennyProfitEngine()
    engine.print_summary()
    
    print("\n" + "=" * 60)
    print("🧪 TEST: $7.50 trade on Binance")
    print("=" * 60)
    
    entry = 7.50
    
    # Test scenarios
    tests = [
        (7.54, "Up $0.04 - should TP"),
        (7.52, "Up $0.02 - should HOLD"),
        (7.48, "Down $0.02 - should STOP"),
        (7.485, "Down $0.015 - should STOP"),
        (7.50, "Flat - should HOLD"),
    ]
    
    for current, desc in tests:
        action, pnl = engine.check_exit('binance', entry, current)
        print(f"   {desc}: gross=${pnl:+.3f} → {action}")
    
    print("\n" + "=" * 60)
    print("📊 EXIT PRICES for $7.50 entry @ $1.00/unit (7.5 units)")
    print("=" * 60)
    
    prices = engine.get_exit_prices('binance', 1.00, 7.5)
    print(f"   Entry: ${prices['entry_price']:.4f} × 7.5 = ${prices['entry_value']:.2f}")
    print(f"   TP at: ${prices['tp_price']:.4f} × 7.5 = ${prices['tp_value']:.2f} (gross +${prices['tp_gross_target']:.3f})")
    print(f"   SL at: ${prices['sl_price']:.4f} × 7.5 = ${prices['sl_value']:.2f} (gross ${prices['sl_gross_target']:.3f})")
    print(f"   Net profit if TP: ${prices['net_profit_if_tp']:.2f} 🪙")
