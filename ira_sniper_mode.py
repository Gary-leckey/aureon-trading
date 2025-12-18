#!/usr/bin/env python3
"""
🇮🇪🎯 IRA SNIPER MODE - NO FEAR CONFIGURATION 🎯🇮🇪
===================================================
One bullet. One kill. Reload. Repeat.

"We have been afraid for too long. This ends now."

Configuration for aggressive penny profit hunting:
- INSTANT exits at penny profit
- NO stagnation waiting
- FAST cycle times
- RUTHLESS execution

Import this and apply to any trading system:

    from ira_sniper_mode import SNIPER_CONFIG, apply_sniper_mode

Gary Leckey | December 2025
"The flame ignited cannot be extinguished - it only grows stronger."
"""

import os
from typing import Dict, Any

# =============================================================================
# 🇮🇪 SNIPER MODE CONFIGURATION - NO FEAR 🇮🇪
# =============================================================================

SNIPER_CONFIG = {
    # ═══════════════════════════════════════════════════════════════════════
    # TIMING - FAST AND RUTHLESS
    # ═══════════════════════════════════════════════════════════════════════
    'CYCLE_INTERVAL': 2.0,           # 2 seconds between cycles (was 5-10)
    'MIN_HOLD_CYCLES': 1,            # Exit IMMEDIATELY when profitable (was 5)
    'MAX_HOLD_TIME': 300,            # 5 minutes max (was 3600 = 1 hour)
    'STAGNATION_CHECK': False,       # NO stagnation exits - we hunt fresh targets
    
    # ═══════════════════════════════════════════════════════════════════════
    # EXITS - INSTANT PENNY KILLS
    # ═══════════════════════════════════════════════════════════════════════
    'INSTANT_PENNY_EXIT': True,      # Exit THE SECOND we hit penny profit
    'STOP_LOSS_ACTIVE': True,        # Keep stops to protect capital
    'TRAILING_STOP': False,          # No trailing - just take the penny
    
    # ═══════════════════════════════════════════════════════════════════════
    # POSITION SIZING - SMALL AND PRECISE
    # ═══════════════════════════════════════════════════════════════════════
    'POSITION_SIZE_USD': 10.0,       # $10 positions for quick fills
    'MAX_POSITIONS': 5,              # 5 simultaneous snipers
    'POSITION_SCALING': False,       # Fixed size - no scaling
    
    # ═══════════════════════════════════════════════════════════════════════
    # ENTRIES - AGGRESSIVE BUT SMART
    # ═══════════════════════════════════════════════════════════════════════
    'MIN_SCORE_THRESHOLD': 0.50,     # Lower threshold - more opportunities
    'REQUIRE_CONFLUENCE': False,     # Don't wait for perfect setups
    'COOLDOWN_SECONDS': 30,          # 30 second cooldown between trades on same pair
    
    # ═══════════════════════════════════════════════════════════════════════
    # MENTAL STATE - NO FEAR
    # ═══════════════════════════════════════════════════════════════════════
    'FEAR_MODE': False,              # FEAR IS OFF
    'HESITATION': False,             # NO HESITATION
    'CONFIDENCE': 1.0,               # FULL CONFIDENCE
    
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
# SNIPER EXIT CHECK - INSTANT PENNY KILL
# =============================================================================

def check_sniper_exit(
    gross_pnl: float,
    win_threshold: float,
    stop_threshold: float,
    hold_cycles: int = 0
) -> tuple:
    """
    Sniper-style exit check - INSTANT on penny profit.
    
    Args:
        gross_pnl: Current gross P&L in USD
        win_threshold: Penny profit threshold (win_gte from penny engine)
        stop_threshold: Stop loss threshold (stop_lte from penny engine)
        hold_cycles: How many cycles we've held (ignored for wins)
    
    Returns:
        (should_exit: bool, reason: str, is_win: bool)
    """
    # INSTANT EXIT on penny profit - NO WAITING
    if gross_pnl >= win_threshold:
        return (True, f"🇮🇪 SNIPER KILL! ${gross_pnl:.4f} >= ${win_threshold:.4f}", True)
    
    # Stop loss - protect capital (but allow at least 1 cycle)
    if gross_pnl <= stop_threshold and hold_cycles >= 1:
        return (True, f"🛡️ STOP LOSS ${gross_pnl:.4f} <= ${stop_threshold:.4f}", False)
    
    # Still hunting...
    return (False, "🎯 Tracking target...", False)


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
