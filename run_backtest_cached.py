#!/usr/bin/env python3
"""Quick runner to test backtest with cached data and fixed imports"""
import subprocess
import sys

print("🚀 Running Aureon Historical Backtest with CACHED DATA...")
print("=" * 60)

result = subprocess.run(
    [sys.executable, "aureon_historical_backtest.py"],
    cwd="/workspaces/aureon-trading",
    capture_output=False
)

sys.exit(result.returncode)
