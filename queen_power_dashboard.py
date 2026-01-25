#!/usr/bin/env python3
"""
⚡ AUREON POWER STATION - MAIN ENERGY INTERFACE ⚡

Everything is Energy. This is the primary dashboard for all system activity.

Real-time Energy Visualization:
- Total System Energy (all balances)
- Energy Flow (in/out per relay)
- Energy Generation (profits/gains)
- Energy Consumption (fees/drains)
- Energy Reserves (idle capital)
- Energy Deployment (active positions)
- Queen's Energy Decisions
- System Power Output

All trading activity, balances, profits, and losses shown as ENERGY.
Port: 8080 (Primary Interface)
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
    ⚡ PRIMARY ENERGY INTERFACE ⚡
    Everything displayed as energy flows and reserves.
    """
    
    def __init__(self):
        self.last_update = 0
        self.update_interval = 3  # seconds
        self.cycle_count = 0
        self.start_time = time.time()
        self.total_energy_at_start = 0.0
        
        # Calculate baseline energy
        self._calculate_baseline_energy()
    
    def _calculate_baseline_energy(self):
        """Calculate total system energy at startup."""
        total = 0.0
        for relay in ['BIN', 'KRK', 'ALP', 'CAP']:
            energy = self.get_relay_energy(relay)
            total += energy['total']
        self.total_energy_at_start = total
    
    def get_total_system_energy(self) -> Dict:
        """Get comprehensive system energy metrics."""
        relays = ['BIN', 'KRK', 'ALP', 'CAP']
        
        total_energy = 0.0
        total_reserves = 0.0
        total_deployed = 0.0
        relay_breakdown = {}
        
        for relay in relays:
            energy = self.get_relay_energy(relay)
            total_energy += energy['total']
            total_reserves += energy['idle']
            total_deployed += energy['positions']
            relay_breakdown[relay] = energy
        
        # Get Queen's energy metrics
        queen_state = self.get_queen_redistribution_state()
        net_gained = queen_state.get('total_net_energy_gained', 0.0)
        drains_avoided = queen_state.get('total_blocked_drains_avoided', 0.0)
        
        # Calculate system growth
        energy_growth = total_energy - self.total_energy_at_start
        
        return {
            'total_energy': total_energy,
            'total_reserves': total_reserves,
            'total_deployed': total_deployed,
            'reserve_percentage': (total_reserves / total_energy * 100) if total_energy > 0 else 0,
            'deployed_percentage': (total_deployed / total_energy * 100) if total_energy > 0 else 0,
            'net_energy_gained': net_gained,
            'energy_conserved': drains_avoided,
            'energy_growth': energy_growth,
            'growth_percentage': (energy_growth / self.total_energy_at_start * 100) if self.total_energy_at_start > 0 else 0,
            'relay_breakdown': relay_breakdown
        }
    
    def get_queen_redistribution_state(self) -> Dict:
        """Get Queen's redistribution state."""
        state = load_json_safe('queen_redistribution_state.json', {
            'last_update': 0.0,
            'total_net_energy_gained': 0.0,
            'total_blocked_drains_avoided': 0.0,
            'decisions_count': 0,
            'executions_count': 0,
            'recent_decisions': [],
            'recent_executions': []
        })
        
        # Calculate time since last update (heartbeat)
        last_update = state.get('last_update', 0.0)
        if last_update > 0:
            state['seconds_since_update'] = time.time() - last_update
            state['is_alive'] = state['seconds_since_update'] < 60  # Active if updated in last minute
        else:
            state['seconds_since_update'] = 999999
            state['is_alive'] = False
        
        return state
    
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
        """Display dashboard header with total system energy."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        runtime = time.time() - self.start_time
        runtime_str = f"{int(runtime//60)}m {int(runtime%60)}s"
        
        # Get total system energy
        energy_data = self.get_total_system_energy()
        total_energy = energy_data['total_energy']
        energy_growth = energy_data['energy_growth']
        growth_pct = energy_data['growth_percentage']
        
        # Energy growth indicator
        if energy_growth > 0:
            growth_icon = "⚡📈"
            growth_color = '\033[92m'  # Green
        elif energy_growth < 0:
            growth_icon = "⚠️📉"
            growth_color = '\033[91m'  # Red
        else:
            growth_icon = "⚡━"
            growth_color = '\033[93m'  # Yellow
        
        print("\033[2J\033[H")  # Clear screen
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print(f"║  ⚡ AUREON POWER STATION - PRIMARY ENERGY INTERFACE{' ' * 26}║")
        print("╠" + "═" * 78 + "╣")
        print(f"║  📅 {now}  ⏱️  Runtime: {runtime_str:<10} 🔄 Cycle: #{self.cycle_count:<6}║")
        print("╠" + "─" * 78 + "╣")
        print(f"║  💎 Total System Energy: {format_usd(total_energy):<15} {growth_icon} Growth: {growth_color}{format_usd(energy_growth):>10}\033[0m ({growth_pct:+.2f}%)  ║")
        print("╚" + "═" * 78 + "╝")
        print()
    
    def display_queen_intelligence(self):
        """Display Queen's energy generation intelligence."""
        state = self.get_queen_redistribution_state()
        
        net_gained = state.get('total_net_energy_gained', 0.0)
        drains_avoided = state.get('total_blocked_drains_avoided', 0.0)
        decisions = state.get('decisions_count', 0)
        executions = state.get('executions_count', 0)
        seconds_since = state.get('seconds_since_update', 999999)
        is_alive = state.get('is_alive', False)
        
        # Heartbeat indicator
        if is_alive:
            heartbeat = "\033[92m💚 ACTIVE\033[0m"
            status_msg = f"\033[90m(updated {seconds_since:.0f}s ago)\033[0m"
        else:
            heartbeat = "\033[91m💔 IDLE\033[0m"
            status_msg = "\033[90m(no recent activity)\033[0m"
        
        # Calculate Queen efficiency (energy generated per decision)
        if decisions > 0:
            efficiency = (net_gained + drains_avoided) / decisions
        else:
            efficiency = 0.0
        
        print("╔" + "═" * 78 + "╗")
        print("║  🐝 QUEEN ENERGY GENERATION INTELLIGENCE" + " " * 36 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        print(f"  ⚡ Engine Status:       {heartbeat} {status_msg}")
        print()
        print(f"  📊 Energy Generation Summary:")
        print(f"     ├─ ⚡ Energy Generated:      {format_usd(net_gained):<15} (Net positive moves)")
        print(f"     ├─ 🛡️  Energy Conserved:      {format_usd(drains_avoided):<15} (Blocked drains)")
        print(f"     └─ 💎 Total Energy Impact:   {format_usd(net_gained + drains_avoided)}")
        print()
        print(f"  🎯 Queen Performance:")
        print(f"     ├─ Decisions Analyzed:      {decisions} opportunities")
        print(f"     ├─ Energy Moves Executed:   {executions} redistributions")
        print(f"     └─ Efficiency:              {format_usd(efficiency)} per decision")
        
        # Show recent decisions
        recent = state.get('recent_decisions', [])
        if recent:
            print()
            print("  📊 Recent Energy Decisions:")
            for i, dec in enumerate(recent[-3:], 1):
                opp = dec.get('opportunity', {})
                decision = dec.get('decision', 'UNKNOWN')
                relay = opp.get('relay', '???')
                target = opp.get('target_asset', '???')
                net_gain = opp.get('net_energy_gain', 0.0)
                confidence = dec.get('queen_confidence', 0.0)
                
                decision_icon = "✅" if decision == 'EXECUTE' else "🚫"
                decision_color = '\033[92m' if decision == 'EXECUTE' else '\033[91m'
                conf_bar = "●" * int(confidence * 5) + "○" * (5 - int(confidence * 5))
                
                prefix = "     └─" if i == len(recent[-3:]) else "     ├─"
                print(f"{prefix} {decision_icon} {decision_color}{decision:<8}\033[0m │ {relay} → {target:<12} │ {format_usd(net_gain):<12} │ {conf_bar}")
        else:
            print()
            print("  📊 \033[90m🔍 Scanning for profitable opportunities...\033[0m")
        print()
    
    def display_power_station(self):
        """Display power station energy flow."""
        state = self.get_power_station_state()
        
        status = state.get('status', 'UNKNOWN')
        cycles = state.get('cycles_run', 0)
        total_energy = state.get('total_energy_now', 0.0)
        deployed = state.get('energy_deployed', 0.0)
        net_flow = state.get('net_flow', 0.0)
        efficiency = state.get('efficiency', 0.0)
        
        status_icon = "🟢" if status == 'RUNNING' else "🟡"
        status_color = '\033[92m' if status == 'RUNNING' else '\033[93m'
        
        print("╔" + "═" * 78 + "╗")
        print("║  ⚡ ENERGY RESERVES & FLOW" + " " * 50 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        print(f"  {status_icon} Power Station Status:  {status_color}{status}\033[0m  \033[90m({cycles} energy cycles)\033[0m")
        print()
        print("  💎 System Energy Status:")
        print(f"     ├─ Total Energy Reserves:    {format_usd(total_energy)}")
        print(f"     ├─ Energy in Positions:      {format_usd(deployed)}")
        print(f"     └─ Net Energy Flow (24h):    {format_usd(net_flow)}")
        print()
        efficiency_bar = "█" * int(efficiency / 10) + "░" * (10 - int(efficiency / 10))
        print(f"  📊 Energy Efficiency:         {efficiency:.1f}% [{efficiency_bar}]")
        print()
    
    def display_relay_status(self):
        """Display energy distribution across relays."""
        print("╔" + "═" * 78 + "╗")
        print("║  🔌 ENERGY DISTRIBUTION BY RELAY" + " " * 44 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        print("  \033[90m(Each relay operates independently with internal energy isolation)\033[0m")
        print()
        
        relays = ['BIN', 'KRK', 'ALP', 'CAP']
        relay_names = {'BIN': 'Binance', 'KRK': 'Kraken', 'ALP': 'Alpaca', 'CAP': 'Capital'}
        total_system_energy = 0.0
        total_idle_energy = 0.0
        
        print(f"  {'RELAY':<10} {'TOTAL':<12} {'IDLE':<12} {'DEPLOYED':<12} {'MOBILITY':<20}")
        print("  " + "─" * 74)
        
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
                mobility = "\033[92m🟢 HIGH\033[0m"
                mobility_bar = "█" * 5
            elif idle_pct > 10:
                mobility = "\033[93m🟡 MED\033[0m"
                mobility_bar = "█" * 3 + "░" * 2
            else:
                mobility = "\033[91m🔴 LOW\033[0m"
                mobility_bar = "█" + "░" * 4
            
            total_str = f"${total:.2f}"
            idle_str = f"${idle:.2f}"
            pos_str = f"${positions:.2f}"
            
            print(f"  {relay:<10} {total_str:<12} {idle_str:<12} {pos_str:<12} {mobility} [{mobility_bar}] {idle_pct:.0f}%")
        
        print("  " + "─" * 74)
        total_idle_pct = (total_idle_energy/total_system_energy*100 if total_system_energy > 0 else 0)
        print(f"  {'TOTAL':<10} ${total_system_energy:<11.2f} ${total_idle_energy:<11.2f} ${total_system_energy-total_idle_energy:<11.2f} \033[96m⚡ System: {total_idle_pct:.0f}% idle\033[0m")
        print()
    
    def display_energy_conservation(self):
        """Display energy conservation and generation metrics."""
        queen_state = self.get_queen_redistribution_state()
        net_gained = queen_state.get('total_net_energy_gained', 0.0)
        drains_avoided = queen_state.get('total_blocked_drains_avoided', 0.0)
        
        total_conserved = net_gained + drains_avoided
        
        print("╔" + "═" * 78 + "╗")
        print("║  🌿 ENERGY CONSERVATION & GENERATION" + " " * 40 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        if total_conserved > 0:
            efficiency = (net_gained / total_conserved * 100)
            print(f"  💎 Net Energy Gained:        {format_usd(net_gained)}")
            print(f"  🛡️  Drains Blocked:           {format_usd(drains_avoided)}")
            print(f"  ✨ Total Conserved:           {format_usd(total_conserved)}")
            print()
            efficiency_bar = "█" * int(efficiency / 10) + "░" * (10 - int(efficiency / 10))
            print(f"  📊 Conservation Rate:        {efficiency:.1f}% [{efficiency_bar}]")
            print(f"     \033[90m(Net gained / Total conserved)\033[0m")
        else:
            print(f"  💎 Net Energy Gained:        {format_usd(net_gained)}")
            print(f"  🛡️  Drains Blocked:           {format_usd(drains_avoided)}")
            print(f"  ✨ Total Conserved:           {format_usd(total_conserved)}")
            print()
            print("  \033[90m📈 Begin trading to track conservation metrics\033[0m")
        print()
    
    async def run(self):
        """Run continuous dashboard updates."""
        print("🐝 Queen Power Dashboard starting...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.cycle_count += 1
                
                self.display_header()
                self.display_queen_intelligence()
                self.display_power_station()
                self.display_relay_status()
                self.display_energy_conservation()
                
                print("┏" + "━" * 78 + "┓")
                print(f"┃  ⏳ Next update in {self.update_interval}s" + " " * 33 + "\033[90mPress Ctrl+C to stop\033[0m" + " " * 3 + "┃")
                print("┗" + "━" * 78 + "┛")
                print()
                
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
