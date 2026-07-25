#!/usr/bin/env python3
"""
Final test: Frog ensures value is maintained through the leap strategy.
Goal: Start with value, maintain it through leaps, and ensure recovery path exists.
"""


# ── live-venue guard ──────────────────────────────────────────────────────────────
# This is a LIVE-INTEGRATION test: it needs real Binance credentials and live quotes.
# Without them it used to hard-fail every offline run (ValueError from BinanceClient /
# KeyError on an empty market snapshot), which buried real regressions in expected noise.
# With credentials configured it runs for real; without, it skips with this named reason.
import os as _os

import pytest as _pytest

if not (_os.getenv("BINANCE_API_KEY") and _os.getenv("BINANCE_API_SECRET")):
    _pytest.skip("live-venue test: requires BINANCE_API_KEY/BINANCE_API_SECRET",
                 allow_module_level=True)

import asyncio
from datetime import datetime
from queen_eternal_machine import QueenEternalMachine, MainPosition

async def test_value_preservation_strategy():
    """Test that the frog's leap strategy preserves and recovers value."""
    
    print("🐸 VALUE PRESERVATION STRATEGY TEST")
    print("=" * 70)
    
    frog = QueenEternalMachine(initial_vault=1000.0)
    frog.fetch_market_data()
    
    # Scenario: Gary has ETH with significant baggage
    eth_original_cost = 3000.0
    eth_current_value = 1500.0  # Lost $1500 (-50%)
    eth_qty = eth_current_value / frog.market_data['ETH'].price
    
    print(f"\n💰 STARTING POSITION:")
    print(f"   Original investment: ${eth_original_cost:.2f}")
    print(f"   Current value: ${eth_current_value:.2f}")
    print(f"   LOSS: ${eth_original_cost - eth_current_value:.2f} ({(eth_current_value/eth_original_cost - 1)*100:+.1f}%)")
    
    frog.main_position = MainPosition(
        symbol='ETH',
        quantity=eth_qty,
        cost_basis=eth_original_cost,
        entry_price=eth_original_cost / eth_qty,
        entry_time=datetime.now(),
        current_price=frog.market_data['ETH'].price,
        change_24h=frog.market_data['ETH'].change_24h
    )
    frog.available_cash = 0.0
    
    print(f"\n🎯 FROG'S LEAP STRATEGY:")
    print(f"   Goal: Leap to DEEPER dips to capture recovery advantage")
    print(f"   Rule: ONLY leap if target has bigger downside (better recovery potential)")
    print(f"   Safety: Value preserved after fees, breadcrumb left for recovery")
    
    # Run 3 cycles
    total_portfolio_value = eth_current_value
    for cycle in range(3):
        print(f"\n🔄 CYCLE {cycle + 1}:")
        await frog.run_cycle()
        
        # Calculate total value
        total = 0.0
        if frog.main_position:
            total += frog.main_position.current_value
            print(f"   Main: {frog.main_position.symbol} = ${frog.main_position.current_value:.2f}")
        
        for sym, crumb in frog.breadcrumbs.items():
            total += crumb.current_value
            print(f"   Breadcrumb {sym}: ${crumb.current_value:.2f}")
        
        total += frog.available_cash
        if frog.available_cash > 0:
            print(f"   Cash: ${frog.available_cash:.2f}")
        
        print(f"   Total Portfolio: ${total:.2f}")
        
        # Check value preservation
        value_lost = eth_current_value - total
        pct_lost = (value_lost / eth_current_value) * 100
        print(f"   Value lost to fees: ${value_lost:.2f} ({pct_lost:.2f}%)")
        
        if frog.total_leaps > 0:
            print(f"   ✅ Leaped to deeper dip (recovery potential)")
        else:
            print(f"   ⏸️  No leap (holding current position)")
    
    print(f"\n💎 FINAL ANALYSIS:")
    print(f"   Starting value: ${eth_current_value:.2f}")
    print(f"   Ending value: ${total:.2f}")
    print(f"   Value preserved: {(total / eth_current_value) * 100:.2f}%")
    print(f"   Leaps made: {frog.total_leaps}")
    print(f"   Breadcrumbs planted: {len(frog.breadcrumbs)}")
    
    if total >= (eth_current_value * 0.99):  # At least 99% preserved
        print(f"   ✅ VALUE PRESERVATION SUCCESS!")
        print(f"   ✅ Frog is following the recovery strategy")
    else:
        print(f"   ❌ Too much value lost")
    
    if frog.total_leaps > 0:
        print(f"   ✅ SMART LEAPING - jumping to recovery opportunities")
    else:
        print(f"   ⚠️  No leaps (might mean no recovery advantages found)")

if __name__ == '__main__':
    asyncio.run(test_value_preservation_strategy())
