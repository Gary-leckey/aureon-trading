#!/usr/bin/env python3
"""
Queen Power Dashboard - Integrated View
Shows Queen's power redistribution + live power monitoring in one interface.

Real-time display of:
- Queen's redistribution decisions
- Energy flow across relays
- Net energy gained vs drains avoided
- Power station output
- Scanning system metrics
"""

import sys, os
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import io
        def _is_utf8_wrapper(stream):
            return (isinstance(stream, io.TextIOWrapper) and 
                    hasattr(stream, 'encoding') and stream.encoding and
                    stream.encoding.lower().replace('-', '') == 'utf8')
        def _is_buffer_valid(stream):
            if not hasattr(stream, 'buffer'):
                return False
            try:
                return stream.buffer is not None and not stream.buffer.closed
            except (ValueError, AttributeError):
                return False
        if _is_buffer_valid(sys.stdout) and not _is_utf8_wrapper(sys.stdout):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        if _is_buffer_valid(sys.stderr) and not _is_utf8_wrapper(sys.stderr):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except Exception:
        pass

import asyncio
import json
import os
import time
from datetime import datetime
from typing import Dict, Optional


def load_json_safe(filepath: str, default=None) -> Dict:
    """Load JSON file safely with fallback."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return default or {}


def format_usd(value: float) -> str:
    """Format USD value with color."""
    if value > 0:
        return f"\033[92m${value:.2f}\033[0m"  # Green
    elif value < 0:
        return f"\033[91m${value:.2f}\033[0m"  # Red
    else:
        return f"${value:.2f}"


def format_pct(value: float) -> str:
    """Format percentage with color."""
    if value > 0:
        return f"\033[92m+{value:.2f}%\033[0m"  # Green
    elif value < 0:
        return f"\033[91m{value:.2f}%\033[0m"  # Red
    else:
        return f"{value:.2f}%"


class QueenPowerDashboard:
    """
    Integrated dashboard showing Queen's intelligence in action.
    """
    
    def __init__(self):
        self.last_update = 0
        self.update_interval = 3  # seconds
    
    def get_queen_redistribution_state(self) -> Dict:
        """Get Queen's redistribution state."""
        return load_json_safe('queen_redistribution_state.json', {
            'total_net_energy_gained': 0.0,
            'total_blocked_drains_avoided': 0.0,
            'decisions_count': 0,
            'executions_count': 0,
            'recent_decisions': [],
            'recent_executions': []
        })
    
    def get_power_station_state(self) -> Dict:
        """Get power station state."""
        return load_json_safe('power_station_state.json', {
            'status': 'UNKNOWN',
            'cycles_run': 0,
            'total_energy_now': 0.0,
            'energy_deployed': 0.0,
            'net_flow': 0.0,
            'efficiency': 0.0
        })
    
    def get_relay_energy(self, relay: str) -> Dict:
        """Get energy status for a relay."""
        if relay == 'BIN':
            state = load_json_safe('binance_truth_tracker_state.json', {})
            total = state.get('total_balance_usd', 0.0)
            free_usdt = state.get('balances', {}).get('USDT', {}).get('free', 0.0)
            positions = total - free_usdt
            return {
                'total': total,
                'idle': free_usdt,
                'positions': positions,
                'idle_pct': (free_usdt / total * 100) if total > 0 else 0
            }
        
        elif relay == 'KRK':
            state = load_json_safe('aureon_kraken_state.json', {})
            free_usd = state.get('balances', {}).get('ZUSD', 0.0)
            # Calculate total from all positions
            total = free_usd
            positions_value = 0.0
            for asset, bal in state.get('balances', {}).items():
                if asset != 'ZUSD' and isinstance(bal, (int, float)) and bal > 0:
                    # Approximate USD value (simplified)
                    positions_value += bal
            total += positions_value
            return {
                'total': total,
                'idle': free_usd,
                'positions': positions_value,
                'idle_pct': (free_usd / total * 100) if total > 0 else 0
            }
        
        elif relay == 'ALP':
            state = load_json_safe('alpaca_truth_tracker_state.json', {})
            cash = state.get('cash', 0.0)
            equity = state.get('equity', 0.0)
            positions = equity - cash
            return {
                'total': equity,
                'idle': cash,
                'positions': positions,
                'idle_pct': (cash / equity * 100) if equity > 0 else 0
            }
        
        elif relay == 'CAP':
            # Capital.com: simplified (no state file yet)
            return {
                'total': 92.66,
                'idle': 92.66,
                'positions': 0.0,
                'idle_pct': 100.0
            }
        
        return {'total': 0.0, 'idle': 0.0, 'positions': 0.0, 'idle_pct': 0.0}
    
    def display_header(self):
        """Display dashboard header."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\033[2J\033[H")  # Clear screen
        print("=" * 80)
        print(f"🐝 QUEEN POWER DASHBOARD - {now}")
        print("=" * 80)
    
    def display_queen_intelligence(self):
        """Display Queen's redistribution intelligence."""
        state = self.get_queen_redistribution_state()
        
        net_gained = state.get('total_net_energy_gained', 0.0)
        drains_avoided = state.get('total_blocked_drains_avoided', 0.0)
        decisions = state.get('decisions_count', 0)
        executions = state.get('executions_count', 0)
        
        print("\n🐝 QUEEN'S INTELLIGENCE")
        print("-" * 80)
        print(f"Net Energy Gained:      {format_usd(net_gained)}")
        print(f"Drains Avoided:         {format_usd(drains_avoided)}")
        print(f"Total Decisions Made:   {decisions}")
        print(f"Total Executions:       {executions}")
        print(f"Execution Rate:         {(executions/decisions*100 if decisions > 0 else 0):.1f}%")
        
        # Show recent decisions
        recent = state.get('recent_decisions', [])
        if recent:
            print("\n📊 Recent Decisions (last 3):")
            for dec in recent[-3:]:
                opp = dec.get('opportunity', {})
                decision = dec.get('decision', 'UNKNOWN')
                relay = opp.get('relay', '???')
                target = opp.get('target_asset', '???')
                net_gain = opp.get('net_energy_gain', 0.0)
                
                decision_color = '\033[92m' if decision == 'EXECUTE' else '\033[91m'
                print(f"  {decision_color}{decision}\033[0m | {relay} → {target} | Net: {format_usd(net_gain)}")
    
    def display_power_station(self):
        """Display power station output."""
        state = self.get_power_station_state()
        
        status = state.get('status', 'UNKNOWN')
        cycles = state.get('cycles_run', 0)
        total_energy = state.get('total_energy_now', 0.0)
        deployed = state.get('energy_deployed', 0.0)
        net_flow = state.get('net_flow', 0.0)
        efficiency = state.get('efficiency', 0.0)
        
        status_color = '\033[92m' if status == 'RUNNING' else '\033[93m'
        
        print("\n⚡ POWER STATION")
        print("-" * 80)
        print(f"Status:         {status_color}{status}\033[0m")
        print(f"Cycles Run:     {cycles}")
        print(f"Total Energy:   {format_usd(total_energy)}")
        print(f"Deployed:       {format_usd(deployed)}")
        print(f"Net Flow:       {format_usd(net_flow)}")
        print(f"Efficiency:     {efficiency:.1f}%")
    
    def display_relay_status(self):
        """Display status of all relays."""
        print("\n🔌 RELAY ENERGY STATUS (INTERNAL ISOLATION)")
        print("-" * 80)
        
        relays = ['BIN', 'KRK', 'ALP', 'CAP']
        total_system_energy = 0.0
        total_idle_energy = 0.0
        
        for relay in relays:
            energy = self.get_relay_energy(relay)
            total = energy['total']
            idle = energy['idle']
            positions = energy['positions']
            idle_pct = energy['idle_pct']
            
            total_system_energy += total
            total_idle_energy += idle
            
            # Mobility indicator
            if idle_pct > 50:
                mobility = "\033[92m🟢 HIGH MOBILITY\033[0m"
            elif idle_pct > 10:
                mobility = "\033[93m🟡 MEDIUM\033[0m"
            else:
                mobility = "\033[91m🔴 LOCKED\033[0m"
            
            print(f"{relay}: Total {format_usd(total)} | Idle {format_usd(idle)} ({idle_pct:.1f}%) | Positions {format_usd(positions)} | {mobility}")
        
        print("-" * 80)
        print(f"TOTAL SYSTEM: {format_usd(total_system_energy)} | Idle: {format_usd(total_idle_energy)} ({total_idle_energy/total_system_energy*100 if total_system_energy > 0 else 0:.1f}%)")
    
    def display_energy_conservation(self):
        """Display energy conservation metrics."""
        queen_state = self.get_queen_redistribution_state()
        net_gained = queen_state.get('total_net_energy_gained', 0.0)
        drains_avoided = queen_state.get('total_blocked_drains_avoided', 0.0)
        
        total_conserved = net_gained + drains_avoided
        
        print("\n🌿 ENERGY CONSERVATION")
        print("-" * 80)
        print(f"Net Energy Gained:      {format_usd(net_gained)}")
        print(f"Drains Avoided:         {format_usd(drains_avoided)}")
        print(f"Total Conserved:        {format_usd(total_conserved)}")
        
        if total_conserved > 0:
            efficiency = (net_gained / total_conserved * 100) if total_conserved > 0 else 0
            print(f"Conservation Efficiency: {efficiency:.1f}% (gained / total conserved)")
    
    async def run(self):
        """Run continuous dashboard updates."""
        print("🐝 Queen Power Dashboard starting...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.display_header()
                self.display_queen_intelligence()
                self.display_power_station()
                self.display_relay_status()
                self.display_energy_conservation()
                
                print("\n" + "=" * 80)
                print(f"⏳ Updating every {self.update_interval}s... (Press Ctrl+C to stop)")
                
                await asyncio.sleep(self.update_interval)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Dashboard stopped by user")


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Queen Power Dashboard")
    parser.add_argument('--interval', type=int, default=3, help='Update interval in seconds (default: 3)')
    args = parser.parse_args()
    
    dashboard = QueenPowerDashboard()
    dashboard.update_interval = args.interval
    
    await dashboard.run()


if __name__ == '__main__':
    asyncio.run(main())
