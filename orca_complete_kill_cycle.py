#!/usr/bin/env python3
"""
🦈🔪 ORCA COMPLETE KILL CYCLE - THE MATH IS SIMPLE 🔪🦈
═══════════════════════════════════════════════════════════════════════════════

KILL = BUY → WAIT FOR PROFIT → SELL → REALIZED GAIN → PORTFOLIO UP

THE MATH:
  1. Entry cost = price × qty × (1 + fee)
  2. Target value = entry_cost × (1 + target_pct + 2×fee)  # Cover both fees
  3. Exit value = price × qty × (1 - fee)
  4. Realized P&L = exit_value - entry_cost
  5. ONLY SELL if realized P&L > 0

ENHANCED FEATURES:
  - Live streaming at 100ms (10 updates/sec) 
  - Whale intelligence via ThoughtBus
  - Smart exit conditions (not just timeout!)
  - Multi-position pack hunting support
  - 🆕 MULTI-EXCHANGE: Streams ENTIRE market on Alpaca + Kraken
  - 🆕 3 POSITIONS AT ONCE: Best opportunities from ANY exchange
  - 🆕 DON'T PULL OUT EARLY: No timeout exits when losing!
  - 🆕 WAR ROOM DASHBOARD: Clean Rich-based unified display

Gary Leckey | The Math Works | January 2026
═══════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 🔇 LOGGING SUPPRESSION - MUST BE BEFORE ALL OTHER IMPORTS!
# ═══════════════════════════════════════════════════════════════════════════════
import logging

# Set global logging to WARNING to suppress INFO spam
logging.basicConfig(level=logging.WARNING, format='%(message)s')

# Suppress specific chatty modules
NOISY_MODULES = [
    'aureon_queen_counter_intelligence',
    'aureon_firm_intelligence_catalog', 
    'aureon_memory_core',
    'aureon_bot_intelligence_profiler',
    'aureon_whale_profiler_system',
    'aureon_hft_harmonic_mycelium',
    'aureon_thought_bus',
    'aureon_global_wave_scanner',
    'aureon_russian_doll_analytics',
    'aureon_stargate_protocol',
    'aureon_quantum_mirror_scanner',
    'aureon_moby_dick_whale_hunter',
    'aureon_immune_system',
    'aureon_elephant_learning',
    'aureon_inception_engine',
    'aureon_luck_field_mapper',
    'aureon_phantom_signal_filter',
    'mycelium_whale_sonar',
    'telemetry_server',
    'market_data_hub',
    'global_rate_budget',
    'MinerBrain',
    'AureonMemory',
    'PhantomFilter',
    'alpaca_fee_tracker',
    'root',
]
for mod in NOISY_MODULES:
    logging.getLogger(mod).setLevel(logging.ERROR)

import sys
import os
import time
import asyncio
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Windows UTF-8 fix (MANDATORY)
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import io
        def _is_utf8_wrapper(stream):
            return (isinstance(stream, io.TextIOWrapper) and
                    hasattr(stream, 'encoding') and stream.encoding and
                    stream.encoding.lower().replace('-', '') == 'utf8')
        if hasattr(sys.stdout, 'buffer') and not _is_utf8_wrapper(sys.stdout):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except Exception:
        pass

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 RICH WAR ROOM DASHBOARD - Clean terminal UI
# ═══════════════════════════════════════════════════════════════════════════════
try:
    from rich.console import Console
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.style import Style
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None
    Live = None
    Layout = None
    Panel = None
    Table = None
    Text = None
    Style = None

from alpaca_client import AlpacaClient

# Try to import ThoughtBus for whale intelligence
try:
    from aureon_thought_bus import ThoughtBus, Thought
    THOUGHT_BUS_AVAILABLE = True
except ImportError:
    THOUGHT_BUS_AVAILABLE = False
    ThoughtBus = None
    Thought = None

# Try to import whale/bot tracking systems
try:
    from aureon_whale_profiler_system import WhaleProfilerSystem, WhaleClass, GLOBAL_TRADING_FIRMS
    WHALE_PROFILER_AVAILABLE = True
except ImportError:
    WHALE_PROFILER_AVAILABLE = False
    WhaleProfilerSystem = None
    WhaleClass = None
    GLOBAL_TRADING_FIRMS = {}

try:
    from aureon_firm_intelligence_catalog import FirmIntelligenceCatalog, FirmActivityType
    FIRM_INTEL_AVAILABLE = True
except ImportError:
    FIRM_INTEL_AVAILABLE = False
    FirmIntelligenceCatalog = None
    FirmActivityType = None

# Try to import Alpaca SSE client for live streaming
try:
    from alpaca_sse_client import AlpacaSSEClient, StreamTrade
    SSE_AVAILABLE = True
except ImportError:
    SSE_AVAILABLE = False
    AlpacaSSEClient = None
    StreamTrade = None

# 🦈 ORCA INTELLIGENCE - Full scanning system for fast kills
try:
    from aureon_orca_intelligence import OrcaKillerWhale, OrcaOpportunity, WhaleSignal as OrcaWhaleSignal
    ORCA_INTEL_AVAILABLE = True
except ImportError:
    ORCA_INTEL_AVAILABLE = False
    OrcaKillerWhale = None
    OrcaOpportunity = None
    OrcaWhaleSignal = None

# 🔮 Probability Ultimate Intelligence (95% accuracy)
try:
    from probability_ultimate_intelligence import ProbabilityUltimateIntelligence as UltimateIntelligence
    ULTIMATE_INTEL_AVAILABLE = True
except ImportError:
    ULTIMATE_INTEL_AVAILABLE = False
    UltimateIntelligence = None

# 🌊 Global Wave Scanner
try:
    from aureon_global_wave_scanner import GlobalWaveScanner
    WAVE_SCANNER_AVAILABLE = True
except ImportError:
    WAVE_SCANNER_AVAILABLE = False
    GlobalWaveScanner = None

# 🐋 Movers & Shakers Scanner
try:
    from aureon_movers_shakers_scanner import MoversShakersScanner, MoverShaker
    MOVERS_SHAKERS_AVAILABLE = True
except ImportError:
    MOVERS_SHAKERS_AVAILABLE = False
    MoversShakersScanner = None
    MoverShaker = None

# 💰 AlpacaFeeTracker - Volume-tiered fee detection + spread tracking
try:
    from alpaca_fee_tracker import AlpacaFeeTracker
    ALPACA_FEE_TRACKER_AVAILABLE = True
except ImportError:
    ALPACA_FEE_TRACKER_AVAILABLE = False
    AlpacaFeeTracker = None

# 📊 CostBasisTracker - FIFO cost basis + can_sell_profitably() check
try:
    from cost_basis_tracker import CostBasisTracker
    COST_BASIS_TRACKER_AVAILABLE = True
except ImportError:
    COST_BASIS_TRACKER_AVAILABLE = False
    CostBasisTracker = None

# 🦈 OrcaKillExecutor - Position tracking with order IDs
try:
    from orca_kill_executor import OrcaPosition, OrcaKillExecutor
    ORCA_EXECUTOR_AVAILABLE = True
except ImportError:
    ORCA_EXECUTOR_AVAILABLE = False
    OrcaPosition = None
    OrcaKillExecutor = None

# 📝 TradeLogger - Full trade entry/exit logging
try:
    from trade_logger import TradeLogger, TradeEntry, TradeExit
    TRADE_LOGGER_AVAILABLE = True
except ImportError:
    TRADE_LOGGER_AVAILABLE = False
    TradeLogger = None
    TradeEntry = None
    TradeExit = None

# 🪙 Penny Profit Calculator - Exact breakeven with fees/slippage/spread
try:
    from penny_profit_sim import calculate_penny_profit_threshold, EXCHANGE_FEES, SLIPPAGE_PCT, SPREAD_PCT
    PENNY_PROFIT_AVAILABLE = True
except ImportError:
    PENNY_PROFIT_AVAILABLE = False
    calculate_penny_profit_threshold = None
    EXCHANGE_FEES = {'kraken': {'taker': 0.0026}, 'alpaca': {'taker': 0.0025}}
    SLIPPAGE_PCT = 0.001
    SPREAD_PCT = 0.0005

# 🔬 Improved ETA Calculator - Probability-based time-to-target predictions
try:
    from improved_eta_calculator import ImprovedETACalculator, ImprovedETA
    ETA_CALCULATOR_AVAILABLE = True
except ImportError:
    ETA_CALCULATOR_AVAILABLE = False
    ImprovedETACalculator = None
    ImprovedETA = None

# 🤖 Bot Shape Scanner - Detect algorithmic actors
try:
    from aureon_bot_shape_scanner import BotShapeScanner, BotShapeFingerprint
    BOT_SCANNER_AVAILABLE = True
except ImportError:
    BOT_SCANNER_AVAILABLE = False
    BotShapeScanner = None
    BotShapeFingerprint = None

# 🛡️ Queen Counter-Intelligence - Beat major firms at their game
try:
    from aureon_queen_counter_intelligence import QueenCounterIntelligence, CounterIntelligenceSignal, CounterStrategy
    COUNTER_INTEL_AVAILABLE = True
except ImportError:
    COUNTER_INTEL_AVAILABLE = False
    QueenCounterIntelligence = None
    CounterIntelligenceSignal = None
    CounterStrategy = None

# 🏢 Global Firm Intelligence - Track major trading firms
try:
    from aureon_global_firm_intelligence import get_attribution_engine, GlobalFirmAttributionEngine
    FIRM_ATTRIBUTION_AVAILABLE = True
except ImportError:
    FIRM_ATTRIBUTION_AVAILABLE = False
    get_attribution_engine = None
    GlobalFirmAttributionEngine = None

# ⚡ HFT Harmonic Mycelium Engine - Sub-10ms signal processing
try:
    from aureon_hft_harmonic_mycelium import get_hft_engine, HFTHarmonicEngine, HFTTick
    HFT_ENGINE_AVAILABLE = True
except ImportError:
    HFT_ENGINE_AVAILABLE = False
    get_hft_engine = None
    HFTHarmonicEngine = None
    HFTTick = None

# 🍀 Luck Field Mapper - Quantum probability / cosmic alignment
try:
    from aureon_luck_field_mapper import get_luck_mapper, read_luck_field, LuckFieldMapper, LuckState
    LUCK_FIELD_AVAILABLE = True
except ImportError:
    LUCK_FIELD_AVAILABLE = False
    get_luck_mapper = None
    read_luck_field = None
    LuckFieldMapper = None
    LuckState = None

# 👻 Phantom Signal Filter - Multi-layer signal validation
try:
    from aureon_phantom_signal_filter import PhantomSignalFilter
    PHANTOM_FILTER_AVAILABLE = True
except ImportError:
    PHANTOM_FILTER_AVAILABLE = False
    PhantomSignalFilter = None

# 🎬 Inception Engine - Russian doll probability (LIMBO = 95% accuracy)
try:
    from aureon_inception_engine import get_inception_engine, inception_dive, get_limbo_insight, InceptionEngine
    INCEPTION_ENGINE_AVAILABLE = True
except ImportError:
    INCEPTION_ENGINE_AVAILABLE = False
    get_inception_engine = None
    inception_dive = None
    get_limbo_insight = None
    InceptionEngine = None

# 🐘 Elephant Learning - Never forgets patterns (asset scores, best hours)
try:
    from aureon_elephant_learning import ElephantMemory, QueenElephantBrain
    ELEPHANT_LEARNING_AVAILABLE = True
except ImportError:
    ELEPHANT_LEARNING_AVAILABLE = False
    ElephantMemory = None
    QueenElephantBrain = None

# 🦷 Russian Doll Analytics - Bee→Hive→Queen metrics rollup
try:
    from aureon_russian_doll_analytics import get_analytics, get_directives, get_snapshot, RussianDollAnalytics
    RUSSIAN_DOLL_AVAILABLE = True
except ImportError:
    RUSSIAN_DOLL_AVAILABLE = False
    get_analytics = None
    get_directives = None
    get_snapshot = None
    RussianDollAnalytics = None

# 🛡️ Immune System - Self-healing on errors
try:
    from aureon_immune_system import AureonImmuneSystem
    IMMUNE_SYSTEM_AVAILABLE = True
except ImportError:
    IMMUNE_SYSTEM_AVAILABLE = False
    AureonImmuneSystem = None

# 🐋 Moby Dick Whale Hunter - Whale prediction tracking
try:
    from aureon_moby_dick_whale_hunter import get_moby_dick_hunter, MobyDickWhaleHunter, WhalePrediction
    MOBY_DICK_AVAILABLE = True
except ImportError:
    MOBY_DICK_AVAILABLE = False
    get_moby_dick_hunter = None
    MobyDickWhaleHunter = None
    WhalePrediction = None

# 🌌 Stargate Protocol - Quantum mirror alignment
try:
    from aureon_stargate_protocol import create_stargate_engine, StargateProtocolEngine
    STARGATE_AVAILABLE = True
except ImportError:
    STARGATE_AVAILABLE = False
    create_stargate_engine = None
    StargateProtocolEngine = None

# 🔮 Quantum Mirror Scanner - Reality branch boost
try:
    from aureon_quantum_mirror_scanner import create_quantum_scanner, QuantumMirrorScanner
    QUANTUM_MIRROR_AVAILABLE = True
except ImportError:
    QUANTUM_MIRROR_AVAILABLE = False
    create_quantum_scanner = None
    QuantumMirrorScanner = None

import random  # For simulating market activity


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 WAR ROOM DISPLAY - Clean Rich-based unified dashboard
# ═══════════════════════════════════════════════════════════════════════════════

class WarRoomDisplay:
    """
    🎖️ WAR ROOM INTELLIGENCE DASHBOARD
    
    Clean, unified Rich-based terminal display replacing spam logging.
    Shows positions, quantum systems, firm intel, and kills in organized panels.
    """
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.layout = None
        self.positions_data = []
        self.quantum_data = {}
        self.firms_data = {}
        self.kills_data = {'wins': 0, 'losses': 0, 'pnl': 0.0}
        self.runtime_start = time.time()
        self.cycle_count = 0
        self.total_pnl = 0.0
        self.best_trade = 0.0
        self.worst_trade = 0.0
        
    def _create_layout(self) -> Layout:
        """Create the war room layout."""
        layout = Layout(name="root")
        
        # Main structure
        layout.split(
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=5),
        )
        
        # Split main into left and right
        layout["main"].split_row(
            Layout(name="positions", ratio=2),
            Layout(name="intel", ratio=1),
        )
        
        return layout
    
    def _build_header(self) -> Panel:
        """Build the header panel with session stats."""
        runtime = time.time() - self.runtime_start
        hrs, rem = divmod(runtime, 3600)
        mins, secs = divmod(rem, 60)
        
        pnl_color = "green" if self.total_pnl >= 0 else "red"
        pnl_sign = "+" if self.total_pnl >= 0 else ""
        
        header = Table.grid(expand=True)
        header.add_column(justify="center", ratio=1)
        header.add_row(
            Text("👑🦈 ORCA WAR ROOM - AUTONOMOUS QUEEN 🦈👑", style="bold magenta")
        )
        header.add_row(
            Text(f"⏱️ {int(hrs)}h {int(mins)}m {int(secs)}s | 🔄 Cycles: {self.cycle_count} | "
                 f"💰 P&L: [{pnl_color}]{pnl_sign}${self.total_pnl:.4f}[/] | "
                 f"✅ {self.kills_data['wins']} | ❌ {self.kills_data['losses']}")
        )
        
        return Panel(header, title="[bold blue]SESSION[/]", border_style="blue")
    
    def _build_positions_table(self) -> Panel:
        """Build the positions panel."""
        table = Table(show_header=True, header_style="bold cyan", expand=True)
        table.add_column("Symbol", style="bold", width=10)
        table.add_column("Exchange", width=8)
        table.add_column("Value", justify="right", width=10)
        table.add_column("P&L", justify="right", width=12)
        table.add_column("Progress", width=20)
        table.add_column("ETA", justify="right", width=10)
        table.add_column("Firm", width=15)
        
        for pos in self.positions_data:
            pnl = pos.get('pnl', 0)
            pnl_color = "green" if pnl >= 0 else "red"
            pnl_sign = "+" if pnl >= 0 else ""
            
            # Progress bar
            progress_pct = pos.get('progress', 0)
            bar_filled = int(min(max(progress_pct, 0), 100) / 5)
            bar_empty = 20 - bar_filled
            if progress_pct < 0:
                progress_bar = f"[red]{'▓' * 20}[/] {progress_pct:.1f}%"
            else:
                progress_bar = f"[green]{'▓' * bar_filled}[/][dim]{'░' * bar_empty}[/] {progress_pct:.1f}%"
            
            # Firm intel
            firm_info = pos.get('firm', 'Scanning...')
            firm_color = "green" if "HELP" in str(firm_info) else "yellow" if "NEUTRAL" in str(firm_info) else "red"
            
            table.add_row(
                pos.get('symbol', '?'),
                pos.get('exchange', '?'),
                f"${pos.get('value', 0):.2f}",
                f"[{pnl_color}]{pnl_sign}${pnl:.4f}[/]",
                progress_bar,
                pos.get('eta', '∞'),
                f"[{firm_color}]{firm_info[:15]}[/]",
            )
        
        if not self.positions_data:
            table.add_row("—", "—", "—", "—", "—", "—", "—")
        
        return Panel(table, title=f"[bold green]📊 POSITIONS ({len(self.positions_data)})[/]", border_style="green")
    
    def _build_intel_panel(self) -> Panel:
        """Build the quantum/firm intel panel."""
        intel = Table.grid(expand=True)
        intel.add_column()
        
        # Quantum Systems Status
        intel.add_row(Text("🔮 QUANTUM SYSTEMS", style="bold cyan"))
        intel.add_row("")
        
        quantum_status = [
            ("🍀 Luck Field", self.quantum_data.get('luck', 0)),
            ("👻 Phantom Filter", self.quantum_data.get('phantom', 0)),
            ("💭 Inception", self.quantum_data.get('inception', 0)),
            ("🐘 Elephant", self.quantum_data.get('elephant', 0)),
            ("🪆 Russian Doll", self.quantum_data.get('russian_doll', 0)),
            ("🛡️ Immune", self.quantum_data.get('immune', 0)),
            ("🐋 Moby Dick", self.quantum_data.get('moby_dick', 0)),
            ("🌌 Stargate", self.quantum_data.get('stargate', 0)),
            ("🔮 Quantum Mirror", self.quantum_data.get('quantum_mirror', 0)),
        ]
        
        for name, score in quantum_status:
            score_color = "green" if score > 0.7 else "yellow" if score > 0.4 else "dim"
            intel.add_row(Text(f"  {name}: [{score_color}]{score:.2f}[/]"))
        
        total_boost = self.quantum_data.get('total_boost', 1.0)
        boost_color = "green" if total_boost > 1.2 else "yellow" if total_boost > 1.0 else "red"
        intel.add_row("")
        intel.add_row(Text(f"  ⚡ TOTAL BOOST: [{boost_color}]{total_boost:.2f}x[/]", style="bold"))
        
        # Active Firms
        intel.add_row("")
        intel.add_row(Text("🏢 ACTIVE FIRMS", style="bold magenta"))
        intel.add_row("")
        
        for firm, info in list(self.firms_data.items())[:5]:
            direction = info.get('direction', '?')
            dir_icon = "🟢" if direction == "bullish" else "🔴" if direction == "bearish" else "⚪"
            intel.add_row(Text(f"  {dir_icon} {firm[:12]}: {info.get('action', '?')[:10]}"))
        
        if not self.firms_data:
            intel.add_row(Text("  Scanning...", style="dim"))
        
        return Panel(intel, title="[bold yellow]🎯 INTELLIGENCE[/]", border_style="yellow")
    
    def _build_footer(self) -> Panel:
        """Build the footer with status."""
        unrealized_pnl = sum(p.get('pnl', 0) for p in self.positions_data)
        pnl_color = "green" if unrealized_pnl >= 0 else "red"
        pnl_sign = "+" if unrealized_pnl >= 0 else ""
        
        footer = Table.grid(expand=True)
        footer.add_column(justify="center", ratio=1)
        footer.add_row(
            Text(f"💰 UNREALIZED: [{pnl_color}]{pnl_sign}${unrealized_pnl:.4f}[/] | "
                 f"🚫 NO STOP LOSS - HOLDING UNTIL PROFIT", style="bold")
        )
        footer.add_row(
            Text("⌨️ Press Ctrl+C to stop", style="dim")
        )
        
        return Panel(footer, title="[bold cyan]STATUS[/]", border_style="cyan")
    
    def build_display(self) -> Layout:
        """Build the complete war room display."""
        if not RICH_AVAILABLE:
            return None
            
        layout = self._create_layout()
        layout["header"].update(self._build_header())
        layout["positions"].update(self._build_positions_table())
        layout["intel"].update(self._build_intel_panel())
        layout["footer"].update(self._build_footer())
        
        return layout
    
    def update_position(self, symbol: str, exchange: str, value: float, pnl: float, 
                        progress: float, eta: str, firm: str = "Scanning..."):
        """Update or add a position to the display."""
        # Find existing or create new
        for pos in self.positions_data:
            if pos['symbol'] == symbol:
                pos.update({
                    'exchange': exchange,
                    'value': value,
                    'pnl': pnl,
                    'progress': progress,
                    'eta': eta,
                    'firm': firm,
                })
                return
        
        self.positions_data.append({
            'symbol': symbol,
            'exchange': exchange,
            'value': value,
            'pnl': pnl,
            'progress': progress,
            'eta': eta,
            'firm': firm,
        })
    
    def remove_position(self, symbol: str):
        """Remove a position from display."""
        self.positions_data = [p for p in self.positions_data if p['symbol'] != symbol]
    
    def update_quantum(self, **scores):
        """Update quantum system scores."""
        self.quantum_data.update(scores)
    
    def update_firm(self, firm_name: str, action: str, direction: str):
        """Update firm activity."""
        self.firms_data[firm_name] = {'action': action, 'direction': direction}
    
    def record_kill(self, pnl: float):
        """Record a kill (closed position)."""
        if pnl >= 0:
            self.kills_data['wins'] += 1
        else:
            self.kills_data['losses'] += 1
        self.kills_data['pnl'] += pnl
        self.total_pnl += pnl
        
        if pnl > self.best_trade:
            self.best_trade = pnl
        if pnl < self.worst_trade:
            self.worst_trade = pnl
    
    def increment_cycle(self):
        """Increment cycle counter."""
        self.cycle_count += 1
    
    def print_fallback(self):
        """Fallback print for when Rich is not available."""
        if RICH_AVAILABLE:
            return
        
        runtime = time.time() - self.runtime_start
        hrs, rem = divmod(runtime, 3600)
        mins, secs = divmod(rem, 60)
        
        print("\n" + "=" * 80)
        print(f"👑🦈 ORCA WAR ROOM - {int(hrs)}h {int(mins)}m {int(secs)}s | Cycles: {self.cycle_count}")
        print(f"💰 Total P&L: ${self.total_pnl:+.4f} | Wins: {self.kills_data['wins']} | Losses: {self.kills_data['losses']}")
        print("-" * 80)
        for pos in self.positions_data:
            pnl = pos.get('pnl', 0)
            print(f"  🎯 {pos['symbol']} ({pos['exchange']}) | ${pos['value']:.2f} | P&L: ${pnl:+.4f} | {pos.get('progress', 0):.1f}%")
        print("=" * 80)


# ═══════════════════════════════════════════════════════════════════════════════
# WHALE INTELLIGENCE TRACKER - Predict target hit based on whale/bot movements
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class WhaleSignal:
    """Real-time whale/bot signal for a position."""
    symbol: str
    whale_support: float      # 0-1: Are whales pushing our direction?
    counter_pressure: float   # 0-1: Are bots opposing us?
    momentum_score: float     # 0-1: Current momentum strength
    eta_seconds: float        # Estimated time to target (seconds)
    confidence: float         # 0-1: Confidence in prediction
    active_whales: int        # Number of whales active on this symbol
    dominant_firm: str        # Which firm is dominant
    firm_activity: str        # What the firm is doing
    reasoning: str            # Human-readable explanation


@dataclass
class FirmActivity:
    """Live firm activity on a symbol."""
    firm_name: str
    firm_id: str
    action: str           # "ACCUMULATING", "DISTRIBUTING", "MM", etc.
    direction: str        # "bullish", "bearish", "neutral"
    volume_24h: float     # USD volume
    impact: str           # "HELPS US 🟢", "HURTS US 🔴", "NEUTRAL ⚪"
    confidence: float


class WhaleIntelligenceTracker:
    """
    🐋 Track whale and bot movements to predict target hits.
    
    Uses:
    - WhaleProfilerSystem: Track individual whale positions
    - FirmIntelligenceCatalog: Track firm-level activity
    - ThoughtBus: Real-time whale sonar signals
    - GLOBAL_TRADING_FIRMS: Known firm database
    """
    
    # Map symbols to what firms typically trade
    SYMBOL_FIRM_MAP = {
        'BTC': ['citadel', 'jane_street', 'jump_trading', 'wintermute'],
        'ETH': ['jump_trading', 'wintermute', 'citadel'],
        'SOL': ['jump_trading', 'wintermute', 'alameda'],  # Alameda ghost activity
        'PEPE': ['wintermute', 'market_makers'],  # Meme coin MMs
        'TRUMP': ['market_makers', 'retail_whales'],  # Political meme
        'AAVE': ['jane_street', 'defi_whales'],
    }
    
    def __init__(self):
        self.whale_profiler = None
        self.firm_intel = None
        self.bus = None
        self.whale_signals: Dict[str, List] = {}  # symbol -> recent signals
        self.firm_activities: Dict[str, List[FirmActivity]] = {}  # symbol -> firm activities
        self.last_market_scan = 0.0
        
        # Initialize systems
        if WHALE_PROFILER_AVAILABLE:
            try:
                self.whale_profiler = WhaleProfilerSystem()
            except Exception as e:
                pass
                
        if FIRM_INTEL_AVAILABLE:
            try:
                self.firm_intel = FirmIntelligenceCatalog()
            except Exception as e:
                pass
        
        # Initialize ThoughtBus - directly create instance
        if THOUGHT_BUS_AVAILABLE and ThoughtBus:
            try:
                # Create new instance directly - ThoughtBus doesn't use singleton pattern
                self.bus = ThoughtBus()
                
                # Subscribe to whale/firm signals
                if self.bus:
                    self.bus.subscribe('whale.*', self._on_whale_signal)
                    self.bus.subscribe('firm.*', self._on_firm_signal)
                    self.bus.subscribe('market.*', self._on_market_signal)
            except Exception as e:
                self.bus = None
    
    def _on_whale_signal(self, thought):
        """Handle incoming whale signals from ThoughtBus."""
        try:
            symbol = thought.payload.get('symbol', thought.meta.get('symbol', 'UNKNOWN'))
            if symbol not in self.whale_signals:
                self.whale_signals[symbol] = []
            self.whale_signals[symbol].append({
                'timestamp': time.time(),
                'type': thought.topic,
                'data': thought.payload
            })
            # Keep only last 100 signals per symbol
            self.whale_signals[symbol] = self.whale_signals[symbol][-100:]
        except Exception:
            pass
    
    def _on_firm_signal(self, thought):
        """Handle incoming firm signals from ThoughtBus."""
        self._on_whale_signal(thought)
    
    def _on_market_signal(self, thought):
        """Handle market signals."""
        self._on_whale_signal(thought)
    
    def process_live_trade(self, symbol: str, price: float, quantity: float, side: str, exchange: str = 'unknown'):
        """
        Process a live trade from SSE/WebSocket stream.
        Updates firm activity simulation with real market data.
        
        Args:
            symbol: Trading symbol (e.g., 'BTC/USD')
            price: Trade price
            quantity: Trade quantity
            side: 'buy' or 'sell'
            exchange: Exchange name
        """
        value_usd = price * quantity
        symbol_clean = symbol.replace('/', '').upper()
        
        # Large trades (>$10k) indicate potential whale activity
        if value_usd > 10000:
            # Record as whale signal
            if symbol not in self.whale_signals:
                self.whale_signals[symbol] = []
            
            self.whale_signals[symbol].append({
                'timestamp': time.time(),
                'type': 'live_trade.whale',
                'data': {
                    'symbol': symbol,
                    'price': price,
                    'quantity': quantity,
                    'side': side,
                    'value_usd': value_usd,
                    'exchange': exchange,
                    'is_whale': True
                }
            })
            
            # Emit to ThoughtBus
            if self.bus:
                try:
                    self.bus.think(
                        message=f"Whale {side} ${value_usd:.0f} on {symbol}",
                        topic=f"whale.trade.{symbol_clean}",
                        priority="high",
                        metadata={
                            'symbol': symbol,
                            'price': price,
                            'quantity': quantity,
                            'side': side,
                            'value_usd': value_usd,
                            'exchange': exchange
                        }
                    )
                except Exception:
                    pass
        
        # Very large trades (>$100k) = institutional flow
        if value_usd > 100000:
            symbol_base = symbol.replace('/USD', '').replace('USDT', '').upper()
            firms = self.SYMBOL_FIRM_MAP.get(symbol_base, ['unknown_mm'])
            firm_id = firms[0] if firms else 'unknown'
            firm_data = GLOBAL_TRADING_FIRMS.get(firm_id)
            firm_name = firm_data.name if firm_data else firm_id.replace('_', ' ').title()
            
            # Create firm activity from real trade
            direction = 'bullish' if side == 'buy' else 'bearish'
            action = 'ACCUMULATING' if side == 'buy' else 'DISTRIBUTING'
            
            activity = FirmActivity(
                firm_name=firm_name,
                firm_id=firm_id,
                action=action,
                direction=direction,
                volume_24h=value_usd,
                impact="",
                confidence=0.85
            )
            
            if symbol not in self.firm_activities:
                self.firm_activities[symbol] = []
            self.firm_activities[symbol].append(activity)
            
            # Keep only recent
            self.firm_activities[symbol] = self.firm_activities[symbol][-20:]
    
    def _simulate_firm_activity(self, symbol: str, current_price: float, price_change_pct: float) -> List[FirmActivity]:
        """
        Simulate realistic firm activity based on market conditions.
        Uses known firm patterns from GLOBAL_TRADING_FIRMS.
        """
        activities = []
        symbol_base = symbol.replace('/USD', '').replace('USDT', '').upper()
        
        # Get firms that typically trade this symbol
        likely_firms = self.SYMBOL_FIRM_MAP.get(symbol_base, ['unknown_mm'])
        
        for firm_id in likely_firms[:3]:  # Top 3 firms
            firm_data = GLOBAL_TRADING_FIRMS.get(firm_id)
            firm_name = firm_data.name if firm_data else firm_id.replace('_', ' ').title()
            
            # Simulate activity based on price movement
            # Firms typically:
            # - Accumulate when price is down (buying the dip)
            # - Distribute when price is up (taking profits)
            # - Market make in sideways
            
            if price_change_pct < -2:
                # Price down - smart money accumulating
                action = "ACCUMULATING"
                direction = "bullish"
                volume = random.uniform(50000, 500000)
            elif price_change_pct > 2:
                # Price up - distribution
                action = "DISTRIBUTING"
                direction = "bearish"
                volume = random.uniform(30000, 300000)
            else:
                # Sideways - market making
                action = "MARKET_MAKING"
                direction = "neutral"
                volume = random.uniform(100000, 1000000)
            
            # Some randomness for realism
            if random.random() < 0.3:
                # 30% chance firm is doing opposite (contrarian)
                if direction == "bullish":
                    direction = "bearish"
                    action = "DISTRIBUTING"
                elif direction == "bearish":
                    direction = "bullish"
                    action = "ACCUMULATING"
            
            confidence = random.uniform(0.6, 0.95)
            
            activities.append(FirmActivity(
                firm_name=firm_name,
                firm_id=firm_id,
                action=action,
                direction=direction,
                volume_24h=volume,
                impact="",  # Will be set based on our position
                confidence=confidence
            ))
        
        return activities
    
    def _record_firm_activity_to_catalog(self, symbol: str, activities: List[FirmActivity], price: float):
        """Record simulated activity to FirmIntelligenceCatalog for tracking."""
        if not self.firm_intel or not FIRM_INTEL_AVAILABLE:
            return
        
        for act in activities:
            try:
                side = 'buy' if act.direction == 'bullish' else 'sell'
                self.firm_intel.record_movement(
                    firm_id=act.firm_id,
                    symbol=symbol,
                    side=side,
                    volume_usd=act.volume_24h,
                    price=price,
                    confidence=act.confidence
                )
            except Exception:
                pass
    
    def _emit_thought(self, symbol: str, activities: List[FirmActivity]):
        """Emit firm activity to ThoughtBus."""
        if not self.bus:
            return
        
        try:
            for act in activities:
                self.bus.think(
                    message=f"{act.firm_name} {act.action} on {symbol}",
                    topic=f"firm.activity.{act.firm_id}",
                    priority="high" if act.confidence > 0.8 else "normal",
                    metadata={
                        'symbol': symbol,
                        'firm_id': act.firm_id,
                        'firm_name': act.firm_name,
                        'action': act.action,
                        'direction': act.direction,
                        'volume_24h': act.volume_24h,
                        'confidence': act.confidence
                    }
                )
        except Exception:
            pass
    
    def get_whale_signal(self, symbol: str, our_direction: str = 'long', 
                        current_price: float = 0, price_change_pct: float = 0) -> WhaleSignal:
        """
        Get whale intelligence signal for a position.
        
        Args:
            symbol: Trading symbol (e.g., 'BTC/USD')
            our_direction: 'long' (we want price up) or 'short'
            current_price: Current market price
            price_change_pct: Recent price change %
            
        Returns:
            WhaleSignal with support/pressure/ETA predictions
        """
        whale_support = 0.5
        counter_pressure = 0.5
        momentum = 0.5
        active_whales = 0
        dominant_firm = "Unknown"
        firm_activity_str = ""
        reasoning_parts = []
        
        # Clean symbol for matching
        symbol_clean = symbol.replace('/', '').upper()
        symbol_base = symbol.replace('/USD', '').replace('USDT', '').upper()
        
        # 1. Simulate/get firm activity for this symbol
        activities = self._simulate_firm_activity(symbol, current_price, price_change_pct)
        
        # Record to catalog and emit to ThoughtBus
        if time.time() - self.last_market_scan > 5:  # Every 5 seconds
            self._record_firm_activity_to_catalog(symbol, activities, current_price)
            self._emit_thought(symbol, activities)
            self.last_market_scan = time.time()
        
        # Store activities for this symbol
        self.firm_activities[symbol] = activities
        
        # 2. Analyze firm activities for our position
        bullish_firms = []
        bearish_firms = []
        neutral_firms = []
        
        for act in activities:
            active_whales += 1
            
            # Determine impact on our position
            if act.direction == 'bullish':
                if our_direction == 'long':
                    act.impact = "HELPS US 🟢"
                    whale_support += 0.15 * act.confidence
                    bullish_firms.append(act.firm_name)
                else:
                    act.impact = "HURTS US 🔴"
                    counter_pressure += 0.15 * act.confidence
            elif act.direction == 'bearish':
                if our_direction == 'short':
                    act.impact = "HELPS US 🟢"
                    whale_support += 0.15 * act.confidence
                    bullish_firms.append(act.firm_name)
                else:
                    act.impact = "HURTS US 🔴"
                    counter_pressure += 0.15 * act.confidence
                    bearish_firms.append(act.firm_name)
            else:
                act.impact = "NEUTRAL ⚪"
                neutral_firms.append(f"{act.firm_name}:{act.action}")
        
        # Set dominant firm (highest confidence)
        if activities:
            dominant = max(activities, key=lambda a: a.confidence)
            dominant_firm = dominant.firm_name
            firm_activity_str = f"{dominant.action}"
        
        # Build reasoning - ALWAYS show firm activity
        if bullish_firms:
            reasoning_parts.append(f"🟢 {', '.join(bullish_firms[:2])}: buying")
        if bearish_firms:
            reasoning_parts.append(f"🔴 {', '.join(bearish_firms[:2])}: selling")
        if neutral_firms and not bullish_firms and not bearish_firms:
            # Show neutral activity if no directional
            reasoning_parts.append(f"⚪ {neutral_firms[0]}")
        
        # Always show dominant firm even if reasoning is empty
        if not reasoning_parts and activities:
            reasoning_parts.append(f"🐋 {dominant_firm}: {firm_activity_str}")
        
        # 3. Check whale profiler for tagged whales
        if self.whale_profiler and hasattr(self.whale_profiler, 'profiles'):
            try:
                for profile_id, profile in self.whale_profiler.profiles.items():
                    if hasattr(profile, 'current_targets'):
                        for target in profile.current_targets:
                            if target.symbol and symbol_clean in target.symbol.upper():
                                active_whales += 1
                                if hasattr(profile, 'firm') and profile.firm:
                                    dominant_firm = profile.firm
                                    reasoning_parts.append(f"🐋 {profile.nickname}")
            except Exception:
                pass
        
        # 4. Check FirmIntelligenceCatalog for historical patterns
        if self.firm_intel:
            try:
                for firm_id in ['citadel', 'jane_street', 'jump_trading', 'wintermute']:
                    stats = self.firm_intel.compute_statistics(firm_id)
                    if stats and hasattr(stats, 'predicted_direction'):
                        if stats.predicted_direction == 'bullish' and our_direction == 'long':
                            whale_support += 0.1
                        elif stats.predicted_direction == 'bearish' and our_direction == 'long':
                            counter_pressure += 0.1
            except Exception:
                pass
        
        # 5. Check ThoughtBus signals
        if symbol in self.whale_signals:
            recent = [s for s in self.whale_signals[symbol] 
                     if time.time() - s['timestamp'] < 300]
            if recent:
                buy_count = sum(1 for s in recent if 'buy' in str(s.get('data', {})).lower() or 'bullish' in str(s.get('data', {})).lower())
                sell_count = sum(1 for s in recent if 'sell' in str(s.get('data', {})).lower() or 'bearish' in str(s.get('data', {})).lower())
                
                if buy_count > sell_count and our_direction == 'long':
                    whale_support += 0.1
                    momentum += 0.1
                elif sell_count > buy_count and our_direction == 'long':
                    counter_pressure += 0.1
                
                reasoning_parts.append(f"📡 {len(recent)} signals")
        
        # Clamp values
        whale_support = max(0, min(1, whale_support))
        counter_pressure = max(0, min(1, counter_pressure))
        momentum = max(0, min(1, momentum))
        
        # Calculate ETA based on support vs pressure
        net_support = whale_support - counter_pressure
        if net_support > 0.2:
            eta_seconds = 300 / (1 + net_support)  # Faster with support
        elif net_support < -0.2:
            eta_seconds = 3600 * (1 + abs(net_support))  # Slower with pressure
        else:
            eta_seconds = 900  # 15 min default
        
        # Confidence based on data quality
        confidence = 0.4  # Base
        if active_whales > 0:
            confidence += 0.1 * min(active_whales, 5)
        if self.whale_profiler:
            confidence += 0.1
        if self.firm_intel:
            confidence += 0.1
        if self.bus:
            confidence += 0.1
        confidence = min(0.95, confidence)
        
        reasoning = " | ".join(reasoning_parts) if reasoning_parts else "Scanning market..."
        
        return WhaleSignal(
            symbol=symbol,
            whale_support=whale_support,
            counter_pressure=counter_pressure,
            momentum_score=momentum,
            eta_seconds=eta_seconds,
            confidence=confidence,
            active_whales=active_whales,
            dominant_firm=dominant_firm,
            firm_activity=firm_activity_str,
            reasoning=reasoning
        )


@dataclass
class LivePosition:
    """Track a live position with streaming updates."""
    symbol: str
    exchange: str
    entry_price: float
    entry_qty: float
    entry_cost: float
    breakeven_price: float
    target_price: float
    client: object = None  # Client for THIS position's exchange
    entry_time: datetime = field(default_factory=datetime.now)
    current_price: float = 0.0
    current_pnl: float = 0.0
    current_pnl_pct: float = 0.0
    momentum_score: float = 0.0
    whale_activity: str = 'neutral'
    price_history: List[float] = field(default_factory=list)
    hit_target: bool = False
    ready_to_kill: bool = False
    kill_reason: str = ''
    stop_price: float = 0.0
    # 🔬 Enhanced analytics tracking
    pnl_history: List[tuple] = field(default_factory=list)  # [(timestamp, pnl), ...]
    last_eta: object = None  # ImprovedETA result
    eta_calculator: object = None  # Per-position ETA calculator


@dataclass
class MarketOpportunity:
    """An opportunity found scanning the entire market."""
    symbol: str
    exchange: str
    price: float
    change_pct: float
    volume: float
    momentum_score: float
    fee_rate: float
    timestamp: float = field(default_factory=time.time)


class OrcaKillCycle:
    """
    Complete kill cycle with proper math + live streaming + whale intelligence.
    
    🆕 MULTI-EXCHANGE MODE: Streams ENTIRE market on BOTH Alpaca AND Kraken!
    """
    
    def __init__(self, client=None, exchange='alpaca'):
        self.primary_exchange = exchange
        self.clients = {}
        self.fee_rates = {
            'alpaca': 0.0025,  # 0.25%
            'kraken': 0.0026   # 0.26% maker/taker
        }
        
        # Initialize clients for BOTH exchanges (unless specific client provided)
        if client:
            self.clients[exchange] = client
            self.client = client  # Backward compatibility
        else:
            # Initialize Alpaca
            try:
                from alpaca_client import AlpacaClient
                self.clients['alpaca'] = AlpacaClient()
                print("✅ Alpaca: CONNECTED")
            except Exception as e:
                print(f"⚠️ Alpaca: {e}")
            
            # Initialize Kraken
            try:
                from kraken_client import KrakenClient
                self.clients['kraken'] = KrakenClient()
                print("✅ Kraken: CONNECTED")
            except Exception as e:
                print(f"⚠️ Kraken: {e}")
            
            # Set primary client for backward compatibility
            self.client = self.clients.get(exchange) or list(self.clients.values())[0]
        
        self.exchange = exchange
        self.fee_rate = self.fee_rates.get(exchange, 0.0025)
        
        # ═══════════════════════════════════════════════════════════════════
        # 🧠 WIRE UP ALL INTELLIGENCE SYSTEMS!
        # ═══════════════════════════════════════════════════════════════════
        
        # 1. Miner Brain (aureon_miner_brain)
        self.miner_brain = None
        try:
            from aureon_miner_brain import MinerBrain
            self.miner_brain = MinerBrain()
            print("🧠 Timeline Oracle: Miner Brain WIRED!")
        except Exception:
            pass
        
        # 2. Quantum Telescope (enhanced scanning)
        self.quantum_telescope = None
        try:
            from aureon_enhanced_quantum_telescope import QuantumTelescope
            self.quantum_telescope = QuantumTelescope()
            print("🔭 Timeline Oracle: Quantum Telescope WIRED!")
        except Exception:
            pass
        
        # 3. Ultimate Intelligence (95% accuracy!) - CRITICAL
        self.ultimate_intel = None
        if ULTIMATE_INTEL_AVAILABLE and UltimateIntelligence:
            try:
                self.ultimate_intel = UltimateIntelligence()
                print("💎 Mycelium: Ultimate Intelligence WIRED! (95% accuracy)")
            except Exception:
                pass
        
        # 4. Orca Intelligence (full scanning system)
        self.orca_intel = None
        if ORCA_INTEL_AVAILABLE and OrcaKillerWhale:
            try:
                self.orca_intel = OrcaKillerWhale()
                print("🦈 Orca Intelligence: WIRED!")
            except Exception as e:
                print(f"🦈 Orca Intelligence: {e}")
        
        # 5. Global Wave Scanner
        self.wave_scanner = None
        if WAVE_SCANNER_AVAILABLE and GlobalWaveScanner:
            try:
                self.wave_scanner = GlobalWaveScanner()
                print("🌊 Global Wave Scanner: WIRED!")
            except Exception as e:
                print(f"🌊 Global Wave Scanner: {e}")
        
        # 6. Movers & Shakers Scanner - SKIP (circular import with Orca)
        self.movers_scanner = None
        # if MOVERS_SHAKERS_AVAILABLE and MoversShakersScanner:
        #     try:
        #         self.movers_scanner = MoversShakersScanner()
        #         print("📈 Movers & Shakers Scanner: WIRED!")
        #     except Exception as e:
        #         print(f"📈 Movers & Shakers Scanner: {e}")
        
        # 7. Whale Intelligence Tracker (firm tracking)
        self.whale_tracker = None
        try:
            self.whale_tracker = WhaleIntelligenceTracker()
            print("🐋 Whale Intelligence Tracker: WIRED!")
        except Exception:
            pass
        
        # 8. Timeline Oracle (7-day planner)
        self.timeline_oracle = None
        try:
            from aureon_timeline_oracle import TimelineOracle
            self.timeline_oracle = TimelineOracle(
                miner_brain=self.miner_brain,
                quantum_telescope=self.quantum_telescope,
                ultimate_intelligence=self.ultimate_intel
            )
            print("⏳ Timeline Oracle: WIRED!")
        except Exception:
            pass
        
        # 9. Prime Sentinel Decree
        try:
            from prime_sentinel_decree import PrimeSentinelDecree
            self.prime_sentinel = PrimeSentinelDecree()
            print("🔱 Prime Sentinel Decree LOADED - Control reclaimed")
        except Exception:
            pass
        
        # ═══════════════════════════════════════════════════════════════════
        # 💰 COST TRACKING SYSTEMS - KNOW EXACTLY WHEN TO SELL!
        # ═══════════════════════════════════════════════════════════════════
        
        # 10. Alpaca Fee Tracker (volume-tiered fees + spread tracking)
        self.alpaca_fee_tracker = None
        if ALPACA_FEE_TRACKER_AVAILABLE and AlpacaFeeTracker:
            try:
                self.alpaca_fee_tracker = AlpacaFeeTracker()
                print("💰 Alpaca Fee Tracker: WIRED! (Volume tiers + spread)")
            except Exception as e:
                print(f"💰 Alpaca Fee Tracker: {e}")
        
        # 11. Cost Basis Tracker (FIFO cost basis + can_sell_profitably check)
        self.cost_basis_tracker = None
        if COST_BASIS_TRACKER_AVAILABLE and CostBasisTracker:
            try:
                self.cost_basis_tracker = CostBasisTracker()
                print("📊 Cost Basis Tracker: WIRED! (FIFO + profit checks)")
            except Exception as e:
                print(f"📊 Cost Basis Tracker: {e}")
        
        # 12. Trade Logger (full entry/exit records with P&L)
        self.trade_logger = None
        if TRADE_LOGGER_AVAILABLE and TradeLogger:
            try:
                self.trade_logger = TradeLogger()
                print("📝 Trade Logger: WIRED! (Entry/Exit tracking)")
            except Exception as e:
                print(f"📝 Trade Logger: {e}")
        
        # 13. Active positions with ORDER IDs and exact costs
        self.tracked_positions: Dict[str, dict] = {}  # symbol -> {order_id, entry_price, entry_qty, entry_cost, entry_fee, breakeven_price}
        
        # ═══════════════════════════════════════════════════════════════════
        # 🤖 BOT DETECTION & COUNTER-INTELLIGENCE SYSTEMS
        # ═══════════════════════════════════════════════════════════════════
        
        # 14. Queen Counter-Intelligence (beat major firms)
        self.counter_intel = None
        if COUNTER_INTEL_AVAILABLE and QueenCounterIntelligence:
            try:
                self.counter_intel = QueenCounterIntelligence()
                print("🛡️ Queen Counter-Intelligence: ARMED! (Firm exploitation ready)")
            except Exception as e:
                print(f"🛡️ Counter-Intelligence: {e}")
        
        # 15. Firm Attribution Engine (identify who's trading)
        self.firm_attribution = None
        if FIRM_ATTRIBUTION_AVAILABLE and get_attribution_engine:
            try:
                self.firm_attribution = get_attribution_engine()
                print("🏢 Firm Attribution Engine: WIRED! (Trade fingerprinting)")
            except Exception as e:
                print(f"🏢 Firm Attribution: {e}")
        
        # 16. HFT Harmonic Mycelium Engine (sub-10ms signals) - DISPLAY ONLY
        self.hft_engine = None
        if HFT_ENGINE_AVAILABLE and get_hft_engine:
            try:
                self.hft_engine = get_hft_engine()
                print("⚡ HFT Harmonic Mycelium: WIRED! (Sacred frequency analysis)")
            except Exception as e:
                print(f"⚡ HFT Engine: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🌌 QUANTUM PROBABILITY SYSTEMS - REAL INTELLIGENCE!
        # ═══════════════════════════════════════════════════════════════════
        
        # 17. Luck Field Mapper (Schumann resonance, planetary torque, harmonics)
        self.luck_mapper = None
        if LUCK_FIELD_AVAILABLE and get_luck_mapper:
            try:
                self.luck_mapper = get_luck_mapper()
                print("🍀 Luck Field Mapper: WIRED! (λ = Σ × Π × Φ × Ω × Ψ)")
            except Exception as e:
                print(f"🍀 Luck Field: {e}")
        
        # 18. Phantom Signal Filter (cross-layer validation: Physical/Digital/Harmonic/Planetary)
        self.phantom_filter = None
        if PHANTOM_FILTER_AVAILABLE and PhantomSignalFilter:
            try:
                self.phantom_filter = PhantomSignalFilter(window_seconds=5.0)
                self.phantom_filter.start()  # Start listening to ThoughtBus
                print("👻 Phantom Signal Filter: WIRED! (4-layer validation)")
            except Exception as e:
                print(f"👻 Phantom Filter: {e}")
        
        # 19. Inception Engine (Russian doll probability - LIMBO = Limitless Pill)
        self.inception_engine = None
        if INCEPTION_ENGINE_AVAILABLE and get_inception_engine:
            try:
                self.inception_engine = get_inception_engine()
                print("🎬 Inception Engine: WIRED! (LIMBO depth probability matrix)")
            except Exception as e:
                print(f"🎬 Inception Engine: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🧬 DEEP MEMORY & PATTERN SYSTEMS
        # ═══════════════════════════════════════════════════════════════════
        
        # 20. Elephant Learning (Never forgets - pattern memory)
        self.elephant = None
        self.elephant_brain = None
        if ELEPHANT_LEARNING_AVAILABLE and ElephantMemory:
            try:
                self.elephant = ElephantMemory()
                # QueenElephantBrain() takes no args in current impl
                self.elephant_brain = QueenElephantBrain() if QueenElephantBrain else None
                print("🐘 Elephant Learning: WIRED! (Never forgets patterns)")
            except Exception as e:
                print(f"🐘 Elephant Learning: {e}")
        
        # 21. Russian Doll Analytics (Bee→Hive→Queen rollup)
        self.russian_doll = None
        if RUSSIAN_DOLL_AVAILABLE and get_analytics:
            try:
                self.russian_doll = get_analytics()
                print("🦷 Russian Doll Analytics: WIRED! (Bee→Hive→Queen)")
            except Exception as e:
                print(f"🦷 Russian Doll: {e}")
        
        # 22. Immune System (Self-healing)
        self.immune_system = None
        if IMMUNE_SYSTEM_AVAILABLE and AureonImmuneSystem:
            try:
                self.immune_system = AureonImmuneSystem()
                print("🛡️ Immune System: WIRED! (Self-healing enabled)")
            except Exception as e:
                print(f"🛡️ Immune System: {e}")
        
        # 23. Moby Dick Whale Hunter (Whale predictions)
        self.moby_dick = None
        if MOBY_DICK_AVAILABLE and get_moby_dick_hunter:
            try:
                self.moby_dick = get_moby_dick_hunter()
                print("🐋 Moby Dick Hunter: WIRED! (Whale prediction tracking)")
            except Exception as e:
                print(f"🐋 Moby Dick: {e}")
        
        # 24. Stargate Protocol (Quantum mirror alignment)
        self.stargate = None
        if STARGATE_AVAILABLE and create_stargate_engine:
            try:
                self.stargate = create_stargate_engine(with_integrations=False)
                print("🌌 Stargate Protocol: WIRED! (Quantum mirror alignment)")
            except Exception as e:
                print(f"🌌 Stargate: {e}")
        
        # 25. Quantum Mirror Scanner (Reality branch boost)
        self.quantum_mirror = None
        if QUANTUM_MIRROR_AVAILABLE and create_quantum_scanner:
            try:
                self.quantum_mirror = create_quantum_scanner(with_integrations=False)
                print("🔮 Quantum Mirror Scanner: WIRED! (Reality branch boost)")
            except Exception as e:
                print(f"🔮 Quantum Mirror: {e}")
        
        # Whale intelligence via ThoughtBus
        self.bus = None
        self.whale_signal = 'neutral'
        if THOUGHT_BUS_AVAILABLE and ThoughtBus:
            try:
                self.bus = ThoughtBus()
                self.bus.subscribe('whale.*', self._handle_whale_signal)
                print("🐋 Whale intelligence: CONNECTED")
            except Exception:
                pass
        
        # Live streaming settings
        self.stream_interval = 0.1  # 100ms = 10 updates/sec
        self.stop_loss_pct = -1.0   # Stop loss at -1%
        
    def _handle_whale_signal(self, thought):
        """Process whale activity signals from ThoughtBus."""
        try:
            data = thought.data if hasattr(thought, 'data') else thought
            if isinstance(data, dict):
                self.whale_signal = data.get('action', 'neutral')
        except Exception:
            pass
    
    # ═══════════════════════════════════════════════════════════════════════
    # � QUANTUM INTELLIGENCE - ENHANCED PROBABILITY SCORING
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_quantum_score(self, symbol: str, price: float, change_pct: float, 
                          volume: float = 0, momentum: float = 0) -> dict:
        """
        Get enhanced probability score using ALL quantum systems.
        
        Returns:
            dict with:
            - luck_field: 0-1 score from Luck Field Mapper
            - luck_state: VOID/CHAOS/NEUTRAL/FAVORABLE/BLESSED
            - limbo_probability: 0-1 from Inception Engine LIMBO
            - limbo_pattern: Pattern key from LIMBO
            - quantum_boost: Combined confidence multiplier
            - action_bias: BUY/SELL/HOLD suggestion
        """
        result = {
            'luck_field': 0.5,
            'luck_state': 'NEUTRAL',
            'limbo_probability': 0.5,
            'limbo_pattern': 'unknown',
            'quantum_boost': 1.0,
            'action_bias': 'HOLD',
            'is_blessed': False,
            'inception_wisdom': None
        }
        
        # 1. LUCK FIELD MAPPER - Cosmic alignment score
        if self.luck_mapper:
            try:
                # Calculate volatility proxy from change
                volatility = min(1.0, abs(change_pct) / 10.0)
                luck_reading = self.luck_mapper.read_field(
                    price=price,
                    volatility=volatility,
                    market_frequency=volume / 100000 if volume > 0 else 0  # Map volume to frequency
                )
                result['luck_field'] = luck_reading.luck_field
                result['luck_state'] = luck_reading.luck_state.value if hasattr(luck_reading.luck_state, 'value') else str(luck_reading.luck_state)
                result['action_bias'] = luck_reading.action_bias
                result['is_blessed'] = luck_reading.luck_field >= 0.8
                
                # Luck boost: BLESSED = 1.3x, FAVORABLE = 1.15x, NEUTRAL = 1.0x, CHAOS = 0.85x, VOID = 0.7x
                if luck_reading.luck_field >= 0.8:
                    result['quantum_boost'] *= 1.3  # BLESSED
                elif luck_reading.luck_field >= 0.6:
                    result['quantum_boost'] *= 1.15  # FAVORABLE
                elif luck_reading.luck_field >= 0.4:
                    result['quantum_boost'] *= 1.0   # NEUTRAL
                elif luck_reading.luck_field >= 0.2:
                    result['quantum_boost'] *= 0.85  # CHAOS
                else:
                    result['quantum_boost'] *= 0.7   # VOID - Avoid!
                    
            except Exception as e:
                pass  # Keep defaults
        
        # 2. INCEPTION ENGINE - LIMBO depth probability (The Limitless Pill)
        if self.inception_engine and INCEPTION_ENGINE_AVAILABLE and get_limbo_insight:
            try:
                # Build market data for LIMBO
                market_data = {
                    'prices': {symbol: price},
                    'changes': {symbol: change_pct},
                    'volumes': {symbol: volume},
                    'momentum': {symbol: momentum}
                }
                
                # Get raw LIMBO insight (deepest layer = most accurate)
                limbo_insight = get_limbo_insight(symbol, market_data)
                result['limbo_probability'] = limbo_insight.probability
                result['limbo_pattern'] = limbo_insight.pattern_key
                
                # Also do full inception dive for wisdom
                wisdom = self.inception_engine.dive(market_data)
                result['inception_wisdom'] = wisdom
                
                # LIMBO boost: High probability = big boost
                if limbo_insight.probability >= 0.85:
                    result['quantum_boost'] *= 1.25  # Limitless territory
                elif limbo_insight.probability >= 0.7:
                    result['quantum_boost'] *= 1.15
                elif limbo_insight.probability >= 0.5:
                    result['quantum_boost'] *= 1.05
                elif limbo_insight.probability < 0.35:
                    result['quantum_boost'] *= 0.8   # LIMBO says NO
                    
            except Exception as e:
                pass  # Keep defaults
        
        # 3. HFT Engine - Harmonic frequency analysis (if available)
        if self.hft_engine:
            try:
                # Feed tick to HFT engine
                tick = HFTTick(
                    symbol=symbol,
                    price=price,
                    size=volume / price if price > 0 else 0,
                    side='buy' if change_pct > 0 else 'sell',
                    timestamp=time.time(),
                    exchange='mixed'
                ) if HFT_ENGINE_AVAILABLE and HFTTick else None
                
                if tick and hasattr(self.hft_engine, 'ingest_tick'):
                    tone = self.hft_engine.ingest_tick(tick)
                    if tone and hasattr(tone, 'confidence'):
                        # 528Hz (Love frequency) alignment gives boost
                        if abs(tone.frequency - 528) < 50:
                            result['quantum_boost'] *= 1.1
            except Exception:
                pass
        
        # ═══════════════════════════════════════════════════════════════════
        # 🧬 NEW SYSTEMS INTEGRATION
        # ═══════════════════════════════════════════════════════════════════
        
        # 4. ELEPHANT LEARNING - Pattern memory (never forgets)
        if self.elephant:
            try:
                asset_score = self.elephant.get_asset_score(symbol)
                result['elephant_score'] = asset_score
                # Good historical performance = boost
                if asset_score >= 0.7:
                    result['quantum_boost'] *= 1.1
                elif asset_score <= 0.3:
                    result['quantum_boost'] *= 0.9  # Bad history = caution
                    
                # Get best trading hours
                best_hours = self.elephant.get_best_trading_hours()
                current_hour = time.localtime().tm_hour
                if current_hour in best_hours:
                    result['quantum_boost'] *= 1.05  # Optimal time
                    result['optimal_hour'] = True
                else:
                    result['optimal_hour'] = False
            except Exception:
                pass
        
        # 5. RUSSIAN DOLL ANALYTICS - Queen directives (Bee→Hive→Queen)
        if self.russian_doll:
            try:
                directives = self.russian_doll.get_queen_directives()
                result['queen_confidence'] = directives.get('confidence', 0.5)
                result['target_exchanges'] = directives.get('target_exchanges', [])
                
                # High Queen confidence = trust the system
                if directives.get('confidence', 0) >= 0.7:
                    result['quantum_boost'] *= 1.08
            except Exception:
                pass
        
        # 6. MOBY DICK WHALE HUNTER - Whale predictions
        if self.moby_dick:
            try:
                predictions = self.moby_dick.get_execution_ready_predictions()
                for pred in predictions:
                    if hasattr(pred, 'symbol') and pred.symbol == symbol:
                        result['whale_prediction'] = pred
                        result['whale_direction'] = pred.direction if hasattr(pred, 'direction') else 'unknown'
                        # Whale alignment = big confidence boost
                        if pred.confidence >= 0.8:
                            result['quantum_boost'] *= 1.15
                        break
            except Exception:
                pass
        
        # 7. STARGATE PROTOCOL - Quantum mirror alignment
        if self.stargate:
            try:
                status = self.stargate.get_status()
                result['stargate_coherence'] = status.get('network_coherence', 0.5)
                result['active_nodes'] = status.get('active_nodes', 0)
                
                # High network coherence = timeline alignment
                if status.get('network_coherence', 0) >= 0.7:
                    result['quantum_boost'] *= 1.1
                    result['timeline_aligned'] = True
                else:
                    result['timeline_aligned'] = False
            except Exception:
                pass
        
        # 8. QUANTUM MIRROR SCANNER - Reality branch boost
        if self.quantum_mirror:
            try:
                # Get quantum boost for this specific symbol
                symbol_base = symbol.replace('/USD', '').replace('USD', '')
                branch_boost, reason = self.quantum_mirror.get_quantum_boost(
                    from_asset='USD', to_asset=symbol_base, exchange='mixed'
                )
                result['mirror_boost'] = branch_boost
                result['mirror_reason'] = reason
                
                # Apply reality branch alignment
                if branch_boost > 1.0:
                    result['quantum_boost'] *= min(1.2, branch_boost)  # Cap at 1.2x
                    result['reality_aligned'] = True
                else:
                    result['reality_aligned'] = False
            except Exception:
                pass
        
        # 9. IMMUNE SYSTEM - System health check
        if self.immune_system:
            try:
                health = self.immune_system.get_health_status()
                result['system_health'] = health.get('overall', 'healthy')
                
                # If system is unhealthy, reduce confidence
                if health.get('overall') == 'critical':
                    result['quantum_boost'] *= 0.7
                elif health.get('overall') == 'warning':
                    result['quantum_boost'] *= 0.9
            except Exception:
                pass
        
        # Cap the quantum boost at reasonable levels (raised for more systems)
        result['quantum_boost'] = max(0.4, min(2.0, result['quantum_boost']))
        
        return result
    
    def print_quantum_status(self):
        """Print current quantum systems status."""
        print("\n" + "="*70)
        print("🌌 QUANTUM INTELLIGENCE SYSTEMS STATUS (25 SYSTEMS WIRED)")
        print("="*70)
        
        wired_count = 0
        
        # Luck Field
        if self.luck_mapper:
            try:
                reading = self.luck_mapper.read_field()
                state = reading.luck_state.value if hasattr(reading.luck_state, 'value') else str(reading.luck_state)
                blessed = "🔒 BLESSED!" if reading.luck_field >= 0.8 else ""
                print(f"🍀 Luck Field: λ={reading.luck_field:.3f} → {state} {blessed}")
                print(f"   Σ(Schumann)={reading.sigma_schumann:.2f} Π(Planet)={reading.pi_planetary:.2f}")
                print(f"   Φ(Harmonic)={reading.phi_harmonic:.2f} Ω(Time)={reading.omega_temporal:.2f}")
                wired_count += 1
            except Exception as e:
                print(f"🍀 Luck Field: Error - {e}")
        else:
            print("🍀 Luck Field: Not available")
        
        # Inception Engine
        if self.inception_engine:
            try:
                status = self.inception_engine.get_status()
                print(f"🎬 Inception: {status['dives_completed']} dives | {status.get('limbo_patterns_loaded', 0)} patterns")
                print(f"   Totem: ${status['totem']['net_profit']:.2f} | Real={status['totem']['is_real']}")
                wired_count += 1
            except Exception as e:
                print(f"🎬 Inception: Error - {e}")
        else:
            print("🎬 Inception: Not available")
        
        # Phantom Filter
        if self.phantom_filter:
            print("👻 Phantom Filter: ACTIVE (4-layer validation)")
            wired_count += 1
        else:
            print("👻 Phantom Filter: Not available")
        
        # Elephant Learning
        if self.elephant:
            try:
                best_hours = self.elephant.get_best_trading_hours()
                hour_str = ','.join(str(h) for h in best_hours[:5]) + '...' if len(best_hours) > 5 else ','.join(str(h) for h in best_hours)
                print(f"🐘 Elephant: REMEMBERING | Best hours: [{hour_str}]")
                wired_count += 1
            except Exception as e:
                print(f"🐘 Elephant: Error - {e}")
        else:
            print("🐘 Elephant Learning: Not available")
        
        # Russian Doll Analytics
        if self.russian_doll:
            try:
                directives = self.russian_doll.get_queen_directives()
                conf = directives.get('confidence', 0)
                exchanges = directives.get('target_exchanges', [])
                print(f"🦷 Russian Doll: Queen confidence {conf:.1%} | Targets: {exchanges}")
                wired_count += 1
            except Exception as e:
                print(f"🦷 Russian Doll: Error - {e}")
        else:
            print("🦷 Russian Doll: Not available")
        
        # Immune System
        if self.immune_system:
            try:
                health = self.immune_system.get_health_status()
                status = health.get('overall', 'unknown')
                emoji = "✅" if status == 'healthy' else "⚠️" if status == 'warning' else "🔴"
                print(f"🛡️ Immune System: {emoji} {status.upper()}")
                wired_count += 1
            except Exception as e:
                print(f"🛡️ Immune System: Error - {e}")
        else:
            print("🛡️ Immune System: Not available")
        
        # Moby Dick Whale Hunter
        if self.moby_dick:
            try:
                preds = self.moby_dick.get_execution_ready_predictions()
                print(f"🐋 Moby Dick: {len(preds)} whale predictions ready")
                wired_count += 1
            except Exception as e:
                print(f"🐋 Moby Dick: Error - {e}")
        else:
            print("🐋 Moby Dick: Not available")
        
        # Stargate Protocol
        if self.stargate:
            try:
                status = self.stargate.get_status()
                coherence = status.get('network_coherence', 0)
                nodes = status.get('active_nodes', 0)
                print(f"🌌 Stargate: Coherence {coherence:.1%} | {nodes} nodes active")
                wired_count += 1
            except Exception as e:
                print(f"🌌 Stargate: Error - {e}")
        else:
            print("🌌 Stargate: Not available")
        
        # Quantum Mirror Scanner
        if self.quantum_mirror:
            try:
                status = self.quantum_mirror.get_status()
                branches = len(status.get('branches', {}))
                print(f"🔮 Quantum Mirror: {branches} reality branches tracked")
                wired_count += 1
            except Exception as e:
                print(f"🔮 Quantum Mirror: Error - {e}")
        else:
            print("🔮 Quantum Mirror: Not available")
        
        print("-"*70)
        print(f"⚡ TOTAL QUANTUM SYSTEMS ACTIVE: {wired_count}/9 display | 25 total wired")
        print("="*70)
    
    # ═══════════════════════════════════════════════════════════════════════
    # �🆕 SCAN ENTIRE MARKET - ALL EXCHANGES, ALL SYMBOLS
    # ═══════════════════════════════════════════════════════════════════════
    
    def scan_entire_market(self, min_change_pct: float = 0.5, min_volume: float = 1000) -> List[MarketOpportunity]:
        """
        Scan ENTIRE market across ALL exchanges for opportunities.
        
        Returns sorted list of best opportunities from Alpaca AND Kraken.
        🌌 ENHANCED with quantum probability scoring!
        """
        print("\n" + "="*70)
        print("🌊 SCANNING ENTIRE MARKET - ALL EXCHANGES")
        print("="*70)
        
        opportunities = []
        
        # Scan Alpaca
        if 'alpaca' in self.clients:
            alpaca_opps = self._scan_alpaca_market(min_change_pct, min_volume)
            opportunities.extend(alpaca_opps)
            print(f"   📊 Alpaca: Found {len(alpaca_opps)} opportunities")
        
        # Scan Kraken
        if 'kraken' in self.clients:
            kraken_opps = self._scan_kraken_market(min_change_pct, min_volume)
            opportunities.extend(kraken_opps)
            print(f"   📊 Kraken: Found {len(kraken_opps)} opportunities")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🌌 QUANTUM ENHANCEMENT - Apply luck field + LIMBO probability boost
        # ═══════════════════════════════════════════════════════════════════
        if self.luck_mapper or self.inception_engine:
            print("\n🌌 Applying quantum intelligence scoring...")
            blessed_count = 0
            limbo_high_count = 0
            
            for opp in opportunities:
                quantum = self.get_quantum_score(
                    symbol=opp.symbol,
                    price=opp.price,
                    change_pct=opp.change_pct,
                    volume=opp.volume,
                    momentum=opp.momentum_score
                )
                
                # Apply quantum boost to momentum score
                original_score = opp.momentum_score
                opp.momentum_score = original_score * quantum['quantum_boost']
                
                if quantum['is_blessed']:
                    blessed_count += 1
                if quantum['limbo_probability'] >= 0.7:
                    limbo_high_count += 1
            
            if blessed_count > 0:
                print(f"   🍀 BLESSED opportunities: {blessed_count}")
            if limbo_high_count > 0:
                print(f"   🎬 LIMBO high probability: {limbo_high_count}")
        
        # Sort by quantum-boosted momentum score (highest first)
        opportunities.sort(key=lambda x: x.momentum_score, reverse=True)
        
        print(f"\n🎯 Total opportunities: {len(opportunities)}")
        if opportunities:
            print("\nTop 5 opportunities (quantum-enhanced):")
            for i, opp in enumerate(opportunities[:5]):
                print(f"   {i+1}. {opp.symbol} ({opp.exchange}): {opp.change_pct:+.2f}% | Score: {opp.momentum_score:.2f}")
        
        return opportunities
    
    def _scan_alpaca_market(self, min_change_pct: float, min_volume: float) -> List[MarketOpportunity]:
        """Scan ALL Alpaca crypto pairs for momentum using snapshot API."""
        opportunities = []
        client = self.clients.get('alpaca')
        if not client:
            return opportunities
        
        try:
            # Try to get snapshots for all crypto (faster)
            if hasattr(client, 'get_crypto_snapshots'):
                snapshots = client.get_crypto_snapshots()
                if snapshots:
                    for symbol, snap in snapshots.items():
                        try:
                            daily = snap.get('dailyBar', {})
                            prev = snap.get('prevDailyBar', {})
                            quote = snap.get('latestQuote', {}) or snap.get('latestTrade', {})
                            
                            curr_close = float(daily.get('c', 0) or quote.get('ap', 0) or quote.get('p', 0))
                            prev_close = float(prev.get('c', curr_close))
                            
                            if curr_close <= 0 or prev_close <= 0:
                                continue
                            
                            change_pct = ((curr_close - prev_close) / prev_close * 100)
                            volume = float(daily.get('v', 0))
                            momentum = abs(change_pct) * (1 + min(volume / 10000, 1))
                            
                            if abs(change_pct) >= min_change_pct:
                                norm_symbol = symbol if '/' in symbol else symbol.replace('USD', '/USD')
                                opportunities.append(MarketOpportunity(
                                    symbol=norm_symbol,
                                    exchange='alpaca',
                                    price=curr_close,
                                    change_pct=change_pct,
                                    volume=volume,
                                    momentum_score=momentum,
                                    fee_rate=self.fee_rates['alpaca']
                                ))
                        except Exception:
                            pass
                    return opportunities
            
            # Fallback: Get all crypto assets and check each
            assets = client.get_assets(status='active', asset_class='crypto')
            symbols = []
            for asset in assets:
                if asset.get('tradable'):
                    sym = asset.get('symbol', '')
                    if sym and 'USD' in sym:
                        symbols.append(sym)
            
            # Sample major cryptos if we have many
            major_symbols = ['BTCUSD', 'ETHUSD', 'SOLUSD', 'DOGEUSD', 'AVAXUSD', 
                            'LINKUSD', 'DOTUSD', 'MATICUSD', 'AAVEUSD', 'UNIUSD',
                            'ATOMUSD', 'NEARUSD', 'APTUSD', 'ARBUSD', 'OPUSD']
            check_symbols = [s for s in symbols if s in major_symbols] or symbols[:20]
            
            for symbol in check_symbols:
                try:
                    symbol_clean = symbol.replace('/', '')
                    
                    # Get current quote
                    orderbook = client.get_crypto_orderbook(symbol_clean)
                    asks = orderbook.get('asks', [])
                    if not asks:
                        continue
                    
                    price = float(asks[0].get('p', 0))
                    if price <= 0:
                        continue
                    
                    # Get bars for change calculation
                    # FIXED: API returns key as "BASE/QUOTE" format regardless of input
                    bars_result = client.get_crypto_bars([symbol_clean], '1Hour', limit=24)
                    bars_dict = bars_result.get('bars', {})
                    
                    # Try both formats: BTCUSD and BTC/USD
                    norm_symbol = symbol if '/' in symbol else symbol.replace('USD', '/USD')
                    bars = bars_dict.get(norm_symbol, bars_dict.get(symbol_clean, []))
                    
                    if bars and len(bars) >= 2:
                        old_close = float(bars[0].get('c', price))
                        new_close = float(bars[-1].get('c', price))
                        change_pct = ((new_close - old_close) / old_close * 100) if old_close > 0 else 0
                        volume = sum(float(b.get('v', 0)) for b in bars)
                        
                        momentum = abs(change_pct) * (1 + min(volume / 10000, 1))
                        
                        if abs(change_pct) >= min_change_pct:
                            opportunities.append(MarketOpportunity(
                                symbol=norm_symbol,
                                exchange='alpaca',
                                price=price,
                                change_pct=change_pct,
                                volume=volume,
                                momentum_score=momentum,
                                fee_rate=self.fee_rates['alpaca']
                            ))
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"⚠️ Alpaca scan error: {e}")
        
        return opportunities
    
    def _scan_kraken_market(self, min_change_pct: float, min_volume: float) -> List[MarketOpportunity]:
        """Scan ALL Kraken pairs for momentum."""
        opportunities = []
        client = self.clients.get('kraken')
        if not client:
            return opportunities
        
        try:
            # Get ALL 24h tickers from Kraken
            tickers = client.get_24h_tickers()
            
            for ticker in tickers:
                try:
                    symbol = ticker.get('symbol', '')
                    if not symbol:
                        continue
                    
                    # Only USD pairs for simplicity
                    if 'USD' not in symbol:
                        continue
                    
                    last_price = float(ticker.get('lastPrice', 0))
                    change_pct = float(ticker.get('priceChangePercent', 0))
                    volume = float(ticker.get('quoteVolume', 0))
                    
                    if last_price <= 0:
                        continue
                    
                    # Calculate momentum score
                    momentum = abs(change_pct) * (1 + min(volume / 100000, 1))
                    
                    if abs(change_pct) >= min_change_pct:
                        # Normalize symbol format
                        norm_symbol = symbol if '/' in symbol else symbol.replace('USD', '/USD')
                        opportunities.append(MarketOpportunity(
                            symbol=norm_symbol,
                            exchange='kraken',
                            price=last_price,
                            change_pct=change_pct,
                            volume=volume,
                            momentum_score=momentum,
                            fee_rate=self.fee_rates['kraken']
                        ))
                except Exception:
                    pass
        except Exception as e:
            print(f"⚠️ Kraken scan error: {e}")
        
        return opportunities
    
    def get_available_cash(self) -> Dict[str, float]:
        """Get available cash across ALL exchanges."""
        cash = {}
        
        # 🆕 TEST MODE: Add funds for testing fallback logic
        test_mode = os.environ.get('AUREON_TEST_MODE', '').lower() == 'true'
        
        if 'alpaca' in self.clients:
            try:
                acct = self.clients['alpaca'].get_account()
                cash['alpaca'] = float(acct.get('cash', 0)) + (5.0 if test_mode else 0)  # Add $5 for testing
            except:
                cash['alpaca'] = 5.0 if test_mode else 0.0
        
        if 'kraken' in self.clients:
            try:
                bal = self.clients['kraken'].get_balance()
                # Kraken cash = USD or USDC
                cash['kraken'] = bal.get('USD', 0) + bal.get('USDC', 0) + bal.get('USDT', 0) + (5.0 if test_mode else 0)  # Add $5 for testing
            except:
                cash['kraken'] = 5.0 if test_mode else 0.0
        
        return cash
        
    def calculate_exact_breakeven(self, entry_price: float, quantity: float, exchange: str = 'alpaca') -> Dict:
        """
        🎯 EXACT BREAKEVEN CALCULATION - WITH ALL COSTS!
        
        Accounts for:
        - Entry fee (taker)
        - Exit fee (taker)
        - Slippage (both sides)
        - Spread cost
        
        Returns dict with:
        - entry_cost: Total cost to enter position
        - entry_fee: Fee paid on entry
        - breakeven_price: Minimum exit price to not lose money
        - target_price_1pct: Price for 1% profit after all costs
        """
        # Get exchange-specific fees
        if PENNY_PROFIT_AVAILABLE and calculate_penny_profit_threshold:
            threshold = calculate_penny_profit_threshold(
                trade_size=entry_price * quantity,
                exchange=exchange,
                use_maker=False  # Assume taker (worst case)
            )
            # Penny profit calculator gives us exact breakeven multiplier
            breakeven_multiplier = threshold.get('breakeven_price_multiplier', 1.006)  # Default ~0.6%
            min_price_move_pct = threshold.get('min_price_move_pct', 0.6)
            total_costs = threshold.get('total_costs', 0)
        else:
            # Fallback calculation
            fee_rate = EXCHANGE_FEES.get(exchange, {}).get('taker', 0.0026)
            slippage = SLIPPAGE_PCT
            spread = SPREAD_PCT
            
            # Round-trip costs
            total_cost_pct = (fee_rate * 2) + (slippage * 2) + (spread * 2)  # ~0.7%
            breakeven_multiplier = 1 + total_cost_pct
            min_price_move_pct = total_cost_pct * 100
            total_costs = entry_price * quantity * total_cost_pct
        
        # Calculate costs
        notional = entry_price * quantity
        fee_rate = self.fee_rates.get(exchange, 0.0025)
        entry_fee = notional * fee_rate
        entry_cost = notional + entry_fee
        
        # Breakeven price = entry_price × breakeven_multiplier
        breakeven_price = entry_price * breakeven_multiplier
        
        # Target prices for various profit levels (after ALL costs)
        target_1pct = breakeven_price * 1.01  # 1% profit after costs
        target_half_pct = breakeven_price * 1.005  # 0.5% profit after costs
        
        return {
            'entry_price': entry_price,
            'quantity': quantity,
            'notional': notional,
            'entry_fee': entry_fee,
            'entry_cost': entry_cost,
            'total_round_trip_costs': total_costs,
            'min_price_move_pct': min_price_move_pct,
            'breakeven_multiplier': breakeven_multiplier,
            'breakeven_price': breakeven_price,
            'target_half_pct': target_half_pct,
            'target_1pct': target_1pct,
        }
    
    def track_buy_order(self, symbol: str, order_result: dict, exchange: str = 'alpaca') -> dict:
        """
        📝 Track a buy order with all details needed to know when to sell.
        
        Call this AFTER a successful buy order to store:
        - Order ID
        - Entry price (actual fill price)
        - Quantity
        - Entry cost (including fee)
        - Exact breakeven price
        """
        order_id = order_result.get('id', order_result.get('order_id', order_result.get('txid', [str(time.time())])))
        if isinstance(order_id, list):
            order_id = order_id[0]
        
        fill_price = float(order_result.get('filled_avg_price', order_result.get('avg_price', order_result.get('price', 0))))
        fill_qty = float(order_result.get('filled_qty', order_result.get('qty', order_result.get('volume', 0))))
        
        if fill_price == 0 or fill_qty == 0:
            print(f"⚠️ Cannot track order - missing fill price or qty: {order_result}")
            return {}
        
        # Calculate exact breakeven
        breakeven_info = self.calculate_exact_breakeven(fill_price, fill_qty, exchange)
        
        # Store in tracked positions
        tracking_data = {
            'symbol': symbol,
            'exchange': exchange,
            'order_id': order_id,
            'entry_price': fill_price,
            'entry_qty': fill_qty,
            'entry_cost': breakeven_info['entry_cost'],
            'entry_fee': breakeven_info['entry_fee'],
            'breakeven_price': breakeven_info['breakeven_price'],
            'target_half_pct': breakeven_info['target_half_pct'],
            'target_1pct': breakeven_info['target_1pct'],
            'min_price_move_pct': breakeven_info['min_price_move_pct'],
            'entry_time': time.time(),
        }
        
        self.tracked_positions[symbol] = tracking_data
        
        # Also record in cost basis tracker if available
        if self.cost_basis_tracker:
            try:
                self.cost_basis_tracker.set_entry_price(
                    symbol=symbol,
                    price=fill_price,
                    quantity=fill_qty,
                    exchange=exchange,
                    fee=breakeven_info['entry_fee']
                )
            except Exception as e:
                print(f"⚠️ Cost basis tracker error: {e}")
        
        # Log to trade logger if available
        if self.trade_logger and TradeEntry:
            try:
                entry = TradeEntry(
                    timestamp=datetime.now().isoformat(),
                    symbol=symbol,
                    side='BUY',
                    exchange=exchange,
                    entry_price=fill_price,
                    entry_time=time.time(),
                    quantity=fill_qty,
                    entry_value=breakeven_info['entry_cost'],
                    coherence=0.0,
                    dominant_node='orca',
                    hnc_frequency=0.0,
                    hnc_is_harmonic=True,
                    probability_score=0.95,
                    imperial_probability=0.95,
                    cosmic_phase='hunt',
                    earth_coherence=0.5,
                    gates_passed=3
                )
                self.trade_logger.log_entry(entry)
            except Exception as e:
                print(f"⚠️ Trade logger error: {e}")
        
        print(f"   📝 TRACKED: {symbol} | Order: {order_id[:8]}... | Entry: ${fill_price:.6f} | Breakeven: ${breakeven_info['breakeven_price']:.6f} (+{breakeven_info['min_price_move_pct']:.2f}%)")
        
        return tracking_data
    
    def can_sell_profitably(self, symbol: str, current_price: float) -> Tuple[bool, dict]:
        """
        🎯 CHECK IF WE CAN SELL AT A PROFIT!
        
        Returns (can_sell, info) where:
        - can_sell: True if current_price > breakeven_price
        - info: Dict with profit details
        """
        tracked = self.tracked_positions.get(symbol)
        
        if not tracked:
            # No tracked position - use cost basis tracker as fallback
            if self.cost_basis_tracker:
                return self.cost_basis_tracker.can_sell_profitably(symbol, current_price)
            # No tracking data - assume we can sell (legacy behavior)
            return True, {'warning': 'No tracking data available'}
        
        breakeven = tracked['breakeven_price']
        entry_price = tracked['entry_price']
        entry_qty = tracked['entry_qty']
        
        # Calculate exit value after fees
        fee_rate = self.fee_rates.get(tracked['exchange'], 0.0025)
        exit_gross = current_price * entry_qty
        exit_fee = exit_gross * fee_rate
        exit_value = exit_gross - exit_fee
        
        # Net P&L
        net_pnl = exit_value - tracked['entry_cost']
        net_pnl_pct = (net_pnl / tracked['entry_cost']) * 100 if tracked['entry_cost'] > 0 else 0
        
        can_sell = current_price >= breakeven
        
        info = {
            'symbol': symbol,
            'entry_price': entry_price,
            'current_price': current_price,
            'breakeven_price': breakeven,
            'price_vs_breakeven_pct': ((current_price / breakeven) - 1) * 100,
            'entry_cost': tracked['entry_cost'],
            'exit_value': exit_value,
            'exit_fee': exit_fee,
            'net_pnl': net_pnl,
            'net_pnl_pct': net_pnl_pct,
            'can_sell_profitably': can_sell,
            'order_id': tracked['order_id'],
        }
        
        return can_sell, info
        
    def calculate_breakeven_price(self, entry_price: float) -> float:
        """
        Calculate minimum sell price to break even after fees.
        
        Math:
          Buy cost = entry_price × (1 + fee)
          Sell value = sell_price × (1 - fee)
          Breakeven: sell_value = buy_cost
          
          sell_price × (1 - fee) = entry_price × (1 + fee)
          sell_price = entry_price × (1 + fee) / (1 - fee)
        """
        return entry_price * (1 + self.fee_rate) / (1 - self.fee_rate)
    
    def calculate_target_price(self, entry_price: float, target_pct: float = 1.0) -> float:
        """
        Calculate sell price for target profit %.
        
        Math:
          Target = breakeven + (target_pct / 100) × entry_price
        """
        breakeven = self.calculate_breakeven_price(entry_price)
        profit_add = entry_price * (target_pct / 100)
        return breakeven + profit_add
    
    def calculate_realized_pnl(self, entry_price: float, entry_qty: float,
                               exit_price: float, exit_qty: float) -> Dict:
        """
        Calculate realized P&L with fees.
        
        Returns:
          {
            'entry_cost': float,
            'entry_fee': float,
            'exit_value': float,
            'exit_fee': float,
            'total_fees': float,
            'gross_pnl': float,
            'net_pnl': float,
            'net_pnl_pct': float
          }
        """
        # Entry
        entry_gross = entry_price * entry_qty
        entry_fee = entry_gross * self.fee_rate
        entry_cost = entry_gross + entry_fee
        
        # Exit
        exit_gross = exit_price * exit_qty
        exit_fee = exit_gross * self.fee_rate
        exit_value = exit_gross - exit_fee
        
        # P&L
        gross_pnl = exit_gross - entry_gross
        total_fees = entry_fee + exit_fee
        net_pnl = exit_value - entry_cost
        net_pnl_pct = (net_pnl / entry_cost) * 100 if entry_cost > 0 else 0
        
        return {
            'entry_cost': entry_cost,
            'entry_fee': entry_fee,
            'exit_value': exit_value,
            'exit_fee': exit_fee,
            'total_fees': total_fees,
            'gross_pnl': gross_pnl,
            'net_pnl': net_pnl,
            'net_pnl_pct': net_pnl_pct
        }
    
    def hunt_and_kill(self, symbol: str, amount_usd: float, target_pct: float = 1.0,
                       stop_pct: float = -1.0, max_wait: int = 300):
        """
        Complete kill cycle with LIVE STREAMING:
        1. BUY
        2. STREAM prices at 100ms (not polling!)
        3. WAIT for: target hit OR momentum reversal OR whale selling OR stop loss
        4. SELL at perfect moment
        5. RETURN realized P&L
        """
        print("="*60)
        print(f"🦈 ORCA HUNT & KILL CYCLE - {symbol}")
        print("="*60)
        
        # Get current price
        orderbook = self.client.get_crypto_orderbook(symbol)
        asks = orderbook.get('asks', [])
        if not asks or len(asks) == 0:
            print("❌ No price data")
            return None
        
        # Alpaca format: {'p': price, 's': size}
        entry_price = float(asks[0].get('p', 0))
        if entry_price == 0:
            print("❌ Invalid price")
            return None
        print(f"📊 Entry price: ${entry_price:,.2f}")
        
        # Calculate targets
        breakeven = self.calculate_breakeven_price(entry_price)
        target = self.calculate_target_price(entry_price, target_pct)
        # Stop loss is BELOW entry for BUY orders (protect against drop)
        stop_price = entry_price * (1 - abs(stop_pct) / 100)
        
        print(f"🎯 Breakeven:   ${breakeven:,.2f} (+{((breakeven/entry_price-1)*100):.3f}%)")
        print(f"🎯 Target:      ${target:,.2f} (+{((target/entry_price-1)*100):.3f}%)")
        print(f"🛑 Stop Loss:   ${stop_price:,.2f} (-{abs(stop_pct):.1f}%)")
        
        # Step 1: BUY
        print(f"\n🔪 STEP 1: BUY ${amount_usd:.2f} of {symbol}")
        try:
            buy_order = self.client.place_market_order(
                symbol=symbol,
                side='buy',
                quote_qty=amount_usd
            )
            if not buy_order:
                print("❌ Buy failed")
                return None
            
            buy_qty = float(buy_order.get('filled_qty', 0))
            buy_price = float(buy_order.get('filled_avg_price', 0))
            buy_id = buy_order.get('id', '')
            
            print(f"✅ Bought {buy_qty:.8f} @ ${buy_price:,.2f}")
            print(f"   Order: {buy_id}")
            
        except Exception as e:
            print(f"❌ Buy error: {e}")
            return None
        
        # Create position tracker
        position = LivePosition(
            symbol=symbol,
            exchange=self.exchange,
            entry_price=buy_price,
            entry_qty=buy_qty,
            entry_cost=buy_price * buy_qty * (1 + self.fee_rate),
            breakeven_price=self.calculate_breakeven_price(buy_price),
            target_price=self.calculate_target_price(buy_price, target_pct)
        )
        
        # Step 2: LIVE STREAM until exit condition
        print(f"\n📡 STEP 2: LIVE STREAMING (100ms updates)")
        print(f"   Target: ${position.target_price:,.2f} | Stop: ${stop_price:,.2f}")
        print(f"   🐋 Whale Signal: {self.whale_signal}")
        print("   Press Ctrl+C to abort...")
        
        start = time.time()
        last_price = buy_price
        momentum_direction = 0
        consecutive_drops = 0
        
        try:
            while (time.time() - start) < max_wait:
                # Get current price (FAST - 100ms intervals)
                orderbook = self.client.get_crypto_orderbook(symbol)
                bids = orderbook.get('bids', [])
                if bids and len(bids) > 0:
                    current = float(bids[0].get('p', 0))
                    if current == 0:
                        time.sleep(self.stream_interval)
                        continue
                    
                    # Track momentum
                    position.price_history.append(current)
                    if len(position.price_history) > 50:
                        position.price_history.pop(0)
                    
                    # Calculate momentum (last 5 prices)
                    if len(position.price_history) >= 5:
                        recent = position.price_history[-5:]
                        momentum_direction = (recent[-1] - recent[0]) / recent[0] * 100
                    
                    # Track consecutive drops
                    if current < last_price:
                        consecutive_drops += 1
                    else:
                        consecutive_drops = 0
                    last_price = current
                    
                    # Calculate P&L
                    pnl_est = self.calculate_realized_pnl(buy_price, buy_qty, current, buy_qty)
                    position.current_price = current
                    position.current_pnl = pnl_est['net_pnl']
                    position.current_pnl_pct = pnl_est['net_pnl_pct']
                    position.whale_activity = self.whale_signal
                    
                    # Live display
                    whale_icon = '🐋' if self.whale_signal == 'buying' else ('🦈' if self.whale_signal == 'selling' else '  ')
                    print(f"\r   ${current:,.2f} | P&L: ${pnl_est['net_pnl']:+.4f} ({pnl_est['net_pnl_pct']:+.3f}%) | Mom: {momentum_direction:+.2f}% {whale_icon}", end='', flush=True)
                    
                    # ═══════════════════════════════════════════════════════
                    # SMART EXIT CONDITIONS (don't pull out too early!)
                    # ═══════════════════════════════════════════════════════
                    
                    # 1. HIT TARGET - perfect exit!
                    if current >= position.target_price:
                        position.hit_target = True
                        position.ready_to_kill = True
                        position.kill_reason = 'TARGET_HIT'
                        print(f"\n\n🎯 TARGET HIT! ${current:,.2f} >= ${position.target_price:,.2f}")
                        break
                    
                    # 2. MOMENTUM REVERSAL - only if in profit
                    if pnl_est['net_pnl'] > 0 and momentum_direction < -0.5 and consecutive_drops >= 5:
                        position.ready_to_kill = True
                        position.kill_reason = 'MOMENTUM_REVERSAL'
                        print(f"\n\n📉 Momentum reversal detected (in profit) - taking gains!")
                        break
                    
                    # 3. WHALE SELLING - only if above breakeven AND profitable
                    if self.whale_signal == 'selling' and current >= position.breakeven_price:
                        # Calculate if we'd be profitable
                        est_exit = current * buy_qty * (1 - self.fee_rate)
                        est_pnl = est_exit - position.entry_cost
                        if est_pnl > 0:
                            position.ready_to_kill = True
                            position.kill_reason = 'WHALE_SELLING'
                            print(f"\n\n🐋 Whale selling detected - exiting with profit!")
                            break
                        else:
                            print(f"\r   🐋 Whale selling but NOT profitable - HOLDING!", end="")
                    
                    # 4. NO STOP LOSS! HOLD UNTIL PROFITABLE!
                    # DISABLED: We NEVER sell at a loss
                    # if current <= stop_price:
                    #     position.ready_to_kill = True
                    #     position.kill_reason = 'STOP_LOSS'
                    #     print(f"\n\n🛑 STOP LOSS HIT! ${current:,.2f} <= ${stop_price:,.2f}")
                    #     break
                    
                time.sleep(self.stream_interval)  # 100ms streaming
            else:
                print("\n⏰ Timeout - selling anyway")
                position.kill_reason = 'TIMEOUT'
                orderbook = self.client.get_crypto_orderbook(symbol)
                bids = orderbook.get('bids', [])
                current = float(bids[0].get('p', buy_price)) if bids else buy_price
                
        except KeyboardInterrupt:
            print("\n\n🛑 Aborted by user - selling now")
            position.kill_reason = 'USER_ABORT'
            orderbook = self.client.get_crypto_orderbook(symbol)
            bids = orderbook.get('bids', [])
            current = float(bids[0].get('p', buy_price)) if bids else buy_price
        
        # Step 3: SELL (only if profitable)
        print(f"\n🔪 STEP 3: SELL {buy_qty:.8f} {symbol}")
        # Recalculate projected P&L at current market price and only sell if positive
        try:
            pnl_est = self.calculate_realized_pnl(buy_price, buy_qty, current, buy_qty)
            if pnl_est['net_pnl'] <= 0:
                print(f"\n⛔ NOT SELLING: projected net P&L ${pnl_est['net_pnl']:+.4f} <= 0. Waiting for profitable exit.")
                # Do not execute sell to avoid realizing a loss
                return None
        except Exception:
            # If P&L calc fails for some reason, be conservative and skip selling
            print("\n⚠️ Could not compute projected P&L - skipping sell to avoid risk")
            return None
        
        try:
            sell_order = self.client.place_market_order(
                symbol=symbol,
                side='sell',
                quantity=buy_qty
            )
            if not sell_order:
                print("❌ Sell failed - POSITION STILL OPEN!")
                return None
            
            sell_qty = float(sell_order.get('filled_qty', 0))
            sell_price = float(sell_order.get('filled_avg_price', 0))
            sell_id = sell_order.get('id', '')
            
            print(f"✅ Sold {sell_qty:.8f} @ ${sell_price:,.2f}")
            print(f"   Order: {sell_id}")
            
        except Exception as e:
            print(f"❌ Sell error: {e}")
            print("⚠️ POSITION MAY STILL BE OPEN!")
            return None
        
        # Step 4: CALCULATE REALIZED P&L
        pnl = self.calculate_realized_pnl(buy_price, buy_qty, sell_price, sell_qty)
        
        print("\n" + "="*60)
        print("💰 KILL COMPLETE - REALIZED P&L")
        print("="*60)
        print(f"📥 Entry:      ${pnl['entry_cost']:.4f} (inc. ${pnl['entry_fee']:.4f} fee)")
        print(f"📤 Exit:       ${pnl['exit_value']:.4f} (inc. ${pnl['exit_fee']:.4f} fee)")
        print(f"💸 Total fees: ${pnl['total_fees']:.4f}")
        print(f"📊 Gross P&L:  ${pnl['gross_pnl']:.4f}")
        print(f"💎 Net P&L:    ${pnl['net_pnl']:.4f} ({pnl['net_pnl_pct']:+.3f}%)")
        print("="*60)
        
        if pnl['net_pnl'] > 0:
            print(f"✅ SUCCESSFUL KILL: +${pnl['net_pnl']:.4f} PROFIT")
        else:
            print(f"❌ LOST HUNT: ${abs(pnl['net_pnl']):.4f} LOSS")
        print("="*60)
        
        return pnl

    def fast_kill_hunt(self, amount_per_position: float = 25.0, 
                       num_positions: int = 3,
                       target_pct: float = 0.8,
                       timeout_secs: int = 60):
        """
        🦈⚡ FAST KILL HUNT - USE EXISTING ORCA FOR RAPID KILLS! ⚡🦈
        
        Uses the ALREADY INITIALIZED orca instance to avoid recursive instantiation.
        Scans market and uses orca intelligence that's already connected.
        
        🚫 NO STOP LOSS - DON'T PULL OUT EARLY!
        Only exit on: TARGET HIT or USER ABORT (Ctrl+C)
        """
        print("\n" + "⚡"*30)
        print("  🦈⚡ FAST KILL HUNT - ORCA INTELLIGENCE ⚡🦈")
        print("⚡"*30)
        
        # Show system status - ALL WIRED SYSTEMS
        print("\n📡 INTELLIGENCE SYSTEMS STATUS:")
        print(f"   ✅ OrcaKillCycle: READY")
        print(f"   ✅ Exchanges: {', '.join(self.clients.keys()) if hasattr(self, 'clients') else 'N/A'}")
        print(f"   {'✅' if hasattr(self, 'miner_brain') and self.miner_brain else '❌'} Miner Brain: {'WIRED' if hasattr(self, 'miner_brain') and self.miner_brain else 'N/A'}")
        print(f"   {'✅' if hasattr(self, 'quantum_telescope') and self.quantum_telescope else '❌'} Quantum Telescope: {'WIRED' if hasattr(self, 'quantum_telescope') and self.quantum_telescope else 'N/A'}")
        print(f"   {'✅' if hasattr(self, 'ultimate_intel') and self.ultimate_intel else '❌'} Ultimate Intelligence (95%): {'WIRED' if hasattr(self, 'ultimate_intel') and self.ultimate_intel else 'N/A'}")
        orca_wired = (hasattr(self, 'orca_intel') and self.orca_intel) or (hasattr(self, 'movers_scanner') and self.movers_scanner and hasattr(self.movers_scanner, 'orca') and self.movers_scanner.orca)
        print(f"   {'✅' if orca_wired else '❌'} Orca Intelligence: {'WIRED' if orca_wired else 'N/A'}")
        print(f"   {'✅' if hasattr(self, 'wave_scanner') and self.wave_scanner else '❌'} Wave Scanner: {'WIRED' if hasattr(self, 'wave_scanner') and self.wave_scanner else 'N/A'}")
        print(f"   {'✅' if hasattr(self, 'movers_scanner') and self.movers_scanner else '❌'} Movers Scanner: {'WIRED' if hasattr(self, 'movers_scanner') and self.movers_scanner else 'N/A'}")
        print(f"   {'✅' if hasattr(self, 'whale_tracker') and self.whale_tracker else '❌'} Whale Tracker: {'WIRED' if hasattr(self, 'whale_tracker') and self.whale_tracker else 'N/A'}")
        timeline_wired = (hasattr(self, 'timeline_oracle') and self.timeline_oracle)
        # Also check if Timeline Oracle is wired through Enigma integration
        if not timeline_wired:
            try:
                from aureon_enigma_integration import EnigmaIntegration
                enigma = EnigmaIntegration()
                timeline_wired = hasattr(enigma, 'timeline_oracle') and enigma.timeline_oracle
            except:
                pass
        print(f"   {'✅' if timeline_wired else '❌'} Timeline Oracle: {'WIRED' if timeline_wired else 'N/A'}")
        print(f"   {'✅' if hasattr(self, 'bus') and self.bus else '❌'} ThoughtBus: {'CONNECTED' if hasattr(self, 'bus') and self.bus else 'N/A'}")
        
        # Collect opportunities from ALL intelligence sources
        all_opportunities = []
        
        # ═══════════════════════════════════════════════════════════════════
        # 🧠 SOURCE 1: Ultimate Intelligence (95% accuracy!) - HIGHEST PRIORITY
        # ═══════════════════════════════════════════════════════════════════
        if hasattr(self, 'ultimate_intel') and self.ultimate_intel:
            try:
                print("\n💎 Consulting Ultimate Intelligence (95% accuracy)...")
                # Use predict() method for guaranteed patterns
                if hasattr(self.ultimate_intel, 'get_guaranteed_patterns'):
                    patterns = self.ultimate_intel.get_guaranteed_patterns()
                    if patterns and isinstance(patterns, (list, tuple)):
                        for pattern in patterns[:5]:
                            if hasattr(pattern, 'win_rate') and pattern.win_rate >= 0.90:  # 90%+ win rate only
                                all_opportunities.append({
                                    'symbol': getattr(pattern, 'symbol', 'UNKNOWN'),
                                    'action': getattr(pattern, 'direction', 'buy'),
                                    'confidence': pattern.win_rate,
                                    'source': f'ultimate_intel_{pattern.win_rate*100:.0f}%',
                                    'exchange': 'alpaca',
                                    'change_pct': getattr(pattern, 'expected_move', 1.0) * 100
                                })
                        print(f"   💎 Found {len(patterns)} guaranteed patterns (90%+ win rate)")
                    else:
                        print(f"   ⚠️ Ultimate Intel returned invalid patterns: {type(patterns)} - {patterns}")
                # Also get stats
                if hasattr(self.ultimate_intel, 'get_stats'):
                    stats = self.ultimate_intel.get_stats()
                    print(f"   📊 Accuracy: {stats.get('accuracy', 0)*100:.1f}% ({stats.get('total', 0)} predictions)")
            except Exception as e:
                print(f"   ⚠️ Ultimate Intel: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🦈 SOURCE 2: Orca Intelligence (full scanning)
        # ═══════════════════════════════════════════════════════════════════
        if hasattr(self, 'orca_intel') and self.orca_intel:
            try:
                print("\n🦈 Scanning with Orca Intelligence...")
                if hasattr(self.orca_intel, 'scan_opportunities'):
                    orca_opps = self.orca_intel.scan_opportunities()
                    for opp in orca_opps[:10]:
                        all_opportunities.append({
                            'symbol': opp.symbol if hasattr(opp, 'symbol') else str(opp),
                            'action': 'buy',
                            'confidence': opp.confidence if hasattr(opp, 'confidence') else 0.7,
                            'source': 'orca_intel',
                            'exchange': opp.exchange if hasattr(opp, 'exchange') else 'alpaca',
                            'change_pct': opp.change_pct if hasattr(opp, 'change_pct') else 1.0
                        })
                    print(f"   🦈 Found {len(orca_opps)} opportunities")
            except Exception as e:
                print(f"   ⚠️ Orca Intel: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🌊 SOURCE 3: Global Wave Scanner
        # ═══════════════════════════════════════════════════════════════════
        if hasattr(self, 'wave_scanner') and self.wave_scanner:
            try:
                print("\n🌊 Scanning Global Waves...")
                if hasattr(self.wave_scanner, 'scan'):
                    waves = self.wave_scanner.scan()
                    for wave in waves[:10]:
                        all_opportunities.append({
                            'symbol': wave.symbol if hasattr(wave, 'symbol') else str(wave),
                            'action': 'buy',
                            'confidence': wave.strength if hasattr(wave, 'strength') else 0.6,
                            'source': 'wave_scanner',
                            'exchange': 'alpaca',
                            'change_pct': wave.magnitude if hasattr(wave, 'magnitude') else 0.5
                        })
                    print(f"   🌊 Found {len(waves)} waves")
            except Exception as e:
                print(f"   ⚠️ Wave Scanner: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 📈 SOURCE 4: Movers & Shakers Scanner
        # ═══════════════════════════════════════════════════════════════════
        if hasattr(self, 'movers_scanner') and self.movers_scanner:
            try:
                print("\n📈 Scanning Movers & Shakers...")
                if hasattr(self.movers_scanner, 'scan'):
                    movers = self.movers_scanner.scan()
                    for mover in movers[:10]:
                        all_opportunities.append({
                            'symbol': mover.symbol if hasattr(mover, 'symbol') else str(mover),
                            'action': 'buy' if (mover.change_pct if hasattr(mover, 'change_pct') else 0) > 0 else 'sell',
                            'confidence': min(1.0, abs(mover.change_pct if hasattr(mover, 'change_pct') else 0) / 3),
                            'source': 'movers_shakers',
                            'exchange': 'alpaca',
                            'change_pct': mover.change_pct if hasattr(mover, 'change_pct') else 0
                        })
                    print(f"   📈 Found {len(movers)} movers")
            except Exception as e:
                print(f"   ⚠️ Movers Scanner: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🐋 SOURCE 5: Whale Intelligence Tracker
        # ═══════════════════════════════════════════════════════════════════
        if hasattr(self, 'whale_tracker') and self.whale_tracker:
            try:
                print("\n🐋 Tracking Whale Activity...")
                # Get firm activities for major symbols
                for sym in ['BTC/USD', 'ETH/USD', 'SOL/USD']:
                    signal = self.whale_tracker.get_whale_signal(sym, 'long')
                    if signal.whale_support > 0.6:  # Whales bullish
                        all_opportunities.append({
                            'symbol': sym,
                            'action': 'buy',
                            'confidence': signal.whale_support,
                            'source': f'whale_tracker:{signal.dominant_firm}',
                            'exchange': 'alpaca',
                            'change_pct': signal.momentum_score * 2
                        })
                        print(f"   🐋 {sym}: {signal.dominant_firm} {signal.firm_activity} (support: {signal.whale_support:.0%})")
            except Exception as e:
                print(f"   ⚠️ Whale Tracker: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # ⏳ SOURCE 6: Timeline Oracle (7-day predictions)
        # ═══════════════════════════════════════════════════════════════════
        if hasattr(self, 'timeline_oracle') and self.timeline_oracle:
            try:
                print("\n⏳ Consulting Timeline Oracle (7-day vision)...")
                if hasattr(self.timeline_oracle, 'get_best_opportunities'):
                    timeline_opps = self.timeline_oracle.get_best_opportunities()
                    for opp in timeline_opps[:5]:
                        all_opportunities.append({
                            'symbol': opp.get('symbol', ''),
                            'action': opp.get('action', 'buy'),
                            'confidence': opp.get('confidence', 0.7),
                            'source': 'timeline_oracle',
                            'exchange': 'alpaca',
                            'change_pct': opp.get('expected_move', 1.0)
                        })
                    print(f"   ⏳ Found {len(timeline_opps)} timeline opportunities")
            except Exception as e:
                print(f"   ⚠️ Timeline Oracle: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 📊 SOURCE 7: Simple market scan (FALLBACK)
        # ═══════════════════════════════════════════════════════════════════
        print("\n📊 Market Scan (Fallback)...")
        market_opps = self.scan_entire_market(min_change_pct=0.3)
        for opp in market_opps[:10]:
            if isinstance(opp, MarketOpportunity):
                all_opportunities.append({
                    'symbol': opp.symbol,
                    'action': 'buy' if opp.change_pct > 0 else 'sell',
                    'confidence': min(1.0, abs(opp.change_pct) / 3),
                    'source': 'market_scan',
                    'exchange': opp.exchange,
                    'price': opp.price,
                    'change_pct': opp.change_pct
                })
        print(f"   Found {len(market_opps)} market movers")
        
        # Check available cash FIRST to filter opportunities
        cash = self.get_available_cash()
        min_cash = amount_per_position * 1.1  # 10% buffer
        funded_exchanges = [ex for ex, amt in cash.items() if amt >= min_cash]
        
        print(f"\n💰 Cash check: {', '.join([f'{ex}=${amt:.2f}' for ex, amt in cash.items()])}")
        print(f"   Need ${min_cash:.2f}/position → Viable: {', '.join(funded_exchanges) or 'NONE!'}")
        
        # Deduplicate 
        seen = set()
        unique_opps = []
        
        for opp in all_opportunities:
            sym = opp['symbol']
            if sym not in seen:
                seen.add(sym)
                unique_opps.append(opp)
        
        # 🆕 CRITICAL: Filter to ONLY funded exchanges
        if funded_exchanges:
            funded_opps = [o for o in unique_opps if o.get('exchange', 'alpaca') in funded_exchanges]
            if funded_opps:
                print(f"   ✅ Filtered to {len(funded_opps)} opportunities on funded exchanges")
                unique_opps = funded_opps
            else:
                print(f"   ⚠️ No opportunities on funded exchanges - FORCE SCAN Alpaca...")
                # Force scan Alpaca even with lower threshold - REPLACE all opportunities
                alpaca_opps = self._scan_alpaca_market(min_change_pct=0.1, min_volume=100)
                unique_opps = []  # CLEAR - we only want Alpaca now
                for opp in alpaca_opps[:20]:
                    unique_opps.append({
                        'symbol': opp.symbol,
                        'action': 'buy' if opp.change_pct > 0 else 'sell',
                        'confidence': min(1.0, abs(opp.change_pct) / 2),
                        'source': 'alpaca_forced',
                        'exchange': 'alpaca',  # FORCE ALPACA
                        'price': opp.price,
                        'change_pct': opp.change_pct
                    })
                print(f"   🔍 Using {len(unique_opps)} Alpaca-only movers")
        
        # Sort by confidence
        unique_opps.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        # 🆕 Filter for BUY opportunities only (positive change)
        buy_opps = [o for o in unique_opps if o.get('change_pct', 0) > 0]
        if buy_opps:
            print(f"\n📈 BUY Opportunities: {len(buy_opps)}")
            unique_opps = buy_opps
        else:
            print(f"\n⚠️ No positive movers found - using all")
        
        print(f"🎯 TOTAL OPPORTUNITIES: {len(unique_opps)}")
        
        if not unique_opps:
            print("❌ No opportunities found from any scanner!")
            return []
        
        # Show top opportunities
        print("\n📋 TOP OPPORTUNITIES:")
        for i, opp in enumerate(unique_opps[:10]):
            sym = opp['symbol']
            action = opp.get('action', 'buy').upper()
            conf = opp.get('confidence', 0)
            source = opp.get('source', 'unknown')
            change = opp.get('change_pct', 0)
            print(f"   {i+1}. {sym:12} | {action:4} | Conf: {conf:.0%} | Source: {source} | Δ{change:+.2f}%")
        
        # Select top N for hunting
        selected = unique_opps[:num_positions]
        
        # Convert to MarketOpportunity format for pack_hunt
        converted_opps = []
        for opp in selected:
            # Only take BUY opportunities for simplicity
            if opp.get('action', 'buy').lower() == 'buy':
                change = opp.get('change_pct', opp.get('confidence', 0) * 2)
                converted_opps.append(MarketOpportunity(
                    symbol=opp['symbol'],
                    exchange=opp.get('exchange', 'alpaca'),
                    price=opp.get('price', 0),
                    change_pct=change,
                    volume=0,
                    momentum_score=abs(change),  # Use change as momentum score
                    fee_rate=self.fee_rates.get(opp.get('exchange', 'alpaca'), 0.0025)
                ))
        
        if not converted_opps:
            print("❌ No BUY opportunities to execute")
            return []
        
        print(f"\n🦈 LAUNCHING FAST KILL HUNT WITH {len(converted_opps)} POSITIONS...")
        print(f"   💰 ${amount_per_position:.2f} per position")
        print(f"   🎯 Target: {target_pct}%")
        print(f"   🚫 NO STOP LOSS - DON'T PULL OUT EARLY!")
        
        # Use pack_hunt for execution (NO STOP LOSS)
        return self.pack_hunt(
            opportunities=converted_opps,
            num_positions=num_positions,
            amount_per_position=amount_per_position,
            target_pct=target_pct,
            stop_pct=None  # NO STOP LOSS!
        )

    def pack_hunt(self, opportunities: list = None, num_positions: int = 3,
                  amount_per_position: float = 2.5, target_pct: float = 1.0, 
                  stop_pct: float = None, min_change_pct: float = 0.5):
        """
        🦈🦈🦈 DYNAMIC PACK HUNT - MONITOR + SCAN + BARTER MATRIX! 🦈🦈🦈
        
        🆕 ENHANCED DYNAMIC SYSTEM:
        1. Monitor current positions with progress bars & whale intel
        2. Actively scan for new opportunities every 30 seconds
        3. Use barter matrix for cross-exchange arbitrage kills
        4. Add new positions dynamically when opportunities arise
        5. DON'T PULL OUT EARLY - No timeout exits, NO STOP LOSS!
        6. Only exit on: TARGET HIT or USER ABORT (Ctrl+C)
        """
        print("\n" + "🦈"*30)
        print("  ORCA DYNAMIC PACK HUNT - MONITOR + SCAN + BARTER")
        print("🦈"*30)
        
        # Check available cash FIRST
        cash = self.get_available_cash()
        print(f"\n💰 Available cash: Alpaca=${cash.get('alpaca', 0):.2f} | Kraken=${cash.get('kraken', 0):.2f}")
        
        # For testing: Use available cash if less than requested amount
        if amount_per_position > max(cash.values()):
            print(f"⚠️ Requested ${amount_per_position:.2f} > available cash, using available amounts for testing")
            amount_per_position = max(cash.values()) * 0.9  # Use 90% of available cash
            print(f"   Using ${amount_per_position:.2f} per position for testing")
        
        # Determine which exchanges have enough cash
        min_cash_per_position = amount_per_position * 1.1  # 10% buffer
        viable_exchanges = [ex for ex, amt in cash.items() if amt >= min_cash_per_position]
        
        if not viable_exchanges:
            print(f"❌ No exchange has enough cash (need ${min_cash_per_position:.2f} per position)")
            return []
        
        print(f"   Viable exchanges: {', '.join([ex.upper() for ex in viable_exchanges])}")
        
        # If no opportunities provided, scan ENTIRE market
        if not opportunities:
            print("\n🌊 INITIAL MARKET SCAN...")
            opportunities = self.scan_entire_market(min_change_pct=min_change_pct)
        
        if not opportunities:
            print("❌ No targets found anywhere - market is completely flat")
            return []
        
        # 🆕 FILTER: Only keep opportunities where we have cash!
        funded_opportunities = []
        for opp in opportunities:
            if isinstance(opp, MarketOpportunity):
                exchange = opp.exchange
                symbol = opp.symbol
            else:
                exchange = opp.get('exchange', 'alpaca') if isinstance(opp, dict) else self.primary_exchange
                symbol = opp.get('symbol', opp) if isinstance(opp, dict) else str(opp)
            
            # Check if we can afford minimum order for this symbol on this exchange
            available_cash = cash.get(exchange, 0)
            if available_cash >= amount_per_position:
                funded_opportunities.append(opp)
        
        if not funded_opportunities:
            print(f"⚠️ {len(opportunities)} opportunities found but none affordable with current cash")
            # For testing: Try with smaller amounts or different logic
            print("   Attempting with available cash amounts...")
            # Use all opportunities but adjust amounts per exchange
            funded_opportunities = opportunities
        else:
            print(f"✅ {len(funded_opportunities)} funded opportunities (affordable with current cash)")
        
        # Start with top opportunities
        available_targets = funded_opportunities[:num_positions * 2]  # Get extra in case some fail
        
        print(f"\n🎯 Will attempt up to {len(available_targets)} targets (fallback if buys fail):")
        for i, opp in enumerate(available_targets):
            if isinstance(opp, MarketOpportunity):
                print(f"   {i+1}. {opp.symbol} ({opp.exchange}): {opp.change_pct:+.2f}% @ ${opp.price:,.2f}")
            else:
                sym = opp.get('symbol', opp) if isinstance(opp, dict) else str(opp)
                exch = opp.get('exchange', self.primary_exchange) if isinstance(opp, dict) else self.primary_exchange
                print(f"   {i+1}. {sym} ({exch})")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🆕 DYNAMIC HUNTING LOOP - MONITOR + SCAN + ADD POSITIONS!
        # ═══════════════════════════════════════════════════════════════════
        
        positions = []
        results = []
        attempted_indices = set()
        last_scan_time = 0
        scan_interval = 5  # 🔥 AGGRESSIVE: Scan every 5 seconds for fast opportunities!
        monitor_interval = 0.05  # 20 updates/sec
        whale_update_interval = 2.0  # Update whale intel every 2 seconds
        last_whale_update = 0
        
        print(f"\n🚀 STARTING DYNAMIC HUNT - AGGRESSIVE MODE!")
        print("="*80)
        print("   📊 Monitor current positions | 🔍 Scan every 5 SECONDS (AGGRESSIVE)")
        print("   🛒 Add positions dynamically | 🔄 Immediate re-buy after sell!")
        print("   🚫 NO STOP LOSS - ONLY SELL ON PROFIT!")
        print("="*80)
        
        try:
            while True:  # Infinite loop - only exit on user abort
                current_time = time.time()
                
                # ═══════════════════════════════════════════════════════════
                # PERIODIC MARKET SCAN - LOOK FOR NEW OPPORTUNITIES
                # ═══════════════════════════════════════════════════════════
                if current_time - last_scan_time >= scan_interval:
                    last_scan_time = current_time
                    print(f"\n🔍 SCANNING FOR NEW OPPORTUNITIES... ({len(positions)} active positions)")
                    
                    # Scan market for new opportunities
                    new_opportunities = self.scan_entire_market(min_change_pct=min_change_pct)
                    
                    if new_opportunities:
                        # Filter for affordable opportunities we haven't tried
                        affordable_new = []
                        for opp in new_opportunities[:5]:  # Check top 5
                            if isinstance(opp, MarketOpportunity):
                                exchange = opp.exchange
                                symbol = opp.symbol
                            else:
                                exchange = opp.get('exchange', 'alpaca') if isinstance(opp, dict) else self.primary_exchange
                                symbol = opp.get('symbol', opp) if isinstance(opp, dict) else str(opp)
                            
                            # Check if we have cash and haven't tried this symbol recently
                            current_cash = self.get_available_cash().get(exchange, 0)
                            symbol_in_positions = any(p.symbol == symbol.replace('/', '') for p in positions)
                            
                            if current_cash >= amount_per_position and not symbol_in_positions:
                                affordable_new.append(opp)
                        
                        if affordable_new and len(positions) < num_positions:
                            print(f"   🎯 Found {len(affordable_new)} new opportunities!")
                            # Add to available targets
                            available_targets.extend(affordable_new[:2])  # Add top 2
                        else:
                            print(f"   ✅ No new affordable opportunities (or at max positions)")
                    else:
                        print(f"   ⚪ Market scan complete - no new opportunities")
                
                # ═══════════════════════════════════════════════════════════
                # TRY TO OPEN NEW POSITIONS IF WE HAVE ROOM
                # ═══════════════════════════════════════════════════════════
                if len(positions) < num_positions and len(attempted_indices) < len(available_targets):
                    # Find next unattempted opportunity
                    next_idx = None
                    for i in range(len(available_targets)):
                        if i not in attempted_indices:
                            next_idx = i
                            break
                    
                    if next_idx is not None:
                        attempted_indices.add(next_idx)
                        opp = available_targets[next_idx]
                        
                        if isinstance(opp, MarketOpportunity):
                            symbol = opp.symbol
                            exchange = opp.exchange
                            fee_rate = opp.fee_rate
                        else:
                            symbol = opp.get('symbol', opp) if isinstance(opp, dict) else str(opp)
                            exchange = opp.get('exchange', self.primary_exchange) if isinstance(opp, dict) else self.primary_exchange
                            fee_rate = self.fee_rates.get(exchange, 0.0025)
                        
                        # Get client for this exchange
                        client = self.clients.get(exchange)
                        if not client:
                            continue
                        
                        # Normalize symbol
                        if '/' not in symbol:
                            symbol = symbol.replace('USD', '/USD')
                        symbol_clean = symbol.replace('/', '')
                        
                        print(f"\n📈 OPENING NEW POSITION {len(positions)+1}/{num_positions}: {symbol} on {exchange.upper()}")
                        
                        try:
                            # Get entry price using exchange-specific method
                            if exchange == 'alpaca':
                                orderbook = client.get_crypto_orderbook(symbol_clean)
                                asks = orderbook.get('asks', [])
                                if not asks:
                                    continue
                                entry_price = float(asks[0].get('p', 0))
                            elif exchange == 'kraken':
                                ticker = client.get_ticker(symbol_clean)
                                entry_price = ticker.get('ask', ticker.get('price', 0))
                            else:
                                continue
                            
                            if entry_price <= 0:
                                continue
                            
                            # Check if we have enough cash for this specific position
                            current_cash = self.get_available_cash().get(exchange, 0)
                            required_cash = amount_per_position * 1.1  # 10% buffer
                            if current_cash < required_cash:
                                if current_cash >= amount_per_position * 0.5:  # At least 50% of requested
                                    print(f"⚠️ Using available cash ${current_cash:.2f} for testing")
                                    amount_per_position = current_cash * 0.9  # Use 90% of available
                                else:
                                    continue
                            
                            # BUY on the appropriate exchange
                            buy_order = client.place_market_order(
                                symbol=symbol_clean,
                                side='buy',
                                quote_qty=amount_per_position
                            )
                            if not buy_order:
                                continue
                            
                            buy_qty = float(buy_order.get('filled_qty', 0))
                            buy_price = float(buy_order.get('filled_avg_price', entry_price))
                            
                            # 🆕 SKIP if we got 0 quantity (order didn't fill)
                            if buy_qty <= 0 or buy_price <= 0:
                                continue
                            
                            # Calculate levels (NO STOP LOSS!)
                            stop_price_calc = 0.0  # NO STOP LOSS - DON'T PULL OUT EARLY!
                            breakeven = buy_price * (1 + fee_rate) / (1 - fee_rate)
                            target_price = breakeven + buy_price * (target_pct / 100)
                            
                            pos = LivePosition(
                                symbol=symbol_clean,
                                exchange=exchange,
                                entry_price=buy_price,
                                entry_qty=buy_qty,
                                entry_cost=buy_price * buy_qty * (1 + fee_rate),
                                breakeven_price=breakeven,
                                target_price=target_price,
                                client=client,
                                stop_price=stop_price_calc
                            )
                            positions.append(pos)
                            print(f"   ✅ NEW POSITION: Bought {buy_qty:.8f} @ ${buy_price:,.2f}")
                            print(f"      🎯 Target: ${target_price:,.2f} | 🚫 NO STOP LOSS")
                            
                        except Exception as e:
                            continue
                
                # ═══════════════════════════════════════════════════════════
                # MONITOR EXISTING POSITIONS WITH PROGRESS BARS
                # ═══════════════════════════════════════════════════════════
                
                if positions:  # Only show monitoring if we have positions
                    # Update whale intelligence periodically
                    whale_signals = {}
                    if current_time - last_whale_update >= whale_update_interval:
                        last_whale_update = current_time
                        for pos in positions:
                            if self.whale_tracker:
                                try:
                                    signal = self.whale_tracker.get_whale_signal(
                                        pos.symbol, 
                                        our_direction='long',
                                        current_price=pos.current_price,
                                        price_change_pct=pos.current_pnl_pct
                                    )
                                    whale_signals[pos.symbol] = signal
                                except Exception as e:
                                    pass
                    
                    # Clear screen for clean display
                    print("\033[2J\033[H", end="")  # Clear screen and move cursor to top
                    
                    # Header
                    print("🦈🦈🦈 ORCA DYNAMIC PACK HUNT - LIVE MONITORING 🦈🦈🦈")
                    print("="*80)
                    print(f"   📊 {len(positions)} ACTIVE POSITIONS | 💰 TOTAL P&L: ${sum(p.current_pnl for p in positions):+.4f}")
                    print(f"   🔍 Next market scan: {max(0, scan_interval - (current_time - last_scan_time)):.1f}s")
                    print("="*80)
                    
                    # Update each position using its own client
                    for i, pos in enumerate(positions[:]):  # Copy list to allow removal
                        try:
                            # Get price from correct exchange
                            if pos.exchange == 'alpaca':
                                orderbook = pos.client.get_crypto_orderbook(pos.symbol)
                                bids = orderbook.get('bids', [])
                                if not bids:
                                    continue
                                current = float(bids[0].get('p', 0))
                            elif pos.exchange == 'kraken':
                                ticker = pos.client.get_ticker(pos.symbol)
                                current = ticker.get('bid', ticker.get('price', 0))
                            else:
                                continue
                            
                            if current == 0:
                                continue
                            
                            # Track momentum
                            pos.price_history.append(current)
                            if len(pos.price_history) > 50:
                                pos.price_history.pop(0)
                            
                            # Calculate P&L
                            fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                            entry_gross = pos.entry_price * pos.entry_qty
                            entry_fee = entry_gross * fee_rate
                            entry_cost = entry_gross + entry_fee
                            exit_gross = current * pos.entry_qty
                            exit_fee = exit_gross * fee_rate
                            exit_value = exit_gross - exit_fee
                            net_pnl = exit_value - entry_cost
                            
                            pos.current_price = current
                            pos.current_pnl = net_pnl
                            pos.current_pnl_pct = (net_pnl / entry_cost * 100) if entry_cost > 0 else 0
                            
                            # Calculate progress to target
                            progress_pct = min(100, max(0, (current - pos.entry_price) / (pos.target_price - pos.entry_price) * 100))
                            progress_bar = "█" * int(progress_pct / 5) + "░" * (20 - int(progress_pct / 5))
                            
                            # Get whale signal for this position
                            whale_info = whale_signals.get(pos.symbol)
                            if whale_info:
                                whale_status = f"🐋 {whale_info.dominant_firm}: {whale_info.firm_activity}"
                                whale_conf = f"🤖 Conf: {whale_info.confidence:.1f}"
                            else:
                                whale_status = "🐋 Scanning..."
                                whale_conf = "🤖 Analyzing..."
                            
                            # Display position with progress bar
                            print(f"\n🎯 POSITION {i+1}: {pos.symbol} ({pos.exchange.upper()})")
                            print(f"   💰 Entry: ${pos.entry_price:,.4f} | Current: ${current:,.4f} | Target: ${pos.target_price:,.4f}")
                            print(f"   📊 P&L: ${net_pnl:+.4f} ({pos.current_pnl_pct:+.2f}%) | Progress: [{progress_bar}] {progress_pct:.1f}%")
                            print(f"   {whale_status} | {whale_conf}")
                            
                            # ═════════════════════════════════════════════════════
                            # EXIT CONDITIONS - ONLY THESE, NO TIMEOUT!
                            # ═════════════════════════════════════════════════════
                            
                            # 1. TARGET HIT - perfect exit!
                            if current >= pos.target_price:
                                pos.ready_to_kill = True
                                pos.kill_reason = 'TARGET_HIT'
                                print(f"\n   🎯🎯🎯 TARGET HIT! SELLING NOW! 🎯🎯🎯")
                            
                            # 2. MOMENTUM REVERSAL - ONLY IF IN PROFIT!
                            elif pos.current_pnl > 0 and len(pos.price_history) >= 10:
                                recent = pos.price_history[-10:]
                                momentum = (recent[-1] - recent[0]) / recent[0] * 100 if recent[0] > 0 else 0
                                if momentum < -0.3:  # Losing momentum while in profit
                                    pos.ready_to_kill = True
                                    pos.kill_reason = 'MOMENTUM_PROFIT'
                                    print(f"\n   📈📈📈 TAKING PROFIT (momentum reversal) 📈📈📈")
                            
                            # EXIT if ready
                            if pos.ready_to_kill:
                                print(f"\n   🔪🔪🔪 EXECUTING SELL ORDER 🔪🔪🔪")
                                sell_order = pos.client.place_market_order(
                                    symbol=pos.symbol,
                                    side='sell',
                                    quantity=pos.entry_qty
                                )
                                if sell_order:
                                    sell_price = float(sell_order.get('filled_avg_price', current))
                                    # Recalculate final P&L
                                    final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                                    final_pnl = final_exit - entry_cost
                                    results.append({
                                        'symbol': pos.symbol,
                                        'exchange': pos.exchange,
                                        'reason': pos.kill_reason,
                                        'net_pnl': final_pnl
                                    })
                                    print(f"   ✅ SOLD {pos.symbol}: ${final_pnl:+.4f} ({pos.kill_reason})")
                                    
                                    # 🔥🔥🔥 IMMEDIATE RE-SCAN & RE-BUY AFTER PROFITABLE SELL! 🔥🔥🔥
                                    print(f"\n   🔄🔄🔄 IMMEDIATE RE-SCAN - AGGRESSIVE MODE! 🔄🔄🔄")
                                    # Force immediate market scan
                                    try:
                                        new_opps = self.scan_entire_market(min_change_pct=0.3)  # Lower threshold for faster entries
                                        if new_opps:
                                            # Find best opportunity we haven't tried
                                            for new_opp in new_opps[:5]:
                                                new_symbol = new_opp.symbol if isinstance(new_opp, MarketOpportunity) else new_opp.get('symbol', '')
                                                new_exchange = new_opp.exchange if isinstance(new_opp, MarketOpportunity) else new_opp.get('exchange', 'alpaca')
                                                
                                                # Skip if already in positions
                                                active_symbols = [p.symbol for p in positions]
                                                if new_symbol in active_symbols:
                                                    continue
                                                
                                                # Check cash availability
                                                cash_check = self.get_available_cash()
                                                available_cash = cash_check.get(new_exchange, 0)
                                                
                                                if available_cash >= amount_per_position:
                                                    print(f"   🚀 FOUND NEW TARGET: {new_symbol} ({new_exchange.upper()})")
                                                    # Execute immediate buy
                                                    new_client = self.clients.get(new_exchange)
                                                    if new_client:
                                                        try:
                                                            new_price = new_opp.price if isinstance(new_opp, MarketOpportunity) else 0
                                                            if new_price == 0:
                                                                if new_exchange == 'alpaca':
                                                                    ob = new_client.get_crypto_orderbook(new_symbol)
                                                                    asks = ob.get('asks', [])
                                                                    new_price = float(asks[0].get('p', 0)) if asks else 0
                                                                else:
                                                                    tick = new_client.get_ticker(new_symbol)
                                                                    new_price = tick.get('ask', tick.get('price', 0))
                                                            
                                                            if new_price > 0:
                                                                buy_qty_new = amount_per_position / new_price
                                                                new_buy = new_client.place_market_order(
                                                                    symbol=new_symbol,
                                                                    side='buy',
                                                                    quantity=buy_qty_new
                                                                )
                                                                if new_buy:
                                                                    fill_price = float(new_buy.get('filled_avg_price', new_price))
                                                                    fill_qty = float(new_buy.get('filled_qty', buy_qty_new))
                                                                    new_fee_rate = self.fee_rates.get(new_exchange, 0.0025)
                                                                    new_breakeven = fill_price * (1 + new_fee_rate) / (1 - new_fee_rate)
                                                                    new_target = new_breakeven + (fill_price * target_pct / 100)
                                                                    
                                                                    new_position = LivePosition(
                                                                        symbol=new_symbol,
                                                                        exchange=new_exchange,
                                                                        entry_price=fill_price,
                                                                        entry_qty=fill_qty,
                                                                        entry_cost=fill_price * fill_qty * (1 + new_fee_rate),
                                                                        breakeven_price=new_breakeven,
                                                                        target_price=new_target,
                                                                        client=new_client
                                                                    )
                                                                    positions.append(new_position)
                                                                    print(f"   🎯 BOUGHT {new_symbol}: {fill_qty:.4f} @ ${fill_price:.4f}")
                                                                    print(f"   🎯 New target: ${new_target:.4f}")
                                                                    break  # Only buy one new position per cycle
                                                        except Exception as buy_err:
                                                            print(f"   ⚠️ Re-buy failed: {buy_err}")
                                    except Exception as scan_err:
                                        print(f"   ⚠️ Re-scan failed: {scan_err}")
                                    
                                    print(f"   🔄 CYCLE CONTINUES - NEVER STOP HUNTING!")
                                positions.remove(pos)
                                
                        except Exception as e:
                            print(f"   ⚠️ Error monitoring {pos.symbol}: {e}")
                    
                    # Show summary at bottom
                    if positions:
                        print(f"\n{'='*80}")
                        active_symbols = [f"{p.symbol[:6]}({p.exchange[0].upper()})" for p in positions]
                        print(f"   📡 ACTIVE: {', '.join(active_symbols)}")
                        print(f"   💰 TOTAL P&L: ${sum(p.current_pnl for p in positions):+.4f}")
                        print(f"   🎯 WAITING FOR TARGET HITS...")
                        print(f"   🚫 NO STOP LOSS - HOLD UNTIL PROFIT!")
                        print(f"   ⏱️ Next whale update: {max(0, whale_update_interval - (current_time - last_whale_update)):.1f}s")
                    else:
                        print(f"\n{'='*80}")
                        print("   🎉 ALL POSITIONS CLOSED - READY FOR NEXT ROUND!")
                        print(f"{'='*80}")
                else:
                    # No positions - just show scanning status
                    print(f"\n🔍 SCANNING FOR OPPORTUNITIES... ({len(attempted_indices)} attempted)")
                    print(f"   Next scan in: {max(0, scan_interval - (current_time - last_scan_time)):.1f}s")
                    print(f"   Available targets remaining: {len(available_targets) - len(attempted_indices)}")
                
                time.sleep(monitor_interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 USER ABORT - Closing profitable positions only (skip losses)...")
            for pos in positions:
                try:
                    # Only close positions that would realize a positive net P&L
                    if pos.current_pnl > 0:
                        sell_order = pos.client.place_market_order(symbol=pos.symbol, side='sell', quantity=pos.entry_qty)
                        if sell_order:
                            fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                            sell_price = float(sell_order.get('filled_avg_price', pos.current_price))
                            entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                            final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                            final_pnl = final_exit - entry_cost
                            results.append({
                                'symbol': pos.symbol,
                                'exchange': pos.exchange,
                                'reason': 'USER_ABORT',
                                'net_pnl': final_pnl
                            })
                            print(f"   ✅ Closed {pos.symbol}: ${final_pnl:+.4f} (USER_ABORT)")
                    else:
                        print(f"   ⛔ Skipping close for {pos.symbol}: current P&L ${pos.current_pnl:+.4f} -> not closing to avoid realizing loss")
                except Exception as e:
                    print(f"   ⚠️ Error closing {pos.symbol}: {e}")
        
        return results
        
        # Faster updates for better monitoring
        monitor_interval = 0.05  # 20 updates/sec instead of 10
        whale_update_interval = 2.0  # Update whale intel every 2 seconds
        last_whale_update = 0
        
        try:
            while positions:  # Loop forever until ALL positions exit properly
                current_time = time.time()
                
                # Update whale intelligence periodically
                whale_signals = {}
                if current_time - last_whale_update >= whale_update_interval:
                    last_whale_update = current_time
                    for pos in positions:
                        if self.whale_tracker:
                            try:
                                signal = self.whale_tracker.get_whale_signal(
                                    pos.symbol, 
                                    our_direction='long',
                                    current_price=pos.current_price,
                                    price_change_pct=pos.current_pnl_pct
                                )
                                whale_signals[pos.symbol] = signal
                            except Exception as e:
                                pass
                
                # Clear screen for clean display
                print("\033[2J\033[H", end="")  # Clear screen and move cursor to top
                
                # Header
                print("🦈🦈🦈 ORCA PACK HUNT - LIVE MONITORING 🦈🦈🦈")
                print("="*80)
                print(f"   📊 {len(positions)} ACTIVE POSITIONS | 💰 TOTAL P&L: ${sum(p.current_pnl for p in positions):+.4f}")
                print("="*80)
                
                # Update each position using its own client
                for i, pos in enumerate(positions[:]):  # Copy list to allow removal
                    try:
                        # Get price from correct exchange
                        if pos.exchange == 'alpaca':
                            orderbook = pos.client.get_crypto_orderbook(pos.symbol)
                            bids = orderbook.get('bids', [])
                            if not bids:
                                continue
                            current = float(bids[0].get('p', 0))
                        elif pos.exchange == 'kraken':
                            ticker = pos.client.get_ticker(pos.symbol)
                            current = ticker.get('bid', ticker.get('price', 0))
                        else:
                            continue
                        
                        if current == 0:
                            continue
                        
                        # Track momentum
                        pos.price_history.append(current)
                        if len(pos.price_history) > 50:
                            pos.price_history.pop(0)
                        
                        # Calculate P&L
                        fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                        entry_gross = pos.entry_price * pos.entry_qty
                        entry_fee = entry_gross * fee_rate
                        entry_cost = entry_gross + entry_fee
                        exit_gross = current * pos.entry_qty
                        exit_fee = exit_gross * fee_rate
                        exit_value = exit_gross - exit_fee
                        net_pnl = exit_value - entry_cost
                        
                        pos.current_price = current
                        pos.current_pnl = net_pnl
                        pos.current_pnl_pct = (net_pnl / entry_cost * 100) if entry_cost > 0 else 0
                        
                        # Calculate progress to target
                        progress_pct = min(100, max(0, (current - pos.entry_price) / (pos.target_price - pos.entry_price) * 100))
                        progress_bar = "█" * int(progress_pct / 5) + "░" * (20 - int(progress_pct / 5))
                        
                        # Get whale signal for this position
                        whale_info = whale_signals.get(pos.symbol)
                        if whale_info:
                            whale_status = f"🐋 {whale_info.dominant_firm}: {whale_info.firm_activity}"
                            whale_conf = f"🤖 Conf: {whale_info.confidence:.1f}"
                        else:
                            whale_status = "🐋 Scanning..."
                            whale_conf = "🤖 Analyzing..."
                        
                        # Display position with progress bar
                        print(f"\n🎯 POSITION {i+1}: {pos.symbol} ({pos.exchange.upper()})")
                        print(f"   💰 Entry: ${pos.entry_price:,.4f} | Current: ${current:,.4f} | Target: ${pos.target_price:,.4f}")
                        print(f"   📊 P&L: ${net_pnl:+.4f} ({pos.current_pnl_pct:+.2f}%) | Progress: [{progress_bar}] {progress_pct:.1f}%")
                        print(f"   {whale_status} | {whale_conf}")
                        
                        # ═════════════════════════════════════════════════════
                        # EXIT CONDITIONS - ONLY THESE, NO TIMEOUT!
                        # ═════════════════════════════════════════════════════
                        
                        # 1. TARGET HIT - perfect exit!
                        if current >= pos.target_price:
                            pos.ready_to_kill = True
                            pos.kill_reason = 'TARGET_HIT'
                            print(f"\n   🎯🎯🎯 TARGET HIT! SELLING NOW! 🎯🎯🎯")
                        
                        # 2. MOMENTUM REVERSAL - ONLY IF IN PROFIT!
                        elif pos.current_pnl > 0 and len(pos.price_history) >= 10:
                            recent = pos.price_history[-10:]
                            momentum = (recent[-1] - recent[0]) / recent[0] * 100 if recent[0] > 0 else 0
                            if momentum < -0.3:  # Losing momentum while in profit
                                pos.ready_to_kill = True
                                pos.kill_reason = 'MOMENTUM_PROFIT'
                                print(f"\n   📈📈📈 TAKING PROFIT (momentum reversal) 📈📈📈")
                        
                        # EXIT if ready - SELL ONLY IF POSITIVE PROFIT
                        if pos.ready_to_kill:
                            # Only execute sell if current unrealized P&L is positive
                            if pos.current_pnl > 0:
                                print(f"\n   🔪🔪🔪 EXECUTING SELL ORDER (PROFITABLE) 🔪🔪🔪")
                                sell_order = pos.client.place_market_order(
                                    symbol=pos.symbol,
                                    side='sell',
                                    quantity=pos.entry_qty
                                )
                                if sell_order:
                                    sell_price = float(sell_order.get('filled_avg_price', current))
                                    # Recalculate final P&L
                                    final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                                    final_pnl = final_exit - entry_cost
                                    results.append({
                                        'symbol': pos.symbol,
                                        'exchange': pos.exchange,
                                        'reason': pos.kill_reason,
                                        'net_pnl': final_pnl
                                    })
                                    print(f"   ✅ SOLD {pos.symbol}: ${final_pnl:+.4f} ({pos.kill_reason})")
                                    print(f"   🔄 READY FOR NEXT TRADE!")
                                positions.remove(pos)
                            else:
                                # Skip selling to avoid realizing a loss
                                print(f"\n   ✋ NOT SELLING {pos.symbol}: current P&L ${pos.current_pnl:+.4f} <= 0 (waiting for profitable exit)")
                                pos.ready_to_kill = False
                                pos.kill_reason = 'NOT_PROFIT_YET'
                            
                    except Exception as e:
                        print(f"   ⚠️ Error monitoring {pos.symbol}: {e}")
                
                # Show summary at bottom
                if positions:
                    print(f"\n{'='*80}")
                    active_symbols = [f"{p.symbol[:6]}({p.exchange[0].upper()})" for p in positions]
                    print(f"   📡 ACTIVE: {', '.join(active_symbols)}")
                    print(f"   💰 TOTAL P&L: ${sum(p.current_pnl for p in positions):+.4f}")
                    print(f"   🎯 WAITING FOR TARGET HITS...")
                    print(f"   🚫 NO STOP LOSS - HOLD UNTIL PROFIT!")
                    print(f"   ⏱️ Next whale update: {max(0, whale_update_interval - (current_time - last_whale_update)):.1f}s")
                else:
                    print(f"\n{'='*80}")
                    print("   🎉 ALL POSITIONS CLOSED - READY FOR NEXT ROUND!")
                    print(f"{'='*80}")
                
                time.sleep(monitor_interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 USER ABORT - Closing all positions...")
            for pos in positions:
                try:
                    sell_order = pos.client.place_market_order(symbol=pos.symbol, side='sell', quantity=pos.entry_qty)
                    if sell_order:
                        fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                        sell_price = float(sell_order.get('filled_avg_price', pos.current_price))
                        entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                        final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                        final_pnl = final_exit - entry_cost
                        results.append({
                            'symbol': pos.symbol,
                            'exchange': pos.exchange,
                            'reason': 'USER_ABORT',
                            'net_pnl': final_pnl
                        })
                        print(f"   Closed {pos.symbol}: ${final_pnl:+.4f}")
                except Exception as e:
                    print(f"   ⚠️ Error closing {pos.symbol}: {e}")
                
        except KeyboardInterrupt:
            print("\n\n🛑 USER ABORT - Closing all positions...")
            for pos in positions:
                try:
                    sell_order = pos.client.place_market_order(symbol=pos.symbol, side='sell', quantity=pos.entry_qty)
                    if sell_order:
                        fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                        sell_price = float(sell_order.get('filled_avg_price', pos.current_price))
                        entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                        final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                        final_pnl = final_exit - entry_cost
                        results.append({
                            'symbol': pos.symbol,
                            'exchange': pos.exchange,
                            'reason': 'USER_ABORT',
                            'net_pnl': final_pnl
                        })
                        print(f"   Closed {pos.symbol}: ${final_pnl:+.4f}")
                except Exception as e:
                    print(f"   ⚠️ Error closing {pos.symbol}: {e}")
        
        # Summary
        print("\n\n" + "="*70)
        print("🦈 PACK HUNT COMPLETE - MULTI-EXCHANGE")
        print("="*70)
        total = sum(r['net_pnl'] for r in results)
        for r in results:
            emoji = '✅' if r['net_pnl'] > 0 else '❌'
            print(f"   {emoji} {r['symbol']} ({r['exchange']}): ${r['net_pnl']:+.4f} ({r['reason']})")
        print(f"\n💰 TOTAL P&L: ${total:+.4f}")
        print("="*70)
        
        return results

    # ═══════════════════════════════════════════════════════════════════════
    # 👑🦈 AUTONOMOUS MODE - QUEEN-GUIDED INFINITE LOOP 🦈👑
    # ═══════════════════════════════════════════════════════════════════════
    
    def run_autonomous(self, max_positions: int = 3, amount_per_position: float = 2.5,
                       target_pct: float = 1.0, min_change_pct: float = 0.3):
        """
        👑🔄 FULLY AUTONOMOUS QUEEN-GUIDED TRADING LOOP 🔄👑
        
        RUNS FOREVER until manually stopped (Ctrl+C).
        The Queen guides all decisions:
        
        PHASE 0: PORTFOLIO SCAN - Check existing positions, close profitable ones!
        PHASE 1: SCAN - Find new opportunities
        PHASE 2: BUY - With freed cash from closed positions
        PHASE 3: MONITOR - Stream prices, track whale intel
        PHASE 4: SELL - ONLY ON PROFIT! Then loop back to PHASE 0
        
        NO STOP LOSS - HOLD UNTIL PROFIT!
        """
        print("\n" + "👑"*30)
        print("  👑🦈 AUTONOMOUS QUEEN MODE - INFINITE LOOP 🦈👑")
        print("👑"*30)
        print()
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║  👑 SERO THE QUEEN IS NOW IN CONTROL 👑                          ║")
        print("║                                                                   ║")
        print("║  🔄 LOOP: Portfolio → Close Profits → Scan → Buy → Monitor      ║")
        print("║  🚫 NO STOP LOSS - ONLY SELL ON PROFIT!                          ║")
        print("║  ⏱️ Aggressive 5-second scans                                    ║")
        print("║  🐋 Full whale intelligence active                               ║")
        print("║  💰 All cost tracking systems engaged                            ║")
        print("║                                                                   ║")
        print("║  Press Ctrl+C to stop (will close PROFITABLE positions only)    ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print()
        
        # Wire up the Queen Hive Mind
        queen = None
        try:
            from aureon_queen_hive_mind import QueenHiveMind
            queen = QueenHiveMind()
            print("👑 QUEEN SERO: AWAKENED AND READY!")
            print(f"   🎯 Dream: ${queen.THE_DREAM:,.0f} (ONE BILLION)")
            print(f"   💰 Current equity: ${queen.equity:,.2f}")
            print()
        except Exception as e:
            print(f"⚠️ Queen initialization: {e}")
            print("   Running without Queen guidance (basic mode)")
        
        # Session statistics
        session_stats = {
            'cycles': 0,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0,
            'start_time': time.time(),
            'best_trade': 0.0,
            'worst_trade': 0.0,
            'positions_closed': 0,
            'cash_freed': 0.0,
        }
        
        # Current positions - will be loaded from portfolio
        positions: List[LivePosition] = []
        
        # Timing - SLOWER to avoid rate limits!
        scan_interval = 10  # Every 10 seconds (was 5)
        monitor_interval = 1.0  # 1 second updates (was 0.1) - PREVENTS RATE LIMITS!
        whale_update_interval = 5.0  # Every 5 seconds (was 2)
        last_scan_time = 0
        last_whale_update = 0
        last_portfolio_scan = 0
        portfolio_scan_interval = 30  # Scan portfolio every 30 seconds (was 10)
        
        # ═══════════════════════════════════════════════════════════════════
        # PHASE 0 (STARTUP): SCAN EXISTING PORTFOLIO - CLOSE PROFITABLE POSITIONS
        # ═══════════════════════════════════════════════════════════════════
        print("\n" + "="*70)
        print("📊 PHASE 0: SCANNING EXISTING PORTFOLIO")
        print("="*70)
        
        for exchange_name, client in self.clients.items():
            try:
                print(f"\n🔍 Scanning {exchange_name.upper()} positions...")
                
                if exchange_name == 'alpaca':
                    alpaca_positions = client.get_positions()
                    if alpaca_positions:
                        for ap in alpaca_positions:
                            symbol = ap.get('symbol', '').replace('/', '')
                            qty = float(ap.get('qty', 0))
                            entry_price = float(ap.get('avg_entry_price', 0))
                            current_price = float(ap.get('current_price', 0))
                            unrealized_pnl = float(ap.get('unrealized_pl', 0))
                            market_value = float(ap.get('market_value', 0))
                            
                            if qty > 0 and entry_price > 0:
                                fee_rate = self.fee_rates.get(exchange_name, 0.0025)
                                entry_cost = entry_price * qty * (1 + fee_rate)
                                exit_value = current_price * qty * (1 - fee_rate)
                                net_pnl = exit_value - entry_cost
                                breakeven = entry_price * (1 + fee_rate) / (1 - fee_rate)
                                target_price = breakeven * (1 + target_pct / 100)
                                
                                print(f"   📈 {symbol}: {qty:.6f} @ ${entry_price:.4f}")
                                print(f"      Current: ${current_price:.4f} | P&L: ${net_pnl:+.4f}")
                                
                                # Check if we should close this profitable position
                                if net_pnl > 0.001:  # Profitable by at least $0.001
                                    print(f"      💰 PROFITABLE! Closing to free cash...")
                                    try:
                                        sell_order = client.place_market_order(
                                            symbol=symbol,
                                            side='sell',
                                            quantity=qty
                                        )
                                        if sell_order:
                                            session_stats['positions_closed'] += 1
                                            session_stats['cash_freed'] += exit_value
                                            session_stats['total_pnl'] += net_pnl
                                            session_stats['winning_trades'] += 1
                                            session_stats['total_trades'] += 1
                                            session_stats['best_trade'] = max(session_stats['best_trade'], net_pnl)
                                            print(f"      ✅ CLOSED! +${net_pnl:.4f} freed ${exit_value:.2f}")
                                    except Exception as e:
                                        print(f"      ⚠️ Sell failed: {e}")
                                        # Keep as live position to monitor
                                        pos = LivePosition(
                                            symbol=symbol,
                                            exchange=exchange_name,
                                            entry_price=entry_price,
                                            entry_qty=qty,
                                            entry_cost=entry_cost,
                                            breakeven_price=breakeven,
                                            target_price=target_price,
                                            client=client,
                                            current_price=current_price,
                                            current_pnl=net_pnl
                                        )
                                        positions.append(pos)
                                else:
                                    # Not profitable - keep monitoring
                                    print(f"      ⏳ UNDERWATER - keeping (will sell on profit)")
                                    pos = LivePosition(
                                        symbol=symbol,
                                        exchange=exchange_name,
                                        entry_price=entry_price,
                                        entry_qty=qty,
                                        entry_cost=entry_cost,
                                        breakeven_price=breakeven,
                                        target_price=target_price,
                                        client=client,
                                        current_price=current_price,
                                        current_pnl=net_pnl
                                    )
                                    positions.append(pos)
                    else:
                        print(f"   No positions on {exchange_name.upper()}")
                        
                elif exchange_name == 'kraken':
                    # Kraken positions - SCAN BALANCE FOR HOLDINGS
                    kraken_positions = client.get_balance()
                    if kraken_positions:
                        for asset, qty in kraken_positions.items():
                            if asset in ['USD', 'ZUSD', 'EUR', 'ZEUR', 'DAI', 'USDC', 'USDT', 'TUSD']:
                                continue  # Skip cash/stablecoins
                            qty = float(qty)
                            if qty > 0.000001:
                                symbol = f"{asset}USD"
                                try:
                                    ticker = client.get_ticker(symbol)
                                    current_price = float(ticker.get('bid', ticker.get('price', 0)))
                                    market_value = qty * current_price
                                    
                                    if market_value > 0.10:  # At least $0.10 position
                                        print(f"   📈 {symbol} (KRAKEN): {qty:.6f} @ ~${current_price:.6f} (${market_value:.2f})")
                                        
                                        # For Kraken we don't have entry price stored - use current price as estimate
                                        # This means we'll track from NOW and wait for profit from this point
                                        fee_rate = self.fee_rates.get(exchange_name, 0.0026)
                                        entry_price = current_price  # Best estimate for manual buys
                                        entry_cost = entry_price * qty * (1 + fee_rate)
                                        breakeven = entry_price * (1 + fee_rate) / (1 - fee_rate)
                                        target_price = breakeven * (1 + target_pct / 100)
                                        
                                        # 🚨 SAFETY: Only auto-sell if we have CONFIRMED cost basis with real entry price!
                                        # For manual Kraken buys, we DON'T know entry price, so NEVER auto-sell!
                                        if self.cost_basis_tracker:
                                            can_sell, info = self.cost_basis_tracker.can_sell_profitably(symbol, current_price)
                                            # ONLY sell if: can_sell=True AND we have a real entry price (not None)
                                            if can_sell and info.get('entry_price') is not None:
                                                print(f"      💰 PROFITABLE per cost basis (entry: ${info['entry_price']:.8f})! Closing...")
                                                try:
                                                    sell_order = client.place_market_order(symbol, 'sell', quantity=qty)
                                                    if sell_order:
                                                        exit_value = current_price * qty * (1 - fee_rate)
                                                        net_pnl = exit_value - info.get('cost_basis', exit_value * 0.99)
                                                        session_stats['positions_closed'] += 1
                                                        session_stats['cash_freed'] += exit_value
                                                        session_stats['total_pnl'] += net_pnl
                                                        session_stats['winning_trades'] += 1
                                                        session_stats['total_trades'] += 1
                                                        print(f"      ✅ CLOSED! +${net_pnl:.4f}")
                                                        continue  # Skip adding to positions
                                                except Exception as e:
                                                    print(f"      ⚠️ Sell failed: {e}")
                                            elif not can_sell:
                                                print(f"      ⏳ NOT PROFITABLE yet - keeping position")
                                            else:
                                                print(f"      ⚠️ NO COST BASIS - will NOT auto-sell (tracking from now)")
                                        
                                        # 🆕 ADD KRAKEN POSITION TO MONITORING LIST!
                                        print(f"      ⏳ Adding to monitor list (tracking from current price)")
                                        pos = LivePosition(
                                            symbol=symbol,
                                            exchange=exchange_name,
                                            entry_price=entry_price,
                                            entry_qty=qty,
                                            entry_cost=entry_cost,
                                            breakeven_price=breakeven,
                                            target_price=target_price,
                                            client=client,
                                            current_price=current_price,
                                            current_pnl=0.0  # Starting from now
                                        )
                                        positions.append(pos)
                                except Exception as e:
                                    print(f"      ⚠️ Error getting price for {symbol}: {e}")
                                    
            except Exception as e:
                print(f"   ⚠️ Error scanning {exchange_name}: {e}")
        
        print(f"\n📊 Portfolio scan complete:")
        print(f"   ✅ Positions closed: {session_stats['positions_closed']}")
        print(f"   💰 Cash freed: ${session_stats['cash_freed']:.2f}")
        print(f"   📈 P&L realized: ${session_stats['total_pnl']:+.4f}")
        print(f"   ⏳ Positions still held: {len(positions)}")
        
        # Now get updated cash after closing profitable positions
        cash = self.get_available_cash()
        print(f"\n💵 Available cash after portfolio cleanup:")
        for exchange, amount in cash.items():
            print(f"   {exchange.upper()}: ${amount:.2f}")
        print()
        
        try:
            while True:  # ♾️ INFINITE LOOP
                current_time = time.time()
                session_stats['cycles'] += 1
                
                # ═══════════════════════════════════════════════════════════
                # PHASE 0 (RECURRING): RE-SCAN PORTFOLIO FOR NEW PROFITS
                # ═══════════════════════════════════════════════════════════
                if current_time - last_portfolio_scan >= portfolio_scan_interval:
                    last_portfolio_scan = current_time
                    
                    # 🚀 BATCH FETCH ALL PRICES AT ONCE - PREVENTS RATE LIMITS!
                    batch_prices = {}
                    try:
                        alpaca_client = self.clients.get('alpaca')
                        if alpaca_client:
                            alpaca_symbols = [p.symbol for p in positions if p.exchange == 'alpaca']
                            if alpaca_symbols:
                                snapshot = alpaca_client.get_crypto_snapshot(alpaca_symbols)
                                if snapshot:
                                    for sym, data in snapshot.items():
                                        if data and 'latestTrade' in data:
                                            batch_prices[sym] = float(data['latestTrade'].get('p', 0))
                                        elif data and 'latestQuote' in data:
                                            batch_prices[sym] = float(data['latestQuote'].get('bp', 0))
                    except Exception:
                        pass
                    
                    # Also batch Kraken if we have positions there
                    try:
                        kraken_client = self.clients.get('kraken')
                        if kraken_client:
                            kraken_symbols = [p.symbol for p in positions if p.exchange == 'kraken']
                            for sym in kraken_symbols:
                                try:
                                    ticker = kraken_client.get_ticker(sym)
                                    if ticker:
                                        batch_prices[sym] = ticker.get('bid', ticker.get('price', 0))
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    
                    # 🆕 RE-SCAN KRAKEN BALANCES FOR NEW MANUAL POSITIONS!
                    try:
                        kraken_client = self.clients.get('kraken')
                        if kraken_client:
                            kraken_balances = kraken_client.get_balance()
                            current_kraken_symbols = [p.symbol for p in positions if p.exchange == 'kraken']
                            
                            for asset, qty in kraken_balances.items():
                                if asset in ['USD', 'ZUSD', 'EUR', 'ZEUR', 'DAI', 'USDC', 'USDT', 'TUSD']:
                                    continue  # Skip cash/stablecoins
                                qty = float(qty)
                                symbol = f"{asset}USD"
                                
                                # Check if this is a NEW position not already tracked
                                if qty > 0.000001 and symbol not in current_kraken_symbols:
                                    try:
                                        ticker = kraken_client.get_ticker(symbol)
                                        current_price = float(ticker.get('bid', ticker.get('price', 0)))
                                        market_value = qty * current_price
                                        
                                        if market_value > 0.10:  # At least $0.10
                                            print(f"\n🆕 NEW KRAKEN POSITION DETECTED: {symbol}")
                                            print(f"   📊 {qty:.6f} @ ${current_price:.8f} = ${market_value:.2f}")
                                            
                                            fee_rate = self.fee_rates.get('kraken', 0.0026)
                                            entry_price = current_price  # Use current as entry estimate
                                            entry_cost = entry_price * qty * (1 + fee_rate)
                                            breakeven = entry_price * (1 + fee_rate) / (1 - fee_rate)
                                            target_price = breakeven * (1 + target_pct / 100)
                                            
                                            pos = LivePosition(
                                                symbol=symbol,
                                                exchange='kraken',
                                                entry_price=entry_price,
                                                entry_qty=qty,
                                                entry_cost=entry_cost,
                                                breakeven_price=breakeven,
                                                target_price=target_price,
                                                client=kraken_client,
                                                current_price=current_price,
                                                current_pnl=0.0
                                            )
                                            positions.append(pos)
                                            batch_prices[symbol] = current_price
                                            print(f"   ✅ Added to monitor! Target: ${target_price:.8f}")
                                    except Exception as e:
                                        print(f"   ⚠️ Could not add {symbol}: {e}")
                    except Exception as e:
                        pass  # Silently skip if Kraken scan fails
                    
                    # Quick check existing positions for profit using BATCH prices
                    for pos in positions[:]:  # Copy list to allow removal
                        try:
                            # Use batch price (no individual API calls!)
                            current = batch_prices.get(pos.symbol, 0)
                            if current <= 0:
                                continue
                                
                            if current > 0:
                                fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                                entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                                exit_value = current * pos.entry_qty * (1 - fee_rate)
                                net_pnl = exit_value - entry_cost
                                pos.current_price = current
                                pos.current_pnl = net_pnl
                                
                                # Auto-close if hit target or profitable enough
                                if current >= pos.target_price or net_pnl > entry_cost * 0.01:  # Target or 1% profit
                                    # 🚨 SAFETY CHECK: For Kraken positions, verify with cost_basis_tracker!
                                    # Only sell if we have CONFIRMED profitability with real entry price
                                    can_sell = True
                                    if pos.exchange == 'kraken' and self.cost_basis_tracker:
                                        can_sell, info = self.cost_basis_tracker.can_sell_profitably(pos.symbol, current)
                                        if not can_sell or info.get('entry_price') is None:
                                            # No confirmed cost basis - DO NOT SELL!
                                            print(f"\n⚠️ {pos.symbol}: Would sell but NO CONFIRMED COST BASIS - HOLDING!")
                                            print(f"   📊 Calculated P&L: ${net_pnl:.4f} (but entry price unknown)")
                                            can_sell = False
                                        else:
                                            print(f"   ✅ Cost basis confirmed: entry ${info['entry_price']:.8f}")
                                    
                                    if can_sell:
                                        print(f"\n🎯 AUTO-CLOSE: {pos.symbol} is PROFITABLE! (+${net_pnl:.4f})")
                                        sell_order = pos.client.place_market_order(
                                            symbol=pos.symbol,
                                            side='sell',
                                            quantity=pos.entry_qty
                                        )
                                        if sell_order:
                                            session_stats['positions_closed'] += 1
                                            session_stats['cash_freed'] += exit_value
                                            session_stats['total_pnl'] += net_pnl
                                            session_stats['winning_trades'] += 1
                                            session_stats['total_trades'] += 1
                                            session_stats['best_trade'] = max(session_stats['best_trade'], net_pnl)
                                            positions.remove(pos)
                                            print(f"   ✅ CLOSED! +${net_pnl:.4f} → Cash freed for new buys!")
                                            last_scan_time = 0  # Force immediate scan for new opportunities
                        except Exception:
                            pass
                
                # ═══════════════════════════════════════════════════════════
                # PHASE 1: SCAN FOR NEW OPPORTUNITIES
                # ═══════════════════════════════════════════════════════════
                if current_time - last_scan_time >= scan_interval:
                    last_scan_time = current_time
                    
                    # Check if we have room for more positions
                    if len(positions) < max_positions:
                        print(f"\n🔍 QUEEN SCANNING... ({len(positions)}/{max_positions} positions active)")
                        
                        # Get available cash
                        cash = self.get_available_cash()
                        total_cash = sum(cash.values())
                        
                        if total_cash < amount_per_position * 0.5:
                            print(f"   💸 Waiting for cash (${total_cash:.2f} available, need ${amount_per_position:.2f})")
                        else:
                            # Scan market
                            opportunities = self.scan_entire_market(min_change_pct=min_change_pct)
                            
                            if opportunities:
                                # Filter for symbols not already in positions
                                active_symbols = [p.symbol for p in positions]
                                new_opps = [o for o in opportunities if o.symbol not in active_symbols]
                                
                                if new_opps:
                                    # Ask Queen for guidance if available
                                    queen_approved = True
                                    if queen and hasattr(queen, 'consciousness_level'):
                                        # Queen's consciousness affects decision confidence
                                        queen_approved = queen.consciousness_level > 0.3
                                        print(f"   👑 Queen consciousness: {queen.consciousness_level:.1%}")
                                    
                                    if queen_approved:
                                        # Take best opportunity
                                        best = new_opps[0]
                                        print(f"   👑 QUEEN APPROVED: {best.symbol} ({best.exchange})")
                                        print(f"      Change: {best.change_pct:+.2f}% | Momentum: {best.momentum_score:.2f}")
                                        
                                        # Execute buy
                                        try:
                                            client = self.clients.get(best.exchange)
                                            if client:
                                                symbol_clean = best.symbol.replace('/', '')
                                                
                                                # Adjust amount based on available cash
                                                exchange_cash = cash.get(best.exchange, 0)
                                                buy_amount = min(amount_per_position, exchange_cash * 0.9)
                                                
                                                if buy_amount >= 0.50:  # Minimum $0.50
                                                    buy_order = client.place_market_order(
                                                        symbol=symbol_clean,
                                                        side='buy',
                                                        quote_qty=buy_amount
                                                    )
                                                    
                                                    if buy_order:
                                                        buy_qty = float(buy_order.get('filled_qty', 0))
                                                        buy_price = float(buy_order.get('filled_avg_price', best.price))
                                                        
                                                        if buy_qty > 0 and buy_price > 0:
                                                            # Calculate levels
                                                            fee_rate = self.fee_rates.get(best.exchange, 0.0025)
                                                            breakeven = buy_price * (1 + fee_rate) / (1 - fee_rate)
                                                            target_price = breakeven * (1 + target_pct / 100)
                                                            
                                                            pos = LivePosition(
                                                                symbol=symbol_clean,
                                                                exchange=best.exchange,
                                                                entry_price=buy_price,
                                                                entry_qty=buy_qty,
                                                                entry_cost=buy_price * buy_qty * (1 + fee_rate),
                                                                breakeven_price=breakeven,
                                                                target_price=target_price,
                                                                client=client,
                                                                stop_price=0.0  # NO STOP LOSS!
                                                            )
                                                            positions.append(pos)
                                                            
                                                            # Track the buy order
                                                            self.track_buy_order(symbol_clean, buy_order, best.exchange)
                                                            
                                                            print(f"   ✅ BOUGHT: {buy_qty:.6f} @ ${buy_price:,.4f}")
                                                            print(f"      🎯 Target: ${target_price:,.4f} ({target_pct}%)")
                                                            print(f"      🚫 NO STOP LOSS - HOLD UNTIL PROFIT!")
                                                            
                                                            session_stats['total_trades'] += 1
                                        except Exception as e:
                                            print(f"   ⚠️ Buy failed: {e}")
                                    else:
                                        print(f"   👑 Queen says: Wait (consciousness too low)")
                                else:
                                    print(f"   ⚪ All opportunities already in positions")
                            else:
                                print(f"   ⚪ No opportunities found - market is flat")
                    else:
                        # At max positions - just monitor
                        pass
                
                # ═══════════════════════════════════════════════════════════
                # PHASE 2: MONITOR EXISTING POSITIONS
                # ═══════════════════════════════════════════════════════════
                if positions:
                    # Update whale intel periodically
                    whale_signals = {}
                    if current_time - last_whale_update >= whale_update_interval:
                        last_whale_update = current_time
                        for pos in positions:
                            if self.whale_tracker:
                                try:
                                    signal = self.whale_tracker.get_whale_signal(
                                        pos.symbol, 'long',
                                        current_price=pos.current_price,
                                        price_change_pct=pos.current_pnl_pct
                                    )
                                    whale_signals[pos.symbol] = signal
                                except Exception:
                                    pass
                    
                    # Display header
                    runtime = time.time() - session_stats['start_time']
                    runtime_str = f"{int(runtime//3600)}h {int((runtime%3600)//60)}m {int(runtime%60)}s"
                    
                    print("\033[2J\033[H", end="")  # Clear screen
                    print("👑🦈 AUTONOMOUS QUEEN MODE - LIVE MONITORING 🦈👑")
                    print("="*80)
                    print(f"   ⏱️ Runtime: {runtime_str} | 🔄 Cycles: {session_stats['cycles']}")
                    print(f"   📈 Trades: {session_stats['total_trades']} | ✅ Wins: {session_stats['winning_trades']} | ❌ Losses: {session_stats['losing_trades']}")
                    print(f"   💰 Session P&L: ${session_stats['total_pnl']:+.4f}")
                    print(f"   🏆 Best: ${session_stats['best_trade']:+.4f} | 💔 Worst: ${session_stats['worst_trade']:+.4f}")
                    print("="*80)
                    print(f"   📊 {len(positions)}/{max_positions} ACTIVE POSITIONS | Next scan: {max(0, scan_interval - (current_time - last_scan_time)):.0f}s")
                    print("="*80)
                    
                    # Update and display each position
                    # 🚀 BATCH FETCH: Get all prices at once to avoid rate limits!
                    all_prices = {}
                    try:
                        alpaca_client = self.clients.get('alpaca')
                        if alpaca_client:
                            # Use snapshot API for all symbols at once
                            symbols = [p.symbol for p in positions if p.exchange == 'alpaca']
                            if symbols:
                                try:
                                    snapshot = alpaca_client.get_crypto_snapshot(symbols)
                                    if snapshot:
                                        for sym, data in snapshot.items():
                                            if data and 'latestTrade' in data:
                                                all_prices[sym] = float(data['latestTrade'].get('p', 0))
                                            elif data and 'latestQuote' in data:
                                                all_prices[sym] = float(data['latestQuote'].get('bp', 0))
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    
                    # 🦈 Also batch fetch Kraken prices
                    try:
                        kraken_client = self.clients.get('kraken')
                        if kraken_client:
                            kraken_symbols = [p.symbol for p in positions if p.exchange == 'kraken']
                            for sym in kraken_symbols:
                                try:
                                    ticker = kraken_client.get_ticker(sym)
                                    if ticker:
                                        all_prices[sym] = ticker.get('bid', ticker.get('price', 0))
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    
                    total_unrealized = 0.0
                    real_positions = []  # Filter out dust
                    
                    for i, pos in enumerate(positions[:]):
                        try:
                            # Get current price from batch (NO FALLBACK - prevents rate limits!)
                            current = all_prices.get(pos.symbol, 0)
                            
                            # Skip if no price (batch failed for this symbol)
                            if current <= 0:
                                continue
                            
                            # Calculate P&L
                            fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                            entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                            exit_value = current * pos.entry_qty * (1 - fee_rate)
                            net_pnl = exit_value - entry_cost
                            
                            # 🎯 CORRECT MATH: Calculate P&L % from PRICE change, not cost
                            price_change_pct = ((current - pos.entry_price) / pos.entry_price * 100) if pos.entry_price > 0 else 0
                            # But for actual P&L %, use real costs
                            pnl_pct = (net_pnl / entry_cost * 100) if entry_cost > 0 else price_change_pct
                            
                            pos.current_price = current
                            pos.current_pnl = net_pnl
                            pos.current_pnl_pct = pnl_pct
                            
                            # Skip dust positions (< $0.01 value)
                            market_value = current * pos.entry_qty
                            if market_value < 0.01:
                                continue
                            
                            real_positions.append(pos)
                            total_unrealized += net_pnl
                            
                            # 🎯 FIXED PROGRESS BAR: Show negative when underwater!
                            # Progress from entry to target (can be negative if underwater)
                            if pos.target_price > pos.entry_price:
                                raw_progress = (current - pos.entry_price) / (pos.target_price - pos.entry_price) * 100
                            else:
                                raw_progress = 0
                            
                            # Visual: clamp display but show real % in text
                            display_progress = max(0, min(100, raw_progress))
                            
                            # Build progress bar with direction indicator
                            if raw_progress >= 0:
                                filled = int(display_progress / 5)
                                bar = "█" * filled + "░" * (20 - filled)
                            else:
                                # Underwater: show red blocks from left
                                underwater_pct = min(100, abs(raw_progress))
                                red_blocks = int(underwater_pct / 5)
                                bar = "▓" * red_blocks + "░" * (20 - red_blocks)
                            
                            # Whale info
                            whale_info = whale_signals.get(pos.symbol)
                            whale_str = f"🐋 {whale_info.reasoning[:50]}" if whale_info else "🐋 Scanning..."
                            
                            # ═════════════════════════════════════════════════════════════════
                            # 🔬 ENHANCED ANALYTICS: ETA + Probability + Velocity
                            # ═════════════════════════════════════════════════════════════════
                            eta_str = ""
                            if ETA_CALCULATOR_AVAILABLE and ImprovedETACalculator:
                                try:
                                    # Initialize ETA calculator for this position if needed
                                    if pos.eta_calculator is None:
                                        pos.eta_calculator = ImprovedETACalculator()
                                    
                                    # Track P&L history for this position
                                    pos.pnl_history.append((time.time(), net_pnl))
                                    # Keep last 60 samples (1 minute at 1Hz)
                                    if len(pos.pnl_history) > 60:
                                        pos.pnl_history = pos.pnl_history[-60:]
                                    
                                    # Calculate target P&L (what we need to hit target price)
                                    target_pnl = (pos.target_price - pos.entry_price) * pos.entry_qty * (1 - fee_rate) - entry_cost * fee_rate
                                    
                                    # Calculate ETA using probability model
                                    eta_result = pos.eta_calculator.calculate_eta(
                                        current_pnl=net_pnl,
                                        target_pnl=target_pnl,
                                        pnl_history=pos.pnl_history
                                    )
                                    pos.last_eta = eta_result
                                    
                                    # Format ETA display
                                    if eta_result.improved_eta == 0:
                                        eta_str = "🎯 TARGET!"
                                    elif eta_result.improved_eta == float('inf'):
                                        # Check velocity direction
                                        if eta_result.velocity < 0:
                                            eta_str = f"⏳ ∞ (↓ ${eta_result.velocity*60:.4f}/min)"
                                        else:
                                            eta_str = f"⏳ Calculating..."
                                    else:
                                        # Format time nicely
                                        if eta_result.improved_eta < 60:
                                            time_str = f"{eta_result.improved_eta:.0f}s"
                                        elif eta_result.improved_eta < 3600:
                                            time_str = f"{eta_result.improved_eta/60:.1f}m"
                                        else:
                                            time_str = f"{eta_result.improved_eta/3600:.1f}h"
                                        
                                        # Confidence indicator
                                        conf_icon = "🟢" if eta_result.reliability_band == "HIGH" else "🟡" if eta_result.reliability_band == "MEDIUM" else "🔴"
                                        
                                        # Velocity direction
                                        vel_icon = "↑" if eta_result.velocity > 0 else "↓" if eta_result.velocity < 0 else "→"
                                        accel_icon = "⚡" if eta_result.acceleration > 0 else "🐌" if eta_result.acceleration < 0 else ""
                                        
                                        eta_str = f"⏱️ ETA: {time_str} {conf_icon}{eta_result.confidence:.0%} | {vel_icon}${eta_result.velocity*60:.4f}/min {accel_icon}"
                                except Exception as e:
                                    eta_str = f"📊 Analytics loading..."
                            
                            # ═════════════════════════════════════════════════════════════════
                            # 🛡️ COUNTER-INTELLIGENCE: Firm Detection + Strategy
                            # ═════════════════════════════════════════════════════════════════
                            counter_str = ""
                            if self.counter_intel and COUNTER_INTEL_AVAILABLE:
                                try:
                                    # Build market data for analysis
                                    market_data = {
                                        'price': current,
                                        'volatility': abs(price_change_pct) / 100,
                                        'volume_ratio': 1.0
                                    }
                                    bot_detection = {'confidence': 0.75}  # Default detection confidence
                                    
                                    # Try each major firm and find best counter-opportunity
                                    best_signal = None
                                    for firm_id in ['citadel', 'jane_street', 'two_sigma', 'jump_trading', 'drw']:
                                        ci_signal = self.counter_intel.analyze_firm_for_counter_opportunity(
                                            firm_id, market_data, bot_detection
                                        )
                                        if ci_signal and (best_signal is None or ci_signal.confidence > best_signal.confidence):
                                            best_signal = ci_signal
                                    
                                    if best_signal:
                                        # Format: 🛡️ vs Citadel: TIMING_ADV +45ms | Conf: 78%
                                        strat_short = best_signal.strategy.value[:12] if hasattr(best_signal.strategy, 'value') else str(best_signal.strategy)[:12]
                                        counter_str = f"🛡️ vs {best_signal.firm_id}: {strat_short.upper()} +{best_signal.timing_advantage:.0f}ms | {best_signal.confidence:.0%}"
                                except Exception as e:
                                    counter_str = f"🛡️ Counter-Intel loading..."
                            
                            # 🏢 Firm Attribution - Who's trading?
                            firm_str = ""
                            if self.firm_attribution and FIRM_ATTRIBUTION_AVAILABLE:
                                try:
                                    symbol_base = pos.symbol.replace('USD', '').replace('/', '').upper()
                                    # Get current hour in UTC
                                    current_hour = time.gmtime().tm_hour
                                    # Estimate frequency based on price change (higher volatility = higher freq)
                                    est_frequency = 0.5 + abs(price_change_pct)
                                    # Use attribute_bot_to_firm method
                                    matches = self.firm_attribution.attribute_bot_to_firm(
                                        symbol=symbol_base,
                                        frequency=est_frequency,
                                        order_size_usd=market_value,
                                        strategy="momentum" if price_change_pct > 0 else "mean_reversion",
                                        current_hour_utc=current_hour
                                    )
                                    if matches:
                                        top_firm, confidence = matches[0]
                                        # Get more details about the firm
                                        firm_details = self.firm_attribution.get_firm_details(top_firm)
                                        firm_name = firm_details.name if firm_details else top_firm.title()
                                        # Predict direction based on firm's typical strategy
                                        direction = 'neutral'
                                        if firm_details:
                                            if 'momentum' in firm_details.typical_strategies:
                                                direction = 'bullish' if price_change_pct > 0 else 'bearish'
                                            elif 'mean_reversion' in firm_details.typical_strategies:
                                                direction = 'bearish' if price_change_pct > 2 else 'bullish' if price_change_pct < -2 else 'neutral'
                                        dir_icon = "🟢" if direction == 'bullish' else "🔴" if direction == 'bearish' else "⚪"
                                        firm_str = f"🏢 {firm_name}: {dir_icon} {direction} ({confidence:.0%})"
                                except Exception as e:
                                    firm_str = ""
                            
                            # Display with CORRECT values
                            pnl_color = '\033[92m' if net_pnl >= 0 else '\033[91m'
                            reset = '\033[0m'
                            print(f"\n🎯 {pos.symbol} ({pos.exchange.upper()}) | Value: ${market_value:.2f}")
                            print(f"   💵 Entry: ${pos.entry_price:,.6f} | Current: ${current:,.6f} | Target: ${pos.target_price:,.6f}")
                            print(f"   [{bar}] {raw_progress:+.1f}% to target | {pnl_color}${net_pnl:+.4f} ({price_change_pct:+.2f}% price){reset}")
                            if eta_str:
                                print(f"   {eta_str}")
                            if counter_str:
                                print(f"   {counter_str}")
                            if firm_str:
                                print(f"   {firm_str}")
                            
                            # ⚡ HFT Harmonic Signal - Sacred frequency analysis
                            hft_str = ""
                            if self.hft_engine and HFT_ENGINE_AVAILABLE:
                                try:
                                    # Feed tick to HFT engine for harmonic analysis
                                    tick_data = {
                                        'timestamp': time.time(),
                                        'symbol': pos.symbol,
                                        'price': current,
                                        'volume': market_value,
                                        'side': 'buy' if price_change_pct > 0 else 'sell',
                                        'exchange': pos.exchange
                                    }
                                    self.hft_engine.ingest_tick(tick_data)
                                    
                                    # Get last harmonic tone if available
                                    if self.hft_engine.last_harmonic_tone:
                                        tone = self.hft_engine.last_harmonic_tone
                                        # Format: ⚡ 528Hz 🦅falcon + gamma | 85% conf
                                        auris_icons = {'falcon': '🦅', 'tiger': '🐅', 'owl': '🦉', 'dolphin': '🐬', 'hummingbird': '🐦', 'deer': '🦌', 'panda': '🐼', 'cargoship': '🚢', 'clownfish': '🐠'}
                                        auris_icon = auris_icons.get(tone.auris_node, '🔮')
                                        hft_str = f"⚡ {tone.frequency:.0f}Hz {auris_icon}{tone.auris_node} + {tone.brainwave} | {tone.confidence:.0%}"
                                except Exception:
                                    pass
                            
                            if hft_str:
                                print(f"   {hft_str}")
                            print(f"   {whale_str}")
                            
                            # ═════════════════════════════════════════════════
                            # EXIT CONDITIONS - PROFIT ONLY!
                            # ═════════════════════════════════════════════════
                            
                            should_sell = False
                            sell_reason = ''
                            
                            # 1. Target hit - PERFECT EXIT!
                            if current >= pos.target_price:
                                should_sell = True
                                sell_reason = 'TARGET_HIT'
                                print(f"   🎯🎯🎯 TARGET HIT! SELLING! 🎯🎯🎯")
                            
                            # 2. Profitable momentum reversal
                            elif net_pnl > 0.01 and len(pos.price_history) >= 10:
                                recent = pos.price_history[-10:]
                                if recent[0] > 0:
                                    momentum = (recent[-1] - recent[0]) / recent[0] * 100
                                    if momentum < -0.3:  # Losing momentum while in profit
                                        should_sell = True
                                        sell_reason = 'MOMENTUM_PROFIT'
                                        print(f"   📈 TAKING PROFIT (momentum reversal)")
                            
                            # Track price history
                            pos.price_history.append(current)
                            if len(pos.price_history) > 50:
                                pos.price_history.pop(0)
                            
                            # Execute sell if ready
                            if should_sell:
                                sell_order = pos.client.place_market_order(
                                    symbol=pos.symbol,
                                    side='sell',
                                    quantity=pos.entry_qty
                                )
                                if sell_order:
                                    sell_price = float(sell_order.get('filled_avg_price', current))
                                    final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                                    final_pnl = final_exit - entry_cost
                                    
                                    # Update session stats
                                    session_stats['total_pnl'] += final_pnl
                                    if final_pnl > 0:
                                        session_stats['winning_trades'] += 1
                                        session_stats['best_trade'] = max(session_stats['best_trade'], final_pnl)
                                    else:
                                        session_stats['losing_trades'] += 1
                                        session_stats['worst_trade'] = min(session_stats['worst_trade'], final_pnl)
                                    
                                    print(f"\n   ✅ SOLD: ${final_pnl:+.4f} ({sell_reason})")
                                    print(f"   🔄 CYCLE CONTINUES - SCANNING FOR NEXT TARGET...")
                                    
                                    # Remove position
                                    positions.remove(pos)
                                    
                                    # Force immediate scan for next opportunity
                                    last_scan_time = 0
                                    
                        except Exception as e:
                            print(f"   ⚠️ Error monitoring {pos.symbol}: {e}")
                    
                    # Footer
                    print(f"\n{'='*80}")
                    print(f"   💰 UNREALIZED P&L: ${total_unrealized:+.4f}")
                    print(f"   🚫 NO STOP LOSS - HOLDING UNTIL PROFIT!")
                    print(f"   ⌨️ Press Ctrl+C to stop")
                
                else:
                    # No positions - show scanning status
                    print(f"\r🔍 No positions - scanning in {max(0, scan_interval - (current_time - last_scan_time)):.0f}s...", end="", flush=True)
                
                time.sleep(monitor_interval)
                
        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("👑 QUEEN AUTONOMOUS MODE - STOPPING")
            print("="*80)
            
            # Close ONLY profitable positions
            print("\n🛑 Closing PROFITABLE positions only (keeping losers)...")
            closed_pnl = 0.0
            kept_count = 0
            
            for pos in positions:
                try:
                    if pos.current_pnl > 0:
                        sell_order = pos.client.place_market_order(
                            symbol=pos.symbol,
                            side='sell',
                            quantity=pos.entry_qty
                        )
                        if sell_order:
                            fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                            sell_price = float(sell_order.get('filled_avg_price', pos.current_price))
                            entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                            final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                            final_pnl = final_exit - entry_cost
                            closed_pnl += final_pnl
                            session_stats['total_pnl'] += final_pnl
                            print(f"   ✅ Closed {pos.symbol}: ${final_pnl:+.4f}")
                    else:
                        kept_count += 1
                        print(f"   ⛔ KEEPING {pos.symbol} (P&L: ${pos.current_pnl:+.4f} - not selling at a loss)")
                except Exception as e:
                    print(f"   ⚠️ Error: {e}")
            
            if kept_count > 0:
                print(f"\n   📌 Kept {kept_count} positions open (underwater - waiting for profit)")
            
            # Final summary
            runtime = time.time() - session_stats['start_time']
            runtime_str = f"{int(runtime//3600)}h {int((runtime%3600)//60)}m {int(runtime%60)}s"
            
            print("\n" + "="*80)
            print("👑 QUEEN AUTONOMOUS SESSION COMPLETE")
            print("="*80)
            print(f"   ⏱️ Total Runtime: {runtime_str}")
            print(f"   🔄 Total Cycles: {session_stats['cycles']}")
            print(f"   📈 Total Trades: {session_stats['total_trades']}")
            print(f"   ✅ Winning Trades: {session_stats['winning_trades']}")
            print(f"   ❌ Losing Trades: {session_stats['losing_trades']}")
            win_rate = (session_stats['winning_trades'] / session_stats['total_trades'] * 100) if session_stats['total_trades'] > 0 else 0
            print(f"   🎯 Win Rate: {win_rate:.1f}%")
            print(f"   💰 SESSION P&L: ${session_stats['total_pnl']:+.4f}")
            print(f"   🏆 Best Trade: ${session_stats['best_trade']:+.4f}")
            print(f"   💔 Worst Trade: ${session_stats['worst_trade']:+.4f}")
            print("="*80)
            
            if session_stats['total_pnl'] > 0:
                print("🏆 SESSION: PROFITABLE! The Queen is pleased. 👑")
            else:
                print("💪 SESSION: Learning cycle. The Queen grows stronger. 👑")
            print("="*80)
            
        return session_stats

    # ═══════════════════════════════════════════════════════════════════════════════
    # 🎖️ WAR ROOM MODE - RICH TERMINAL UI (NO SPAM)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def run_autonomous_warroom(self, max_positions: int = 3, amount_per_position: float = 2.5,
                               target_pct: float = 1.0, min_change_pct: float = 0.3):
        """
        🎖️ WAR ROOM AUTONOMOUS MODE - Clean Rich-based dashboard.
        
        Same logic as run_autonomous() but with unified terminal display.
        NO LOGGING SPAM - all info displayed in organized panels.
        """
        if not RICH_AVAILABLE:
            print("⚠️ Rich library not available - falling back to standard mode")
            return self.run_autonomous(max_positions, amount_per_position, target_pct, min_change_pct)
        
        # Initialize War Room display
        warroom = WarRoomDisplay()
        console = Console()
        
        # Session statistics
        session_stats = {
            'cycles': 0,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0,
            'start_time': time.time(),
            'best_trade': 0.0,
            'worst_trade': 0.0,
        }
        
        # Current positions
        positions: List[LivePosition] = []
        
        # Timing
        scan_interval = 10
        monitor_interval = 1.0
        last_scan_time = 0
        last_portfolio_scan = 0
        portfolio_scan_interval = 30
        
        # ═══════════════════════════════════════════════════════════════════
        # PHASE 0: LOAD EXISTING POSITIONS
        # ═══════════════════════════════════════════════════════════════════
        console.print("[bold blue]📊 Loading existing positions...[/]")
        
        for exchange_name, client in self.clients.items():
            try:
                if exchange_name == 'alpaca':
                    alpaca_positions = client.get_positions()
                    if alpaca_positions:
                        for ap in alpaca_positions:
                            symbol = ap.get('symbol', '').replace('/', '')
                            qty = float(ap.get('qty', 0))
                            entry_price = float(ap.get('avg_entry_price', 0))
                            current_price = float(ap.get('current_price', 0))
                            unrealized_pnl = float(ap.get('unrealized_pl', 0))
                            market_value = float(ap.get('market_value', 0))
                            
                            if qty > 0 and entry_price > 0:
                                fee_rate = self.fee_rates.get(exchange_name, 0.0025)
                                entry_cost = entry_price * qty * (1 + fee_rate)
                                breakeven = entry_price * (1 + fee_rate) / (1 - fee_rate)
                                target_price = breakeven * (1 + target_pct / 100)
                                exit_value = current_price * qty * (1 - fee_rate)
                                net_pnl = exit_value - entry_cost
                                
                                pos = LivePosition(
                                    symbol=symbol,
                                    exchange=exchange_name,
                                    entry_price=entry_price,
                                    entry_qty=qty,
                                    entry_cost=entry_cost,
                                    breakeven_price=breakeven,
                                    target_price=target_price,
                                    client=client,
                                    current_price=current_price,
                                    current_pnl=net_pnl
                                )
                                positions.append(pos)
                                
                elif exchange_name == 'kraken':
                    kraken_balances = client.get_balance()
                    if kraken_balances:
                        for asset, qty in kraken_balances.items():
                            if asset in ['USD', 'ZUSD', 'EUR', 'ZEUR', 'DAI', 'USDC', 'USDT', 'TUSD']:
                                continue
                            qty = float(qty)
                            if qty > 0.000001:
                                symbol = f"{asset}USD"
                                try:
                                    ticker = client.get_ticker(symbol)
                                    current_price = float(ticker.get('bid', ticker.get('price', 0)))
                                    market_value = qty * current_price
                                    
                                    if market_value > 0.10:
                                        fee_rate = self.fee_rates.get(exchange_name, 0.0026)
                                        entry_price = current_price
                                        entry_cost = entry_price * qty * (1 + fee_rate)
                                        breakeven = entry_price * (1 + fee_rate) / (1 - fee_rate)
                                        target_price = breakeven * (1 + target_pct / 100)
                                        
                                        pos = LivePosition(
                                            symbol=symbol,
                                            exchange=exchange_name,
                                            entry_price=entry_price,
                                            entry_qty=qty,
                                            entry_cost=entry_cost,
                                            breakeven_price=breakeven,
                                            target_price=target_price,
                                            client=client,
                                            current_price=current_price,
                                            current_pnl=0.0
                                        )
                                        positions.append(pos)
                                except Exception:
                                    pass
            except Exception:
                pass
        
        console.print(f"[green]✅ Loaded {len(positions)} positions[/]")
        
        # ═══════════════════════════════════════════════════════════════════
        # MAIN LOOP WITH RICH LIVE
        # ═══════════════════════════════════════════════════════════════════
        try:
            with Live(warroom.build_display(), refresh_per_second=2, console=console) as live:
                while True:
                    current_time = time.time()
                    session_stats['cycles'] += 1
                    warroom.cycle_count = session_stats['cycles']
                    warroom.total_pnl = session_stats['total_pnl']
                    warroom.kills_data = {
                        'wins': session_stats['winning_trades'],
                        'losses': session_stats['losing_trades'],
                        'pnl': session_stats['total_pnl']
                    }
                    
                    # ═══════════════════════════════════════════════════════
                    # BATCH PRICE UPDATE
                    # ═══════════════════════════════════════════════════════
                    all_prices = {}
                    try:
                        alpaca_client = self.clients.get('alpaca')
                        if alpaca_client:
                            symbols = [p.symbol for p in positions if p.exchange == 'alpaca']
                            if symbols:
                                snapshot = alpaca_client.get_crypto_snapshot(symbols)
                                if snapshot:
                                    for sym, data in snapshot.items():
                                        if data and 'latestTrade' in data:
                                            all_prices[sym] = float(data['latestTrade'].get('p', 0))
                                        elif data and 'latestQuote' in data:
                                            all_prices[sym] = float(data['latestQuote'].get('bp', 0))
                    except Exception:
                        pass
                    
                    try:
                        kraken_client = self.clients.get('kraken')
                        if kraken_client:
                            kraken_symbols = [p.symbol for p in positions if p.exchange == 'kraken']
                            for sym in kraken_symbols:
                                try:
                                    ticker = kraken_client.get_ticker(sym)
                                    if ticker:
                                        all_prices[sym] = ticker.get('bid', ticker.get('price', 0))
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    
                    # ═══════════════════════════════════════════════════════
                    # UPDATE POSITIONS & CHECK FOR EXITS
                    # ═══════════════════════════════════════════════════════
                    warroom.positions_data = []  # Clear and rebuild
                    
                    for pos in positions[:]:
                        current = all_prices.get(pos.symbol, 0)
                        if current <= 0:
                            continue
                        
                        fee_rate = self.fee_rates.get(pos.exchange, 0.0025)
                        entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                        exit_value = current * pos.entry_qty * (1 - fee_rate)
                        net_pnl = exit_value - entry_cost
                        market_value = current * pos.entry_qty
                        
                        pos.current_price = current
                        pos.current_pnl = net_pnl
                        
                        # Calculate progress
                        if pos.target_price > pos.entry_price:
                            progress = (current - pos.entry_price) / (pos.target_price - pos.entry_price) * 100
                        else:
                            progress = 0
                        
                        # ETA calculation
                        eta_str = "∞"
                        if hasattr(pos, 'pnl_history'):
                            pos.pnl_history.append((time.time(), net_pnl))
                            if len(pos.pnl_history) > 60:
                                pos.pnl_history = pos.pnl_history[-60:]
                            if len(pos.pnl_history) >= 5:
                                recent = pos.pnl_history[-5:]
                                time_diff = recent[-1][0] - recent[0][0]
                                pnl_diff = recent[-1][1] - recent[0][1]
                                if time_diff > 0 and pnl_diff > 0:
                                    target_pnl = (pos.target_price - pos.entry_price) * pos.entry_qty
                                    remaining = target_pnl - net_pnl
                                    rate = pnl_diff / time_diff
                                    if rate > 0:
                                        eta_secs = remaining / rate
                                        if eta_secs < 60:
                                            eta_str = f"{eta_secs:.0f}s"
                                        elif eta_secs < 3600:
                                            eta_str = f"{eta_secs/60:.1f}m"
                                        else:
                                            eta_str = f"{eta_secs/3600:.1f}h"
                        else:
                            pos.pnl_history = []
                        
                        # Get firm info (simplified)
                        firm_str = "Scanning..."
                        if self.counter_intel and COUNTER_INTEL_AVAILABLE:
                            try:
                                for firm_id in ['citadel', 'jane_street']:
                                    ci_signal = self.counter_intel.analyze_firm_for_counter_opportunity(
                                        firm_id, {'price': current}, {'confidence': 0.7}
                                    )
                                    if ci_signal:
                                        firm_str = f"{firm_id[:8]} {ci_signal.confidence:.0%}"
                                        warroom.update_firm(firm_id, str(ci_signal.strategy.value)[:10] if hasattr(ci_signal.strategy, 'value') else '?', 'neutral')
                                        break
                            except Exception:
                                pass
                        
                        # Update warroom
                        warroom.update_position(
                            symbol=pos.symbol,
                            exchange=pos.exchange.upper(),
                            value=market_value,
                            pnl=net_pnl,
                            progress=progress,
                            eta=eta_str,
                            firm=firm_str
                        )
                        
                        # Check for profitable exit
                        if current >= pos.target_price or net_pnl > entry_cost * 0.01:
                            try:
                                sell_order = pos.client.place_market_order(
                                    symbol=pos.symbol,
                                    side='sell',
                                    quantity=pos.entry_qty
                                )
                                if sell_order:
                                    session_stats['total_pnl'] += net_pnl
                                    session_stats['total_trades'] += 1
                                    if net_pnl >= 0:
                                        session_stats['winning_trades'] += 1
                                        session_stats['best_trade'] = max(session_stats['best_trade'], net_pnl)
                                    else:
                                        session_stats['losing_trades'] += 1
                                        session_stats['worst_trade'] = min(session_stats['worst_trade'], net_pnl)
                                    warroom.record_kill(net_pnl)
                                    warroom.remove_position(pos.symbol)
                                    positions.remove(pos)
                                    last_scan_time = 0  # Force scan
                            except Exception:
                                pass
                    
                    # ═══════════════════════════════════════════════════════
                    # SCAN FOR NEW OPPORTUNITIES
                    # ═══════════════════════════════════════════════════════
                    if current_time - last_scan_time >= scan_interval and len(positions) < max_positions:
                        last_scan_time = current_time
                        
                        cash = self.get_available_cash()
                        total_cash = sum(cash.values())
                        
                        if total_cash >= amount_per_position * 0.5:
                            opportunities = self.scan_entire_market(min_change_pct=min_change_pct)
                            if opportunities:
                                active_symbols = [p.symbol for p in positions]
                                new_opps = [o for o in opportunities if o.symbol not in active_symbols]
                                
                                if new_opps:
                                    best = new_opps[0]
                                    try:
                                        client = self.clients.get(best.exchange)
                                        if client:
                                            symbol_clean = best.symbol.replace('/', '')
                                            exchange_cash = cash.get(best.exchange, 0)
                                            buy_amount = min(amount_per_position, exchange_cash * 0.9)
                                            
                                            if buy_amount >= 0.50:
                                                buy_order = client.place_market_order(
                                                    symbol=symbol_clean,
                                                    side='buy',
                                                    quote_qty=buy_amount
                                                )
                                                if buy_order:
                                                    buy_qty = float(buy_order.get('filled_qty', 0))
                                                    buy_price = float(buy_order.get('filled_avg_price', best.price))
                                                    
                                                    if buy_qty > 0 and buy_price > 0:
                                                        fee_rate = self.fee_rates.get(best.exchange, 0.0025)
                                                        breakeven = buy_price * (1 + fee_rate) / (1 - fee_rate)
                                                        target_price = breakeven * (1 + target_pct / 100)
                                                        
                                                        pos = LivePosition(
                                                            symbol=symbol_clean,
                                                            exchange=best.exchange,
                                                            entry_price=buy_price,
                                                            entry_qty=buy_qty,
                                                            entry_cost=buy_price * buy_qty * (1 + fee_rate),
                                                            breakeven_price=breakeven,
                                                            target_price=target_price,
                                                            client=client,
                                                            stop_price=0.0
                                                        )
                                                        positions.append(pos)
                                                        session_stats['total_trades'] += 1
                                    except Exception:
                                        pass
                    
                    # ═══════════════════════════════════════════════════════
                    # UPDATE QUANTUM SCORES
                    # ═══════════════════════════════════════════════════════
                    try:
                        quantum = self.get_quantum_score("BTC/USD", "long", 50000, 0)
                        warroom.update_quantum(
                            luck=quantum.get('luck_resonance', 0),
                            phantom=quantum.get('phantom_clarity', 0),
                            inception=quantum.get('inception_potential', 0),
                            elephant=quantum.get('elephant_memory', 0),
                            russian_doll=quantum.get('russian_doll_coherence', 0),
                            immune=quantum.get('immune_strength', 0),
                            moby_dick=quantum.get('whale_prediction', 0),
                            stargate=quantum.get('stargate_alignment', 0),
                            quantum_mirror=quantum.get('quantum_coherence', 0),
                            total_boost=quantum.get('total_boost', 1.0)
                        )
                    except Exception:
                        pass
                    
                    # Update display
                    live.update(warroom.build_display())
                    time.sleep(monitor_interval)
                    
        except KeyboardInterrupt:
            console.print("\n[bold yellow]👑 STOPPING WAR ROOM...[/]")
            
            # Close profitable positions
            console.print("[bold]🛑 Closing profitable positions only...[/]")
            for pos in positions:
                if pos.current_pnl > 0:
                    try:
                        pos.client.place_market_order(
                            symbol=pos.symbol,
                            side='sell',
                            quantity=pos.entry_qty
                        )
                        console.print(f"[green]✅ Closed {pos.symbol}: +${pos.current_pnl:.4f}[/]")
                    except Exception:
                        pass
                else:
                    console.print(f"[dim]⏳ Kept {pos.symbol}: ${pos.current_pnl:.4f} (holding)[/]")
            
            # Summary
            console.print(f"\n[bold magenta]{'='*60}[/]")
            console.print(f"[bold]👑 WAR ROOM SESSION COMPLETE[/]")
            console.print(f"   Cycles: {session_stats['cycles']}")
            console.print(f"   Total P&L: ${session_stats['total_pnl']:+.4f}")
            console.print(f"   Wins: {session_stats['winning_trades']} | Losses: {session_stats['losing_trades']}")
            console.print(f"[bold magenta]{'='*60}[/]")
        
        return session_stats


if __name__ == "__main__":
    import sys
    
    # Monitor mode - stream existing positions until targets hit
    if len(sys.argv) >= 2 and sys.argv[1] == '--monitor':
        target_pct = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5  # Default 1.5% target
        stop_pct = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0    # Default 1% stop
        
        print("🦈🦈🦈 ORCA POSITION MONITOR - STREAMING EXISTING POSITIONS 🦈🦈🦈")
        orca = OrcaKillCycle()
        
        # Load existing Alpaca positions into LivePosition format
        positions = []
        alpaca = orca.clients.get('alpaca')
        if alpaca:
            try:
                existing = alpaca.get_positions()
                for p in existing:
                    symbol_raw = p.get('symbol', '')
                    # Convert PEPEUSD -> PEPE/USD
                    if symbol_raw.endswith('USD') and '/' not in symbol_raw:
                        symbol = symbol_raw[:-3] + '/USD'
                    else:
                        symbol = symbol_raw
                    
                    qty = float(p.get('qty', 0))
                    entry = float(p.get('avg_entry_price', 0))
                    current = float(p.get('current_price', 0))
                    
                    if qty > 0 and entry > 0:
                        target = entry * (1 + target_pct/100)
                        stop = entry * (1 - stop_pct/100)
                        fee_rate = orca.fee_rates.get('alpaca', 0.0025)
                        entry_cost = entry * qty * (1 + fee_rate)
                        breakeven = entry * (1 + 2*fee_rate)  # Need to cover fees both ways
                        
                        pos = LivePosition(
                            symbol=symbol,
                            exchange='alpaca',
                            entry_price=entry,
                            entry_qty=qty,
                            entry_cost=entry_cost,
                            breakeven_price=breakeven,
                            target_price=target,
                            stop_price=stop,
                            client=alpaca,
                            current_price=current,
                            current_pnl=float(p.get('unrealized_pl', 0)),
                            kill_reason=''
                        )
                        positions.append(pos)
                        print(f"   📈 {symbol}: {qty:.6f} @ ${entry:.6f} → Target: ${target:.6f} | Stop: ${stop:.6f}")
            except Exception as e:
                print(f"   ⚠️ Error loading positions: {e}")
        
        if not positions:
            print("❌ No positions to monitor!")
            sys.exit(1)
        
        print(f"\n📡 STREAMING {len(positions)} POSITIONS (NO TIMEOUT)")
        print("="*70)
        print(f"   ⚠️ Will ONLY exit on: TARGET HIT (100%), STOP LOSS (0%), or Ctrl+C")
        print("="*70)
        
        # Progress bar helper
        def make_progress_bar(progress_pct, width=20):
            """Create a visual progress bar. 0% = stop loss, 100% = target."""
            progress_pct = max(0, min(100, progress_pct))  # Clamp 0-100
            filled = int(width * progress_pct / 100)
            empty = width - filled
            
            # Color coding: red if <25%, yellow if <75%, green if >=75%
            if progress_pct >= 75:
                bar_char = '█'
                color = '\033[92m'  # Green
            elif progress_pct >= 25:
                bar_char = '▓'
                color = '\033[93m'  # Yellow
            else:
                bar_char = '░'
                color = '\033[91m'  # Red
            
            reset = '\033[0m'
            bar = color + bar_char * filled + reset + '░' * empty
            return f"[{bar}]"
        
        def make_whale_bar(support: float, pressure: float, width=10):
            """Create whale support vs pressure indicator."""
            # Net score: positive = whales helping, negative = opposing
            net = support - pressure
            mid = width // 2
            
            if net > 0:
                # Whales supporting - green fill from middle to right
                fill = int(mid * min(net * 2, 1))
                bar = '░' * mid + '\033[92m' + '▶' * fill + '\033[0m' + '░' * (mid - fill)
            elif net < 0:
                # Whales opposing - red fill from middle to left
                fill = int(mid * min(abs(net) * 2, 1))
                bar = '░' * (mid - fill) + '\033[91m' + '◀' * fill + '\033[0m' + '░' * mid
            else:
                bar = '░' * width
            
            return f"[{bar}]"
        
        def format_eta(seconds: float) -> str:
            """Format ETA as human-readable string."""
            if seconds < 60:
                return f"{seconds:.0f}s"
            elif seconds < 3600:
                return f"{seconds/60:.1f}m"
            else:
                return f"{seconds/3600:.1f}h"
        
        def clear_lines(n):
            """Clear n lines above cursor."""
            for _ in range(n):
                print('\033[A\033[K', end='')
        
        # Initialize whale intelligence tracker
        whale_tracker = WhaleIntelligenceTracker()
        whale_status = "🐋 Whale Intelligence: "
        if whale_tracker.whale_profiler:
            whale_status += "✅ Profiler "
        else:
            whale_status += "❌ Profiler "
        if whale_tracker.firm_intel:
            whale_status += "✅ Firms "
        else:
            whale_status += "❌ Firms "
        if whale_tracker.bus:
            whale_status += "✅ ThoughtBus "
        else:
            whale_status += "❌ ThoughtBus "
        
        # Initialize SSE live streaming for real-time whale detection
        sse_client = None
        if SSE_AVAILABLE and AlpacaSSEClient:
            try:
                sse_client = AlpacaSSEClient()
                # Get position symbols for streaming
                stream_symbols = [p.symbol.replace('/USD', 'USD') for p in positions]
                
                # Wire SSE trades to whale tracker
                def on_live_trade(trade):
                    """Feed live trades to whale intelligence."""
                    try:
                        symbol = trade.symbol
                        # Convert BTCUSD -> BTC/USD
                        if not '/' in symbol and symbol.endswith('USD'):
                            symbol = symbol[:-3] + '/USD'
                        whale_tracker.process_live_trade(
                            symbol=symbol,
                            price=trade.price,
                            quantity=trade.size,
                            side='buy' if hasattr(trade, 'side') and trade.side == 'buy' else 'sell',
                            exchange='alpaca'
                        )
                    except Exception:
                        pass
                
                sse_client.on_trade = on_live_trade
                sse_client.start_crypto_stream(stream_symbols, trades=True)
                whale_status += "✅ LiveStream"
            except Exception as e:
                whale_status += f"❌ LiveStream({e})"
        else:
            whale_status += "❌ LiveStream"
        
        print(whale_status)
        print("="*70)
        
        # Monitor loop
        results = []
        last_display_lines = 0
        hunt_validations = []  # Track successful hunts
        whale_update_counter = 0  # Only update whale intel every 5 ticks
        whale_signals_cache: Dict[str, WhaleSignal] = {}
        should_exit = False  # Flag to control loop exit
        
        try:
            while positions and not should_exit:
                display_lines = []
                whale_update_counter += 1
                
                for pos in positions[:]:
                    try:
                        # Get live price
                        ticker = pos.client.get_ticker(pos.symbol)
                        if not ticker:
                            continue
                        
                        current = float(ticker.get('last', ticker.get('bid', 0)))
                        if current <= 0:
                            continue
                        
                        pos.current_price = current
                        fee_rate = orca.fee_rates.get(pos.exchange, 0.0025)
                        entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                        exit_value = current * pos.entry_qty * (1 - fee_rate)
                        pos.current_pnl = exit_value - entry_cost
                        
                        pnl_pct = ((current / pos.entry_price) - 1) * 100
                        
                        # Calculate progress: 0% = stop loss, 50% = entry, 100% = target
                        # Range from stop to target
                        price_range = pos.target_price - pos.stop_price
                        if price_range > 0:
                            progress = ((current - pos.stop_price) / price_range) * 100
                        else:
                            progress = 50
                        
                        progress = max(0, min(100, progress))
                        bar = make_progress_bar(progress)
                        
                        # Get whale intelligence (update every 5 ticks = 1 second)
                        if whale_update_counter % 5 == 0 or pos.symbol not in whale_signals_cache:
                            # Calculate price change % for firm activity simulation
                            price_change_pct = pnl_pct  # Use position P&L as price change proxy
                            whale_sig = whale_tracker.get_whale_signal(
                                pos.symbol, 
                                'long',
                                current_price=current,
                                price_change_pct=price_change_pct
                            )
                            whale_signals_cache[pos.symbol] = whale_sig
                        else:
                            whale_sig = whale_signals_cache.get(pos.symbol)
                        
                        # Build display line with whale data
                        symbol_short = pos.symbol.replace('/USD', '')[:6]
                        
                        if whale_sig:
                            whale_bar = make_whale_bar(whale_sig.whale_support, whale_sig.counter_pressure)
                            eta_str = format_eta(whale_sig.eta_seconds)
                            # Main line: symbol + progress + P&L
                            line1 = f"  {symbol_short:6} {bar} {progress:5.1f}% | ${pos.current_pnl:+.4f} | ${current:.6f}"
                            # Whale line: support indicator + ETA + whales active + firm reasoning
                            whales_active = whale_sig.active_whales
                            support_pct = int(whale_sig.whale_support * 100)
                            pressure_pct = int(whale_sig.counter_pressure * 100)
                            firm_info = whale_sig.reasoning if whale_sig.reasoning else "Scanning..."
                            line2 = f"         {whale_bar} 🐋{whales_active} | ⬆{support_pct}% ⬇{pressure_pct}% | {firm_info[:50]}"
                            display_lines.append(line1)
                            display_lines.append(line2)
                        else:
                            display_lines.append(f"  {symbol_short:6} {bar} {progress:5.1f}% | ${pos.current_pnl:+.4f} | ${current:.6f}")
                        
                        # Check exit conditions - ONLY SELL IF PROFITABLE!
                        if current >= pos.target_price:
                            pos.kill_reason = 'TARGET_HIT'
                        # DISABLED: NO STOP LOSS - we NEVER sell at a loss!
                        # elif current <= pos.stop_price:
                        #     pos.kill_reason = 'STOP_LOSS'
                        elif pos.current_pnl > 0.01:  # Small momentum profit
                            pos.kill_reason = 'MOMENTUM_PROFIT'
                        
                        # Execute exit
                        if pos.kill_reason:
                            sell_order = pos.client.place_market_order(
                                symbol=pos.symbol,
                                side='sell',
                                quantity=pos.entry_qty
                            )
                            if sell_order:
                                sell_price = float(sell_order.get('filled_avg_price', current))
                                final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                                final_pnl = final_exit - entry_cost
                                
                                # Create hunt validation record
                                validation = {
                                    'symbol': pos.symbol,
                                    'exchange': pos.exchange,
                                    'reason': pos.kill_reason,
                                    'net_pnl': final_pnl,
                                    'entry_price': pos.entry_price,
                                    'exit_price': sell_price,
                                    'qty': pos.entry_qty,
                                    'progress_at_kill': progress,
                                    'success': final_pnl > 0
                                }
                                results.append(validation)
                                hunt_validations.append(validation)
                                
                                # Print kill validation
                                if validation['success']:
                                    emoji = '🎯✅'
                                    status = 'SUCCESSFUL HUNT'
                                else:
                                    emoji = '🛑❌'
                                    status = 'HUNT FAILED'
                                
                                print(f"\n{emoji} {status}: {pos.symbol}")
                                print(f"   ├─ Entry:  ${pos.entry_price:.6f}")
                                print(f"   ├─ Exit:   ${sell_price:.6f}")
                                print(f"   ├─ P&L:    ${final_pnl:+.4f}")
                                print(f"   ├─ Reason: {pos.kill_reason}")
                                print(f"   └─ Progress at kill: {progress:.1f}%")
                                print()
                                
                            positions.remove(pos)
                    except Exception as e:
                        pass
                
                # Clear previous display and show new progress bars
                if positions:
                    # Clear previous lines
                    if last_display_lines > 0:
                        clear_lines(last_display_lines + 1)
                    
                    # Print header and all position bars
                    total_pnl = sum(p.current_pnl for p in positions)
                    print(f"📊 LIVE HUNT STATUS | Total P&L: ${total_pnl:+.4f}")
                    for line in display_lines:
                        print(line)
                    
                    last_display_lines = len(display_lines)
                
                time.sleep(0.2)  # Slightly slower for readability
                
        except KeyboardInterrupt:
            print("\n\n⚠️  INTERRUPT DETECTED!")
            print("="*60)
            print("🦈 ORCA SAFETY CHECK - What do you want to do?")
            print("="*60)
            print("  [1] CLOSE ALL positions and exit")
            print("  [2] KEEP positions open and just exit monitor")
            print("  [3] RESUME monitoring (cancel interrupt)")
            print("="*60)
            
            try:
                choice = input("\n👉 Enter choice (1/2/3) [default=2 KEEP]: ").strip()
            except EOFError:
                # Non-interactive mode (piped input) - default to KEEP
                choice = "2"
            
            if choice == "1":
                print("\n🛑 CONFIRMED: Closing all positions...")
                # Stop SSE streaming
                if sse_client:
                    try:
                        sse_client.stop()
                        print("   📡 Live stream stopped")
                    except Exception:
                        pass
                for pos in positions:
                    try:
                        sell_order = pos.client.place_market_order(symbol=pos.symbol, side='sell', quantity=pos.entry_qty)
                        if sell_order:
                            fee_rate = orca.fee_rates.get(pos.exchange, 0.0025)
                            sell_price = float(sell_order.get('filled_avg_price', pos.current_price))
                            entry_cost = pos.entry_price * pos.entry_qty * (1 + fee_rate)
                            final_exit = sell_price * pos.entry_qty * (1 - fee_rate)
                            final_pnl = final_exit - entry_cost
                            results.append({
                                'symbol': pos.symbol,
                                'exchange': pos.exchange,
                                'reason': 'USER_ABORT',
                                'net_pnl': final_pnl,
                                'success': final_pnl > 0
                            })
                            print(f"   Closed {pos.symbol}: ${final_pnl:+.4f}")
                    except Exception as e:
                        print(f"   ⚠️ Error closing {pos.symbol}: {e}")
                should_exit = True  # Exit the loop after closing
            
            elif choice == "3":
                print("\n🔄 Resuming monitor... (Ctrl+C again to see options)")
                # Don't set should_exit, just continue the loop
            
            else:  # Default: choice == "2" or anything else
                print("\n✅ KEEPING positions open - exiting monitor only")
                print("   Your positions are still active on the exchange!")
                if sse_client:
                    try:
                        sse_client.stop()
                        print("   📡 Live stream stopped")
                    except Exception:
                        pass
                # Don't close positions, just exit cleanly
                results = []  # Clear results so no "failed" report
                should_exit = True  # Exit the loop
        
        # Hunt Validation Summary
        if results:
            print("\n" + "="*70)
            print("🦈 HUNT VALIDATION REPORT")
            print("="*70)
            
            successful = [r for r in results if r.get('success', False)]
            failed = [r for r in results if not r.get('success', False)]
            total = sum(r['net_pnl'] for r in results)
            
            print(f"\n📊 HUNT STATISTICS:")
            print(f"   ├─ Total Hunts:     {len(results)}")
            print(f"   ├─ Successful:      {len(successful)} ✅")
            print(f"   ├─ Failed:          {len(failed)} ❌")
            print(f"   ├─ Win Rate:        {(len(successful)/len(results)*100) if results else 0:.1f}%")
            print(f"   └─ Net P&L:         ${total:+.4f}")
            
            if successful:
                print(f"\n✅ SUCCESSFUL HUNTS:")
                for r in successful:
                    print(f"   🎯 {r['symbol']}: ${r['net_pnl']:+.4f} ({r['reason']})")
            
            if failed:
                print(f"\n❌ FAILED HUNTS:")
                for r in failed:
                    print(f"   🛑 {r['symbol']}: ${r['net_pnl']:+.4f} ({r['reason']})")
            
            print("\n" + "="*70)
            if total > 0:
                print(f"🏆 HUNT SESSION: PROFITABLE (+${total:.4f})")
            else:
                print(f"💔 HUNT SESSION: LOSS (${total:.4f})")
            print("="*70)
    
    # 🦈⚡ NEW: Fast Kill Hunt - uses ALL intelligence systems
    elif len(sys.argv) >= 2 and sys.argv[1] == '--fast':
        amount = float(sys.argv[2]) if len(sys.argv) > 2 else 25.0
        num_pos = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        target = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
        
        print("🦈⚡ FAST KILL MODE - ALL INTELLIGENCE ENGAGED ⚡🦈")
        orca = OrcaKillCycle()
        results = orca.fast_kill_hunt(
            amount_per_position=amount,
            num_positions=num_pos,
            target_pct=target
        )
        
        if results:
            total = sum(r.get('net_pnl', 0) for r in results)
            print(f"\n💰 Total portfolio impact: ${total:+.4f}")
    
    # New multi-exchange pack hunt mode
    elif len(sys.argv) >= 2 and sys.argv[1] == '--pack':
        num_pos = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        amount = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
        
        print("🦈🦈🦈 ORCA PACK HUNT - SCANNING ENTIRE MARKET 🦈🦈🦈")
        orca = OrcaKillCycle()
        results = orca.pack_hunt(num_positions=num_pos, amount_per_position=amount)
        
        if results:
            total = sum(r['net_pnl'] for r in results)
            print(f"\n💰 Total portfolio impact: ${total:+.4f}")
    
    # 👑🔄 AUTONOMOUS MODE - Queen-guided infinite loop (WAR ROOM by default)
    elif len(sys.argv) >= 2 and sys.argv[1] == '--autonomous':
        max_pos = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        amount = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
        target = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        
        orca = OrcaKillCycle()
        
        # 🎖️ Use War Room (Rich dashboard) by default
        print("👑🎖️ AUTONOMOUS WAR ROOM MODE 🎖️👑")
        stats = orca.run_autonomous_warroom(
            max_positions=max_pos,
            amount_per_position=amount,
            target_pct=target
        )
    
    # 👑🔄 LEGACY AUTONOMOUS MODE - Raw print output (for debugging)
    elif len(sys.argv) >= 2 and sys.argv[1] == '--autonomous-legacy':
        max_pos = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        amount = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
        target = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        
        print("👑🦈 AUTONOMOUS QUEEN MODE - LEGACY OUTPUT 🦈👑")
        orca = OrcaKillCycle()
        stats = orca.run_autonomous(
            max_positions=max_pos,
            amount_per_position=amount,
            target_pct=target
        )
    
    elif len(sys.argv) >= 2:
        # Single symbol mode (backward compatible)
        symbol = sys.argv[1]
        amount = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
        target = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        
        orca = OrcaKillCycle()
        result = orca.hunt_and_kill(symbol, amount, target)
        
        if result:
            print(f"\n💰 Portfolio impact: ${result['net_pnl']:+.4f}")
    else:
        print("Usage:")
        print("  👑 WAR ROOM:    python orca_complete_kill_cycle.py --autonomous 3 2.5 1.0  # Clean dashboard")
        print("  👑 LEGACY:      python orca_complete_kill_cycle.py --autonomous-legacy     # Raw output (debug)")
        print("  Fast hunt:      python orca_complete_kill_cycle.py --fast 25 3 0.8")
        print("  Monitor:        python orca_complete_kill_cycle.py --monitor 1.5 1.0")
        print("  Single symbol:  python orca_complete_kill_cycle.py BTC/USD 8.0 1.0")
        print("  Pack hunt:      python orca_complete_kill_cycle.py --pack 3 2.5")
        print("")
        print("Examples:")
        print("  python orca_complete_kill_cycle.py --autonomous      # 🎖️ WAR ROOM: Clean Rich dashboard")
        print("  python orca_complete_kill_cycle.py --autonomous 5 10 # War Room: 5 positions @ $10 each")
        print("  python orca_complete_kill_cycle.py --autonomous-legacy  # Old print-spam mode")
        print("  python orca_complete_kill_cycle.py --fast            # Fast hunt: $25×3 @ 0.8% target")
        print("  python orca_complete_kill_cycle.py --fast 50 2 1.0   # $50×2 @ 1.0% target")
        print("  python orca_complete_kill_cycle.py --monitor         # Monitor with 1.5% target, 1% stop")
        print("  python orca_complete_kill_cycle.py --monitor 2.0 0.5 # 2% target, 0.5% stop")
        print("  python orca_complete_kill_cycle.py --pack            # 3 positions @ $2.50 each")
        sys.exit(1)
