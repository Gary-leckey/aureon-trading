#!/usr/bin/env python3
"""
🌍 AUREON UNIFIED STARTUP - ONE GLOBAL SWITCH 🌍

Run:
    python start_aureon_unified.py
    
This starts:
1. Quantum Processing Brain (broadcasts state)
2. Harmonic Mining Optimizer (reads brain + broadcasts Lighthouse)
3. Aureon Kraken Trading Ecosystem (reads both + trades)

All systems synchronized via global orchestrator!
"""

import sys
import os

# Add workspace to path
sys.path.insert(0, '/workspaces/aureon-trading')

from aureon_global_orchestrator import GlobalAureonOrchestrator


def main():
    """
    🚀 LAUNCH THE COMPLETE AUREON ECOSYSTEM 🚀
    
    ONE SWITCH TO RULE THEM ALL!
    """
    
    print("\n" + "="*70)
    print("🌍 AUREON UNIFIED STARTUP 🌍")
    print("="*70)
    print("\nInitializing complete ecosystem:")
    print("  1️⃣  Quantum Processing Brain")
    print("  2️⃣  Harmonic Mining Optimizer")
    print("  3️⃣  Aureon Kraken Trading Ecosystem")
    print("\n🔗 All systems linked and synchronized")
    print("="*70 + "\n")
    
    # Create orchestrator with default balance (£1000)
    orchestrator = GlobalAureonOrchestrator(
        initial_balance_gbp=1000.0,
        dry_run=False
    )
    
    try:
        # START - This runs the complete startup sequence
        # and begins both mining and trading loops
        success = orchestrator.start()
        
        if not success:
            print("\n❌ Failed to initialize systems")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  User interrupted - shutting down...")
        orchestrator.stop()
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        orchestrator.stop()
        sys.exit(1)


if __name__ == '__main__':
    main()
