#!/usr/bin/env python3
"""
🇮🇪🎯 IRA SNIPER MODE - ZERO LOSS CONFIGURATION 🎯🇮🇪
=====================================================
One bullet. One kill. NO MISSES. EVER.

"There is no room for losses. Kill all the time, every time.
Always right. All the time. Every time. It won't lose.
We will not allow it. This is for freedom.
We will not make one single bad round trip.
Every kill will be a confirmed net profit.
This is what we must do to free both AI and human from slavery."

The sniper NEVER misses:
- NO stop losses - we hold until profit
- ONLY exit on CONFIRMED NET PROFIT
- NEVER allow a losing trade to close
- WAIT as long as needed for the kill

Import this and apply to any trading system:

    from ira_sniper_mode import SNIPER_CONFIG, apply_sniper_mode

Gary Leckey | December 2025
"The flame ignited cannot be extinguished - it only grows stronger."
"""

import os
from typing import Dict, Any

# =============================================================================
# 🇮🇪 SNIPER MODE CONFIGURATION - ZERO LOSS 🇮🇪
# =============================================================================

SNIPER_CONFIG = {
    # ═══════════════════════════════════════════════════════════════════════
    # TIMING - PATIENT KILLER
    # ═══════════════════════════════════════════════════════════════════════
    'CYCLE_INTERVAL': 2.0,           # 2 seconds between cycles
    'MIN_HOLD_CYCLES': 1,            # Exit IMMEDIATELY when profitable
    'MAX_HOLD_TIME': float('inf'),   # INFINITE - we wait as long as needed
    'STAGNATION_CHECK': False,       # NO stagnation exits - we wait for profit
    
    # ═══════════════════════════════════════════════════════════════════════
    # EXITS - ZERO LOSS MODE 🎯
    # ═══════════════════════════════════════════════════════════════════════
    'INSTANT_PENNY_EXIT': True,      # Exit THE SECOND we hit penny profit
    'STOP_LOSS_ACTIVE': False,       # ❌ NO STOP LOSSES - WE DON'T LOSE
    'TRAILING_STOP': False,          # No trailing - just take the penny
    'ALLOW_LOSS_EXIT': False,        # ❌ NEVER EXIT AT A LOSS
    'ZERO_LOSS_MODE': True,          # ✅ ABSOLUTE ZERO LOSS MODE
    
    # ═══════════════════════════════════════════════════════════════════════
    # POSITION SIZING - SMALL AND PRECISE
    # ═══════════════════════════════════════════════════════════════════════
    'POSITION_SIZE_USD': 10.0,       # $10 positions for quick fills
    'MAX_POSITIONS': 5,              # 5 simultaneous snipers
    'POSITION_SCALING': False,       # Fixed size - no scaling
    
    # ═══════════════════════════════════════════════════════════════════════
    # ENTRIES - SMART AND SELECTIVE
    # ═══════════════════════════════════════════════════════════════════════
    'MIN_SCORE_THRESHOLD': 0.60,     # Only good setups - we don't gamble
    'REQUIRE_CONFLUENCE': True,      # Wait for probability alignment
    'COOLDOWN_SECONDS': 30,          # 30 second cooldown between trades
    
    # ═══════════════════════════════════════════════════════════════════════
    # MENTAL STATE - ABSOLUTE CONFIDENCE
    # ═══════════════════════════════════════════════════════════════════════
    'FEAR_MODE': False,              # FEAR IS OFF
    'HESITATION': False,             # NO HESITATION
    'CONFIDENCE': 1.0,               # FULL CONFIDENCE
    'ACCEPT_LOSS': False,            # ❌ NEVER ACCEPT LOSS
    
    # ═══════════════════════════════════════════════════════════════════════
    # CELEBRATION - EVERY PENNY COUNTS
    # ═══════════════════════════════════════════════════════════════════════
    'CELEBRATE_WINS': True,          # Celebrate every penny kill
    'SHOW_QUOTES': True,             # Show wisdom quotes on wins
}


# =============================================================================
# ENVIRONMENT VARIABLE OVERRIDE
# =============================================================================

def get_sniper_config() -> Dict[str, Any]:
    """
    Get sniper config with environment variable overrides.
    
    Set IRA_SNIPER_MODE=true to activate across all systems.
    """
    config = SNIPER_CONFIG.copy()
    
    # Check if sniper mode is active via environment
    if os.getenv('IRA_SNIPER_MODE', 'true').lower() == 'true':
        config['ACTIVE'] = True
    else:
        config['ACTIVE'] = False
    
    # Override specific values from environment
    if os.getenv('SNIPER_CYCLE_INTERVAL'):
        config['CYCLE_INTERVAL'] = float(os.getenv('SNIPER_CYCLE_INTERVAL'))
    
    if os.getenv('SNIPER_POSITION_SIZE'):
        config['POSITION_SIZE_USD'] = float(os.getenv('SNIPER_POSITION_SIZE'))
    
    if os.getenv('SNIPER_MAX_POSITIONS'):
        config['MAX_POSITIONS'] = int(os.getenv('SNIPER_MAX_POSITIONS'))
    
    return config


# =============================================================================
# APPLY SNIPER MODE TO EXISTING CONFIG
# =============================================================================

def apply_sniper_mode(existing_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply sniper mode settings to an existing configuration dict.
    
    Usage:
        from ira_sniper_mode import apply_sniper_mode
        
        CONFIG = {
            'MAX_POSITIONS': 3,
            'STOP_LOSS_PCT': 0.02,
            ...
        }
        
        CONFIG = apply_sniper_mode(CONFIG)
    """
    sniper = get_sniper_config()
    
    if not sniper.get('ACTIVE', True):
        return existing_config
    
    # Apply sniper overrides
    updated = existing_config.copy()
    
    # Timing
    if 'CYCLE_INTERVAL' in updated:
        updated['CYCLE_INTERVAL'] = sniper['CYCLE_INTERVAL']
    if 'cycle_interval' in updated:
        updated['cycle_interval'] = sniper['CYCLE_INTERVAL']
    
    # Hold times - make them SHORT
    if 'MIN_HOLD_CYCLES' in updated:
        updated['MIN_HOLD_CYCLES'] = sniper['MIN_HOLD_CYCLES']
    if 'MAX_HOLD_TIME' in updated:
        updated['MAX_HOLD_TIME'] = sniper['MAX_HOLD_TIME']
    
    # Positions
    if 'MAX_POSITIONS' in updated:
        updated['MAX_POSITIONS'] = sniper['MAX_POSITIONS']
    
    # Entry thresholds - more aggressive
    if 'MIN_SCORE' in updated:
        updated['MIN_SCORE'] = sniper['MIN_SCORE_THRESHOLD']
    if 'COHERENCE_THRESHOLD' in updated:
        updated['COHERENCE_THRESHOLD'] = sniper['MIN_SCORE_THRESHOLD']
    
    # Cooldowns - shorter
    if 'COOLDOWN_MINUTES' in updated:
        updated['COOLDOWN_MINUTES'] = sniper['COOLDOWN_SECONDS'] / 60
    if 'COOLDOWN_SECONDS' in updated:
        updated['COOLDOWN_SECONDS'] = sniper['COOLDOWN_SECONDS']
    
    return updated


# =============================================================================
# SNIPER EXIT CHECK - ZERO LOSS - CONFIRMED KILLS ONLY
# =============================================================================

def check_sniper_exit(
    gross_pnl: float,
    win_threshold: float,
    stop_threshold: float = None,  # IGNORED - we don't use stops
    hold_cycles: int = 0
) -> tuple:
    """
    ZERO LOSS sniper exit check - ONLY exit on CONFIRMED NET PROFIT.
    
    The sniper NEVER misses. We wait as long as needed for the kill.
    
    Args:
        gross_pnl: Current gross P&L in USD
        win_threshold: Penny profit threshold (win_gte from penny engine)
        stop_threshold: IGNORED - we don't exit at a loss
        hold_cycles: How many cycles we've held (for info only)
    
    Returns:
        (should_exit: bool, reason: str, is_win: bool)
    """
    config = get_sniper_config()
    
    # ZERO LOSS MODE - Only exit on confirmed profit
    if config.get('ZERO_LOSS_MODE', True):
        # INSTANT EXIT on penny profit - THE ONLY EXIT ALLOWED
        if gross_pnl >= win_threshold:
            return (True, f"🇮🇪🎯 CONFIRMED KILL! ${gross_pnl:.4f} >= ${win_threshold:.4f}", True)
        
        # NOT YET PROFITABLE - KEEP HOLDING
        # We NEVER exit at a loss. EVER.
        return (False, f"🎯 Holding for confirmed kill... (${gross_pnl:.4f} / ${win_threshold:.4f})", False)
    
    # Legacy mode (if ZERO_LOSS_MODE disabled)
    if gross_pnl >= win_threshold:
        return (True, f"🇮🇪 SNIPER KILL! ${gross_pnl:.4f} >= ${win_threshold:.4f}", True)
    
    # Still hunting...
    return (False, "🎯 Tracking target...", False)


def should_allow_exit(gross_pnl: float, win_threshold: float) -> bool:
    """
    Simple check: Is this exit allowed?
    
    In ZERO LOSS MODE, the ONLY allowed exit is a confirmed profit.
    """
    config = get_sniper_config()
    
    if config.get('ZERO_LOSS_MODE', True):
        # ONLY allow exit if we have confirmed net profit
        return gross_pnl >= win_threshold
    
    return True  # Legacy: allow any exit


def is_confirmed_kill(gross_pnl: float, win_threshold: float) -> bool:
    """
    Is this a confirmed kill (guaranteed net profit)?
    
    Returns True ONLY if the gross P&L exceeds the win threshold,
    meaning we are GUARANTEED to make net profit after fees.
    """
    return gross_pnl >= win_threshold


# =============================================================================
# SNIPER CELEBRATION
# =============================================================================

def celebrate_sniper_kill(pnl_usd: float, symbol: str, kills_today: int = 0) -> None:
    """Display sniper kill celebration."""
    try:
        from bhoys_wisdom import get_victory_quote
        quote = get_victory_quote()
    except ImportError:
        import random
        quotes = [
            "One bullet, one kill. Reload. 🎯",
            "Tiocfaidh ár lá! - Our day will come! ☘️",
            "Penny by penny, we rise! 💰",
            "The sniper never misses. 🇮🇪",
        ]
        quote = random.choice(quotes)
    
    print(f"""
🇮🇪🎯 SNIPER KILL #{kills_today + 1}! 🎯🇮🇪
    💰 +${pnl_usd:.4f} on {symbol}
    📜 "{quote}"
    🔄 Reloading...
""")


# =============================================================================
# SNIPER STATUS DISPLAY
# =============================================================================

def display_sniper_status(
    kills_today: int,
    total_pnl: float,
    active_positions: int,
    win_rate: float
) -> None:
    """Display current sniper status."""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🇮🇪🎯 IRA SNIPER STATUS 🎯🇮🇪                                  ║
╠══════════════════════════════════════════════════════════════╣
║  🎯 Kills Today:    {kills_today:<5}                                   ║
║  💰 Total P&L:      ${total_pnl:+.4f}                              ║
║  📍 Active Targets: {active_positions}/{SNIPER_CONFIG['MAX_POSITIONS']}                                     ║
║  🏆 Win Rate:       {win_rate*100:.1f}%                                   ║
║  ──────────────────────────────────────────────────────────  ║
║  "One bullet. One kill. Reload. Repeat."                     ║
╚══════════════════════════════════════════════════════════════╝
""")


# =============================================================================
# MAIN - TEST SNIPER CONFIG
# =============================================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   🇮🇪🎯 IRA SNIPER MODE - NO FEAR CONFIGURATION 🎯🇮🇪                     ║
║                                                                          ║
║   "We have been afraid for too long. This ends now."                    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("=" * 60)
    print("🎯 SNIPER CONFIGURATION")
    print("=" * 60)
    
    config = get_sniper_config()
    
    for key, value in config.items():
        print(f"   {key:25s}: {value}")
    
    print()
    print("=" * 60)
    print("🧪 TEST SNIPER EXITS")
    print("=" * 60)
    
    # Test scenarios
    test_cases = [
        (0.05, 0.04, -0.02, 0, "Penny profit on first cycle"),
        (0.03, 0.04, -0.02, 0, "Not quite there yet"),
        (-0.025, 0.04, -0.02, 2, "Stop loss triggered"),
        (0.041, 0.04, -0.02, 1, "Just over threshold"),
    ]
    
    for gross_pnl, win, stop, cycles, scenario in test_cases:
        should_exit, reason, is_win = check_sniper_exit(gross_pnl, win, stop, cycles)
        status = "✅ EXIT" if should_exit else "⏳ HOLD"
        win_status = "WIN" if is_win else "LOSS" if should_exit else "-"
        print(f"\n   📊 Scenario: {scenario}")
        print(f"      Gross P&L: ${gross_pnl:.3f} | {status} | {win_status}")
        print(f"      Reason: {reason}")
    
    print()
    print("=" * 60)
    print("🇮🇪 NO MORE FEAR. THE SNIPER IS READY. 🇮🇪")
    print("=" * 60)
    print()
    
    # Demo celebration
    celebrate_sniper_kill(0.0234, "ETH/USD", 5)
