#!/bin/bash
# 🦈 Orca Kill Cycle Startup Script
# Waits for command center to be healthy before starting trading

echo "🦈 Orca Kill Cycle starting up..."
echo "   Waiting 30 seconds for Command Center health check..."

# Wait for command center to be healthy
sleep 30

# Check if command center is healthy
for i in {1..10}; do
    if curl -sf http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ Command Center is healthy - starting Orca Kill Cycle"
        break
    fi
    echo "   Waiting for Command Center... (attempt $i/10)"
    sleep 5
done

# Start the Orca Kill Cycle with trading parameters
# Args: max_positions=3, amount_per_position=$1.00, target_pct=1.0%
echo "🦈🔪 LAUNCHING ORCA AUTONOMOUS TRADING 🔪🦈"
exec python -u orca_complete_kill_cycle.py --autonomous 3 1.0 1.0
