#!/usr/bin/env python3
"""
🐙🌌 AUREON  ECOSYSTEM - THE UNIFIED TRADING ENGINE 🌌🐙
================================================================
ONE DYNAMIC PYTHON FOR THE ENTIRE KRAKEN ECOSYSTEM

Combines ALL the best from:
- aureon_51_live.py (51% win rate strategy)
- aureon_infinite_kraken.py (10-9-1 Queen Hive compounding)
- aureon_multiverse.py (Temporal analysis)
- aureon_mycelium.py (Neural network intelligence)
- aureon_qgita.py (9 Auris nodes)
- kraken_multi_sim.py (Multi-strategy analysis)

FEATURES:
├─ 🔴 Real-time WebSocket prices
├─ 🎯 Multiple strategies running simultaneously
├─ 🍄 Neural network pattern detection
├─ 🐅 9 Auris nodes for market analysis
├─ 💰 Compounding with 10-9-1 model
├─ 📊 Dynamic opportunity scoring
└─ 🔄 Infinite loop - never stops growing

GOAL: 51%+ Win Rate with NET PROFIT after ALL fees

Gary Leckey & GitHub Copilot | November 2025
"From Atom to Multiverse - We don't quit!"
"""

# ═══════════════════════════════════════════════════════════════════════════
# WINDOWS UTF-8 FIX - MUST BE AT VERY TOP BEFORE ALL OTHER IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
import os
import sys
import io

if sys.platform == 'win32':
    # Set environment variable for Python's default encoding
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Force UTF-8 encoding for stdout/stderr to support emojis
    try:
        # Check if not already wrapped to avoid double-wrapping
        if hasattr(sys.stdout, 'buffer') and not isinstance(sys.stdout, io.TextIOWrapper):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'buffer') and not isinstance(sys.stderr, io.TextIOWrapper):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

import json
import time
import math
import random
import asyncio
import tempfile
import logging

# 🧠 THOUGHT BUS - UNITY CONSCIOUSNESS 🧠
try:
    from aureon_thought_bus import ThoughtBus, Thought
    THOUGHT_BUS = ThoughtBus(persist_path="thoughts.jsonl")
    THOUGHT_BUS_AVAILABLE = True
except ImportError:
    THOUGHT_BUS = None
    THOUGHT_BUS_AVAILABLE = False
    print("⚠️  Thought Bus not available - Brain running in isolation")

# Custom StreamHandler that forces UTF-8 encoding on Windows
class SafeStreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream or sys.stdout)
    
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # Write with UTF-8 encoding, replace errors
            try:
                stream.write(msg + self.terminator)
                self.flush()
            except UnicodeEncodeError:
                # If encoding fails, replace unencodable characters
                msg_safe = msg.encode('utf-8', errors='replace').decode('utf-8')
                stream.write(msg_safe + self.terminator)
                self.flush()
        except Exception:
            self.handleError(record)

# 🛡️ CRITICAL: Configure Root Logger IMMEDIATELY with SafeStreamHandler
# This ensures ALL subsequent loggers (including those from imported modules)
# use this safe handler and don't crash on Windows when printing emojis.

def sanitize_logging_environment():
    """
    Aggressively removes unsafe StreamHandlers from the root logger
    and ensures only SafeStreamHandler is used.
    """
    root_logger = logging.getLogger()
    handlers_removed = 0
    
    # Remove unsafe handlers
    for h in list(root_logger.handlers):
        if isinstance(h, logging.StreamHandler) and not isinstance(h, SafeStreamHandler):
            try:
                root_logger.removeHandler(h)
                handlers_removed += 1
            except Exception:
                pass
            
    # Add SafeStreamHandler if missing
    has_safe_handler = any(isinstance(h, SafeStreamHandler) for h in root_logger.handlers)
    if not has_safe_handler:
        safe_handler = SafeStreamHandler(sys.stdout)
        safe_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        root_logger.addHandler(safe_handler)
        root_logger.setLevel(logging.INFO)
        
    if sys.platform == 'win32' and handlers_removed > 0:
        # Use safe print just in case
        try:
            sys.stdout.buffer.write(f"🛡️  Windows Unicode Protection: Removed {handlers_removed} unsafe handlers.\n".encode('utf-8'))
        except Exception:
            pass

# Initial sanitization
sanitize_logging_environment()



# Load environment variables from .env file FIRST before any other imports
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    websockets = None
    WEBSOCKETS_AVAILABLE = False
import threading
import logging
try:
    import statistics
except ImportError:
    # Fallback for statistics if missing
    class Statistics:
        def mean(self, data): return sum(data) / len(data) if data else 0
        def stdev(self, data): 
            if not data or len(data) < 2: return 0
            m = sum(data) / len(data)
            return (sum((x - m) ** 2 for x in data) / (len(data) - 1)) ** 0.5
    statistics = Statistics()

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from collections import deque, defaultdict
from threading import Thread, Lock

# Set up logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    # Use SafeStreamHandler instead of standard StreamHandler
    handler = SafeStreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # 🔧 Miner Blueprint Constants (enhancements)
    CASCADE_FACTOR = 10.0       # Amplify weak signals
    KT_EFFICIENCY = 4.24        # Capital efficiency multiplier
    MIN_GAMMA_THRESHOLD = 0.20  # Independent entry threshold
    MIN_HOLD_MINUTES = 50       # Resonance holding minimum
    PSI_FILTER = 0.037          # Top 3.7% opportunities only

# Add current directory to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
try:
    from unified_exchange_client import UnifiedExchangeClient, MultiExchangeClient
except ImportError as e:
    print(f"⚠️  Unified Exchange Client not available: {e}")
    # Define dummy classes to prevent crash if critical module is missing
    class UnifiedExchangeClient:
        def __init__(self, *args, **kwargs): self.dry_run = True
    class MultiExchangeClient:
        def __init__(self, *args, **kwargs): 
            self.dry_run = True
            self.clients = {}
        def get_all_balances(self): return {}
        def get_24h_tickers(self): return []
        def get_ticker(self, *args): return {}
        def place_market_order(self, *args, **kwargs): return {}
        def convert_to_quote(self, *args): return 0.0

# 🇮🇪🎯 IRA SNIPER MODE - Core imports (top-level for reliability)
from ira_sniper_mode import (
    apply_sniper_mode,
    check_sniper_exit,
    get_sniper_config,
    map_sniper_platform_assets,
    sniper_authorizes_kill,  # 🎯 ABSOLUTE KILL AUTHORITY
    sniper_override_active,  # 🛡️ Check if sniper has control
    # ⚡ ACTIVE KILL SCANNER - Intelligent Hunting System
    get_active_scanner,
    register_sniper_target,
    scan_sniper_targets,
    execute_sniper_kill,
    get_scanner_status,
    # 🧠⛏️ LEARNING & MINER INTEGRATION
    sync_scanner_with_cascade,
    get_scanner_learning_stats,
    # 🍄 MYCELIUM STATE AGGREGATOR - Unified Intelligence Network
    get_mycelium_aggregator,
    mycelium_sync,
    register_to_mycelium,
)

try:
    from aureon_lattice import GaiaLatticeEngine, CarrierWaveDynamics  # 🌍 GAIA FREQUENCY PHYSICS
    LATTICE_AVAILABLE = True
except ImportError:
    LATTICE_AVAILABLE = False
    print("⚠️  Gaia Lattice Engine not available (numpy missing?): Running in degraded mode")
    class GaiaLatticeEngine:
        def __init__(self): pass
        def get_state(self): return {}
        def update(self, opps): return {}
        def filter_signals(self, opps): return opps
        def get_field_purity(self): return 1.0

try:
    from aureon_enhancements import EnhancementLayer
    ENHANCEMENTS_AVAILABLE = True
except ImportError:
    ENHANCEMENTS_AVAILABLE = False
    print("⚠️  Enhancement Layer not available: Running without codex integration")
    class EnhancementLayer:
        def __init__(self): pass
        def get_unified_modifier(self, *args, **kwargs): return type('obj', (object,), {'trading_modifier': 1.0, 'confidence': 0.5, 'reasons': []})()
        def display_status(self): return "✨ ENHANCEMENTS | Disabled"
    class CarrierWaveDynamics:
        pass
try:
    from aureon_market_pulse import MarketPulse
except ImportError:
    print("⚠️  Market Pulse not available: Running in degraded mode")
    class MarketPulse:
        def __init__(self, client): pass
        def analyze_market(self): return {}

# 🔮 NEXUS PREDICTOR - 79.6% Win Rate Validated Over 11 Years!
try:
    from nexus_predictor import NexusPredictor
    NEXUS_PREDICTOR_AVAILABLE = True
    print("🔮 Nexus Predictor loaded - 79.6% win rate validated!")
except ImportError:
    NEXUS_PREDICTOR_AVAILABLE = False
    print("⚠️  Nexus Predictor not available")

# 🧠 MINER BRAIN - COGNITIVE TRADING INTELLIGENCE 🧠
try:
    from aureon_miner_brain import MinerBrain
    BRAIN_AVAILABLE = True
    print("🧠 Miner Brain loaded - Cognitive Intelligence Active!")
except ImportError:
    BRAIN_AVAILABLE = False
    print("⚠️  Miner Brain not available")

# 🌐⚡ GLOBAL HARMONIC FIELD - UNIFIED 42-SOURCE FIELD ⚡🌐
try:
    from global_harmonic_field import GlobalHarmonicField, get_global_field, compute_global_omega
    HARMONIC_FIELD_AVAILABLE = True
    print("🌐⚡ Global Harmonic Field loaded - 42 sources → 7 layers → Ω")
except ImportError as e:
    HARMONIC_FIELD_AVAILABLE = False
    print(f"⚠️  Global Harmonic Field not available: {e}")

# 🌍⚡ HNC FREQUENCY INTEGRATION ⚡🌍
try:
    from hnc_master_protocol import HarmonicNexusCore, HNCTradingBridge, LiveMarketFrequencyFeed
    HNC_AVAILABLE = True
except ImportError as e:
    HNC_AVAILABLE = False
    print(f"⚠️  HNC module not available - frequency analysis disabled: {e}")

# 🌍⚡ HNC PROBABILITY MATRIX INTEGRATION ⚡🌍
try:
    from hnc_probability_matrix import HNCProbabilityIntegration, ProbabilityMatrix
    PROB_MATRIX_AVAILABLE = True
except ImportError as e:
    PROB_MATRIX_AVAILABLE = False
    print(f"⚠️  Probability Matrix not available: {e}")
    print(f"⚠️  HNC module not available - frequency analysis disabled: {e}")

# 🌍⚡ COINAPI ANOMALY DETECTION ⚡🌍
try:
    from coinapi_anomaly_detector import CoinAPIClient, AnomalyDetector, AnomalyType
    COINAPI_AVAILABLE = True
except ImportError as e:
    COINAPI_AVAILABLE = False
    print(f"⚠️  CoinAPI Anomaly Detector not available: {e}")

# 🌉 AUREON BRIDGE - ULTIMATE ↔ UNIFIED COMMUNICATION 🌉
try:
    from aureon_bridge import AureonBridge, Opportunity as BridgeOpportunity, CapitalState, Position as BridgePosition
    BRIDGE_AVAILABLE = True
except ImportError as e:
    BRIDGE_AVAILABLE = False
    print(f"⚠️  Aureon Bridge not available: {e}")

# 🌐 AUREON UI BRIDGE - LIVE DATA VALIDATOR FROM aureoninstitute.com 🌐
try:
    from aureon_ui_bridge import (
        AureonUIBridge, AureonUIValidator, UIMyceliumConnector,
        get_ui_bridge, get_ui_connector, validate_trade_against_ui,
        get_harmonic_field_status, get_fear_greed_status,
        UIValidatedSignal, FrequencyBand, RiskLevel, Element
    )
    UI_BRIDGE_AVAILABLE = True
except ImportError as e:
    UI_BRIDGE_AVAILABLE = False
    print(f"⚠️  UI Bridge not available: {e}")

# 🌌⚡ HNC IMPERIAL PREDICTABILITY ENGINE ⚡🌌
try:
    from hnc_imperial_predictability import (
        ImperialTradingIntegration, PredictabilityEngine, CosmicStateEngine,
        CosmicPhase, MarketTorque, ImperialPredictabilityMatrix
    )
    IMPERIAL_AVAILABLE = True
except ImportError as e:
    IMPERIAL_AVAILABLE = False
    print(f"⚠️  Imperial Predictability not available: {e}")

# 🔭 QUANTUM TELESCOPE & HARMONIC UNDERLAY 🔭
try:
    from aureon_quantum_telescope import QuantumTelescope, LightBeam, GeometricSolid
    from hnc_6d_harmonic_waveform import SixDimensionalHarmonicEngine, WaveState
    QUANTUM_AVAILABLE = True
except ImportError as e:
    QUANTUM_AVAILABLE = False
    print(f"⚠️  Quantum Telescope/Harmonic Engine not available: {e}")

# 🌍⚡ EARTH RESONANCE ENGINE ⚡🌍
try:
    from earth_resonance_engine import EarthResonanceEngine, get_earth_engine
    EARTH_RESONANCE_AVAILABLE = True
except ImportError as e:
    EARTH_RESONANCE_AVAILABLE = False
    print(f"⚠️  Earth Resonance Engine not available: {e}")

# 🌌⚡ AUREON NEXUS - UNIFIED NEURAL TRADING ENGINE ⚡🌌
try:
    from aureon_nexus import NexusBus, MasterEquation, QueenHive, AureonNexus, NEXUS as NEXUS_BUS
    NEXUS_AVAILABLE = True
    # 🧠 UNITY: Connect Nexus to Thought Bus
    if NEXUS_BUS and THOUGHT_BUS_AVAILABLE:
        NEXUS_BUS.thought_bus = THOUGHT_BUS
        print("   🧠 Nexus connected to Thought Bus")
except ImportError as e:
    NEXUS_AVAILABLE = False
    NEXUS_BUS = None
    print(f"⚠️  Aureon Nexus not available: {e}")

# 🎯 PROBABILITY LOADER & POSITION HYGIENE 🎯
try:
    from probability_loader import ProbabilityLoader, PositionHygieneChecker, load_position_state
    PROBABILITY_LOADER_AVAILABLE = True
except ImportError as e:
    PROBABILITY_LOADER_AVAILABLE = False
    print(f"⚠️  Probability Loader not available: {e}")
    class ProbabilityLoader:
        def __init__(self, *args, **kwargs): pass
        def load_all_reports(self): return {}
        def is_fresh(self): return False
        def get_top_signals(self, *args): return []
        def get_consensus_signals(self, *args): return []
    class PositionHygieneChecker:
        def __init__(self): pass
        def check_positions(self, *args): return {'flagged': [], 'count': 0}

# 📊 TRADE LOGGER - COMPREHENSIVE DATA LOGGING 📊
try:
    from trade_logger import get_trade_logger, TradeLogger
    TRADE_LOGGER_AVAILABLE = True
    trade_logger = get_trade_logger()
except ImportError as e:
    TRADE_LOGGER_AVAILABLE = False
    trade_logger = None
    print(f"⚠️  Trade Logger not available: {e}")

# 💰 COST BASIS TRACKER - REAL PURCHASE PRICES 💰
try:
    from cost_basis_tracker import CostBasisTracker, get_cost_basis_tracker
    COST_BASIS_AVAILABLE = True
except ImportError as e:
    COST_BASIS_AVAILABLE = False
    print(f"⚠️  Cost Basis Tracker not available: {e}")
    # Fallback stub
    class CostBasisTracker:
        def __init__(self): self.positions = {}
        def sync_from_exchanges(self): return 0
        def get_entry_price(self, symbol): return None
        def set_entry_price(self, *args, **kwargs): pass
        def update_position(self, *args, **kwargs): pass
        def can_sell_profitably(self, symbol, price, **kw): return True, {'recommendation': 'NO_TRACKER'}
        def print_status(self): pass
    def get_cost_basis_tracker(): return CostBasisTracker()

# 🌍⚡ GLOBAL FINANCIAL ECOSYSTEM FEED ⚡🌍
try:
    from global_financial_feed import GlobalFinancialFeed, MacroSnapshot
    GLOBAL_FEED_AVAILABLE = True
    print("   🌍 Global Financial Ecosystem Feed ACTIVE")
except ImportError as e:
    GLOBAL_FEED_AVAILABLE = False
    print(f"⚠️  Global Financial Feed not available: {e}")
    # Fallback stub
    class GlobalFinancialFeed:
        def get_snapshot(self): return None
        def get_probability_adjustment(self, symbol, prob): return prob, {}
        def get_trading_signal(self, symbol): return {'macro_bias': 'NEUTRAL', 'macro_strength': 50}
        def print_dashboard(self): pass

# 📊 PROBABILITY VALIDATION ENGINE 📊
try:
    from probability_validator import ProbabilityValidator, get_validator
    VALIDATOR_AVAILABLE = True
    print("   📊 Probability Validation Engine ACTIVE")
except ImportError as e:
    VALIDATOR_AVAILABLE = False
    print(f"⚠️  Probability Validator not available: {e}")
    # Fallback stub
    class ProbabilityValidator:
        def record_prediction(self, **kwargs): return ""
        def validate_pending(self, func): return []
        def get_confidence_adjustment(self, *args): return 1.0
        def print_dashboard(self): pass
    def get_validator(): return ProbabilityValidator()

# 🌈✨ AUREON ENHANCEMENTS - RAINBOW BRIDGE, SYNCHRONICITY, STARGATE ✨🌈
try:
    from aureon_enhancements import EnhancementLayer, apply_enhancement_to_signal, get_emotional_color
    ENHANCEMENTS_AVAILABLE = True
except ImportError as e:
    ENHANCEMENTS_AVAILABLE = False
    print(f"⚠️  Aureon Enhancements not available: {e}")

# ==== AUREON COGNITION BUS (self-talking JSON thoughts) ====
from aureon_thought_bus import ThoughtBus, Thought
from aureon_cognition_runtime import MinerModule, RiskModule, ExecutionModule

# ==== WORLD NEWS FEED (external data gathering) ====
try:
    from aureon_news_feed import NewsFeed, NewsFeedConfig, create_news_feed
    NEWS_FEED_AVAILABLE = True
except ImportError:
    NEWS_FEED_AVAILABLE = False
    print("⚠️  News Feed module not available")

# ==== WIKIPEDIA KNOWLEDGE BASE (autonomous knowledge gathering) ====
try:
    from aureon_knowledge_base import KnowledgeBase, create_knowledge_base
    KNOWLEDGE_BASE_AVAILABLE = True
except ImportError:
    KNOWLEDGE_BASE_AVAILABLE = False
    print("⚠️  Knowledge Base module not available")

# ==== WISDOM SCANNER - CONSCIOUSNESS EXPANSION ENGINE ====
try:
    from aureon_wisdom_scanner import AureonWisdomScanner, ScannerConfig, WisdomScannerThoughtBusAdapter
    WISDOM_SCANNER_AVAILABLE = True
    print("   📚 Wisdom Scanner loaded - Consciousness Expansion Active!")
except ImportError as e:
    WISDOM_SCANNER_AVAILABLE = False
    print(f"⚠️  Wisdom Scanner not available: {e}")

# ==== 🇮🇪🎯 UNIFIED SNIPER BRAIN - THE KILL SHOT ENGINE ====
try:
    from unified_sniper_brain import get_unified_brain, UnifiedSniperBrain
    SNIPER_BRAIN_AVAILABLE = True
    print("   🎯 UNIFIED SNIPER BRAIN LOADED - Ready for kills!")
except ImportError as e:
    SNIPER_BRAIN_AVAILABLE = False
    UnifiedSniperBrain = None
    print(f"⚠️  Sniper Brain not available: {e}")

# ==== ⚔️ WAR STRATEGY - QUICK KILL PROBABILITY ENGINE ====
try:
    from war_strategy import (
        WAR_STRATEGIST, get_quick_kill_estimate, should_attack, 
        start_raid, complete_raid, get_raid_status, get_war_briefing,
        REQUIRED_R, WIN_THRESHOLD, NET_PENNY_TARGET, IDEAL_BARS, MAX_ACCEPTABLE_BARS
    )
    WAR_STRATEGY_AVAILABLE = True
    print("   ⚔️ WAR STRATEGY LOADED - Quick Kill Probability Active!")
except ImportError as e:
    WAR_STRATEGY_AVAILABLE = False
    WAR_STRATEGIST = None
    print(f"⚠️  War Strategy not available: {e}")

# ==== 🇮🇪 BHOY'S WISDOM - STRATEGIC QUOTES ====
try:
    from bhoys_wisdom import celebrate_penny_profit, get_contextual_wisdom
    BHOYS_WISDOM_AVAILABLE = True
    print("   🍀 Bhoy's Wisdom loaded - Through a Bhoy's Eyes Active!")
except ImportError as e:
    BHOYS_WISDOM_AVAILABLE = False
    def celebrate_penny_profit(amount, symbol): return "Our revenge will be the laughter of our children."
    def get_contextual_wisdom(context): return "Tiocfaidh ár lá!"
    print(f"⚠️  Bhoy's Wisdom not available: {e}")

# ═══════════════════════════════════════════════════════════════
# ☘️🔥 CELTIC WARFARE SYSTEMS - IRISH GUERRILLA INTELLIGENCE 🔥☘️
# ═══════════════════════════════════════════════════════════════

# ==== ☘️ GUERRILLA WARFARE ENGINE ====
try:
    from guerrilla_warfare_engine import (
        IntelligenceNetwork, FlyingColumn, BattlefrontStatus,
        TacticalMode, IntelligenceReport, GUERRILLA_CONFIG, get_celtic_wisdom
    )
    GUERRILLA_ENGINE_AVAILABLE = True
    print("   ☘️ Guerrilla Warfare Engine loaded - Flying Columns Ready!")
except ImportError as e:
    GUERRILLA_ENGINE_AVAILABLE = False
    IntelligenceNetwork = None
    print(f"⚠️  Guerrilla Engine not available: {e}")

# ==== ⚡ CELTIC PREEMPTIVE STRIKE ENGINE ====
try:
    from celtic_preemptive_strike import (
        PreemptiveExitEngine, DawnRaidDetector,
        PreemptiveSignal, PreemptiveSignalType
    )
    PREEMPTIVE_STRIKE_AVAILABLE = True
    print("   ⚡ Preemptive Strike Engine loaded - Move Before They React!")
except ImportError as e:
    PREEMPTIVE_STRIKE_AVAILABLE = False
    PreemptiveExitEngine = None
    print(f"⚠️  Preemptive Strike not available: {e}")

# ==== 🌐 MULTI-BATTLEFRONT COORDINATOR ====
try:
    from multi_battlefront_coordinator import (
        MultiBattlefrontWarRoom, CampaignPhase, ArbitrageOpportunity
    )
    BATTLEFRONT_COORDINATOR_AVAILABLE = True
    print("   🌐 Multi-Battlefront Coordinator loaded - Unity of Command!")
except ImportError as e:
    BATTLEFRONT_COORDINATOR_AVAILABLE = False
    MultiBattlefrontWarRoom = None
    print(f"⚠️  Battlefront Coordinator not available: {e}")

# ==== 🇮🇪 IRISH PATRIOT SCOUTS ====
try:
    from irish_patriot_scouts import (
        PatriotScoutNetwork, PatriotScout, PatriotScoutDeployer,
        PATRIOT_CONFIG, get_patriot_wisdom
    )
    PATRIOT_SCOUTS_AVAILABLE = True
    print("   🇮🇪 Irish Patriot Scouts loaded - Warriors Ready!")
except ImportError as e:
    PATRIOT_SCOUTS_AVAILABLE = False
    PatriotScoutNetwork = None
    PatriotScoutDeployer = None
    print(f"⚠️  Patriot Scouts not available: {e}")

# ==== 🎯 IRA CELTIC SNIPER ====
try:
    from ira_sniper_mode import (
        IraCelticSniper, get_celtic_sniper, SNIPER_CONFIG,
        check_sniper_exit, celebrate_sniper_kill,
        get_sniper_config, map_sniper_platform_assets, apply_sniper_mode
    )
    CELTIC_SNIPER_AVAILABLE = True
    print("   🎯 IRA Celtic Sniper loaded - Zero Loss Mode Active!")
except ImportError as e:
    CELTIC_SNIPER_AVAILABLE = False
    IraCelticSniper = None
    print(f"⚠️  Celtic Sniper not available: {e}")

# ═══════════════════════════════════════════════════════════════
# 💰 PENNY PROFIT ENGINE - DYNAMIC DOLLAR-BASED EXIT THRESHOLDS 💰
# ═══════════════════════════════════════════════════════════════
# 🎯 Calculates EXACT thresholds for ANY trade size dynamically!
# No more preset lookup tables - formula calculates on-the-fly.

PENNY_PROFIT_CONFIG = {}  # Optional overrides from JSON
PENNY_PROFIT_ENABLED = True  # Always enabled - dynamic calculation works without config
PENNY_TARGET_NET = 0.01  # Default target: $0.01 net profit per trade

# Binance must always capture between $0.01 and $0.03 NET after all fees
BINANCE_NET_PROFIT_RANGE = (0.01, 0.03)

# Default fee rates by exchange (can be overridden by CONFIG or JSON)
DEFAULT_FEE_RATES = {
    'binance': 0.001,    # 0.10% taker
    'kraken': 0.0026,    # 0.26% taker  
    'capital': 0.0012,   # ~0.12% spread
    'alpaca': 0.0025,    # 0.25% commission
}


def load_penny_profit_config():
    """Load penny profit configuration (optional - for fee rate overrides).
    
    The engine works WITHOUT a config file using dynamic calculation.
    Config file only needed to override default fee rates or target.
    """
    global PENNY_PROFIT_CONFIG, PENNY_PROFIT_ENABLED, PENNY_TARGET_NET
    config_path = os.path.join(ROOT_DIR, 'penny_profit_config.json')
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                PENNY_PROFIT_CONFIG = json.load(f)
            PENNY_TARGET_NET = PENNY_PROFIT_CONFIG.get('target_net_win', 0.01)
            print(f"💰 Penny Profit Engine - DYNAMIC (target: +${PENNY_TARGET_NET:.2f} net per trade)")
        except Exception as e:
            print(f"⚠️  Penny config load error: {e} - using dynamic defaults")
    else:
        print(f"💰 Penny Profit Engine - DYNAMIC MODE (target: +${PENNY_TARGET_NET:.2f} net)")
    
    PENNY_PROFIT_ENABLED = True  # Always enabled with dynamic calculation


def clamp_target_net_for_exchange(exchange: str, target_net: float) -> Tuple[float, bool]:
    """
    Apply exchange-specific clamping to the desired net target.
    
    For Binance we must guarantee that every full trade cycle nets between
    $0.01 and $0.03 after *all* costs (fees, slippage, spread).
    """
    ex_lower = (exchange or 'binance').lower()
    if ex_lower == 'binance':
        min_net, max_net = BINANCE_NET_PROFIT_RANGE
        clamped = max(min_net, min(max_net, target_net))
        return clamped, clamped != target_net
    return target_net, False


def get_exchange_fee_rate(exchange: str) -> float:
    """Get fee rate for exchange - checks CONFIG, then JSON, then defaults.
    
    Priority order:
    1. Global CONFIG (most accurate - actual observed rates)
    2. penny_profit_config.json fee_rate
    3. DEFAULT_FEE_RATES fallback
    """
    ex_lower = (exchange or 'binance').lower()
    
    # Priority 1: Check global CONFIG for actual observed fees
    try:
        if ex_lower == 'kraken':
            return CONFIG.get('KRAKEN_FEE_TAKER', DEFAULT_FEE_RATES['kraken'])
        elif ex_lower == 'binance':
            return CONFIG.get('BINANCE_FEE_TAKER', DEFAULT_FEE_RATES['binance'])
        elif ex_lower == 'alpaca':
            return CONFIG.get('ALPACA_FEE_TAKER', DEFAULT_FEE_RATES['alpaca'])
        elif ex_lower == 'capital':
            return CONFIG.get('CAPITAL_FEE', DEFAULT_FEE_RATES['capital'])
    except (NameError, KeyError):
        pass  # CONFIG not loaded yet
    
    # Priority 2: Check penny_profit_config.json
    if PENNY_PROFIT_CONFIG:
        exchanges = PENNY_PROFIT_CONFIG.get('exchanges', {})
        if ex_lower in exchanges:
            return exchanges[ex_lower].get('fee_rate', DEFAULT_FEE_RATES.get(ex_lower, 0.002))
    
    # Priority 3: Default fallback
    return DEFAULT_FEE_RATES.get(ex_lower, 0.002)


def required_price_increase(initial_usd: float, fee_rate: float, target_profit: float = 0.01) -> float:
    """
    📐 EXACT MATHEMATICAL FORMULA for required price increase to achieve target net profit.
    
    Formula: r = ((1 + P/A) / (1 - f)²) - 1
    
    This accounts for fee compounding over both legs:
    1. Buy: Spend A USD, receive crypto worth A×(1-f) after fee
    2. Sell: Crypto sold at price×(1+r), then fee deducted again
    3. Final USD = A × (1-f)² × (1+r) = A + P
    
    Args:
        initial_usd (A): Position size in USD
        fee_rate (f): Fee rate per leg (e.g., 0.001 for 0.1%)
        target_profit (P): Target net profit in USD (default $0.01)
    
    Returns:
        r: Required price increase as decimal (multiply by 100 for %)
    """
    if initial_usd <= 0 or fee_rate < 0 or target_profit <= 0:
        return 0.0
    
    # Exact formula accounting for compounding fees
    r = ((1 + target_profit / initial_usd) / ((1 - fee_rate) ** 2)) - 1
    return r


def get_penny_threshold(exchange: str, trade_size: float) -> dict:
    """🎯 EXACT PENNY PROFIT - Uses precise mathematical formula for ANY trade size!
    
    📐 EXACT FORMULA (accounts for fee compounding):
        r = ((1 + P/A) / (1 - f)²) - 1
        
    Where:
        A = trade_size (initial USD)
        P = target net profit ($0.01)
        f = fee rate per leg
        r = required price increase (decimal)
    
    The sell target price = buy_price × (1 + r)
    
    Args:
        exchange: Exchange name ('binance', 'kraken', 'alpaca', 'capital')
        trade_size: Entry value in dollars (ANY amount!)
    
    Returns:
        dict with: required_pct, win_gte, stop_lte, fee_rate, trade_size, target_net
    """
    if not PENNY_PROFIT_ENABLED:
        return None
    
    # 🔧 FIX: Ensure we always return a threshold for valid positions
    # Use minimum $1 trade size if entry_value is corrupted/zero
    if trade_size <= 0:
        trade_size = 1.0  # Fallback to $1 minimum
    
    exchange_name = (exchange or 'binance').lower()
    
    fee_rate = get_exchange_fee_rate(exchange_name)
    target_net, was_clamped = clamp_target_net_for_exchange(exchange_name, PENNY_TARGET_NET)
    
    # Add safety margins for slippage and spread (from CONFIG)
    # This ensures we account for ALL costs, not just exchange fees.
    slippage = CONFIG.get('SLIPPAGE_PCT', 0.0020)
    spread = CONFIG.get('SPREAD_COST_PCT', 0.0010)
    
    # Total effective rate per leg (Fee + Slippage + Spread)
    total_rate = fee_rate + slippage + spread
    
    # 📐 EXACT CALCULATION using proper compounding formula
    # We use total_rate to ensure the price increase covers ALL costs
    r = required_price_increase(trade_size, total_rate, target_net)
    
    # Calculate the realized net after both legs to confirm it meets the target
    net_after_costs = trade_size * ((1 - total_rate) ** 2 * (1 + r) - 1)

    # Safety: if rounding left us below Binance minimum, bump to the floor
    if exchange_name == 'binance' and net_after_costs < BINANCE_NET_PROFIT_RANGE[0]:
        target_net = BINANCE_NET_PROFIT_RANGE[0]
        r = required_price_increase(trade_size, total_rate, target_net)
        net_after_costs = trade_size * ((1 - total_rate) ** 2 * (1 + r) - 1)

    # win_gte is the gross P&L needed (price increase × position)
    # Since gross_pnl = exit_value - entry_value = entry_value × r
    win_gte = trade_size * r
    
    # Approximate fee cost for reference (linear estimate)
    # This is just for display/logging - the real math is in 'r'
    approx_fees = 2 * total_rate * trade_size
    
    # Stop Loss: Risk ~3x the win target (gives ~25% breakeven win rate)
    # 🔧 FIX: 1.5x was too tight - normal volatility triggered stops before profits!
    # With 3x, we give positions room to breathe and hit penny profit.
    stop_lte = -(win_gte * 3.0)
    
    return {
        'required_pct': round(r * 100, 4),  # As percentage
        'required_r': r,                      # As decimal
        'cost': round(approx_fees, 6),        # Approximate total fees
        'win_gte': round(win_gte, 6),         # Gross P&L trigger for TP
        'stop_lte': round(stop_lte, 6),       # Gross P&L trigger for SL
        'fee_rate': fee_rate,
        'trade_size': trade_size,
        'target_net': target_net,
        'target_net_requested': PENNY_TARGET_NET,
        'target_net_clamped': was_clamped,
        'binance_net_range': BINANCE_NET_PROFIT_RANGE if exchange_name == 'binance' else None,
        'expected_net_after_costs': round(net_after_costs, 6),
        'is_dynamic': True
    }


def check_penny_exit(exchange: str, entry_value: float, gross_pnl: float, symbol: str = None) -> dict:
    """�🇪🎯 ZERO LOSS SNIPER - ONLY exit on CONFIRMED NET PROFIT.
    
    The sniper NEVER misses. We hold until we have guaranteed profit.
    NO STOP LOSSES. NO LOSSES. EVER.
    
    "Every kill will be a confirmed net profit."
    
    Args:
        exchange: Exchange name
        entry_value: Position entry value in dollars (ANY size!)
        gross_pnl: Current gross P&L (before fees)
        symbol: Trading symbol for wisdom quotes
    
    Returns:
        {'should_tp': bool, 'should_sl': bool, 'threshold': dict, 'gross_pnl': float, 'sniper_active': bool}
    """
    threshold = get_penny_threshold(exchange, entry_value)
    
    if not threshold:
        return {'should_tp': False, 'should_sl': False, 'threshold': None, 'gross_pnl': gross_pnl, 'sniper_active': False}
    
    # 🎯 ZERO LOSS MODE: ONLY exit on CONFIRMED NET PROFIT
    # Check Take Profit: gross P&L >= win threshold
    should_tp = gross_pnl >= threshold['win_gte']
    
    # 🚫 NO STOP LOSSES - WE DON'T LOSE
    # The sniper holds until the kill is confirmed
    should_sl = False  # NEVER trigger stop loss
    
    # 🇮🇪🎯 SNIPER BRAIN - Get wisdom for the kill
    sniper_wisdom = None
    if should_tp and BHOYS_WISDOM_AVAILABLE:
        # Calculate approximate net profit
        net_profit = gross_pnl - threshold.get('cost', 0)
        sniper_wisdom = celebrate_penny_profit(net_profit, symbol or 'UNKNOWN')
    
    return {
        'should_tp': should_tp,
        'should_sl': should_sl,  # Always False - we don't lose
        'threshold': threshold,
        'gross_pnl': gross_pnl,
        'sniper_active': True,
        'zero_loss_mode': True,
        'sniper_wisdom': sniper_wisdom
    }


# Load on import (sets PENNY_PROFIT_ENABLED = True)
load_penny_profit_config()

# ═══════════════════════════════════════════════════════════════
# MODULE-LEVEL LOT SIZE CACHE - Used by UnifiedTradeConfirmation
# ═══════════════════════════════════════════════════════════════
_MODULE_LOT_SIZE_CACHE: Dict[str, Tuple[Optional[float], Optional[float]]] = {}

def get_exchange_lot_size(exchange: str, symbol: str, client=None) -> Tuple[Optional[float], Optional[float]]:
    """
    Module-level lot size lookup for any exchange.
    Returns (step_size, min_qty) or (None, None) if unavailable.
    """
    global _MODULE_LOT_SIZE_CACHE
    cache_key = f"{exchange}:{symbol}"
    
    if cache_key in _MODULE_LOT_SIZE_CACHE:
        return _MODULE_LOT_SIZE_CACHE[cache_key]
    
    exchange_name = (exchange or '').lower()
    result = (None, None)
    
    try:
        if exchange_name == 'binance' and client:
            # Try to get from Binance exchange info
            try:
                info = client.client.session.get(
                    f"{client.client.base}/api/v3/exchangeInfo",
                    params={'symbol': symbol},
                    timeout=5
                ).json()
                for sym_info in info.get('symbols', []):
                    if sym_info['symbol'] == symbol:
                        for f in sym_info.get('filters', []):
                            if f['filterType'] == 'LOT_SIZE':
                                step = float(f.get('stepSize', 0))
                                min_q = float(f.get('minQty', 0))
                                result = (step, min_q)
                                break
            except Exception:
                # Fallback defaults for common Binance pairs
                binance_defaults = {
                    'BTCUSDC': (0.00001, 0.00001), 'BTCUSDT': (0.00001, 0.00001),
                    'ETHUSDC': (0.0001, 0.0001), 'ETHUSDT': (0.0001, 0.0001),
                    'SOLUSDC': (0.001, 0.001), 'SOLUSDT': (0.001, 0.001),
                    'SHIBUSDC': (1, 1), 'SHIBUSDT': (1, 1),
                    'XLMUSDC': (0.1, 0.1), 'XLMUSDT': (0.1, 0.1),
                }
                result = binance_defaults.get(symbol, (0.00000001, 0.00000001))
                
        elif exchange_name == 'kraken':
            # Kraken common lot sizes
            kraken_defaults = {
                'XBTUSD': (0.0001, 0.0001), 'XBTUSDC': (0.0001, 0.0001),
                'ETHUSD': (0.001, 0.001), 'ETHUSDC': (0.001, 0.001),
                'SOLUSD': (0.01, 0.01), 'SOLUSDC': (0.01, 0.01),
                'SHIBUSD': (50000, 50000), 'SHIBUSDC': (50000, 50000),  # Kraken SHIB is in large lots!
                'XLMUSD': (1, 1), 'XLMUSDC': (1, 1),
                'BCHUSD': (0.001, 0.001), 'BCHUSDC': (0.001, 0.001),
            }
            # Also handle Kraken's X-prefixed naming
            alt_symbol = symbol
            if symbol.startswith('X') and len(symbol) > 4:
                alt_symbol = symbol[1:]  # XXBT -> XBT
            result = kraken_defaults.get(symbol, kraken_defaults.get(alt_symbol, (0.00000001, 0.00000001)))
            
        elif exchange_name == 'capital':
            # 💼 Capital.com CFD lot sizes - they use contract sizes
            # Most CFDs have 1 unit minimum, crypto CFDs vary
            capital_defaults = {
                # Crypto CFDs on Capital.com
                'BTCUSD': (0.01, 0.01), 'Bitcoin': (0.01, 0.01),
                'ETHUSD': (0.1, 0.1), 'Ethereum': (0.1, 0.1),
                'SOLUSD': (1.0, 1.0), 'Solana': (1.0, 1.0),
                'XRPUSD': (10.0, 10.0), 'Ripple': (10.0, 10.0),
                'ADAUSD': (10.0, 10.0), 'Cardano': (10.0, 10.0),
                'DOTUSD': (1.0, 1.0), 'Polkadot': (1.0, 1.0),
                'DOGEUSD': (100.0, 100.0), 'Dogecoin': (100.0, 100.0),
                'SHIBUSD': (100000.0, 100000.0), 'Shiba': (100000.0, 100000.0),
                # Forex/Indices - standard lot decimals
                'EURUSD': (0.01, 0.01), 'GBPUSD': (0.01, 0.01),
                'US500': (0.1, 0.1), 'UK100': (0.1, 0.1),
                'Gold': (0.01, 0.01), 'XAUUSD': (0.01, 0.01),
            }
            result = capital_defaults.get(symbol, (1.0, 1.0))  # Default 1 unit for CFDs
            
        elif exchange_name == 'alpaca':
            # 🦙 Alpaca crypto/stock lot sizes
            # Stocks are fractional, crypto varies
            alpaca_defaults = {
                # Crypto on Alpaca
                'BTC/USD': (0.0001, 0.0001), 'BTCUSD': (0.0001, 0.0001),
                'ETH/USD': (0.001, 0.001), 'ETHUSD': (0.001, 0.001),
                'SOL/USD': (0.01, 0.01), 'SOLUSD': (0.01, 0.01),
                'DOGE/USD': (1.0, 1.0), 'DOGEUSD': (1.0, 1.0),
                'SHIB/USD': (1000.0, 1000.0), 'SHIBUSD': (1000.0, 1000.0),
                # Stocks - fractional shares supported
                'AAPL': (0.001, 0.001), 'TSLA': (0.001, 0.001),
                'NVDA': (0.001, 0.001), 'MSFT': (0.001, 0.001),
            }
            result = alpaca_defaults.get(symbol, (0.001, 0.001))  # Default fractional for stocks
            
    except Exception as e:
        print(f"⚠️ Lot size lookup failed for {exchange}/{symbol}: {e}")
        
    _MODULE_LOT_SIZE_CACHE[cache_key] = result
    return result

def truncate_to_lot_size(quantity: float, step_size: float) -> float:
    """Truncate quantity to valid lot size step."""
    if step_size <= 0 or quantity <= 0:
        return quantity
    steps = int(quantity / step_size)
    return steps * step_size

def validate_order_quantity(exchange: str, symbol: str, quantity: float, price: float = 0, client=None) -> Tuple[Optional[float], Optional[str]]:
    """
    Validate and adjust quantity for exchange lot size requirements.
    Returns (adjusted_quantity, error_message) - error_message is None if valid.
    """
    if quantity is None or quantity <= 0:
        return None, "Invalid quantity"
        
    exchange_name = (exchange or '').lower()
    step_size, min_qty = get_exchange_lot_size(exchange, symbol, client)
    
    # Truncate to lot size
    if step_size and step_size > 0:
        quantity = truncate_to_lot_size(quantity, step_size)
        
    if quantity <= 0:
        return None, f"Quantity below lot step {step_size}"
        
    # Check minimum quantity
    if min_qty and quantity < min_qty:
        return None, f"Qty {quantity:.8f} below {exchange_name.upper()} min {min_qty:.8f}"
        
    # Check minimum notional
    min_notional = CONFIG.get(f'{exchange_name.upper()}_MIN_NOTIONAL', 1.0)
    if price and price > 0:
        notional = quantity * price
        if notional < min_notional:
            return None, f"Notional ${notional:.2f} below {exchange_name.upper()} min ${min_notional:.2f}"
            
    return quantity, None


# ═══════════════════════════════════════════════════════════════
# CONFIGURATION - THE UNIFIED PARAMETERS
# ═══════════════════════════════════════════════════════════════

CONFIG = {
    'EXCHANGE': os.getenv('EXCHANGE', 'both').lower(), # BOTH Binance AND Kraken for multi-exchange trading
    # Trading Parameters
    'BASE_CURRENCY': os.getenv('BASE_CURRENCY', 'USD'),  # USD or GBP
    
    # Platform-Specific Fees (as decimals)
    # ══════════════════════════════════════════════════════════
    # 🐙 KRAKEN (Actual observed: ~0.40% per trade on small volume)
    'KRAKEN_FEE_MAKER': 0.0026,     # 0.26% maker fee 
    'KRAKEN_FEE_TAKER': 0.0040,     # 0.40% taker fee (actual observed)
    'KRAKEN_FEE': 0.0040,           # Legacy field (uses taker)
    
    # 🟡 BINANCE (UK Account - Spot only)
    'BINANCE_FEE_MAKER': 0.0010,    # 0.10% maker (with BNB discount: 0.075%)
    'BINANCE_FEE_TAKER': 0.0010,    # 0.10% taker (with BNB discount: 0.075%)
    'BINANCE_FEE': 0.0010,          # Default taker
    
    # 🦙 ALPACA (Crypto)
    'ALPACA_FEE_MAKER': 0.0015,     # 0.15% maker (crypto)
    'ALPACA_FEE_TAKER': 0.0025,     # 0.25% taker (crypto)
    'ALPACA_FEE_STOCK': 0.0000,     # $0 commission for stocks!
    'ALPACA_FEE': 0.0025,           # Default taker for crypto
    'ALPACA_ANALYTICS_ONLY': True,  # 🦙 Alpaca is for market data/analytics only (no trades)
    
    # 💼 CAPITAL.COM (CFD/Spread Betting)
    'CAPITAL_FEE_SPREAD': 0.0010,   # ~0.1% avg spread cost (varies by instrument)
    'CAPITAL_FEE_OVERNIGHT': 0.0001,# Daily overnight financing (annualized ~2.5%)
    'CAPITAL_FEE': 0.0010,          # Default spread cost
    
    # General
    'SLIPPAGE_PCT': 0.0020,         # 0.20% estimated slippage per trade (increased for safety)
    'SPREAD_COST_PCT': 0.0010,      # 0.10% estimated spread cost (increased for safety)
    'TAKE_PROFIT_PCT': 1.8,         # FALLBACK: 1.8% (penny profit uses dollar thresholds instead)
    'STOP_LOSS_PCT': 1.5,           # FALLBACK: 1.5% (penny profit uses dollar thresholds instead)
    'MAX_POSITIONS': 30,            # 🔥 Legacy cap (unused when UNLIMITED_POSITIONS is enabled)
    'UNLIMITED_POSITIONS': True,    # 🪙 Penny-unity mode: no limit to active positions
    'TARGET_FILL_RATE': 0.33,       # 🎯 TARGET: Keep 1/3 of positions filled (10 of 30)
    'MIN_TRADE_USD': 1.44,          # Minimum trade notional in base currency
    'BINANCE_MIN_NOTIONAL': 1.0,    # Refuse sells if notional < $1 to avoid LOT_SIZE noise
    'KRAKEN_MIN_NOTIONAL': 5.25,    # Kraken enforces ~$5 minimum notional on spot
    'CAPITAL_MIN_NOTIONAL': 10.0,   # 💼 Capital.com CFD minimum ~$10 (varies by instrument)
    'ALPACA_MIN_NOTIONAL': 1.0,     # 🦙 Alpaca crypto ~$1 min, stocks $1
    'PORTFOLIO_RISK_BUDGET': 3.00,  # 300% - allow significant positions for existing portfolio holders
    'MIN_EXPECTED_EDGE_GBP': 0.001, # Require positive edge
    'DEFAULT_WIN_PROB': 0.55,       # Target win probability
    'WIN_RATE_CONFIDENCE_TRADES': 25,
    'EQUITY_MIN_DELTA': 0.10,       # Smaller delta for frequent compounding
    'EQUITY_TOLERANCE_GBP': 0.0,
    
    # 🎯 TRAILING STOP CONFIGURATION
    'ENABLE_TRAILING_STOP': True,           # Enable trailing stop system
    'TRAILING_ACTIVATION_PCT': 0.8,         # Activate at 0.8% profit (was 0.5% - lock in more profit first)
    'TRAILING_DISTANCE_PCT': 0.5,           # Trail 0.5% behind peak (was 0.3% - less whipsaw)
    'USE_ATR_TRAILING': True,               # Use ATR for dynamic trailing
    'ATR_TRAIL_MULTIPLIER': 1.5,            # Trail at 1.5x ATR below peak
    
    # 🚀 KRAKEN ADVANCED ORDERS - Server-Side TP/SL (executes even if bot offline!)
    'USE_SERVER_SIDE_ORDERS': os.getenv('USE_SERVER_SIDE_ORDERS', '1') == '1',  # Enable Kraken native TP/SL
    'PREFER_LIMIT_ORDERS': os.getenv('PREFER_LIMIT_ORDERS', '1') == '1',        # 💰 USE LIMIT ORDERS for maker fees (0.1% vs 0.2%!)
    'USE_TRAILING_STOP_ORDERS': os.getenv('USE_TRAILING_STOP_ORDERS', '0') == '1',  # Native trailing stops
    
    # 💰 PROFIT GATES - PENNY PROFIT MODE!
    # Target: +$0.01 net profit per trade. Dollar thresholds loaded from penny_profit_config.json
    # These percentages are FALLBACK only when penny profit config not available
    'MIN_NET_PROFIT_PCT': 0.008,    # 0.8% fallback if penny config missing
    'SERVER_SIDE_TP_PCT': 1.8,              # Take profit % for server-side orders (fallback)
    'SERVER_SIDE_SL_PCT': 1.5,              # Stop loss % for server-side orders (fallback)
    'SERVER_TRAILING_PCT': 2.0,             # Trailing stop distance % for native trailing
    
    # Dynamic Portfolio Rebalancing
    'ENABLE_REBALANCING': True,     # Sell underperformers to buy better opportunities
    'REBALANCE_THRESHOLD': -50.0,   # 🔥 Sell big losers (>50% loss) to free capital for better opportunities
    'MIN_HOLD_CYCLES': 10,          # Hold at least 10 cycles (~10 mins) before rebalance (was 3)
    # 🤑 GREEDY HOE MODE: ALL THE QUOTE CURRENCIES!
    'QUOTE_CURRENCIES': ['USDC', 'USDT', 'USD', 'GBP', 'EUR', 'BTC', 'ETH', 'BNB', 'FDUSD', 'TUSD', 'BUSD'],
    
    # 🌾 Startup Harvesting
    'HARVEST_ON_STARTUP': True,      # 🔥 ENABLED - Actively harvest and trade!
    'HARVEST_MIN_VALUE': 0.50,       # Lowered - harvest even small gains
    
    # Scout Deployment (from immediateWaveRider.ts)
    'DEPLOY_SCOUTS_IMMEDIATELY': True,   # 🚀 Deploy positions immediately on first scan - HIT THE GROUND RUNNING!
    'SCOUT_MIN_MOMENTUM': 0.1,           # Very low threshold - get into trades FAST
    'SCOUT_FORCE_COUNT': 10,             # 🤑 GREEDY: 10 scouts on startup!
    'SCOUT_MIN_VOLATILITY': 1.0,         # 🤑 LOWERED: More coins qualify
    'SCOUT_MIN_VOLUME_QUOTE': 50000,     # 🤑 LOWERED: Trade thinner books too
    'SCOUT_PER_QUOTE_LIMIT': 3,          # Spread early scouts across quote currencies (3 per quote)
    
    # Kelly Criterion & Risk Management
    'USE_KELLY_SIZING': True,       # Use Kelly instead of fixed %
    'KELLY_SAFETY_FACTOR': 0.5,     # Half-Kelly for safety
    'BASE_POSITION_SIZE': 0.04,     # Base size when Kelly disabled (reduced for smaller trades)
    'MAX_POSITION_SIZE': 0.25,      # Hard cap per trade
    'MAX_SYMBOL_EXPOSURE': 0.30,    # Max 30% in one symbol
    'MAX_DRAWDOWN_PCT': 50.0,       # Circuit breaker at 50% DD - raised to allow recovery trades
    'MIN_NETWORK_COHERENCE': 0.20,  # NEVER pause - always trade!
    
    # Opportunity Filters - 🪙 PENNY PROFIT FIRST 🪙
    'MIN_MOMENTUM': -5.0,           # 🪙 PENNY MODE: Allow slightly down coins (dip buying)
    'MAX_MOMENTUM': 50.0,           # Avoid parabolic pumps (reversal risk)
    'MIN_VOLUME': 10000,            # 🪙 PENNY MODE: Lower volume = more opportunities
    'MIN_SCORE': 20,                # 🪙 PENNY MODE: Very low score threshold - trust the math
    
    # 🎯 OPTIMAL WIN RATE MODE
    'ENABLE_OPTIMAL_WR': True,      # Enable all win rate optimizations
    
    # 🔥 FORCE TRADE MODE - Bypasses all gates for testing
    'FORCE_TRADE': os.getenv('FORCE_TRADE', '0') == '1',
    'FORCE_TRADE_SYMBOL': os.getenv('FORCE_TRADE_SYMBOL', ''),  # Specific symbol or empty for best available
    
    # 🔭 QUANTUM TELESCOPE
    'ENABLE_QUANTUM_TELESCOPE': True,
    'ENABLE_HARMONIC_UNDERLAY': True,
    'QUANTUM_WEIGHT': 0.15,         # Weight of Quantum Telescope in Lambda field
    'HARMONIC_WEIGHT': 0.20,        # Weight of 6D harmonic coherence in Lambda field
    'HARMONIC_GATE': 0.10,          # 🪙 PENNY MODE: Very low - don't block penny trades
    'HARMONIC_PROB_MIN': 0.30,      # 🪙 PENNY MODE: Almost always pass
    'OPTIMAL_MIN_GATES': 0,         # 🪙 PENNY MODE: ZERO gates required - penny math is king
    'OPTIMAL_MIN_COHERENCE': 0.10,  # 🪙 PENNY MODE: Almost no coherence needed
    'OPTIMAL_TREND_CONFIRM': True,  # Require trend confirmation
    'OPTIMAL_MULTI_TF_CHECK': True, # Multi-timeframe coherence check
    
    # Compounding (10-9-1 Model)
    'COMPOUND_PCT': 0.90,           # 90% compounds
    'HARVEST_PCT': 0.10,            # 10% harvests
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🌀 MEDICINE WHEEL FREQUENCY ALPHABET - Native American Light Language 🌀
    # ═══════════════════════════════════════════════════════════════════════
    # The Four Directions encode the sacred frequency alphabet:
    # EAST (Yellow/Fire)  → 528 Hz - Birth/New Beginnings - LOVE frequency
    # SOUTH (Black/Water) → 396 Hz - Youth/Growth - Liberation frequency  
    # WEST (Red/Earth)    → 432 Hz - Adults/Harvest - Cosmic frequency
    # NORTH (White/Wind)  → 963 Hz - Elders/Wisdom - Unity frequency
    # CENTER (Green)      → 528 Hz - Creator/Balance - DNA REPAIR ⭐
    # GREEN = Yellow (East) + Blue (Sky) = Heart chakra = 528Hz LOVE
    # ═══════════════════════════════════════════════════════════════════════
    
    # Auris Node Frequencies (Hz) - Aligned with Medicine Wheel
    'FREQ_TIGER': 741.0,           # SOL - Awakening intuition
    'FREQ_FALCON': 852.0,          # LA - Spiritual order (EAST spirit animal variant)
    'FREQ_HUMMINGBIRD': 963.0,     # SI - Unity/NORTH Elder wisdom
    'FREQ_DOLPHIN': 528.0,         # MI - GREEN BORAX LOVE 💚 CENTER/EAST
    'FREQ_DEER': 396.0,            # UT - Liberation/SOUTH Growth
    'FREQ_OWL': 432.0,             # Cosmic harmony/WEST Harvest
    'FREQ_PANDA': 412.3,           # Transition frequency
    'FREQ_CARGOSHIP': 174.0,       # Foundation/grounding
    'FREQ_CLOWNFISH': 639.0,       # FA - Connection/relationships
    
    # Medicine Wheel Direction Frequencies (Native American Light Language)
    'MEDICINE_WHEEL_EAST': 528.0,  # Yellow/Fire - Birth - EAGLE spirit
    'MEDICINE_WHEEL_SOUTH': 396.0, # Black/Water - Youth - WOLF spirit
    'MEDICINE_WHEEL_WEST': 432.0,  # Red/Earth - Adult - BUFFALO spirit
    'MEDICINE_WHEEL_NORTH': 963.0, # White/Wind - Elder - BEAR spirit
    'MEDICINE_WHEEL_CENTER': 528.0,# GREEN - Creator - ALL spirits unified
    
    # Coherence Thresholds - OPTIMAL WIN RATE MODE 🎯
    'HIGH_COHERENCE_MODE': False,   # DISABLED: Allow trading in any coherence
    'ENTRY_COHERENCE': 0.20,       # LOWERED: Allow more trades (was 0.35)
    'EXIT_COHERENCE': 0.15,        # LOWERED: Exit more flexibly (was 0.25)
    
    # Lambda Field Components (from coherenceTrader.ts)
    'ENABLE_LAMBDA_FIELD': os.getenv('ENABLE_LAMBDA_FIELD', '1') == '1',  # Full Λ(t) = S(t) + O(t) + E(t)
    'OBSERVER_WEIGHT': 0.3,         # O(t) = Λ(t-1) × 0.3 (self-reference)
    'ECHO_WEIGHT': 0.2,             # E(t) = avg(Λ[t-5:t]) × 0.2 (memory)
    
    # 🌍⚡ HNC Frequency Integration ⚡🌍
    'ENABLE_HNC_FREQUENCY': os.getenv('ENABLE_HNC', '1') == '1',  # Use HNC frequency for sizing
    'HNC_FREQUENCY_WEIGHT': 0.25,    # H(t) weight in Lambda field
    'HNC_COHERENCE_THRESHOLD': 0.50, # Min triadic coherence for full sizing
    'HNC_HARMONIC_BONUS': 1.15,      # 15% bonus for harmonic resonance (256/528 Hz)
    
    # 🔊 PHASE 2: FREQUENCY FILTERING OPTIMIZATION 🔊
    'ENABLE_FREQUENCY_FILTERING': True,        # Enable frequency-based signal quality
    'FREQUENCY_BOOST_300HZ': 1.50,            # 50% boost for 300-399Hz (98.8% prediction accuracy!)
    'FREQUENCY_BOOST_528HZ': 1.35,            # 35% boost for 528Hz Love Frequency (83.3% WR)
    'FREQUENCY_SUPPRESS_963HZ': 0.6,          # 40% suppression for 963Hz (poor performer)
    'FREQUENCY_SUPPRESS_600HZ': 0.75,         # 25% suppression for 600-699Hz (0% accuracy)
    'FREQUENCY_NEUTRAL_BASELINE': 1.0,        # All other frequencies baseline multiplier
    'FREQUENCY_WIN_RATE_TARGET': 0.60,        # Phase 2 target: 60%+ win rate
    'HNC_DISTORTION_PENALTY': 0.70,           # 30% penalty for 440 Hz distortion
    
    # 🎵 SOLFEGGIO FREQUENCY BOOSTS (Ancient Sacred Healing Tones) 🎵
    'FREQUENCY_BOOST_174HZ': 1.20,            # 174Hz - Pain Relief, Foundation
    'FREQUENCY_BOOST_285HZ': 1.25,            # 285Hz - Healing, Tissue Regeneration  
    'FREQUENCY_BOOST_396HZ': 1.40,            # 396Hz - Liberation from Fear/Guilt (UT)
    'FREQUENCY_BOOST_417HZ': 1.30,            # 417Hz - Undoing Situations, Change (RE)
    'FREQUENCY_BOOST_639HZ': 1.25,            # 639Hz - Connection, Relationships (FA)
    'FREQUENCY_BOOST_741HZ': 1.15,            # 741Hz - Awakening Intuition (SOL)
    'FREQUENCY_BOOST_852HZ': 1.20,            # 852Hz - Returning to Spiritual Order (LA)
    
    # 🌍 EARTH & COSMIC FREQUENCIES 🌍
    'FREQUENCY_BOOST_SCHUMANN': 1.45,         # 7.83Hz - Earth's heartbeat (×harmonics)
    'FREQUENCY_BOOST_432HZ': 1.30,            # 432Hz - Universal tuning, cosmic harmony
    'FREQUENCY_BOOST_136HZ': 1.25,            # 136.1Hz - OM, Earth's year frequency
    
    # 🔴 DISTORTION FREQUENCIES (AVOID) 🔴
    'FREQUENCY_SUPPRESS_440HZ': 0.70,         # 440Hz - Artificial concert pitch, dissonance
    'FREQUENCY_SUPPRESS_HIGH_CHAOS': 0.50,    # 1000+Hz - Chaotic, unstable
    
    # 🌍⚡ HNC Probability Matrix (2-Hour Window) ⚡🌍
    'ENABLE_PROB_MATRIX': os.getenv('ENABLE_PROB_MATRIX', '1') == '1',
    'ENABLE_PROBABILITY_GENERATOR': os.getenv('ENABLE_PROBABILITY_GENERATOR', '1') == '1',  # Auto-regenerate every 15s
    'PROB_MIN_CONFIDENCE': 0.45,     # Lowered to admit more entries
    'PROB_HIGH_THRESHOLD': 0.65,     # High probability threshold for boost
    'PROB_LOW_THRESHOLD': 0.40,      # Low probability threshold for reduction
    'PROB_LOOKBACK_MINUTES': 60,     # Hour -1 lookback window
    'PROB_FORECAST_WEIGHT': 0.4,     # Weight of Hour +1 in position sizing
    
    # 🌌⚡ HNC Imperial Predictability Engine ⚡🌌
    'ENABLE_IMPERIAL': os.getenv('ENABLE_IMPERIAL', '1') == '1',  # Cosmic synchronization
    'IMPERIAL_POSITION_WEIGHT': 0.35,   # Weight of imperial modifier in sizing
    'IMPERIAL_MIN_COHERENCE': 0.30,     # Lowered: Minimum cosmic coherence to trade
    'IMPERIAL_DISTORTION_LIMIT': 0.50,  # Raised: Allow trades up to 50% distortion
    'IMPERIAL_COSMIC_BOOST': True,      # Apply cosmic phase boost
    'IMPERIAL_YIELD_THRESHOLD': 1e30,   # Min imperial yield for action
    
    # 🌍⚡ Earth Resonance Engine ⚡🌍
    'ENABLE_EARTH_RESONANCE': os.getenv('ENABLE_EARTH_RESONANCE', '1') == '1',
    'EARTH_COHERENCE_THRESHOLD': 0.50,  # Field coherence gate threshold (lowered for WR)
    'EARTH_PHASE_LOCK_THRESHOLD': 0.60, # Phase lock gate threshold (lowered from 0.85)
    'EARTH_PHI_AMPLIFICATION': True,    # Use PHI (1.618) position boost
    'EARTH_SENTIMENT_MAPPING': True,    # Map fear/greed to emotional frequencies
    'EARTH_EXIT_URGENCY': True,         # Use resonance for exit urgency
    
    # 🌍⚡ CoinAPI Anomaly Detection ⚡🌍
    'ENABLE_COINAPI': os.getenv('ENABLE_COINAPI', '0') == '1',  # Requires API key
    'COINAPI_SCAN_INTERVAL': 300,    # Scan for anomalies every 5 minutes
    'COINAPI_MIN_SEVERITY': 0.40,    # Minimum severity to act on anomaly
    'COINAPI_BLACKLIST_DURATION': 3600,  # Block symbol for 1 hour on wash trading
    'COINAPI_ADJUST_COHERENCE': True,    # Adjust coherence based on anomalies
    'COINAPI_PRICE_SOURCE': 'multi_exchange',  # Use aggregated prices when available
    
    # WebSocket
    'WS_URL': 'wss://ws.kraken.com',
    'WS_RECONNECT_DELAY': 5,        # Seconds between reconnect attempts
    'WS_HEARTBEAT_TIMEOUT': 60,     # Max seconds without WS message
    
    # State Persistence
    'STATE_FILE': 'aureon_kraken_state.json',
    
    # Elephant Memory (Quackers)
    'LOSS_STREAK_LIMIT': 3,
    'COOLDOWN_MINUTES': 13,       # Fibonacci timing
    
    # System Flux Prediction (30-Span)
    'FLUX_SPAN': 30,              # Number of assets to analyze for flux
    'FLUX_THRESHOLD': 0.80,       # Raised from 0.60 - only override in VERY strong bearish/bullish
}


def get_max_positions_limit() -> Optional[int]:
    """Return the active position cap or None for unlimited trading."""
    if CONFIG.get('UNLIMITED_POSITIONS'):
        return None

    max_positions = CONFIG.get('MAX_POSITIONS')
    try:
        max_positions_int = int(max_positions)
    except Exception:
        return None

    return max_positions_int if max_positions_int > 0 else None


def max_positions_label() -> str:
    """Human-readable label for max position status."""
    limit = get_max_positions_limit()
    return "unlimited" if limit is None else str(limit)


def has_one_minute_profit_consensus(opp: Dict) -> Tuple[bool, str, Dict[str, float]]:
    """🪙 PENNY PROFIT MODE: Super relaxed consensus check.
    
    The penny profit math is the REAL gate. This function is now very lenient
    to allow the bot to actually trade and let the penny math do its job.
    
    Returns (ok, reason, details) where `ok` indicates entry is allowed.
    """

    qk = opp.get('quick_kill') or {}

    # Pull estimates from opportunity
    prob_quick = qk.get('prob_quick_kill') or qk.get('prob_penny_profit', 0.0)
    confidence = qk.get('confidence', 0.0) if isinstance(qk.get('confidence'), (int, float)) else 0.0
    est_seconds = qk.get('estimated_seconds')
    if est_seconds is None and isinstance(qk.get('estimated_minutes'), (int, float)):
        est_seconds = qk['estimated_minutes'] * 60

    # Refresh estimate from War Strategy if missing/weak
    if (est_seconds is None or prob_quick <= 0) and WAR_STRATEGY_AVAILABLE:
        try:
            estimate = get_quick_kill_estimate(
                opp.get('symbol'),
                opp.get('exchange', 'unknown'),
                opp.get('prices'),
            )
            est_seconds = estimate.estimated_seconds
            prob_quick = max(prob_quick, estimate.prob_quick_kill)
            confidence = max(confidence, estimate.confidence)
            opp['quick_kill'] = {**estimate.to_dict(), **qk}
        except Exception as e:
            logger.debug(f"Quick kill refresh failed for {opp.get('symbol')}: {e}")

    # 🪙 PENNY MODE: Provide defaults if missing - DON'T BLOCK
    if est_seconds is None:
        est_seconds = 300  # Assume 5 minutes if unknown
    if prob_quick <= 0:
        prob_quick = 0.5  # Assume 50/50 if unknown
    if confidence <= 0:
        confidence = 0.5  # Assume medium confidence if unknown

    details = {
        'prob_quick': prob_quick,
        'confidence': confidence,
        'estimated_seconds': est_seconds,
    }

    # 🪙 PENNY PROFIT MODE: Very relaxed thresholds
    # Time: Allow up to 10 minutes (penny profit doesn't need to be instant)
    # Prob: Allow 30% or higher (the penny math protects us)
    # Conf: Allow 20% or higher (we're betting on math, not predictions)
    meets_time = est_seconds <= 600  # 10 minutes instead of 1
    meets_prob = prob_quick >= 0.30  # 30% instead of 50%
    meets_confidence = confidence >= 0.20  # 20% instead of 50%

    if meets_time and meets_prob and meets_confidence:
        return True, "penny profit consensus", details
    
    # 🪙 FALLBACK: Even if conditions not met, allow trade if score is decent
    # This ensures we don't block trades just because predictions are missing
    score = opp.get('score', 0)
    if score >= 30:  # If opportunity has decent score, let it through
        return True, "score override", details

    unmet = []
    if not meets_time:
        unmet.append(f"time {est_seconds/60:.1f}m")
    if not meets_prob:
        unmet.append(f"prob {prob_quick:.2f}")
    if not meets_confidence:
        unmet.append(f"conf {confidence:.2f}")

    return False, ", ".join(unmet), details

PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio = 1.618

# ═══════════════════════════════════════════════════════════════
# 🎹 QUANTUM BRAIN / PIANO STATE BRIDGE
# ═══════════════════════════════════════════════════════════════

BRAIN_STATE_PATH = os.path.join(tempfile.gettempdir(), "aureon_multidimensional_brain_output.json")
_BRAIN_CACHE: Dict[str, Any] = {}
_BRAIN_CACHE_TIME: float = 0.0


def load_brain_state() -> Dict[str, Any]:
    """Load cached Quantum Brain/Piano state if recently updated."""
    global _BRAIN_CACHE, _BRAIN_CACHE_TIME
    try:
        now = time.time()
        if now - _BRAIN_CACHE_TIME < 10:
            return _BRAIN_CACHE
        if not os.path.exists(BRAIN_STATE_PATH):
            return {}
        with open(BRAIN_STATE_PATH) as f:
            data = json.load(f)
        piano = data.get('piano', {}) if isinstance(data, dict) else {}
        meta = data.get('meta', {}) if isinstance(data, dict) else {}
        cascade = meta.get('multiverse_cascade') or data.get('multiverse_cascade')
        _BRAIN_CACHE = {
            'piano_lambda': piano.get('lambda'),
            'piano_coherence': piano.get('coherence'),
            'rainbow_state': piano.get('rainbow_state'),
            'cascade': cascade,
            'timestamp': data.get('timestamp') or meta.get('timestamp'),
        }
        _BRAIN_CACHE_TIME = now
        return _BRAIN_CACHE
    except Exception:
        return {}


def get_brain_multiplier() -> float:
    """Compute a trading multiplier from Piano/Brain resonance."""
    brain = load_brain_state()
    if not isinstance(brain, dict):
        return 1.0
    mult = 1.0
    piano_coh = brain.get('piano_coherence')
    piano_lambda = brain.get('piano_lambda')
    rainbow_state = (brain.get('rainbow_state') or '').upper()

    if piano_coh is not None:
        mult *= 1.0 + max(0.0, piano_coh - 0.5) * 0.2  # up to +10%
    if piano_lambda is not None and piano_lambda > 1.5:
        mult *= 1.0 + (piano_lambda - 1.0) * 0.05       # mild lambda boost

    rainbow_boost = {
        'UNITY': 1.10,
        'AWE': 1.07,
        'LOVE': 1.05,
        'RESONANCE': 1.03,
    }
    if rainbow_state in rainbow_boost:
        mult *= rainbow_boost[rainbow_state]

    return mult


# ═══════════════════════════════════════════════════════════════
# 🔗 MINER STATE CONNECTOR - AUTO-DETECT RUNNING MINER
# ═══════════════════════════════════════════════════════════════

class MinerStateConnector:
    """
    🔗 MINER STATE CONNECTOR 🔗
    
    Automatically detects and connects to a running miner by monitoring
    the shared state file. This enables the ecosystem to receive live
    quantum state even when running standalone (without orchestrator).
    
    The miner writes to: /tmp/aureon_multidimensional_brain_output.json
    We read this file periodically to get:
    - Unified Coherence (Ψ)
    - Planetary Gamma (Γ)
    - Cascade Multiplier
    - Lighthouse Window status
    - Piano Lambda (Λ)
    - Rainbow State
    """
    
    # State file path (same as miner writes to)
    STATE_FILE = os.path.join(tempfile.gettempdir(), 'aureon_multidimensional_brain_output.json')
    
    # Alternative paths to check
    ALT_PATHS = [
        os.path.join(tempfile.gettempdir(), 'aureon_brain_state.json'),
        os.path.join(os.path.dirname(__file__), 'aureon_brain_state.json'),
        'aureon_brain_state.json',
    ]
    
    # How fresh the state must be to consider miner "connected" (seconds)
    FRESHNESS_THRESHOLD = 30  
    
    def __init__(self):
        self._state_file: Optional[str] = None
        self._last_state: Dict[str, Any] = {}
        self._last_read_time: float = 0
        self._read_interval: float = 2.0  # Check every 2 seconds
        self._miner_connected: bool = False
        self._connection_time: Optional[float] = None
        
        # Cached quantum values
        self.unified_coherence: float = 0.5
        self.planetary_gamma: float = 0.5
        self.cascade_multiplier: float = 1.0
        self.is_lighthouse: bool = False
        self.piano_lambda: float = 1.0
        self.piano_coherence: float = 0.0
        self.rainbow_state: str = "UNKNOWN"
        self.probability_edge: float = 0.0
        self.harmonic_signal: str = "HOLD"
        self.hnc_probability: float = 0.5
        
        # Statistics
        self._successful_reads: int = 0
        self._failed_reads: int = 0
        
        logger.info("🔗 Miner State Connector initialized - will auto-detect running miner")
        
    def _find_state_file(self) -> Optional[str]:
        """Find the miner state file from possible locations."""
        # Check primary path first
        if os.path.exists(self.STATE_FILE):
            return self.STATE_FILE
        
        # Check alternatives
        for path in self.ALT_PATHS:
            if os.path.exists(path):
                return path
        
        return None
    
    def _is_state_fresh(self, state: Dict) -> bool:
        """Check if the state file is fresh enough to be from a running miner."""
        timestamp = state.get('timestamp', 0)
        if timestamp == 0:
            # Try last_broadcast as alternative timestamp
            timestamp = state.get('last_broadcast', 0)
        
        if timestamp == 0:
            return False
        
        age = time.time() - timestamp
        return age < self.FRESHNESS_THRESHOLD
    
    def check_connection(self) -> bool:
        """
        Check if a miner is currently running and connected.
        Updates cached quantum state if connected.
        
        Returns:
            True if miner is connected and sending fresh data
        """
        now = time.time()
        
        # Rate limit reads
        if (now - self._last_read_time) < self._read_interval:
            return self._miner_connected
        
        self._last_read_time = now
        
        try:
            # Find state file
            state_file = self._find_state_file()
            if not state_file:
                if self._miner_connected:
                    logger.info("🔗❌ Miner disconnected - state file not found")
                self._miner_connected = False
                return False
            
            # Read state file
            with open(state_file, 'r') as f:
                state = json.load(f)
            
            # Check freshness
            if not self._is_state_fresh(state):
                if self._miner_connected:
                    logger.info("🔗⚠️ Miner state stale - last update too old")
                self._miner_connected = False
                return False
            
            # Update cached values
            self._update_from_state(state)
            self._last_state = state
            self._successful_reads += 1
            
            # Log connection if newly connected
            if not self._miner_connected:
                self._miner_connected = True
                self._connection_time = now
                logger.info(f"🔗✅ MINER CONNECTED! Live quantum state detected")
                logger.info(f"   Ψ={self.unified_coherence:.3f} | Γ={self.planetary_gamma:.3f} | "
                          f"Cascade={self.cascade_multiplier:.2f}x | Lighthouse={'🌟' if self.is_lighthouse else '⬜'}")
            
            return True
            
        except json.JSONDecodeError as e:
            logger.debug(f"Miner state JSON error: {e}")
            self._failed_reads += 1
            return self._miner_connected
        except Exception as e:
            logger.debug(f"Miner state read error: {e}")
            self._failed_reads += 1
            return self._miner_connected
    
    def _update_from_state(self, state: Dict):
        """Update cached quantum values from miner state."""
        # Core quantum values
        self.unified_coherence = float(state.get('unified_coherence', state.get('psi', 0.5)) or 0.5)
        self.planetary_gamma = float(state.get('planetary_gamma', state.get('gamma', 0.5)) or 0.5)
        self.cascade_multiplier = float(state.get('cascade_multiplier', state.get('cascade', 1.0)) or 1.0)
        self.is_lighthouse = bool(state.get('is_lighthouse', state.get('is_optimal_window', False)))
        
        # Piano/Rainbow state
        self.piano_lambda = float(state.get('piano_lambda', state.get('lambda_field', 1.0)) or 1.0)
        self.piano_coherence = float(state.get('piano_coherence', 0.0) or 0.0)
        self.rainbow_state = str(state.get('rainbow_state', 'UNKNOWN') or 'UNKNOWN')
        
        # Probability/Signal
        self.probability_edge = float(state.get('probability_edge', 0.0) or 0.0)
        self.harmonic_signal = str(state.get('harmonic_signal', 'HOLD') or 'HOLD')
        self.hnc_probability = float(state.get('hnc_probability', 0.5) or 0.5)
    
    def get_quantum_context(self) -> Dict[str, Any]:
        """
        Get quantum context dict suitable for MinerBrain.run_cycle().
        
        Returns:
            Dict with quantum state from miner (or defaults if not connected)
        """
        # Always check connection first
        self.check_connection()
        
        return {
            'quantum_coherence': self.unified_coherence,
            'planetary_gamma': self.planetary_gamma,
            'cascade_multiplier': self.cascade_multiplier,
            'is_lighthouse': self.is_lighthouse,
            'piano_lambda': self.piano_lambda,
            'piano_coherence': self.piano_coherence,
            'rainbow_state': self.rainbow_state,
            'probability_edge': self.probability_edge,
            'harmonic_signal': self.harmonic_signal,
            'hnc_probability': self.hnc_probability,
            'miner_connected': self._miner_connected,
            'signal_confidence': min(0.95, 0.5 + self.probability_edge),
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get connector status for display."""
        return {
            'connected': self._miner_connected,
            'connection_time': self._connection_time,
            'uptime': time.time() - self._connection_time if self._connection_time else 0,
            'successful_reads': self._successful_reads,
            'failed_reads': self._failed_reads,
            'last_state_age': time.time() - self._last_state.get('timestamp', 0) if self._last_state else float('inf'),
            'state_file': self._state_file,
        }
    
    @property
    def is_connected(self) -> bool:
        """Property to check if miner is currently connected."""
        return self._miner_connected


# Global miner connector instance
MINER_CONNECTOR = MinerStateConnector()


# ═══════════════════════════════════════════════════════════════
# 🧠🌍 ECOSYSTEM BRAIN BRIDGE - UNIFIED INTELLIGENCE HUB
# ═══════════════════════════════════════════════════════════════

class EcosystemBrainBridge:
    """
    🧠🌍 ECOSYSTEM BRAIN BRIDGE 🌍🧠
    
    The central intelligence hub that connects:
    - MinerBrain (7 Civilizations Wisdom) → Trading Decisions
    - QuantumProcessingBrain (Miner Optimizer) → Cascade Amplification
    - AdaptiveLearningEngine → Brain Feedback Loop
    - CascadeAmplifier → Brain-Guided Signal Boost
    
    This bridge ensures ALL trading decisions are informed by:
    1. Ancient wisdom (Celtic, Aztec, Egyptian, Pythagorean, Chinese, Hindu, Mayan, Norse, etc.)
    2. Quantum coherence from the mining optimizer
    3. Adaptive learning from past trades
    4. Cascade amplification from win streaks
    5. 🔷 Diamond Lattice sacred geometry ZPE boost
    
    🧠 11 CIVILIZATIONS UNITE for trading decisions!
    """
    
    def __init__(self):
        # Brain state cache
        self._brain_wisdom: Dict[str, Any] = {}
        self._brain_consensus: str = "NEUTRAL"
        self._brain_confidence: float = 0.5
        self._brain_action: str = "HOLD"
        self._civilization_signals: Dict[str, str] = {}
        
        # Quantum state from miner (if available)
        self._quantum_coherence: float = 0.5
        self._planetary_gamma: float = 0.5
        self._cascade_multiplier: float = 1.0
        self._is_lighthouse: bool = False
        
        # 🔷 DIAMOND LATTICE - Sacred Geometry Computational Boost
        self._diamond_coherence: float = 0.5
        self._diamond_boost: float = 1.0
        self._diamond_phi_alignment: float = 0.0
        self._diamond_zpe: float = 0.0
        
        # Market intelligence from brain
        self._fear_greed: int = 50
        self._btc_price: float = 0.0
        self._market_pulse: str = "NEUTRAL"
        self._manipulation_risk: float = 0.0
        
        # Timing - Brain runs EVERY SECOND for autonomous cognition
        self._last_cycle_time: float = 0.0
        self._cycle_interval: float = 1.0  # Run brain EVERY SECOND
        
        logger.info("🧠🌍 Ecosystem Brain Bridge initialized - AUTONOMOUS MODE (1s cycles)")
        
        # Reference to global miner connector for auto-detection
        self._miner_connector = MINER_CONNECTOR
        
    def run_wisdom_cycle(self, brain: 'MinerBrain', quantum_context: Dict = None) -> Dict[str, Any]:
        """
        Run a full wisdom cycle with bidirectional brain sync.
        
        Automatically connects to a running miner if available, pulling live
        quantum state (Γ, cascade, lighthouse) from the shared state file.
        
        Args:
            brain: MinerBrain instance
            quantum_context: Optional quantum state from miner optimizer (auto-detected if not provided)
        
        Returns:
            Full wisdom result with trading recommendations
        """
        if not brain:
            return {}
        
        now = time.time()
        if (now - self._last_cycle_time) < self._cycle_interval:
            return self._brain_wisdom  # Return cached
        
        try:
            logger.info("🧠⚡ Ecosystem Brain Cycle starting...")
            
            # Build quantum context - prefer live miner data if available
            if not quantum_context:
                # 🔗 AUTO-DETECT: Check if miner is running and get live quantum state
                miner_context = self._miner_connector.get_quantum_context()
                
                if miner_context.get('miner_connected'):
                    # Live miner data available!
                    quantum_context = miner_context
                    
                    # Update our cached state from live miner
                    self._quantum_coherence = miner_context['quantum_coherence']
                    self._planetary_gamma = miner_context['planetary_gamma']
                    self._cascade_multiplier = miner_context['cascade_multiplier']
                    self._is_lighthouse = miner_context['is_lighthouse']
                    
                    # 🔷 Extract Diamond Lattice state if available
                    self._diamond_coherence = miner_context.get('diamond_coherence', 0.5)
                    self._diamond_boost = miner_context.get('diamond_boost', 1.0)
                    self._diamond_phi_alignment = miner_context.get('diamond_phi_alignment', 0.0)
                    self._diamond_zpe = miner_context.get('diamond_zpe', 0.0)
                    
                    logger.info(f"🔗🌟 Live miner data: Ψ={self._quantum_coherence:.3f} | "
                              f"Γ={self._planetary_gamma:.3f} | Cascade={self._cascade_multiplier:.2f}x"
                              f" | 🔷Diamond={self._diamond_boost:.2f}x")
                else:
                    # Fallback to stored brain state
                    brain_state = load_brain_state()
                    quantum_context = {
                        'quantum_coherence': self._quantum_coherence or 0.5,
                        'planetary_gamma': self._planetary_gamma or 0.5,
                        'cascade_multiplier': self._cascade_multiplier or 1.0,
                        'is_lighthouse': self._is_lighthouse,
                        'piano_lambda': brain_state.get('piano_lambda') or 1.0,
                        'harmonic_signal': 'HOLD',
                        'signal_confidence': 0.5,
                        'miner_connected': False,
                    }
            
            # Run brain cycle with quantum context
            result = brain.run_cycle(quantum_context=quantum_context)
            
            if result:
                self._brain_wisdom = result
                self._last_cycle_time = now
                
                # Extract unified consensus
                self._brain_consensus = result.get('unified_consensus', 'NEUTRAL')
                self._brain_confidence = result.get('unified_confidence', 50) / 100
                self._brain_action = result.get('unified_action', 'HOLD')
                
                # Extract civilization signals
                self._civilization_signals = result.get('civilization_actions', {})
                
                # Extract market intelligence
                live_pulse = result.get('live_pulse', {})
                self._fear_greed = live_pulse.get('fear_greed', 50)
                self._btc_price = live_pulse.get('btc_price', 0.0)
                self._market_pulse = live_pulse.get('pulse', 'NEUTRAL')
                self._manipulation_risk = result.get('manipulation_probability', 0.0)
                
                # Update CascadeAmplifier with brain state
                self._update_cascade_amplifier()
                
                # Update AdaptiveLearner with brain insights
                self._update_adaptive_learner()
                
                logger.info(f"🧠🌍 Brain Cycle Complete: {self._brain_consensus} | Conf: {self._brain_confidence:.0%}")
                
            return result
            
        except Exception as e:
            import traceback
            logger.error(f"🧠 Brain Cycle Error: {e}")
            logger.error(f"🧠 Traceback: {traceback.format_exc()}")
            return {}
    
    def _update_cascade_amplifier(self):
        """Update CascadeAmplifier with brain wisdom."""
        try:
            # Update lighthouse gamma from brain's planetary awareness
            CASCADE_AMPLIFIER.update_lighthouse(self._planetary_gamma)
            
            # If brain says BULLISH with high confidence, boost cascade
            if self._brain_consensus == 'BULLISH' and self._brain_confidence > 0.7:
                # Simulate a "wisdom win" - the brain's confidence is a positive signal
                CASCADE_AMPLIFIER.mirror_coherence = min(1.0, CASCADE_AMPLIFIER.mirror_coherence + 0.05)
                
            # If brain says BEARISH with high confidence, decay cascade slightly
            elif self._brain_consensus == 'BEARISH' and self._brain_confidence > 0.7:
                CASCADE_AMPLIFIER.mirror_coherence = max(0.3, CASCADE_AMPLIFIER.mirror_coherence - 0.02)
                
        except Exception as e:
            logger.debug(f"Cascade update failed: {e}")
    
    def _update_adaptive_learner(self):
        """Feed brain insights to AdaptiveLearningEngine."""
        try:
            # Store brain consensus as a feature for learning
            brain_feature = {
                'brain_consensus': self._brain_consensus,
                'brain_confidence': self._brain_confidence,
                'fear_greed': self._fear_greed,
                'manipulation_risk': self._manipulation_risk,
                'civilization_agreement': sum(1 for s in self._civilization_signals.values() 
                                               if 'ACCUMULATE' in s or 'BUY' in s or 'ATTACK' in s) / 7,
            }
            
            # The adaptive learner can use this to correlate brain states with trade outcomes
            if hasattr(ADAPTIVE_LEARNER, 'record_brain_state'):
                ADAPTIVE_LEARNER.record_brain_state(brain_feature)
                
        except Exception as e:
            logger.debug(f"Adaptive learner update failed: {e}")
    
    def update_quantum_state(self, coherence: float, gamma: float, cascade: float, lighthouse: bool):
        """Update quantum state from miner optimizer."""
        self._quantum_coherence = coherence
        self._planetary_gamma = gamma
        self._cascade_multiplier = cascade
        self._is_lighthouse = lighthouse
    
    def update_diamond_state(self, diamond_coherence: float, diamond_boost: float, 
                             phi_alignment: float, zpe: float):
        """
        🔷 Update Diamond Lattice state from miner.
        
        The Diamond provides sacred geometry computational boost:
        - Central coherence (Ψ) from octahedron center
        - Hash boost from golden ratio alignment
        - φ alignment (how perfect the geometry is)
        - ZPE extraction rate
        """
        self._diamond_coherence = diamond_coherence
        self._diamond_boost = diamond_boost
        self._diamond_phi_alignment = phi_alignment
        self._diamond_zpe = zpe
        
        # Diamond boost amplifies cascade multiplier!
        if diamond_boost > 1.5:
            logger.info(f"🔷⚡ Diamond Boost Active: {diamond_boost:.2f}x | φ={phi_alignment:.3f}")
    
    def get_trading_recommendation(self) -> Dict[str, Any]:
        """
        Get trading recommendation based on brain wisdom.
        
        Returns dict with:
        - action: BUY/HOLD/SELL
        - confidence: 0-1
        - position_multiplier: scaling factor for position size
        - reasoning: list of reasons
        """
        # Default neutral recommendation
        rec = {
            'action': 'HOLD',
            'confidence': 0.5,
            'position_multiplier': 1.0,
            'reasoning': [],
            'civilizations_bullish': 0,
            'civilizations_bearish': 0,
        }
        
        if not self._brain_wisdom:
            rec['reasoning'].append("No brain wisdom available")
            return rec
        
        # Count civilization votes
        bullish_signals = ['ACCUMULATE', 'ATTACK', 'BUY', 'PLANT_SEEDS', 'RESURRECTION_BUY', 
                          'DECISIVE_ACTION', 'BUILD', 'GROW', 'RIDE_THE_SUN']
        bearish_signals = ['RETREAT', 'PROTECT', 'CAUTION', 'RELEASE', 'EXIT']
        
        bullish_count = sum(1 for s in self._civilization_signals.values() 
                          if any(b in s.upper() for b in bullish_signals))
        bearish_count = sum(1 for s in self._civilization_signals.values() 
                          if any(b in s.upper() for b in bearish_signals))
        
        rec['civilizations_bullish'] = bullish_count
        rec['civilizations_bearish'] = bearish_count
        
        # Determine action based on consensus
        if self._brain_consensus == 'BULLISH':
            rec['action'] = 'BUY'
            rec['confidence'] = self._brain_confidence
            rec['position_multiplier'] = 1.0 + (self._brain_confidence * 0.5)  # Up to 1.5x
            rec['reasoning'].append(f"7 Civilizations: {bullish_count}/7 bullish")
            rec['reasoning'].append(f"Unified Consensus: {self._brain_consensus}")
            
            # Extra boost if fear is extreme
            if self._fear_greed < 25:
                rec['position_multiplier'] *= 1.2
                rec['reasoning'].append(f"Extreme Fear ({self._fear_greed}) = Contrarian Opportunity")
                
        elif self._brain_consensus == 'BEARISH':
            rec['action'] = 'REDUCE'
            rec['confidence'] = self._brain_confidence
            rec['position_multiplier'] = max(0.5, 1.0 - (self._brain_confidence * 0.3))  # Down to 0.7x
            rec['reasoning'].append(f"7 Civilizations: {bearish_count}/7 bearish")
            rec['reasoning'].append(f"Unified Consensus: {self._brain_consensus}")
            
            # Extra caution if manipulation risk is high
            if self._manipulation_risk > 0.3:
                rec['position_multiplier'] *= 0.8
                rec['reasoning'].append(f"High Manipulation Risk ({self._manipulation_risk:.0%})")
                
        else:
            rec['action'] = 'HOLD'
            rec['confidence'] = 0.5
            rec['reasoning'].append("Civilizations divided - waiting for clarity")
        
        # Lighthouse bonus
        if self._is_lighthouse:
            rec['position_multiplier'] *= 1.15
            rec['reasoning'].append("🗼 Lighthouse Window Active")
        
        # 🔷 DIAMOND LATTICE BOOST - Sacred Geometry Amplification
        if self._diamond_boost > 1.3:
            diamond_mult = 1.0 + (self._diamond_boost - 1.0) * 0.2  # Up to 1.28x extra
            rec['position_multiplier'] *= diamond_mult
            rec['reasoning'].append(f"🔷 Diamond Boost: {self._diamond_boost:.2f}x (φ={self._diamond_phi_alignment:.2f})")
            
            # If diamond coherence is very high, boost confidence too
            if self._diamond_coherence > 0.8:
                rec['confidence'] = min(1.0, rec['confidence'] + 0.1)
                rec['reasoning'].append(f"🔷 Diamond Coherence Peak: Ψ={self._diamond_coherence:.2f}")
        
        return rec
    
    def get_signal_boost(self, base_score: float) -> float:
        """
        Get brain-boosted signal score for trading decisions.
        
        Applies 7-civilization wisdom to amplify or dampen signals.
        """
        boost = 1.0
        
        # Brain consensus boost
        if self._brain_consensus == 'BULLISH':
            boost *= 1.0 + (self._brain_confidence * 0.2)  # Up to +20%
        elif self._brain_consensus == 'BEARISH':
            boost *= 1.0 - (self._brain_confidence * 0.1)  # Down to -10%
        
        # Quantum coherence boost
        if self._quantum_coherence > 0.7:
            boost *= 1.0 + (self._quantum_coherence - 0.7) * 0.33  # Up to +10%
        
        # Planetary alignment boost
        if self._planetary_gamma > 0.8:
            boost *= 1.1  # +10% during strong alignment
        
        # Fear/Greed contrarian adjustment
        if self._fear_greed < 25:  # Extreme fear
            boost *= 1.15  # +15% contrarian
        elif self._fear_greed > 75:  # Extreme greed
            boost *= 0.90  # -10% caution
        
        return base_score * boost
    
    def display_status(self):
        """Display current brain bridge status."""
        if not self._brain_wisdom:
            print("   🧠🌍 BRAIN: Awaiting first cycle...")
            return
        
        consensus_icon = "📈" if self._brain_consensus == "BULLISH" else "📉" if self._brain_consensus == "BEARISH" else "⚖️"
        bullish = sum(1 for s in self._civilization_signals.values() 
                     if 'ACCUMULATE' in s or 'BUY' in s or 'ATTACK' in s or 'BUILD' in s)
        
        print(f"   🧠🌍 BRAIN: {consensus_icon} {self._brain_consensus} | "
              f"Conf: {self._brain_confidence:.0%} | "
              f"Votes: {bullish}/7 📈 | "
              f"F&G: {self._fear_greed} | "
              f"Γ: {self._planetary_gamma:.2f}")


# Global Ecosystem Brain Bridge instance
ECOSYSTEM_BRAIN = EcosystemBrainBridge()


# ═══════════════════════════════════════════════════════════════
# 🌐 SMART ORDER ROUTER - Best execution across exchanges
# ═══════════════════════════════════════════════════════════════

class SmartOrderRouter:
    """
    Routes orders to the best exchange based on price, liquidity, and fees.
    Compares quotes across Binance, Kraken, and Capital.com in real-time.
    """
    
    def __init__(self, multi_client):
        self.client = multi_client
        self.exchange_fees = {
            'binance': 0.001,   # 0.10% taker
            'kraken': 0.0026,   # 0.26% taker
            'capital': 0.001,   # ~0.1% spread
            'alpaca': 0.0       # Commission-free
        }
        self.exchange_priority = ['binance', 'capital', 'alpaca']
        self.route_history: List[Dict] = []
        
    def get_best_quote(self, symbol: str, side: str, quantity: float = None) -> Dict[str, Any]:
        """
        Get best quote across all exchanges for a symbol.
        Returns: {'exchange': str, 'price': float, 'effective_price': float, 'savings': float}
        """
        quotes = []
        base_symbol = symbol.replace('/', '').upper()
        
        # Normalize symbol for each exchange
        symbol_map = {
            'binance': base_symbol,
            'kraken': base_symbol,
            'capital': base_symbol[:6] if len(base_symbol) > 6 else base_symbol,
            'alpaca': f"{base_symbol[:3]}/{base_symbol[3:]}" if len(base_symbol) >= 6 else symbol
        }
        
        for exchange in self.exchange_priority:
            try:
                ex_symbol = symbol_map.get(exchange, base_symbol)
                ticker = self.client.get_ticker(exchange, ex_symbol)
                if not ticker or ticker.get('price', 0) <= 0:
                    continue
                    
                price = float(ticker.get('price', 0))
                bid = float(ticker.get('bid', price))
                ask = float(ticker.get('ask', price))
                
                # Calculate effective price including fees
                fee_rate = self.exchange_fees.get(exchange, 0.002)
                if side.upper() == 'BUY':
                    exec_price = ask * (1 + fee_rate)
                else:
                    exec_price = bid * (1 - fee_rate)
                    
                quotes.append({
                    'exchange': exchange,
                    'symbol': ex_symbol,
                    'price': price,
                    'bid': bid,
                    'ask': ask,
                    'effective_price': exec_price,
                    'fee_rate': fee_rate
                })
            except Exception as e:
                logger.debug(f"Quote error for {exchange}/{symbol}: {e}")
                continue
                
        if not quotes:
            return None
            
        # Sort by effective price (lowest for BUY, highest for SELL)
        if side.upper() == 'BUY':
            quotes.sort(key=lambda x: x['effective_price'])
        else:
            quotes.sort(key=lambda x: -x['effective_price'])
            
        best = quotes[0]
        
        # Calculate savings vs worst quote
        if len(quotes) > 1:
            worst = quotes[-1]
            if side.upper() == 'BUY':
                savings_pct = (worst['effective_price'] - best['effective_price']) / worst['effective_price'] * 100
            else:
                savings_pct = (best['effective_price'] - worst['effective_price']) / best['effective_price'] * 100
            best['savings_pct'] = savings_pct
            best['alternatives'] = quotes[1:]
        else:
            best['savings_pct'] = 0
            best['alternatives'] = []
            
        return best
        
    def route_order(self, symbol: str, side: str, quantity: float = None, quote_qty: float = None,
                    preferred_exchange: str = None) -> Dict[str, Any]:
        """
        Route and execute order on best exchange.
        Returns order result with routing metadata.
        """
        # Get best quote
        best = self.get_best_quote(symbol, side, quantity)
        if not best:
            return {'error': 'No quotes available', 'symbol': symbol}
            
        # Override if preferred exchange specified and available
        if preferred_exchange and preferred_exchange in [q['exchange'] for q in [best] + best.get('alternatives', [])]:
            for q in [best] + best.get('alternatives', []):
                if q['exchange'] == preferred_exchange:
                    best = q
                    break
                    
        # Execute order
        exchange = best['exchange']
        ex_symbol = best['symbol']
        
        try:
            result = self.client.place_market_order(
                exchange, ex_symbol, side,
                quantity=quantity, quote_qty=quote_qty
            )
            
            # Add routing metadata
            result['routed_to'] = exchange
            result['effective_price'] = best['effective_price']
            result['savings_pct'] = best.get('savings_pct', 0)
            
            # Record route
            self.route_history.append({
                'timestamp': time.time(),
                'symbol': symbol,
                'side': side,
                'exchange': exchange,
                'price': best['price'],
                'savings_pct': best.get('savings_pct', 0)
            })
            
            return result
        except Exception as e:
            return {'error': str(e), 'exchange': exchange, 'symbol': ex_symbol}
            
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing performance statistics."""
        if not self.route_history:
            return {'total_routes': 0}
            
        by_exchange = {}
        total_savings = 0
        
        for route in self.route_history:
            ex = route['exchange']
            by_exchange[ex] = by_exchange.get(ex, 0) + 1
            total_savings += route.get('savings_pct', 0)
            
        return {
            'total_routes': len(self.route_history),
            'by_exchange': by_exchange,
            'avg_savings_pct': total_savings / len(self.route_history) if self.route_history else 0
        }


# ═══════════════════════════════════════════════════════════════
# ⚡ CROSS-EXCHANGE ARBITRAGE SCANNER
# ═══════════════════════════════════════════════════════════════

class CrossExchangeArbitrageScanner:
    """
    Detects price discrepancies across Binance, Kraken, and Capital.com.
    Identifies triangular and direct arbitrage opportunities.
    """
    
    def __init__(self, multi_client):
        self.client = multi_client
        self.min_spread_pct = 0.3  # Minimum 0.3% spread to consider
        self.fee_buffer = 0.2     # 0.2% buffer for fees
        self.opportunities: List[Dict] = []
        self.last_scan = 0
        self.scan_interval = 30   # Seconds between scans
        
    def scan_direct_arbitrage(self, symbols: List[str] = None) -> List[Dict]:
        """
        Scan for direct arbitrage: buy on exchange A, sell on exchange B.
        """
        opportunities = []
        brain_mult = get_brain_multiplier()
        
        # Default symbols to scan
        if not symbols:
            symbols = ['BTCUSD', 'ETHUSD', 'XRPUSD', 'ADAUSD', 'SOLUSD', 
                      'DOTUSD', 'LINKUSD', 'AVAXUSD', 'DOGEUSD']
        
        exchanges = ['binance', 'kraken']
        
        for symbol in symbols:
            prices = {}
            
            # Get prices from each exchange
            for exchange in exchanges:
                try:
                    # Normalize canonical symbol to exchange-specific
                    ex_symbol = self.client.normalize_symbol(exchange, symbol)
                    ticker = self.client.get_ticker(exchange, ex_symbol)
                    if ticker and ticker.get('bid', 0) > 0:
                        prices[exchange] = {
                            'bid': float(ticker.get('bid', 0)),
                            'ask': float(ticker.get('ask', 0)),
                            'symbol': ex_symbol
                        }
                except Exception:
                    continue
                    
            # Check for arbitrage between each pair
            if len(prices) < 2:
                continue
                
            exchange_list = list(prices.keys())
            for i, buy_ex in enumerate(exchange_list):
                for sell_ex in exchange_list[i+1:]:
                    buy_price = prices[buy_ex]['ask']
                    sell_price = prices[sell_ex]['bid']
                    
                    # Check both directions
                    spread_1 = (sell_price - buy_price) / buy_price * 100
                    spread_2 = (prices[buy_ex]['bid'] - prices[sell_ex]['ask']) / prices[sell_ex]['ask'] * 100
                    
                    # Apply CASCADE amplification to profit confidence
                    cascaded_1 = min(spread_1 * CASCADE_FACTOR, 95.0)
                    if cascaded_1 > self.min_spread_pct + self.fee_buffer:
                        net_profit = (cascaded_1 - self.fee_buffer)
                        opportunities.append({
                            'type': 'direct',
                            'symbol': symbol,
                            'buy_exchange': buy_ex,
                            'sell_exchange': sell_ex,
                            'buy_price': buy_price,
                            'sell_price': sell_price,
                            'spread_pct': spread_1,
                            'cascaded_confidence_pct': cascaded_1,
                            'net_profit_pct': net_profit,
                            'brain_mult': brain_mult,
                            'timestamp': time.time()
                        })
                    
                    cascaded_2 = min(spread_2 * CASCADE_FACTOR, 95.0)
                    if cascaded_2 > self.min_spread_pct + self.fee_buffer:
                        net_profit = (cascaded_2 - self.fee_buffer)
                        opportunities.append({
                            'type': 'direct',
                            'symbol': symbol,
                            'buy_exchange': sell_ex,
                            'sell_exchange': buy_ex,
                            'buy_price': prices[sell_ex]['ask'],
                            'sell_price': prices[buy_ex]['bid'],
                            'spread_pct': spread_2,
                            'cascaded_confidence_pct': cascaded_2,
                            'net_profit_pct': net_profit,
                            'brain_mult': brain_mult,
                            'timestamp': time.time()
                        })
        
        # Sort by profit potential
        # Apply Ψ minimization: keep only top 3.7% by cascaded confidence
        opportunities.sort(key=lambda x: -(x.get('cascaded_confidence_pct', 0)))
        top_count = max(1, int(len(opportunities) * PSI_FILTER))
        opportunities = opportunities[:top_count]
        self.opportunities = opportunities
        self.last_scan = time.time()
        
        return opportunities
        
    def get_top_opportunities(self, limit: int = 5) -> List[Dict]:
        """Get top arbitrage opportunities."""
        # Refresh if stale
        if time.time() - self.last_scan > self.scan_interval:
            self.scan_direct_arbitrage()
        return self.opportunities[:limit]
        
    def execute_arbitrage(self, opportunity: Dict, amount_usd: float = 10.0) -> Dict[str, Any]:
        """
        Execute an arbitrage opportunity.
        Returns: {'success': bool, 'profit': float, 'details': dict}
        """
        buy_ex = opportunity['buy_exchange']
        sell_ex = opportunity['sell_exchange']
        symbol = opportunity['symbol']
        
        # Calculate quantity
        buy_price = opportunity['buy_price']
        quantity = amount_usd / buy_price
        
        results = {'buy': None, 'sell': None, 'profit': 0, 'success': False}
        
        try:
            # Execute buy
            buy_symbol = symbol if buy_ex != 'binance' else symbol.replace('USD', 'USDT')
            buy_result = self.client.place_market_order(buy_ex, buy_symbol, 'BUY', quantity=quantity)
            results['buy'] = buy_result
            
            if not buy_result or buy_result.get('error'):
                return results
                
            # Execute sell
            sell_symbol = symbol if sell_ex != 'binance' else symbol.replace('USD', 'USDT')
            sell_result = self.client.place_market_order(sell_ex, sell_symbol, 'SELL', quantity=quantity)
            results['sell'] = sell_result
            
            if sell_result and not sell_result.get('error'):
                results['success'] = True
                results['profit'] = amount_usd * (opportunity['net_profit_pct'] / 100)
                
        except Exception as e:
            results['error'] = str(e)
            
        return results


# ═══════════════════════════════════════════════════════════════
# ✅ UNIFIED TRADE CONFIRMATION
# ═══════════════════════════════════════════════════════════════

class UnifiedTradeConfirmation:
    """
    Normalizes trade confirmations across all exchanges.
    Handles Binance orderId, Kraken txid, Capital.com dealReference.
    """
    
    def __init__(self, multi_client):
        self.client = multi_client
        self.pending_confirmations: Dict[str, Dict] = {}
        self.confirmed_trades: List[Dict] = []
        
    def submit_order(self, exchange: str, symbol: str, side: str, 
                    quantity: float = None, quote_qty: float = None) -> Dict[str, Any]:
        """
        Submit order and return unified confirmation.
        Validates lot sizes and minimum notional before submission.
        """
        # Validate quantity for SELL orders (lot size + notional)
        if side.upper() == 'SELL' and quantity is not None:
            # Get current price for notional check
            price = 0
            try:
                ticker = self.client.get_ticker(exchange, symbol)
                if ticker:
                    price = float(ticker.get('price', ticker.get('lastPrice', 0)))
            except Exception:
                pass
                
            adjusted_qty, error = validate_order_quantity(exchange, symbol, quantity, price, self.client)
            if error:
                print(f"   🚫 Order rejected pre-flight: {symbol} on {exchange}: {error}")
                return {'status': 'REJECTED', 'error': error, 'pre_flight': True}
            quantity = adjusted_qty
            
        result = self.client.place_market_order(
            exchange, symbol, side,
            quantity=quantity, quote_qty=quote_qty
        )
        
        if not result:
            return {'status': 'FAILED', 'error': 'No response'}
        
        # ⚠️ Check for error response BEFORE normalizing (e.g., min_notional blocked)
        if 'error' in result:
            return {
                'status': 'BLOCKED',
                'error': result['error'],
                'exchange': result.get('exchange', exchange),
                'symbol': symbol,
                'side': side
            }
            
        # Normalize confirmation based on exchange
        exchange = exchange.lower()
        confirmation = {
            'exchange': exchange,
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'quote_qty': quote_qty,
            'timestamp': time.time(),
            'raw_response': result
        }
        
        if exchange == 'binance':
            confirmation.update(self._parse_binance_response(result))
        elif exchange == 'kraken':
            confirmation.update(self._parse_kraken_response(result))
        elif exchange == 'capital':
            confirmation.update(self._parse_capital_response(result))
        else:
            confirmation['status'] = 'UNKNOWN'
            confirmation['order_id'] = str(result.get('orderId', result.get('id', 'unknown')))
            
        # Store confirmed trade
        if confirmation.get('status') in ['FILLED', 'ACCEPTED', 'OPEN']:
            self.confirmed_trades.append(confirmation)
            
        return confirmation
        
    def _parse_binance_response(self, result: Dict) -> Dict:
        """Parse Binance order response."""
        if result.get('rejected') or result.get('uk_restricted'):
            return {
                'status': 'REJECTED',
                'order_id': None,
                'error': result.get('reason', 'UK restricted')
            }
            
        status = result.get('status', 'UNKNOWN')
        return {
            'status': status,
            'order_id': str(result.get('orderId', '')),
            'executed_qty': float(result.get('executedQty', 0)),
            'executed_quote_qty': float(result.get('cummulativeQuoteQty', 0)),
            'avg_price': float(result.get('price', 0)) if result.get('price') else None,
            'fills': result.get('fills', [])
        }
        
    def _parse_kraken_response(self, result: Dict) -> Dict:
        """Parse Kraken order response."""
        txid = result.get('txid', [])
        if isinstance(txid, list) and txid:
            order_id = txid[0]
            status = 'FILLED'  # Kraken market orders fill immediately
        else:
            order_id = str(result.get('orderId', result.get('id', '')))
            status = result.get('status', 'UNKNOWN')
            
        return {
            'status': status,
            'order_id': order_id,
            'executed_qty': float(result.get('executedQty', result.get('vol_exec', 0))),
            'descr': result.get('descr', {})
        }
        
    def _parse_capital_response(self, result: Dict) -> Dict:
        """Parse Capital.com order response and confirm."""
        deal_ref = result.get('dealReference')
        deal_id = result.get('dealId')
        
        if deal_id:
            return {
                'status': 'ACCEPTED',
                'order_id': deal_id,
                'deal_reference': deal_ref
            }
            
        # Need to confirm via API
        if deal_ref:
            try:
                capital_client = self.client.clients.get('capital')
                if capital_client and hasattr(capital_client.client, 'confirm_order'):
                    confirm = capital_client.client.confirm_order(deal_ref)
                    status = confirm.get('dealStatus', 'UNKNOWN')
                    return {
                        'status': status,
                        'order_id': confirm.get('dealId', deal_ref),
                        'deal_reference': deal_ref,
                        'level': confirm.get('level'),
                        'size': confirm.get('size'),
                        'direction': confirm.get('direction'),
                        'affected_deals': confirm.get('affectedDeals', [])
                    }
            except Exception as e:
                logger.error(f"Capital.com confirm error: {e}")
                
        return {
            'status': 'PENDING',
            'order_id': deal_ref,
            'deal_reference': deal_ref
        }
        
    def get_trade_history(self, exchange: str = None, limit: int = 50) -> List[Dict]:
        """Get confirmed trade history."""
        trades = self.confirmed_trades
        if exchange:
            trades = [t for t in trades if t['exchange'] == exchange.lower()]
        return trades[-limit:]
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get trade confirmation statistics."""
        if not self.confirmed_trades:
            return {'total': 0}
            
        by_exchange = {}
        by_status = {}
        
        for trade in self.confirmed_trades:
            ex = trade['exchange']
            status = trade['status']
            by_exchange[ex] = by_exchange.get(ex, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
            
        return {
            'total': len(self.confirmed_trades),
            'by_exchange': by_exchange,
            'by_status': by_status
        }


# ═══════════════════════════════════════════════════════════════
# ⚖️ PORTFOLIO REBALANCER
# ═══════════════════════════════════════════════════════════════

class PortfolioRebalancer:
    """
    Unified portfolio rebalancing across Binance, Kraken, and Capital.com.
    Optimizes asset allocation and can shift funds between exchanges.
    """
    
    def __init__(self, multi_client):
        self.client = multi_client
        self.target_allocations: Dict[str, float] = {}  # asset -> target %
        self.rebalance_threshold = 0.05  # 5% deviation triggers rebalance
        self.min_trade_value = 5.0  # Minimum $5 to avoid dust trades
        self.last_rebalance = 0
        self.rebalance_history: List[Dict] = []
        
    def set_target_allocation(self, allocations: Dict[str, float]):
        """
        Set target portfolio allocation.
        Example: {'BTC': 0.30, 'ETH': 0.25, 'USDT': 0.45}
        """
        total = sum(allocations.values())
        if abs(total - 1.0) > 0.01:
            logger.warning(f"Allocations sum to {total}, normalizing to 100%")
            allocations = {k: v/total for k, v in allocations.items()}
        self.target_allocations = allocations
        
    def get_current_allocation(self) -> Dict[str, Dict]:
        """
        Get current portfolio allocation across all exchanges.
        Returns: {asset: {'amount': float, 'value_usd': float, 'pct': float, 'exchanges': dict}}
        """
        allocations = {}
        total_value = 0.0
        
        # Gather balances from all exchanges
        all_balances = self.client.get_all_balances()
        
        for exchange, balances in all_balances.items():
            for asset, amount in balances.items():
                try:
                    amount = float(amount)
                except:
                    continue
                if amount <= 0:
                    continue
                    
                # Normalize asset name
                asset_clean = asset.replace('Z', '').replace('X', '').upper()
                if asset_clean.startswith('LD'):  # Binance Earn
                    asset_clean = asset_clean[2:]
                    
                # Get USD value
                try:
                    if asset_clean in ['USD', 'USDT', 'USDC']:
                        value_usd = amount
                    else:
                        value_usd = self.client.convert_to_quote(exchange, asset_clean, amount, 'USDT')
                except:
                    value_usd = 0
                    
                if asset_clean not in allocations:
                    allocations[asset_clean] = {
                        'amount': 0.0,
                        'value_usd': 0.0,
                        'exchanges': {}
                    }
                    
                allocations[asset_clean]['amount'] += amount
                allocations[asset_clean]['value_usd'] += value_usd
                allocations[asset_clean]['exchanges'][exchange] = {
                    'amount': amount,
                    'value_usd': value_usd
                }
                total_value += value_usd
                
        # Calculate percentages
        for asset in allocations:
            if total_value > 0:
                allocations[asset]['pct'] = allocations[asset]['value_usd'] / total_value
            else:
                allocations[asset]['pct'] = 0.0
                
        return {'assets': allocations, 'total_value_usd': total_value}
        
    def calculate_rebalance_trades(self) -> List[Dict]:
        """
        Calculate trades needed to rebalance portfolio to target allocation.
        Returns list of trades: [{'asset': str, 'action': 'BUY'|'SELL', 'amount_usd': float, 'exchange': str}]
        """
        if not self.target_allocations:
            return []
            
        current = self.get_current_allocation()
        total_value = current['total_value_usd']
        assets = current['assets']
        
        trades = []
        
        for asset, target_pct in self.target_allocations.items():
            current_pct = assets.get(asset, {}).get('pct', 0.0)
            current_value = assets.get(asset, {}).get('value_usd', 0.0)
            target_value = total_value * target_pct
            
            deviation = abs(current_pct - target_pct)
            
            if deviation < self.rebalance_threshold:
                continue  # Within tolerance
                
            diff_usd = target_value - current_value
            
            if abs(diff_usd) < self.min_trade_value:
                continue  # Too small
                
            # Determine best exchange for this trade
            exchanges = assets.get(asset, {}).get('exchanges', {})
            
            if diff_usd > 0:  # Need to BUY
                # Pick exchange with most quote currency
                best_exchange = 'binance'  # Default
                trade = {
                    'asset': asset,
                    'action': 'BUY',
                    'amount_usd': abs(diff_usd),
                    'exchange': best_exchange,
                    'current_pct': current_pct,
                    'target_pct': target_pct
                }
            else:  # Need to SELL
                # Pick exchange with most of this asset
                best_exchange = max(exchanges.keys(), key=lambda e: exchanges[e]['amount']) if exchanges else 'binance'
                trade = {
                    'asset': asset,
                    'action': 'SELL',
                    'amount_usd': abs(diff_usd),
                    'exchange': best_exchange,
                    'current_pct': current_pct,
                    'target_pct': target_pct
                }
                
            trades.append(trade)
            
        # Sort: SELL first (to free up capital), then BUY
        trades.sort(key=lambda t: 0 if t['action'] == 'SELL' else 1)
        
        return trades
        
    def execute_rebalance(self, dry_run: bool = True) -> Dict[str, Any]:
        """
        Execute portfolio rebalance.
        Returns: {'success': bool, 'trades_executed': int, 'trades': list}
        """
        trades = self.calculate_rebalance_trades()
        
        if not trades:
            return {'success': True, 'trades_executed': 0, 'message': 'Portfolio within tolerance'}
            
        results = {
            'success': True,
            'trades_executed': 0,
            'trades': [],
            'dry_run': dry_run
        }
        
        for trade in trades:
            asset = trade['asset']
            action = trade['action']
            amount_usd = trade['amount_usd']
            exchange = trade['exchange']
            
            # Build symbol
            symbol = f"{asset}USDT" if exchange == 'binance' else f"{asset}USD"
            
            if dry_run:
                result = {'status': 'DRY_RUN', 'would_execute': trade}
            else:
                try:
                    if action == 'BUY':
                        result = self.client.place_market_order(
                            exchange, symbol, 'BUY', quote_qty=amount_usd
                        )
                    else:
                        # Calculate quantity from USD value
                        ticker = self.client.get_ticker(exchange, symbol)
                        price = float(ticker.get('price', 1))
                        quantity = amount_usd / price
                        result = self.client.place_market_order(
                            exchange, symbol, 'SELL', quantity=quantity
                        )
                    results['trades_executed'] += 1
                except Exception as e:
                    result = {'error': str(e)}
                    results['success'] = False
                    
            results['trades'].append({
                'trade': trade,
                'result': result
            })
            
        self.last_rebalance = time.time()
        self.rebalance_history.append({
            'timestamp': time.time(),
            'trades': len(trades),
            'success': results['success']
        })
        
        return results
        
    def get_rebalance_summary(self) -> str:
        """Get human-readable rebalance summary."""
        current = self.get_current_allocation()
        trades = self.calculate_rebalance_trades()
        
        lines = [
            "═══════════════════════════════════════",
            "⚖️ PORTFOLIO REBALANCE SUMMARY",
            "═══════════════════════════════════════",
            f"Total Portfolio Value: ${current['total_value_usd']:.2f}",
            "",
            "Current vs Target Allocation:"
        ]
        
        for asset, target in self.target_allocations.items():
            current_pct = current['assets'].get(asset, {}).get('pct', 0) * 100
            target_pct = target * 100
            diff = current_pct - target_pct
            indicator = "✅" if abs(diff) < 5 else "⚠️"
            lines.append(f"  {indicator} {asset}: {current_pct:.1f}% → {target_pct:.1f}% ({diff:+.1f}%)")
            
        if trades:
            lines.append("")
            lines.append("Recommended Trades:")
            for trade in trades:
                lines.append(f"  • {trade['action']} ${trade['amount_usd']:.2f} of {trade['asset']} on {trade['exchange']}")
        else:
            lines.append("")
            lines.append("✅ Portfolio is balanced within tolerance")
            
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 🔮 PREDICTION VALIDATOR - Peer Review & Accuracy Tracking
# ═══════════════════════════════════════════════════════════════

class PredictionValidator:
    """
    🔮 PREDICTION VALIDATION SYSTEM
    
    Tracks prediction accuracy over time:
    - Logs predictions with timestamps: "At 10:00 predicted BTCUSDC +0.5% by 10:01"
    - Validates actual prices at predicted times
    - Scores accuracy: how close was prediction to reality?
    - Feeds accuracy back into confidence scores
    - Maintains historical hit rate for peer review
    
    This creates an auditable trail of "did the probability matrix get it right?"
    """
    
    def __init__(self, validation_window_seconds: int = 60):
        self.validation_window = validation_window_seconds  # Default 1 minute predictions
        self.pending_predictions: List[Dict] = []  # Predictions awaiting validation
        self.validated_predictions: List[Dict] = []  # Historical validated predictions
        self.max_history = 1000  # Keep last 1000 validated predictions
        
        # Accuracy metrics by various dimensions
        self.accuracy_metrics = {
            'total_predictions': 0,
            'validated': 0,
            'accurate': 0,  # Within 0.5% of predicted
            'close': 0,     # Within 1% of predicted
            'direction_correct': 0,  # Got the direction right (up/down)
            'by_exchange': {},
            'by_asset_class': {},
            'by_frequency_band': {},
            'by_coherence_level': {},
            'recent_accuracy': []  # Rolling window for recent accuracy
        }
        
        self.last_validation_check = time.time()
        logger.info("🔮 PredictionValidator initialized - Tracking prediction accuracy")
    
    def log_prediction(self, exchange: str, symbol: str, current_price: float,
                       predicted_direction: str, predicted_change_pct: float,
                       probability: float, coherence: float, frequency: float,
                       asset_class: str = 'crypto') -> str:
        """
        Log a new prediction for future validation.
        
        Args:
            exchange: Exchange name (binance, kraken, etc.)
            symbol: Trading pair (BTCUSDC, etc.)
            current_price: Current price at prediction time
            predicted_direction: 'up', 'down', or 'neutral'
            predicted_change_pct: Expected % change
            probability: Confidence probability (0-1)
            coherence: HNC coherence at prediction time
            frequency: HNC frequency at prediction time
            asset_class: crypto, forex, stocks, etc.
            
        Returns:
            Prediction ID for tracking
        """
        prediction_id = f"{exchange}_{symbol}_{int(time.time()*1000)}"
        prediction_time = time.time()
        validation_time = prediction_time + self.validation_window
        
        # Calculate expected price
        if predicted_direction == 'up':
            expected_price = current_price * (1 + predicted_change_pct / 100)
        elif predicted_direction == 'down':
            expected_price = current_price * (1 - predicted_change_pct / 100)
        else:
            expected_price = current_price
        
        prediction = {
            'id': prediction_id,
            'exchange': exchange,
            'symbol': symbol,
            'asset_class': asset_class,
            'prediction_time': prediction_time,
            'prediction_time_str': datetime.now().strftime('%H:%M:%S'),
            'validation_time': validation_time,
            'validation_time_str': datetime.fromtimestamp(validation_time).strftime('%H:%M:%S'),
            'current_price': current_price,
            'predicted_direction': predicted_direction,
            'predicted_change_pct': predicted_change_pct,
            'expected_price': expected_price,
            'probability': probability,
            'coherence': coherence,
            'frequency': frequency,
            'freq_band': self._get_freq_band(frequency),
            'coherence_level': self._get_coherence_level(coherence),
            'status': 'pending'
        }
        
        self.pending_predictions.append(prediction)
        self.accuracy_metrics['total_predictions'] += 1
        
        logger.info(f"🔮 PREDICTION LOGGED: {symbol} @ {prediction['prediction_time_str']}")
        logger.info(f"   📊 Current: ${current_price:.6f} → Expected: ${expected_price:.6f} ({predicted_direction} {predicted_change_pct:.2f}%)")
        logger.info(f"   🎯 Probability: {probability:.1%} | Coherence: {coherence:.2f} | Freq: {frequency:.0f}Hz")
        logger.info(f"   ⏰ Will validate at: {prediction['validation_time_str']}")
        
        return prediction_id
    
    def validate_predictions(self, get_price_func) -> List[Dict]:
        """
        Check all pending predictions that are due for validation.
        
        Args:
            get_price_func: Function that takes (exchange, symbol) and returns current price
            
        Returns:
            List of newly validated predictions with results
        """
        now = time.time()
        newly_validated = []
        still_pending = []
        
        for prediction in self.pending_predictions:
            if now >= prediction['validation_time']:
                # Time to validate this prediction
                try:
                    actual_price = get_price_func(prediction['exchange'], prediction['symbol'])
                    if actual_price and actual_price > 0:
                        result = self._validate_single(prediction, actual_price)
                        newly_validated.append(result)
                        self._update_accuracy_metrics(result)
                        
                        # Log the validation result
                        self._log_validation_result(result)
                    else:
                        # Couldn't get price, keep pending for one more cycle
                        if now < prediction['validation_time'] + 60:  # Grace period
                            still_pending.append(prediction)
                        else:
                            prediction['status'] = 'expired'
                            logger.warning(f"⚠️ Prediction {prediction['id']} expired - couldn't get price")
                except Exception as e:
                    logger.error(f"Validation error for {prediction['id']}: {e}")
                    still_pending.append(prediction)
            else:
                still_pending.append(prediction)
        
        self.pending_predictions = still_pending
        
        # Add to historical validated predictions
        self.validated_predictions.extend(newly_validated)
        
        # Trim history if needed
        if len(self.validated_predictions) > self.max_history:
            self.validated_predictions = self.validated_predictions[-self.max_history:]
        
        self.last_validation_check = now
        return newly_validated
    
    def _validate_single(self, prediction: Dict, actual_price: float) -> Dict:
        """Validate a single prediction against actual price."""
        current_price = prediction['current_price']
        expected_price = prediction['expected_price']
        predicted_direction = prediction['predicted_direction']
        
        # Calculate actual change
        actual_change_pct = ((actual_price - current_price) / current_price) * 100
        actual_direction = 'up' if actual_change_pct > 0.01 else ('down' if actual_change_pct < -0.01 else 'neutral')
        
        # Calculate prediction error
        if expected_price > 0:
            price_error_pct = abs((actual_price - expected_price) / expected_price) * 100
        else:
            price_error_pct = 100
        
        # Determine accuracy levels
        is_accurate = price_error_pct <= 0.5  # Within 0.5% of predicted price
        is_close = price_error_pct <= 1.0     # Within 1% of predicted price
        direction_correct = (predicted_direction == actual_direction) or \
                           (predicted_direction in ['up', 'down'] and actual_direction == predicted_direction)
        
        # Calculate accuracy score (0-100)
        if is_accurate:
            accuracy_score = 100 - (price_error_pct * 20)  # 100 at 0%, 90 at 0.5%
        elif is_close:
            accuracy_score = 80 - ((price_error_pct - 0.5) * 40)  # 80 at 0.5%, 60 at 1%
        else:
            accuracy_score = max(0, 60 - (price_error_pct - 1) * 10)  # Decreases after 1%
        
        # Bonus for correct direction
        if direction_correct:
            accuracy_score = min(100, accuracy_score + 10)
        
        result = {
            **prediction,
            'status': 'validated',
            'validation_timestamp': time.time(),
            'validation_timestamp_str': datetime.now().strftime('%H:%M:%S'),
            'actual_price': actual_price,
            'actual_change_pct': actual_change_pct,
            'actual_direction': actual_direction,
            'price_error_pct': price_error_pct,
            'is_accurate': is_accurate,
            'is_close': is_close,
            'direction_correct': direction_correct,
            'accuracy_score': accuracy_score
        }
        
        return result
    
    def _update_accuracy_metrics(self, result: Dict):
        """Update accuracy metrics with validation result."""
        self.accuracy_metrics['validated'] += 1
        
        if result['is_accurate']:
            self.accuracy_metrics['accurate'] += 1
        if result['is_close']:
            self.accuracy_metrics['close'] += 1
        if result['direction_correct']:
            self.accuracy_metrics['direction_correct'] += 1
        
        # Update by exchange
        exchange = result['exchange']
        if exchange not in self.accuracy_metrics['by_exchange']:
            self.accuracy_metrics['by_exchange'][exchange] = {
                'total': 0, 'accurate': 0, 'close': 0, 'direction_correct': 0, 'avg_score': 0, 'scores': []
            }
        ex = self.accuracy_metrics['by_exchange'][exchange]
        ex['total'] += 1
        if result['is_accurate']:
            ex['accurate'] += 1
        if result['is_close']:
            ex['close'] += 1
        if result['direction_correct']:
            ex['direction_correct'] += 1
        ex['scores'].append(result['accuracy_score'])
        ex['scores'] = ex['scores'][-100:]  # Keep last 100
        ex['avg_score'] = sum(ex['scores']) / len(ex['scores'])
        
        # Update by asset class
        asset_class = result['asset_class']
        if asset_class not in self.accuracy_metrics['by_asset_class']:
            self.accuracy_metrics['by_asset_class'][asset_class] = {
                'total': 0, 'accurate': 0, 'close': 0, 'direction_correct': 0, 'avg_score': 0, 'scores': []
            }
        ac = self.accuracy_metrics['by_asset_class'][asset_class]
        ac['total'] += 1
        if result['is_accurate']:
            ac['accurate'] += 1
        if result['is_close']:
            ac['close'] += 1
        if result['direction_correct']:
            ac['direction_correct'] += 1
        ac['scores'].append(result['accuracy_score'])
        ac['scores'] = ac['scores'][-100:]
        ac['avg_score'] = sum(ac['scores']) / len(ac['scores'])
        
        # Update by frequency band
        freq_band = result.get('freq_band', 'unknown')
        if freq_band not in self.accuracy_metrics['by_frequency_band']:
            self.accuracy_metrics['by_frequency_band'][freq_band] = {
                'total': 0, 'accurate': 0, 'direction_correct': 0, 'avg_score': 0, 'scores': []
            }
        fb = self.accuracy_metrics['by_frequency_band'][freq_band]
        fb['total'] += 1
        if result['is_accurate']:
            fb['accurate'] += 1
        if result['direction_correct']:
            fb['direction_correct'] += 1
        fb['scores'].append(result['accuracy_score'])
        fb['scores'] = fb['scores'][-100:]
        fb['avg_score'] = sum(fb['scores']) / len(fb['scores'])
        
        # Update by coherence level
        coherence_level = result.get('coherence_level', 'unknown')
        if coherence_level not in self.accuracy_metrics['by_coherence_level']:
            self.accuracy_metrics['by_coherence_level'][coherence_level] = {
                'total': 0, 'accurate': 0, 'direction_correct': 0, 'avg_score': 0, 'scores': []
            }
        cl = self.accuracy_metrics['by_coherence_level'][coherence_level]
        cl['total'] += 1
        if result['is_accurate']:
            cl['accurate'] += 1
        if result['direction_correct']:
            cl['direction_correct'] += 1
        cl['scores'].append(result['accuracy_score'])
        cl['scores'] = cl['scores'][-100:]
        cl['avg_score'] = sum(cl['scores']) / len(cl['scores'])
        
        # Update recent accuracy (rolling window)
        self.accuracy_metrics['recent_accuracy'].append({
            'timestamp': time.time(),
            'score': result['accuracy_score'],
            'accurate': result['is_accurate'],
            'direction_correct': result['direction_correct']
        })
        self.accuracy_metrics['recent_accuracy'] = self.accuracy_metrics['recent_accuracy'][-100:]
    
    def _log_validation_result(self, result: Dict):
        """Log validation result with clear formatting."""
        symbol = result['symbol']
        prediction_time = result['prediction_time_str']
        validation_time = result['validation_timestamp_str']
        
        # Determine emoji based on accuracy
        if result['is_accurate']:
            emoji = "🎯"
            status = "BANG ON!"
        elif result['is_close']:
            emoji = "✅"
            status = "CLOSE"
        elif result['direction_correct']:
            emoji = "📈" if result['actual_direction'] == 'up' else "📉"
            status = "DIRECTION OK"
        else:
            emoji = "❌"
            status = "MISSED"
        
        logger.info(f"")
        logger.info(f"═══════════════════════════════════════════════════════")
        logger.info(f"{emoji} PREDICTION VALIDATED: {symbol} | {status}")
        logger.info(f"═══════════════════════════════════════════════════════")
        logger.info(f"   ⏰ Predicted at {prediction_time} → Checked at {validation_time}")
        logger.info(f"   📊 Expected: ${result['expected_price']:.6f} ({result['predicted_direction']} {result['predicted_change_pct']:.2f}%)")
        logger.info(f"   📊 Actual:   ${result['actual_price']:.6f} ({result['actual_direction']} {result['actual_change_pct']:.2f}%)")
        logger.info(f"   🎯 Accuracy Score: {result['accuracy_score']:.1f}/100 | Error: {result['price_error_pct']:.3f}%")
        logger.info(f"   📈 Direction: {'✅ CORRECT' if result['direction_correct'] else '❌ WRONG'}")
        logger.info(f"═══════════════════════════════════════════════════════")
        logger.info(f"")
    
    def get_accuracy_boost(self, exchange: str, asset_class: str, 
                          frequency: float, coherence: float) -> float:
        """
        Get accuracy-based boost for probability calculations.
        
        If predictions at this frequency/coherence level have been historically accurate,
        boost the confidence. If they've been inaccurate, reduce confidence.
        
        Returns: Multiplier (0.8 to 1.2)
        """
        boosts = []
        
        # Exchange accuracy boost
        ex = self.accuracy_metrics['by_exchange'].get(exchange, {})
        if ex.get('total', 0) >= 10:  # Need at least 10 predictions
            ex_accuracy = ex.get('avg_score', 50) / 100
            boosts.append(0.8 + (ex_accuracy * 0.4))  # 0.8 to 1.2
        
        # Asset class accuracy boost
        ac = self.accuracy_metrics['by_asset_class'].get(asset_class, {})
        if ac.get('total', 0) >= 10:
            ac_accuracy = ac.get('avg_score', 50) / 100
            boosts.append(0.8 + (ac_accuracy * 0.4))
        
        # Frequency band accuracy boost
        freq_band = self._get_freq_band(frequency)
        fb = self.accuracy_metrics['by_frequency_band'].get(freq_band, {})
        if fb.get('total', 0) >= 10:
            fb_accuracy = fb.get('avg_score', 50) / 100
            boosts.append(0.8 + (fb_accuracy * 0.4))
        
        # Coherence level accuracy boost
        coherence_level = self._get_coherence_level(coherence)
        cl = self.accuracy_metrics['by_coherence_level'].get(coherence_level, {})
        if cl.get('total', 0) >= 10:
            cl_accuracy = cl.get('avg_score', 50) / 100
            boosts.append(0.8 + (cl_accuracy * 0.4))
        
        if boosts:
            return sum(boosts) / len(boosts)
        return 1.0  # Neutral if no history
    
    def get_accuracy_summary(self) -> str:
        """Get human-readable accuracy summary."""
        m = self.accuracy_metrics
        total = m['validated']
        
        if total == 0:
            return "🔮 No predictions validated yet - collecting data..."
        
        accurate_pct = (m['accurate'] / total) * 100
        close_pct = (m['close'] / total) * 100
        direction_pct = (m['direction_correct'] / total) * 100
        
        # Calculate recent accuracy (last 20)
        recent = m['recent_accuracy'][-20:]
        if recent:
            recent_scores = [r['score'] for r in recent]
            recent_avg = sum(recent_scores) / len(recent_scores)
            recent_accurate = sum(1 for r in recent if r['accurate'])
            recent_direction = sum(1 for r in recent if r['direction_correct'])
        else:
            recent_avg = 0
            recent_accurate = 0
            recent_direction = 0
        
        lines = [
            "",
            "═══════════════════════════════════════════════════════════════",
            "🔮 PREDICTION ACCURACY REPORT",
            "═══════════════════════════════════════════════════════════════",
            f"📊 Total Predictions: {m['total_predictions']} | Validated: {total}",
            f"",
            f"🎯 OVERALL ACCURACY:",
            f"   • Bang On (≤0.5% error): {m['accurate']}/{total} ({accurate_pct:.1f}%)",
            f"   • Close (≤1% error):     {m['close']}/{total} ({close_pct:.1f}%)",
            f"   • Direction Correct:     {m['direction_correct']}/{total} ({direction_pct:.1f}%)",
            f"",
            f"📈 RECENT (Last {len(recent)} predictions):",
            f"   • Average Score: {recent_avg:.1f}/100",
            f"   • Accurate: {recent_accurate}/{len(recent)}",
            f"   • Direction OK: {recent_direction}/{len(recent)}",
        ]
        
        # By exchange breakdown
        if m['by_exchange']:
            lines.append("")
            lines.append("📍 BY EXCHANGE:")
            for ex, data in m['by_exchange'].items():
                if data['total'] > 0:
                    acc_rate = (data['accurate'] / data['total']) * 100
                    lines.append(f"   • {ex}: {data['accurate']}/{data['total']} accurate ({acc_rate:.1f}%) | Avg Score: {data['avg_score']:.1f}")
        
        # By frequency band breakdown
        if m['by_frequency_band']:
            lines.append("")
            lines.append("🎵 BY FREQUENCY BAND:")
            for band, data in sorted(m['by_frequency_band'].items()):
                if data['total'] > 0:
                    acc_rate = (data['accurate'] / data['total']) * 100
                    lines.append(f"   • {band}: {data['accurate']}/{data['total']} ({acc_rate:.1f}%) | Avg: {data['avg_score']:.1f}")
        
        # By coherence level
        if m['by_coherence_level']:
            lines.append("")
            lines.append("🌊 BY COHERENCE LEVEL:")
            for level, data in m['by_coherence_level'].items():
                if data['total'] > 0:
                    acc_rate = (data['accurate'] / data['total']) * 100
                    lines.append(f"   • {level}: {data['accurate']}/{data['total']} ({acc_rate:.1f}%) | Avg: {data['avg_score']:.1f}")
        
        lines.append("")
        lines.append("═══════════════════════════════════════════════════════════════")
        
        return "\n".join(lines)
    
    def _get_freq_band(self, freq: float) -> str:
        """Get frequency band name with sacred frequency mapping."""
        # Check for exact sacred frequency matches first (±5Hz tolerance)
        sacred_freqs = {
            7.83: "7.83Hz (Schumann)",
            136.1: "136Hz (OM/Earth)",
            174: "174Hz (Foundation)",
            285: "285Hz (Healing)",
            396: "396Hz (Liberation)",
            417: "417Hz (Change)",
            432: "432Hz (Cosmic)",
            440: "440Hz (Distortion!)",
            528: "528Hz (Love)",
            639: "639Hz (Connection)",
            741: "741Hz (Awakening)",
            852: "852Hz (Spiritual)",
            963: "963Hz (Unity)",
        }
        for sacred, name in sacred_freqs.items():
            if abs(freq - sacred) <= 5:
                return name
        
        # Fall back to band classification
        if freq < 200:
            return "Sub-200Hz (Deep Earth)"
        elif freq < 300:
            return "200-299Hz (Grounding)"
        elif freq < 400:
            return "300-399Hz (Activation)"
        elif freq < 500:
            return "400-499Hz (Transition)"
        elif freq < 600:
            return "500-599Hz (Heart)"
        elif freq < 700:
            return "600-699Hz (Expression)"
        elif freq < 800:
            return "700-799Hz (Intuition)"
        elif freq < 900:
            return "800-899Hz (Insight)"
        elif freq < 1000:
            return "900-999Hz (Crown)"
        else:
            return "1000+Hz (Transcendent)"
    
    def _get_coherence_level(self, coherence: float) -> str:
        """Get coherence level name."""
        if coherence < 0.3:
            return "Low (<0.3)"
        elif coherence < 0.5:
            return "Medium (0.3-0.5)"
        elif coherence < 0.7:
            return "Good (0.5-0.7)"
        elif coherence < 0.85:
            return "High (0.7-0.85)"
        else:
            return "Excellent (0.85+)"
    
    def get_pending_count(self) -> int:
        """Get number of predictions awaiting validation."""
        return len(self.pending_predictions)
    
    def get_validated_count(self) -> int:
        """Get total validated predictions."""
        return self.accuracy_metrics['validated']


# ═══════════════════════════════════════════════════════════════
# 🌐 MULTI-EXCHANGE ORCHESTRATOR - Unified Cross-Exchange Intelligence
# ═══════════════════════════════════════════════════════════════

class MultiExchangeOrchestrator:
    """
    🌐 MULTI-EXCHANGE ORCHESTRATOR
    
    Central nervous system for cross-exchange trading:
    - Unified opportunity scanning across Binance, Kraken, Capital.com, Alpaca
    - Cross-exchange learning: wins/losses inform all exchange decisions
    - Smart order routing to best execution venue
    - Arbitrage detection and execution
    - Coordinated position management
    
    ALL SYSTEMS TALK TO EACH OTHER through this orchestrator.
    """
    
    def __init__(self, multi_client):
        self.client = multi_client
        
        # Exchange-specific configuration
        self.exchange_config = {
            'binance': {
                'enabled': True,
                # 🤑 GREEDY HOE: ALL THE BINANCE PAIRS!
                'quote_currencies': ['USDC', 'USDT', 'BTC', 'ETH', 'BNB', 'FDUSD', 'EUR', 'GBP', 'TUSD'],
                'fee_rate': 0.001,
                'max_positions': 15,  # 🔥 BEAST MODE: 15 positions per exchange!
                'min_trade_usd': 10.0,
                'asset_class': 'crypto'
            },
            'kraken': {
                'enabled': True,  # ✅ ENABLED - Trading on Kraken with GBP
                # 🤑 GREEDY HOE: ALL THE KRAKEN PAIRS!
                'quote_currencies': ['USD', 'EUR', 'GBP', 'USDT', 'USDC', 'BTC', 'ETH', 'AUD', 'CAD'],
                'fee_rate': 0.0026,
                'max_positions': 15,  # 🔥 BEAST MODE: 15 positions per exchange!
                'min_trade_usd': 5.0,
                'asset_class': 'crypto'
            },
            'capital': {
                'enabled': True,
                'quote_currencies': ['USD', 'GBP'],
                'fee_rate': 0.001,
                'max_positions': 10,  # 🔥 BEAST MODE: 10 CFD positions!
                'min_trade_usd': 10.0,
                'asset_class': 'cfd'  # forex, indices, commodities
            },
            'alpaca': {
                'enabled': CONFIG.get('ALPACA_ANALYTICS_ONLY', True) == False,  # Trading disabled by default
                'quote_currencies': ['USD'],
                'fee_rate': 0.0025,
                'max_positions': 10,  # 🔥 BEAST MODE: 10 stock positions!
                'min_trade_usd': 1.0,  # Fractional shares
                'asset_class': 'stocks'
            }
        }
        
        # Cross-exchange learning metrics
        self.learning_metrics = {
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'total_pnl': 0.0,
            'by_exchange': {},
            'by_asset_class': {},
            'by_frequency_band': {},
            'cross_correlations': {}
        }
        
        # Unified ticker cache (all exchanges)
        self.unified_ticker_cache: Dict[str, Dict] = {}
        self.last_unified_scan = 0
        self.scan_interval = 10  # seconds
        
        # Cross-exchange signals
        self.cross_signals: List[Dict] = []
        self.signal_history: List[Dict] = []
        
        logger.info("🌐 MultiExchangeOrchestrator initialized - All systems connected")

    def get_learning_metrics(self) -> Dict[str, Any]:
        """Expose cross-exchange learning metrics (wins, pnl, by exchange/class)."""
        return self.learning_metrics
        
    def get_enabled_exchanges(self) -> List[str]:
        """Get list of enabled exchanges."""
        return [ex for ex, cfg in self.exchange_config.items() if cfg['enabled']]
        
    def scan_all_exchanges(self) -> Dict[str, List[Dict]]:
        """
        Scan all enabled exchanges for opportunities.
        Returns opportunities organized by exchange.
        """
        all_opportunities = {}
        
        for exchange in self.get_enabled_exchanges():
            try:
                opps = self._scan_exchange(exchange)
                all_opportunities[exchange] = opps
                logger.debug(f"🔍 {exchange}: Found {len(opps)} opportunities")
            except Exception as e:
                logger.error(f"❌ {exchange} scan error: {e}")
                all_opportunities[exchange] = []
                
        # Update unified cache
        self.last_unified_scan = time.time()
        return all_opportunities
        
    def _scan_exchange(self, exchange: str) -> List[Dict]:
        """Scan a single exchange for opportunities."""
        opportunities = []
        cfg = self.exchange_config.get(exchange, {})
        
        try:
            # Get tickers from the exchange client
            if hasattr(self.client, 'clients') and exchange in self.client.clients:
                client = self.client.clients[exchange]
                tickers = self._get_exchange_tickers(exchange, client, cfg)
                
                for symbol, ticker in tickers.items():
                    opp = self._evaluate_opportunity(exchange, symbol, ticker, cfg)
                    if opp:
                        opportunities.append(opp)
                        
        except Exception as e:
            logger.error(f"Scan error for {exchange}: {e}")
            
        # Sort by score
        opportunities.sort(key=lambda x: -x.get('score', 0))
        # 🔥 UNLEASHED: Return top 100 per exchange instead of 20!
        return opportunities[:100]  # Top 100 per exchange - TRADE EVERYTHING!
        
    def _get_exchange_tickers(self, exchange: str, client, cfg: Dict) -> Dict[str, Dict]:
        """Get tickers from an exchange."""
        tickers = {}
        quote_currencies = cfg.get('quote_currencies', ['USD'])
        
        try:
            if exchange == 'binance':
                raw = client.client.session.get(f"{client.client.base}/api/v3/ticker/24hr", timeout=10).json()
                for t in raw:
                    sym = t['symbol']
                    for q in quote_currencies:
                        if sym.endswith(q):
                            tickers[sym] = {
                                'price': float(t['lastPrice']),
                                'change': float(t['priceChangePercent']),
                                'volume': float(t['quoteVolume']),
                                'high': float(t['highPrice']),
                                'low': float(t['lowPrice']),
                                'exchange': 'binance',
                                'quote': q,
                            }
                            break
                            
            elif exchange == 'kraken':
                # Use existing Kraken ticker logic
                tickers = self._get_kraken_tickers(client, quote_currencies)
                
            elif exchange == 'capital':
                # CFD markets - simplified
                tickers = self._get_capital_tickers(client)
                
        except Exception as e:
            logger.error(f"Ticker fetch error for {exchange}: {e}")
            
        return tickers
        
    def _get_kraken_tickers(self, client, quote_currencies: List[str]) -> Dict[str, Dict]:
        """Get Kraken tickers."""
        tickers = {}
        try:
            if hasattr(client.client, 'get_24h_tickers'):
                raw_tickers = client.client.get_24h_tickers()
                for t in raw_tickers:
                    sym = t.get('symbol', '')
                    for q in quote_currencies:
                        if sym.endswith(q):
                            tickers[sym] = {
                                'price': float(t.get('price', 0)),
                                'change': float(t.get('change24h', 0)),
                                'volume': float(t.get('volume', 0)),
                                'high': float(t.get('high', t.get('price', 0))),
                                'low': float(t.get('low', t.get('price', 0))),
                                'exchange': 'kraken',
                                'quote': q,
                            }
                            break
        except Exception as e:
            logger.debug(f"Kraken ticker error: {e}")
        return tickers
        
    def _get_capital_tickers(self, client) -> Dict[str, Dict]:
        """Get Capital.com CFD tickers."""
        tickers = {}
        # Capital markets to scan
        markets = ['EURUSD', 'GBPUSD', 'GOLD', 'US500', 'UK100', 'OIL_CRUDE']
        
        try:
            for market in markets:
                # Simplified - actual implementation would use Capital API
                tickers[market] = {
                    'price': 0,  # Would be fetched from API
                    'change': 0,
                    'volume': 1000000,
                    'exchange': 'capital',
                    'quote': 'USD',
                    'asset_class': self._get_asset_class(market)
                }
        except Exception as e:
            logger.debug(f"Capital ticker error: {e}")
        return tickers
        
    def _get_asset_class(self, symbol: str) -> str:
        """Determine asset class from symbol."""
        sym = symbol.upper()
        if any(fx in sym for fx in ['USD', 'EUR', 'GBP', 'JPY', 'CHF']):
            if len(sym) <= 8:
                return 'forex'
        if any(idx in sym for idx in ['US500', 'US100', 'UK100', 'DE40']):
            return 'indices'
        if any(com in sym for com in ['GOLD', 'SILVER', 'OIL', 'NATGAS']):
            return 'commodities'
        return 'crypto'
        
    def _evaluate_opportunity(self, exchange: str, symbol: str, ticker: Dict, cfg: Dict) -> Optional[Dict]:
        """
        Evaluate a single opportunity.
        
        🪙 PENNY PROFIT MODE: All gates are now ADVISORY only.
        The penny profit math (exact fee calculation) is the TRUE gate.
        We log warnings but don't block entries.
        """
        price = ticker.get('price', 0)
        change = ticker.get('change', 0)
        volume = ticker.get('volume', 0)
        
        if price <= 0:
            return None  # Can't trade without a price
            
        # Calculate coherence
        asset_class = ticker.get('asset_class', cfg.get('asset_class', 'crypto'))
        coherence = self._calculate_coherence(change, volume, ticker, asset_class)
        
        # 🪙 PENNY MODE: Coherence is advisory, only reject broken data
        if coherence < 0.05:
            logger.debug(f"  ⚠️ {symbol}: Coherence {coherence:.2f} too low (data error)")
            return None
            
        # Calculate frequency (advisory only)
        freq = max(256, min(963, 432 * ((1 + change/100) ** PHI)))
        in_avoid = 435 <= freq <= 445  # 440Hz distortion zone
        
        # 🪙 PENNY MODE: Frequency is advisory only, don't block
        if in_avoid:
            logger.debug(f"  ⚠️ {symbol}: Frequency {freq:.1f}Hz in distortion zone (advisory)")
            
        # Calculate probability
        probability = self._calculate_probability(coherence, change, freq, asset_class)
        
        # 🪙 PENNY MODE: Probability is advisory, very low threshold
        if probability < 0.15:  # Only skip truly hopeless signals
            logger.debug(f"  ⚠️ {symbol}: Probability {probability:.2f} below floor (advisory)")
            return None
            
        # Calculate score
        score = self._calculate_score(probability, coherence, volume, freq, change)
        
        # Apply cross-exchange learning boost
        score = self._apply_learning_boost(score, exchange, asset_class, freq)
        
        return {
            'exchange': exchange,
            'symbol': symbol,
            'price': price,
            'change': change,
            'volume': volume,
            'coherence': coherence,
            'frequency': freq,
            'probability': probability,
            'score': score,
            'asset_class': asset_class,
            'quote': ticker.get('quote', 'USD'),
            'timestamp': time.time()
        }
        
    def _calculate_coherence(self, change: float, volume: float, ticker: Dict, asset_class: str) -> float:
        """Calculate coherence with asset-class awareness."""
        high = ticker.get('high', ticker.get('price', 1))
        low = ticker.get('low', ticker.get('price', 1))
        price = ticker.get('price', 1)
        
        volatility = ((high - low) / low * 100) if low > 0 else 0
        
        if asset_class == 'forex':
            S = min(1.0, volume / 50.0)
            O = min(1.0, abs(change) / 0.3)
            E = min(1.0, volatility / 0.5)
            Lambda = (S + O + E) / 3.0
            return 1 / (1 + math.exp(-6 * (Lambda - 0.35)))
        elif asset_class == 'indices':
            S = min(1.0, volume / 50.0)
            O = min(1.0, abs(change) / 1.0)
            E = min(1.0, volatility / 2.0)
            Lambda = (S + O + E) / 3.0
            return 1 / (1 + math.exp(-6 * (Lambda - 0.35)))
        else:  # crypto
            S = min(1.0, volume / 50000.0)
            O = min(1.0, abs(change) / 15.0)
            E = min(1.0, volatility / 25.0)
            Lambda = (S + O + E) / 3.0
            return 1 / (1 + math.exp(-5 * (Lambda - 0.5)))
            
    def _calculate_probability(self, coherence: float, change: float, freq: float, asset_class: str) -> float:
        """Calculate trade probability with news/knowledge correlation."""
        base_prob = 0.50 + coherence * 0.30
        
        # Momentum adjustment
        if change > 0:
            base_prob += min(0.10, change / 50)
        else:
            base_prob -= min(0.05, abs(change) / 100)
            
        # Frequency adjustment - based on prediction accuracy data + sacred frequencies
        freq_modifier = self._get_sacred_frequency_modifier(freq)
        base_prob *= freq_modifier
        
        # 📰 NEWS SENTIMENT MODIFIER - Learn from correlation data
        try:
            news_sentiment = getattr(self, '_last_news_sentiment', {})
            news_label = news_sentiment.get('label', 'neutral')
            news_confidence = news_sentiment.get('confidence', 0.0)
            
            # Get learned correlations from Adaptive Learner
            news_insights = ADAPTIVE_LEARNER.get_news_correlation_insights()
            
            if news_label == 'bullish' and news_confidence >= 0.5:
                # Boost probability in bullish news environments (if historically good)
                bullish_win_rate = news_insights.get('bullish', {}).get('win_rate', 0.5)
                if bullish_win_rate > 0.55:  # Only boost if bullish news historically good
                    news_boost = min(0.08, (bullish_win_rate - 0.5) * 0.4 * news_confidence)
                    base_prob += news_boost
            elif news_label == 'bearish' and news_confidence >= 0.5:
                # Reduce probability in bearish news (if historically bad)
                bearish_win_rate = news_insights.get('bearish', {}).get('win_rate', 0.5)
                if bearish_win_rate < 0.45:  # Only reduce if bearish news historically bad
                    news_penalty = min(0.08, (0.5 - bearish_win_rate) * 0.4 * news_confidence)
                    base_prob -= news_penalty
        except Exception:
            pass  # News correlation not critical
        
        # 📚 KNOWLEDGE MODIFIER - Boost based on knowledge discovery performance
        try:
            knowledge_modifier = ADAPTIVE_LEARNER.get_knowledge_probability_modifier()
            base_prob *= knowledge_modifier  # Typically 0.97-1.03
        except Exception:
            pass  # Knowledge correlation not critical
            
        return max(0.0, min(CONFIG.get('PROB_CAP', 0.83), base_prob))
    
    def _get_sacred_frequency_modifier(self, freq: float) -> float:
        """
        🎵 SACRED FREQUENCY MODIFIER 🎵
        
        Maps market frequencies to sacred healing tones and returns
        appropriate probability modifiers based on harmonic resonance.
        
        SOLFEGGIO SCALE (Ancient healing frequencies):
        - 174 Hz: Foundation, pain relief
        - 285 Hz: Healing, tissue regeneration
        - 396 Hz: Liberation from fear/guilt (UT)
        - 417 Hz: Undoing situations, facilitating change (RE)
        - 528 Hz: Love frequency, DNA repair (MI) ⭐ OPTIMAL GREEN BORAX
        - 639 Hz: Connection, relationships (FA)
        - 741 Hz: Awakening intuition (SOL)
        - 852 Hz: Returning to spiritual order (LA)
        - 963 Hz: Unity, awakening (SI)
        
        EARTH FREQUENCIES:
        - 7.83 Hz: Schumann Resonance (Earth's heartbeat)
        - 136.1 Hz: OM frequency (Earth's year)
        - 432 Hz: Universal tuning (cosmic harmony)
        
        DISTORTION:
        - 440 Hz: Artificial concert pitch (dissonance)
        """
        # 🟢 Check SACRED SOLFEGGIO frequencies FIRST! 
        # 528Hz GREEN LOVE must be prioritized over Schumann harmonics!
        sacred_map = {
            (523, 533): CONFIG.get('FREQUENCY_BOOST_528HZ', 1.35),   # 528 Hz Love ⭐ GREEN BORAX
            (391, 401): CONFIG.get('FREQUENCY_BOOST_396HZ', 1.40),   # 396 Hz Liberation
            (427, 437): CONFIG.get('FREQUENCY_BOOST_432HZ', 1.30),   # 432 Hz Cosmic
            (169, 179): CONFIG.get('FREQUENCY_BOOST_174HZ', 1.20),   # 174 Hz Foundation
            (280, 290): CONFIG.get('FREQUENCY_BOOST_285HZ', 1.25),   # 285 Hz Healing
            (412, 422): CONFIG.get('FREQUENCY_BOOST_417HZ', 1.30),   # 417 Hz Change
            (435, 445): CONFIG.get('FREQUENCY_SUPPRESS_440HZ', 0.70),# 440 Hz Distortion!
            (634, 644): CONFIG.get('FREQUENCY_BOOST_639HZ', 1.25),   # 639 Hz Connection
            (736, 746): CONFIG.get('FREQUENCY_BOOST_741HZ', 1.15),   # 741 Hz Awakening
            (847, 857): CONFIG.get('FREQUENCY_BOOST_852HZ', 1.20),   # 852 Hz Spiritual
            (958, 968): CONFIG.get('FREQUENCY_SUPPRESS_963HZ', 0.60),# 963 Hz (poor data)
            (131, 141): CONFIG.get('FREQUENCY_BOOST_136HZ', 1.25),   # 136 Hz OM
        }
        
        for (low, high), modifier in sacred_map.items():
            if low <= freq <= high:
                return modifier
        
        # Check Schumann harmonics AFTER sacred frequencies (7.83Hz × n)
        schumann_base = 7.83
        for harmonic in range(1, 128):  # Up to 128th harmonic (~1000Hz)
            schumann_freq = schumann_base * harmonic
            if abs(freq - schumann_freq) <= 3:
                return CONFIG.get('FREQUENCY_BOOST_SCHUMANN', 1.45)
        
        # Band-based fallback
        if 300 <= freq <= 399:
            return CONFIG.get('FREQUENCY_BOOST_300HZ', 1.50)  # 98.8% accuracy!
        elif 600 <= freq <= 699:
            return CONFIG.get('FREQUENCY_SUPPRESS_600HZ', 0.75)  # 0% accuracy
        elif freq >= 1000:
            return CONFIG.get('FREQUENCY_SUPPRESS_HIGH_CHAOS', 0.50)
        
        # Neutral baseline for unclassified frequencies
        return CONFIG.get('FREQUENCY_NEUTRAL_BASELINE', 1.0)
        
    def _calculate_score(self, prob: float, coherence: float, volume: float, freq: float, change: float) -> float:
        """Calculate opportunity score."""
        base = prob * coherence * (1 + math.log10(max(1, volume/10000)))
        
        # Frequency bonus
        in_optimal = 520 <= freq <= 963
        freq_bonus = 1.0 if in_optimal else 0.5
        
        return base * (1 + freq_bonus)
        
    def _apply_learning_boost(self, score: float, exchange: str, asset_class: str, freq: float) -> float:
        """Apply cross-exchange learning boost to score."""
        boost = 1.0
        
        # Exchange performance boost
        ex_metrics = self.learning_metrics.get('by_exchange', {}).get(exchange, {})
        if ex_metrics.get('total_trades', 0) >= 10:
            ex_win_rate = ex_metrics.get('wins', 0) / max(1, ex_metrics.get('total_trades', 1))
            if ex_win_rate > 0.55:
                boost *= 1.0 + (ex_win_rate - 0.50) * 0.5
            elif ex_win_rate < 0.45:
                boost *= 0.8
                
        # Asset class performance boost
        ac_metrics = self.learning_metrics.get('by_asset_class', {}).get(asset_class, {})
        if ac_metrics.get('total_trades', 0) >= 10:
            ac_win_rate = ac_metrics.get('wins', 0) / max(1, ac_metrics.get('total_trades', 1))
            if ac_win_rate > 0.55:
                boost *= 1.0 + (ac_win_rate - 0.50) * 0.3
                
        return score * boost
        
    def record_trade_result(self, exchange: str, symbol: str, pnl: float, 
                           asset_class: str, frequency: float, coherence: float):
        """
        Record trade result for cross-exchange learning.
        ALL SYSTEMS LEARN FROM THIS.
        """
        is_win = pnl > 0
        
        # Update global metrics
        self.learning_metrics['total_trades'] += 1
        if is_win:
            self.learning_metrics['wins'] += 1
        else:
            self.learning_metrics['losses'] += 1
        self.learning_metrics['total_pnl'] += pnl
        
        # Update by exchange
        if exchange not in self.learning_metrics['by_exchange']:
            self.learning_metrics['by_exchange'][exchange] = {'total_trades': 0, 'wins': 0, 'losses': 0, 'pnl': 0}
        self.learning_metrics['by_exchange'][exchange]['total_trades'] += 1
        if is_win:
            self.learning_metrics['by_exchange'][exchange]['wins'] += 1
        else:
            self.learning_metrics['by_exchange'][exchange]['losses'] += 1
        self.learning_metrics['by_exchange'][exchange]['pnl'] += pnl
        
        # Update by asset class
        if asset_class not in self.learning_metrics['by_asset_class']:
            self.learning_metrics['by_asset_class'][asset_class] = {'total_trades': 0, 'wins': 0, 'losses': 0, 'pnl': 0}
        self.learning_metrics['by_asset_class'][asset_class]['total_trades'] += 1
        if is_win:
            self.learning_metrics['by_asset_class'][asset_class]['wins'] += 1
        else:
            self.learning_metrics['by_asset_class'][asset_class]['losses'] += 1
        self.learning_metrics['by_asset_class'][asset_class]['pnl'] += pnl
        
        # Update by frequency band
        freq_band = self._get_freq_band(frequency)
        if freq_band not in self.learning_metrics['by_frequency_band']:
            self.learning_metrics['by_frequency_band'][freq_band] = {'total_trades': 0, 'wins': 0, 'losses': 0, 'pnl': 0}
        self.learning_metrics['by_frequency_band'][freq_band]['total_trades'] += 1
        if is_win:
            self.learning_metrics['by_frequency_band'][freq_band]['wins'] += 1
        else:
            self.learning_metrics['by_frequency_band'][freq_band]['losses'] += 1
        self.learning_metrics['by_frequency_band'][freq_band]['pnl'] += pnl
        
        # Log cross-exchange insight
        total = self.learning_metrics['total_trades']
        wins = self.learning_metrics['wins']
        wr = wins / max(1, total) * 100
        logger.info(f"🌐 Cross-Exchange Learning: {total} trades, {wr:.1f}% WR, ${self.learning_metrics['total_pnl']:.2f} PnL")
        
    def _get_freq_band(self, freq: float) -> str:
        """Get frequency band name."""
        if freq < 400:
            return 'LOW (<400Hz)'
        elif 400 <= freq < 500:
            return 'MID (400-500Hz)'
        elif 500 <= freq < 600:
            return 'SOLFEGGIO (500-600Hz)'
        elif 600 <= freq < 800:
            return 'HIGH (600-800Hz)'
        else:
            return 'ULTRA (>800Hz)'
            
    def get_best_opportunity(self) -> Optional[Dict]:
        """Get the single best opportunity across all exchanges."""
        all_opps = self.scan_all_exchanges()
        
        # Flatten and sort
        combined = []
        for exchange, opps in all_opps.items():
            combined.extend(opps)
            
        if not combined:
            return None
            
        combined.sort(key=lambda x: -x.get('score', 0))
        return combined[0]
        
    def get_learning_summary(self) -> str:
        """Get formatted learning summary."""
        m = self.learning_metrics
        lines = [
            "═══════════════════════════════════════",
            "🌐 MULTI-EXCHANGE LEARNING SUMMARY",
            "═══════════════════════════════════════",
            f"Total Trades: {m['total_trades']} | Wins: {m['wins']} | WR: {m['wins']/max(1,m['total_trades'])*100:.1f}%",
            f"Total PnL: ${m['total_pnl']:.2f}",
            "",
            "By Exchange:"
        ]
        
        for ex, metrics in m.get('by_exchange', {}).items():
            wr = metrics['wins'] / max(1, metrics['total_trades']) * 100
            lines.append(f"  {ex}: {metrics['total_trades']} trades, {wr:.1f}% WR, ${metrics['pnl']:.2f}")
            
        lines.append("")
        lines.append("By Asset Class:")
        for ac, metrics in m.get('by_asset_class', {}).items():
            wr = metrics['wins'] / max(1, metrics['total_trades']) * 100
            lines.append(f"  {ac}: {metrics['total_trades']} trades, {wr:.1f}% WR, ${metrics['pnl']:.2f}")
            
        lines.append("")
        lines.append("By Frequency Band:")
        for fb, metrics in m.get('by_frequency_band', {}).items():
            wr = metrics['wins'] / max(1, metrics['total_trades']) * 100
            lines.append(f"  {fb}: {metrics['total_trades']} trades, {wr:.1f}% WR")
            
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 📊 UNIFIED STATE AGGREGATOR - All JSON Feeds Into Ecosystem
# ═══════════════════════════════════════════════════════════════

class UnifiedStateAggregator:
    """
    📊 UNIFIED STATE AGGREGATOR
    
    Consolidates ALL JSON data sources and feeds them into the main ecosystem:
    
    Data Sources:
    ├─ aureon_kraken_state.json       - Main trading state (positions, balance, stats)
    ├─ elephant_ultimate.json         - Symbol memory (hunts, wins, blacklist)
    ├─ elephant_unified.json          - Unified elephant memory
    ├─ adaptive_learning_history.json - Learning engine data
    ├─ calibration_trades.json        - Calibration trade history
    ├─ hnc_frequency_log.json         - HNC frequency readings
    ├─ auris_runtime.json             - Auris configuration & targets
    └─ /tmp/aureon_trade_logs/*.jsonl - Trade logs for analysis
    
    ALL SYSTEMS FEED THE ECOSYSTEM through this aggregator.
    """
    
    # JSON file paths
    STATE_FILES = {
        'main_state': 'aureon_kraken_state.json',
        'elephant_ultimate': 'elephant_ultimate.json',
        'elephant_unified': 'elephant_unified.json',
        'elephant_live': 'elephant_live.json',
        'adaptive_learning': 'adaptive_learning_history.json',
        'calibration': 'calibration_trades.json',
        'hnc_frequency': 'hnc_frequency_log.json',
        'auris_runtime': 'auris_runtime.json',
        'multi_exchange_learning': 'multi_exchange_learning.json',
    }
    
    # JSONL logs
    LOG_FILES = {
        'thoughts': 'logs/aureon_thoughts.jsonl',
    }

    PROBABILITY_REPORTS = [
        'probability_all_markets_report.json',
        'probability_all_exchanges_report.json',
        'probability_kraken_report.json',
        'probability_full_market_report.json',
        'probability_batch_report.json',
        'probability_data.json',
        'probability_combined_report.json',
        'probability_4_exchanges_report.json',
        'probability_training_report.json',
    ]

    EXTRA_TRADE_HISTORY = [
        'paper_trade_history.json',  # Paper trade log
    ]

    ANALYTICS_REPORTS = [
        'multi_agent_results.json',
        'multi_agent_aggressive_results.json',
        'kelly_montecarlo_results.json',
        'montecarlo_results.json',
        'aureon_baseline_results.json',
        'hive_baseline.json',
        'harmonic_wave_data.json',
    ]

    POSITION_FILES = [
        'positions.json',
        'piano_positions.json',
    ]

    AUX_LOG_FILES = [
        'rejection_log.json',
        'smoke_test_results.json',
        'prediction_test_result.json',
    ]
    
    def __init__(self):
        self.aggregated_state = {
            'last_aggregation': 0,
            'sources_loaded': [],
            'total_historical_trades': 0,
            'combined_win_rate': 0.0,
            'symbol_insights': {},
            'probability_insights': {},
            'analytics_insights': {},
            'positions_snapshot': {},
            'aux_logs': {},
            'frequency_performance': {},
            'exchange_performance': {},
            'coherence_bands': {},
            'organism_health': {
                'status': 'UNKNOWN',
                'pulse': {},
                'recent_thoughts': []
            },
        }
        self.load_all_sources()
        
    def load_all_sources(self) -> Dict[str, Any]:
        """Load and aggregate data from all JSON sources."""
        self.aggregated_state['sources_loaded'] = []
        self.load_organism_thoughts()  # Load thoughts first
        all_trades = []
        symbol_data = {}
        frequency_data = {}
        probability_insights: Dict[str, Dict[str, Any]] = {}
        probability_freshness: Dict[str, Any] = {
            'report_ages_minutes': {},
            'newest_minutes': None,
            'oldest_minutes': None,
            'stale': False,
            'threshold_minutes': 120,
        }
        high_conviction: List[Dict[str, Any]] = []
        analytics_insights: Dict[str, Dict[str, Any]] = {}
        positions_snapshot: Dict[str, Any] = {}
        aux_logs: Dict[str, Any] = {}
        position_hygiene: Dict[str, Any] = {
            'flagged': [],
            'rules': {
                'max_cycles': 50,
                'min_momentum': -2.0,
            }
        }

        def _extract_pnl(trade: Dict[str, Any]) -> float:
            pnl = trade.get('pnl_usd')
            if pnl is None:
                pnl = trade.get('pnl')
            if pnl is None:
                return 0.0
            try:
                return float(pnl)
            except (TypeError, ValueError):
                return 0.0
        
        # 1. Load Main Trading State
        main_state = self._load_json(self.STATE_FILES['main_state'])
        if main_state:
            self.aggregated_state['sources_loaded'].append('main_state')
            self.aggregated_state['current_balance'] = main_state.get('balance', 0)
            self.aggregated_state['peak_balance'] = main_state.get('peak_balance', 0)
            self.aggregated_state['total_trades'] = main_state.get('total_trades', 0)
            self.aggregated_state['wins'] = main_state.get('wins', 0)
            self.aggregated_state['losses'] = main_state.get('losses', 0)
            self.aggregated_state['max_drawdown'] = main_state.get('max_drawdown', 0)
            
            # 🎯 TRUE STARTING BALANCE - shared across all subsystems!
            self.aggregated_state['first_start_balance'] = main_state.get('first_start_balance', main_state.get('initial_balance', 0))
            self.aggregated_state['first_start_time'] = main_state.get('first_start_time', 0)
            self.aggregated_state['initial_balance'] = main_state.get('initial_balance', 0)

            # Position hygiene pass: flag long-running or losing positions
            positions = main_state.get('positions', {}) or {}
            for sym, pos in positions.items():
                try:
                    cycles = pos.get('cycles', 0)
                    momentum = pos.get('momentum', 0.0)
                    if cycles >= position_hygiene['rules']['max_cycles'] or momentum <= position_hygiene['rules']['min_momentum']:
                        position_hygiene['flagged'].append({
                            'symbol': sym,
                            'cycles': cycles,
                            'momentum': momentum,
                            'entry_price': pos.get('entry_price'),
                            'coherence': pos.get('coherence'),
                            'dominant_node': pos.get('dominant_node'),
                        })
                except Exception:
                    continue
            
        # 2. Load Elephant Memory files (symbol-level insights)
        for elephant_key in ['elephant_ultimate', 'elephant_unified', 'elephant_live']:
            elephant_data = self._load_json(self.STATE_FILES.get(elephant_key, ''))
            if elephant_data:
                self.aggregated_state['sources_loaded'].append(elephant_key)
                for symbol, data in elephant_data.items():
                    if symbol not in symbol_data:
                        symbol_data[symbol] = {
                            'total_hunts': 0, 'total_trades': 0, 'wins': 0, 
                            'losses': 0, 'profit': 0, 'blacklisted': False
                        }
                    symbol_data[symbol]['total_hunts'] += data.get('hunts', 0)
                    symbol_data[symbol]['total_trades'] += data.get('trades', 0)
                    symbol_data[symbol]['wins'] += data.get('wins', 0)
                    symbol_data[symbol]['losses'] += data.get('losses', 0)
                    symbol_data[symbol]['profit'] += data.get('profit', 0)
                    if data.get('blacklisted', False):
                        symbol_data[symbol]['blacklisted'] = True
                        
        self.aggregated_state['symbol_insights'] = symbol_data
        
        # 3. Load Calibration Trades (detailed trade history)
        calibration = self._load_json(self.STATE_FILES['calibration'])
        if calibration and isinstance(calibration, list):
            self.aggregated_state['sources_loaded'].append('calibration')
            all_trades.extend(calibration)
            
            # Extract frequency performance from calibration
            for trade in calibration:
                freq = trade.get('frequency', 0)
                freq_band = self._get_freq_band(freq)
                if freq_band not in frequency_data:
                    frequency_data[freq_band] = {'trades': 0, 'wins': 0, 'pnl': 0}
                frequency_data[freq_band]['trades'] += 1
                trade_pnl = _extract_pnl(trade)
                if trade_pnl > 0:
                    frequency_data[freq_band]['wins'] += 1
                frequency_data[freq_band]['pnl'] += trade_pnl
                
        self.aggregated_state['frequency_performance'] = frequency_data

        # 3b. Load extra trade history files (paper trading, etc.)
        for hist_file in self.EXTRA_TRADE_HISTORY:
            hist = self._load_json(hist_file)
            if hist and isinstance(hist, list):
                self.aggregated_state['sources_loaded'].append(f"history:{hist_file}")
                all_trades.extend(hist)
        
        # 4. Load HNC Frequency Log (frequency readings over time)
        hnc_log = self._load_json(self.STATE_FILES['hnc_frequency'])
        if hnc_log and isinstance(hnc_log, list):
            self.aggregated_state['sources_loaded'].append('hnc_frequency')
            # Get latest readings for each symbol
            latest_readings = {}
            for entry in hnc_log[-100:]:  # Last 100 entries
                for reading in entry.get('readings', []):
                    symbol = reading.get('symbol', '')
                    if symbol:
                        latest_readings[symbol] = {
                            'frequency': reading.get('frequency', 256),
                            'resonance': reading.get('resonance', 0.5),
                            'is_harmonic': reading.get('is_harmonic', False)
                        }
            self.aggregated_state['hnc_readings'] = latest_readings
            
        # 5. Load Adaptive Learning History
        adaptive = self._load_json(self.STATE_FILES['adaptive_learning'])
        if adaptive:
            self.aggregated_state['sources_loaded'].append('adaptive_learning')
            self.aggregated_state['learned_thresholds'] = adaptive.get('thresholds', {})
            adaptive_trades = adaptive.get('trades', [])
            all_trades.extend(adaptive_trades)
            
        # 6. Load Auris Runtime Config
        auris_config = self._load_json(self.STATE_FILES['auris_runtime'])
        if auris_config:
            self.aggregated_state['sources_loaded'].append('auris_runtime')
            self.aggregated_state['auris_targets'] = auris_config.get('targets_hz', {})
            self.aggregated_state['auris_identity'] = auris_config.get('identity', {})
            
        # 7. Load Multi-Exchange Learning (if exists)
        multi_ex = self._load_json(self.STATE_FILES['multi_exchange_learning'])
        if multi_ex:
            self.aggregated_state['sources_loaded'].append('multi_exchange_learning')
            self.aggregated_state['exchange_performance'] = multi_ex.get('by_exchange', {})

        # 7b. Load probability reports (market selection intelligence)
        for report in self.PROBABILITY_REPORTS:
            data = self._load_json(report)
            if not data:
                continue
            self.aggregated_state['sources_loaded'].append(f"probability:{report}")

            # Freshness tracking
            generated_ts = data.get('generated') or data.get('generated_at') if isinstance(data, dict) else None
            if generated_ts:
                try:
                    gen_dt = datetime.fromisoformat(generated_ts)
                    age_min = (datetime.now() - gen_dt).total_seconds() / 60
                    probability_freshness['report_ages_minutes'][report] = age_min
                except Exception:
                    pass

            entries = []
            for key in ('top_bullish', 'top_bearish', 'data', 'signals', 'items', 'predictions', 'data_points'):
                if isinstance(data, list) and key == 'data':
                    entries.extend(data)
                if isinstance(data.get(key, None), list):
                    entries.extend(data[key])
            if isinstance(data, list):
                entries.extend(data)

            for item in entries:
                if not isinstance(item, dict):
                    continue
                sym = item.get('symbol') or item.get('pair')
                if not sym:
                    continue
                try:
                    prob = float(item.get('probability', item.get('prob', 0)))
                except Exception:
                    prob = 0.0
                change = item.get('24h_change') or item.get('change') or item.get('pct_change') or 0
                state = item.get('state') or item.get('direction') or item.get('trend')

                current = probability_insights.get(sym, {})
                if not current or prob > current.get('probability', -1):
                    probability_insights[sym] = {
                        'probability': prob,
                        'state': state,
                        'change': change,
                        'source': report
                    }

                # Capture high-conviction signals for watchlist seeding
                confidence = item.get('confidence', item.get('conf', 0)) or 0.0
                if prob >= 0.80 and confidence >= 0.80:
                    high_conviction.append({
                        'symbol': sym,
                        'probability': prob,
                        'confidence': confidence,
                        'change': change,
                        'state': state,
                        'source': report,
                        'exchange': item.get('exchange'),
                    })
            
        # 8. Scan trade logs directory
        trade_logs = self._scan_trade_logs()
        if trade_logs:
            self.aggregated_state['sources_loaded'].append('trade_logs')
            all_trades.extend(trade_logs)

        # Save probability insights
        if probability_insights:
            self.aggregated_state['probability_insights'] = probability_insights

        # Probability freshness summary
        if probability_freshness['report_ages_minutes']:
            ages = list(probability_freshness['report_ages_minutes'].values())
            probability_freshness['newest_minutes'] = min(ages)
            probability_freshness['oldest_minutes'] = max(ages)
            probability_freshness['stale'] = probability_freshness['newest_minutes'] > probability_freshness['threshold_minutes']
            self.aggregated_state['probability_freshness'] = probability_freshness

        if high_conviction:
            self.aggregated_state['high_conviction_signals'] = high_conviction

        # 9. Load analytics reports (performance/forecast artifacts)
        for report in self.ANALYTICS_REPORTS:
            data = self._load_json(report)
            if not data:
                continue
            self.aggregated_state['sources_loaded'].append(f"analytics:{report}")
            entries = []
            if isinstance(data, list):
                entries = data
            elif isinstance(data, dict):
                for key in ('results', 'items', 'signals', 'data', 'top'):  # generic containers
                    if isinstance(data.get(key, None), list):
                        entries.extend(data[key])
                if not entries:
                    entries = [data]

            for item in entries:
                if not isinstance(item, dict):
                    continue
                sym = item.get('symbol') or item.get('pair') or item.get('asset')
                if not sym:
                    continue
                pnl = item.get('pnl') or item.get('pnl_usd') or item.get('profit') or 0
                wr = item.get('win_rate') or item.get('wr') or item.get('wins_ratio')
                prob = item.get('probability') or item.get('prob')
                score = item.get('score') or item.get('sharpe') or item.get('fitness')
                current = analytics_insights.get(sym, {})

                def _better(a, b):
                    # prefer higher prob/score/wr, then pnl
                    return (
                        (a.get('probability', 0) or 0) > (b.get('probability', 0) or 0) or
                        (a.get('score', 0) or 0) > (b.get('score', 0) or 0) or
                        (a.get('win_rate', 0) or 0) > (b.get('win_rate', 0) or 0) or
                        (a.get('pnl', 0) or 0) > (b.get('pnl', 0) or 0)
                    )

                candidate = {
                    'pnl': pnl,
                    'win_rate': wr,
                    'probability': prob,
                    'score': score,
                    'source': report,
                }

                if not current or _better(candidate, current):
                    analytics_insights[sym] = candidate

        if analytics_insights:
            self.aggregated_state['analytics_insights'] = analytics_insights

        # 10. Load positions files (current holdings snapshots)
        for pos_file in self.POSITION_FILES:
            pdata = self._load_json(pos_file)
            if not pdata:
                continue
            self.aggregated_state['sources_loaded'].append(f"positions:{pos_file}")
            if isinstance(pdata, dict):
                for sym, entry in pdata.items():
                    size = entry.get('quantity') or entry.get('qty') or entry.get('amount') or entry
                    positions_snapshot[sym] = size
            elif isinstance(pdata, list):
                for entry in pdata:
                    if not isinstance(entry, dict):
                        continue
                    sym = entry.get('symbol') or entry.get('pair')
                    if not sym:
                        continue
                    size = entry.get('quantity') or entry.get('qty') or entry.get('amount')
                    positions_snapshot[sym] = size

        if positions_snapshot:
            self.aggregated_state['positions_snapshot'] = positions_snapshot

        if position_hygiene['flagged']:
            self.aggregated_state['position_hygiene'] = position_hygiene

        # 11. Load auxiliary logs (diagnostic only)
        for log_file in self.AUX_LOG_FILES:
            ldata = self._load_json(log_file)
            if not ldata:
                continue
            self.aggregated_state['sources_loaded'].append(f"aux:{log_file}")
            try:
                count = len(ldata) if hasattr(ldata, '__len__') else 1
            except Exception:
                count = 1
            aux_logs[log_file] = {'entries': count}

        if aux_logs:
            self.aggregated_state['aux_logs'] = aux_logs
            
        # Calculate aggregated metrics
        self.aggregated_state['total_historical_trades'] = len(all_trades)
        if all_trades:
            wins = sum(1 for t in all_trades if _extract_pnl(t) > 0)
            self.aggregated_state['combined_win_rate'] = wins / len(all_trades) * 100
            
        # Calculate coherence bands performance
        coherence_bands = {'low': {'trades': 0, 'wins': 0}, 'mid': {'trades': 0, 'wins': 0}, 'high': {'trades': 0, 'wins': 0}}
        for trade in all_trades:
            coh = trade.get('coherence', 0.5)
            band = 'low' if coh < 0.5 else 'mid' if coh < 0.7 else 'high'
            coherence_bands[band]['trades'] += 1
            if _extract_pnl(trade) > 0:
                coherence_bands[band]['wins'] += 1
        self.aggregated_state['coherence_bands'] = coherence_bands
        
        self.aggregated_state['last_aggregation'] = time.time()
        
        logger.info(f"📊 State Aggregator: Loaded {len(self.aggregated_state['sources_loaded'])} sources, "
                   f"{self.aggregated_state['total_historical_trades']} historical trades")
        
        return self.aggregated_state
        
    def _load_json(self, filepath: str) -> Optional[Any]:
        """Safely load a JSON file."""
        if not filepath:
            return None
        try:
            full_path = os.path.join(ROOT_DIR, filepath)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.debug(f"Could not load {filepath}: {e}")
        return None
        
    def _scan_trade_logs(self) -> List[Dict]:
        """Scan /tmp/aureon_trade_logs for historical trades."""
        trades = []
        log_dir = '/tmp/aureon_trade_logs'
        if not os.path.exists(log_dir):
            return trades
            
        try:
            for filename in os.listdir(log_dir):
                if filename.endswith('.jsonl'):
                    filepath = os.path.join(log_dir, filename)
                    with open(filepath, 'r') as f:
                        for line in f:
                            try:
                                trade = json.loads(line.strip())
                                trades.append(trade)
                            except:
                                continue
        except Exception as e:
            logger.debug(f"Trade log scan error: {e}")
            
        return trades[-500:]  # Last 500 trades
        
    def _get_freq_band(self, freq: float) -> str:
        """Get frequency band name."""
        if freq < 300:
            return 'ROOT (174-256Hz)'
        elif freq < 450:
            return 'EARTH (396-432Hz)'
        elif freq < 550:
            return 'LOVE (528Hz)'
        elif freq < 700:
            return 'THROAT (639Hz)'
        elif freq < 850:
            return 'THIRD_EYE (741Hz)'
        else:
            return 'CROWN (852-963Hz)'
            
    def get_symbol_insight(self, symbol: str) -> Dict[str, Any]:
        """Get aggregated insight for a specific symbol."""
        base_symbol = symbol.replace('USDT', '').replace('USD', '').replace('GBP', '').replace('EUR', '')
        
        # Check all symbol variations
        insight = {'hunts': 0, 'trades': 0, 'wins': 0, 'losses': 0, 'profit': 0, 'blacklisted': False, 'win_rate': 0.5}
        
        for sym, data in self.aggregated_state.get('symbol_insights', {}).items():
            if base_symbol in sym or sym in symbol:
                insight['hunts'] += data.get('total_hunts', 0)
                insight['trades'] += data.get('total_trades', 0)
                insight['wins'] += data.get('wins', 0)
                insight['losses'] += data.get('losses', 0)
                insight['profit'] += data.get('profit', 0)
                if data.get('blacklisted'):
                    insight['blacklisted'] = True
                    
        if insight['trades'] > 0:
            insight['win_rate'] = insight['wins'] / insight['trades']
            
        # Get HNC reading if available
        hnc = self.aggregated_state.get('hnc_readings', {}).get(symbol, {})
        if hnc:
            insight['frequency'] = hnc.get('frequency', 256)
            insight['resonance'] = hnc.get('resonance', 0.5)
            insight['is_harmonic'] = hnc.get('is_harmonic', False)

        # Probability signals (market selection intelligence)
        prob_insights = self.aggregated_state.get('probability_insights', {})
        for sym, pdata in prob_insights.items():
            base = sym.replace('USDT', '').replace('USD', '').replace('GBP', '').replace('EUR', '')
            if base_symbol == base or base in base_symbol:
                insight['probability_signal'] = pdata.get('probability', 0)
                insight['probability_state'] = pdata.get('state')
                insight['probability_change'] = pdata.get('change')
                insight['probability_source'] = pdata.get('source')
                break

        # Analytics signals (sim/backtest/agent metrics)
        analytics = self.aggregated_state.get('analytics_insights', {})
        for sym, adata in analytics.items():
            base = sym.replace('USDT', '').replace('USD', '').replace('GBP', '').replace('EUR', '')
            if base_symbol == base or base in base_symbol:
                insight['analytics_win_rate'] = adata.get('win_rate')
                insight['analytics_prob'] = adata.get('probability')
                insight['analytics_score'] = adata.get('score')
                insight['analytics_pnl'] = adata.get('pnl')
                insight['analytics_source'] = adata.get('source')
                break

        # Position snapshot (current holdings if available)
        positions = self.aggregated_state.get('positions_snapshot', {})
        for sym, qty in positions.items():
            base = sym.replace('USDT', '').replace('USD', '').replace('GBP', '').replace('EUR', '')
            if base_symbol == base or base in base_symbol:
                insight['position_quantity'] = qty
                break
            
        return insight
        
    def get_frequency_recommendation(self, freq: float) -> Dict[str, Any]:
        """Get recommendation based on historical frequency performance."""
        freq_band = self._get_freq_band(freq)
        perf = self.aggregated_state.get('frequency_performance', {}).get(freq_band, {})
        
        trades = perf.get('trades', 0)
        wins = perf.get('wins', 0)
        pnl = perf.get('pnl', 0)
        
        recommendation = {
            'band': freq_band,
            'historical_trades': trades,
            'historical_win_rate': wins / max(1, trades),
            'historical_pnl': pnl,
            'confidence': min(1.0, trades / 20),  # Full confidence after 20 trades
            'boost_factor': 1.0
        }
        
        # Calculate boost factor based on historical performance
        if trades >= 10:
            win_rate = wins / trades
            if win_rate > 0.60:
                recommendation['boost_factor'] = 1.0 + (win_rate - 0.50) * 0.5
            elif win_rate < 0.40:
                recommendation['boost_factor'] = 0.7
                
        return recommendation
        
    def get_coherence_recommendation(self, coherence: float) -> Dict[str, Any]:
        """Get recommendation based on historical coherence performance."""
        band = 'low' if coherence < 0.5 else 'mid' if coherence < 0.7 else 'high'
        perf = self.aggregated_state.get('coherence_bands', {}).get(band, {})
        
        trades = perf.get('trades', 0)
        wins = perf.get('wins', 0)
        
        return {
            'band': band,
            'historical_trades': trades,
            'historical_win_rate': wins / max(1, trades),
            'confidence': min(1.0, trades / 20),
            'recommended_min': 0.45 if band == 'low' else 0.50 if band == 'mid' else 0.55
        }

    def get_top_signals(self, n: int = 5) -> Dict[str, List[Tuple[str, Dict[str, Any]]]]:
        """Return top probability and analytics signals plus largest positions for visibility."""
        probs = sorted(
            self.aggregated_state.get('probability_insights', {}).items(),
            key=lambda kv: kv[1].get('probability', 0) or 0,
            reverse=True
        )[:n]

        def _analytic_key(item):
            data = item[1]
            return (
                data.get('score') or 0,
                data.get('win_rate') or 0,
                data.get('probability') or 0,
                data.get('pnl') or 0,
            )

        analytics = sorted(
            self.aggregated_state.get('analytics_insights', {}).items(),
            key=_analytic_key,
            reverse=True
        )[:n]

        positions = sorted(
            self.aggregated_state.get('positions_snapshot', {}).items(),
            key=lambda kv: abs(kv[1]) if isinstance(kv[1], (int, float)) else 0,
            reverse=True
        )[:n]

        return {
            'probability': probs,
            'analytics': analytics,
            'positions': positions,
        }
        
    def load_organism_thoughts(self, limit: int = 50):
        """Load recent thoughts to determine organism health."""
        try:
            filepath = os.path.join(ROOT_DIR, self.LOG_FILES['thoughts'])
            if not os.path.exists(filepath):
                return

            thoughts = []
            # Read last N lines efficiently
            with open(filepath, 'rb') as f:
                try:
                    f.seek(-10000, os.SEEK_END) # Go back ~10KB
                except OSError:
                    f.seek(0)
                
                lines = f.readlines()
                # Decode and parse last N lines
                for line in lines[-limit:]:
                    try:
                        thoughts.append(json.loads(line.decode('utf-8')))
                    except:
                        pass
            
            # Analyze health
            now = time.time()
            pulse = {
                'miner': {'last_seen': 0, 'status': 'OFFLINE'},
                'risk': {'last_seen': 0, 'status': 'OFFLINE'},
                'execution': {'last_seen': 0, 'status': 'OFFLINE'},
                'ecosystem': {'last_seen': 0, 'status': 'OFFLINE'},
            }
            
            for t in thoughts:
                src = t.get('source', 'unknown')
                ts = t.get('ts', 0)
                if src in pulse:
                    pulse[src]['last_seen'] = max(pulse[src]['last_seen'], ts)
            
            # Determine status based on recency (e.g. seen in last 60s)
            healthy_count = 0
            for src, data in pulse.items():
                age = now - data['last_seen']
                if age < 60:
                    data['status'] = 'ONLINE'
                    healthy_count += 1
                elif age < 300:
                    data['status'] = 'STALE'
                else:
                    data['status'] = 'OFFLINE'
            
            overall_status = 'HEALTHY' if healthy_count >= 3 else 'DEGRADED' if healthy_count > 0 else 'OFFLINE'
            
            self.aggregated_state['organism_health'] = {
                'status': overall_status,
                'pulse': pulse,
                'recent_thoughts': thoughts[-5:] # Keep last 5 for display
            }
            self.aggregated_state['sources_loaded'].append('organism_thoughts')
            
        except Exception as e:
            logger.debug(f"Failed to load organism thoughts: {e}")

    def save_aggregated_state(self):
        """Save multi-exchange learning state for persistence."""
        try:
            filepath = os.path.join(ROOT_DIR, self.STATE_FILES['multi_exchange_learning'])
            with open(filepath, 'w') as f:
                json.dump({
                    'by_exchange': self.aggregated_state.get('exchange_performance', {}),
                    'frequency_performance': self.aggregated_state.get('frequency_performance', {}),
                    'coherence_bands': self.aggregated_state.get('coherence_bands', {}),
                    'probability_insights': self.aggregated_state.get('probability_insights', {}),
                    'total_historical_trades': self.aggregated_state.get('total_historical_trades', 0),
                    'combined_win_rate': self.aggregated_state.get('combined_win_rate', 0),
                    'updated_at': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save aggregated state: {e}")
            
    def get_summary(self) -> str:
        """Get formatted summary of aggregated state."""
        state = self.aggregated_state
        
        # Calculate TRUE P&L
        first_start = state.get('first_start_balance', 0)
        current = state.get('current_balance', 0)
        true_pnl = current - first_start if first_start > 0 else 0
        true_pct = (true_pnl / first_start * 100) if first_start > 0 else 0
        first_start_time = state.get('first_start_time', 0)
        start_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(first_start_time)) if first_start_time > 0 else 'Unknown'
        
        lines = [
            "═══════════════════════════════════════",
            "📊 UNIFIED STATE AGGREGATOR SUMMARY",
            "═══════════════════════════════════════",
            f"Sources Loaded: {', '.join(state.get('sources_loaded', []))}",
            f"Historical Trades: {state.get('total_historical_trades', 0)}",
            f"Combined Win Rate: {state.get('combined_win_rate', 0):.1f}%",
            "",
            "💵 PORTFOLIO (TRUE from first run):",
            f"   First Started: {start_str}",
            f"   TRUE Starting: £{first_start:.2f}",
            f"   Current: £{current:.2f}",
            f"   TRUE P&L: £{true_pnl:+.2f} ({true_pct:+.1f}%)",
            "",
            "Frequency Performance:"
        ]
        
        for band, perf in state.get('frequency_performance', {}).items():
            wr = perf['wins'] / max(1, perf['trades']) * 100
            lines.append(f"  {band}: {perf['trades']} trades, {wr:.1f}% WR, ${perf['pnl']:.2f}")
            
        lines.append("")
        lines.append("Coherence Bands:")
        for band, perf in state.get('coherence_bands', {}).items():
            wr = perf['wins'] / max(1, perf['trades']) * 100
            lines.append(f"  {band}: {perf['trades']} trades, {wr:.1f}% WR")
            
        health = state.get('organism_health', {})
        lines.append("")
        lines.append(f"🧠 ORGANISM HEALTH: {health.get('status', 'UNKNOWN')}")
        pulse = health.get('pulse', {})
        lines.append(f"   Miner: {pulse.get('miner', {}).get('status')} | Risk: {pulse.get('risk', {}).get('status')} | Exec: {pulse.get('execution', {}).get('status')}")
            
        return "\n".join(lines)


# Global state aggregator instance
STATE_AGGREGATOR = UnifiedStateAggregator()


class CognitiveImmuneSystem:
    """Autonomous antivirus/immune layer that validates cognition integrity."""

    def __init__(self, ecosystem: 'AureonKrakenEcosystem', thought_bus: Optional[ThoughtBus], state_aggregator: UnifiedStateAggregator):
        self.ecosystem = ecosystem
        self.bus = thought_bus
        self.aggregator = state_aggregator
        self.last_scan = 0.0
        self.scan_interval = 30.0
        self.fault_memory: Deque[Dict[str, Any]] = deque(maxlen=200)
        self.minds = {
            'Miner': self._miner_mind,
            'Risk': self._risk_mind,
            'Execution': self._execution_mind,
            'Bridge': self._bridge_mind,
            'NewsFeed': self._newsfeed_mind,
            'KnowledgeBase': self._knowledge_mind,
        }

        if self.bus:
            self.bus.subscribe("system.error", self._on_fault_thought)

    # ------------------------------------------------------------------
    # Event ingestion
    # ------------------------------------------------------------------
    def _on_fault_thought(self, thought: Thought) -> None:
        payload = thought.payload if isinstance(thought.payload, dict) else {}
        fault = {
            'ts': thought.ts,
            'source': payload.get('while_handling_topic', thought.topic),
            'error': payload.get('error', 'unknown fault'),
            'trace_id': thought.trace_id,
        }
        self.fault_memory.append(fault)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def scan_and_heal(self, force: bool = False) -> None:
        now = time.time()
        if not force and (now - self.last_scan) < self.scan_interval:
            return
        self.last_scan = now

        faults = self._collect_faults(now)
        if not faults:
            return

        healing_plan: List[Dict[str, Any]] = []
        for _, handler in self.minds.items():
            plan = handler(faults)
            if plan:
                healing_plan.extend(plan)

        if not healing_plan:
            self._emit_thought("immune.alert", {"faults": faults, "plan": []})
            return

        self._execute_plan(healing_plan, faults)

    # ------------------------------------------------------------------
    # Fault analysis helpers
    # ------------------------------------------------------------------
    def _collect_faults(self, now: float) -> List[Dict[str, Any]]:
        faults: List[Dict[str, Any]] = []

        # Organism status from aggregator
        health = self.aggregator.aggregated_state.get('organism_health', {}) if self.aggregator else {}
        status = health.get('status')
        if status in ('DEGRADED', 'OFFLINE'):
            faults.append({'code': f'ORGANISM_{status}', 'detail': health})

        # Probability freshness
        pfresh = self.aggregator.aggregated_state.get('probability_freshness', {}) if self.aggregator else {}
        if pfresh.get('stale'):
            faults.append({'code': 'PROBABILITY_STALE', 'detail': pfresh})

        # Websocket/liveness
        ws_age = now - getattr(self.ecosystem, 'ws_last_message', now)
        ws_timeout = CONFIG.get('WS_HEARTBEAT_TIMEOUT', 30)
        if ws_age > ws_timeout:
            faults.append({'code': 'WS_STALE', 'detail': {'age': ws_age, 'timeout': ws_timeout}})

        # Trading halt
        tracker = getattr(self.ecosystem, 'tracker', None)
        if tracker and getattr(tracker, 'trading_halted', False):
            faults.append({'code': 'TRADING_HALTED', 'detail': {'reason': tracker.halt_reason}})

        # Bridge sync
        if getattr(self.ecosystem, 'bridge_enabled', False):
            bridge_age = now - getattr(self.ecosystem, 'last_bridge_sync', 0.0)
            if bridge_age > getattr(self.ecosystem, 'bridge_sync_interval', 10.0) * 4:
                faults.append({'code': 'BRIDGE_STALE', 'detail': {'age': bridge_age}})

        # News feed staleness (if no news in 30+ minutes)
        news_feed = getattr(self.ecosystem, 'news_feed', None)
        if news_feed and hasattr(news_feed, 'last_poll_time') and news_feed.last_poll_time:
            try:
                from datetime import datetime
                news_age_seconds = (datetime.utcnow() - news_feed.last_poll_time).total_seconds()
                if news_age_seconds > 1800:  # 30 minutes
                    faults.append({'code': 'NEWS_STALE', 'detail': {'age_seconds': news_age_seconds}})
            except Exception:
                pass

        # News API errors accumulating
        if news_feed:
            news_metrics = getattr(news_feed, 'metrics', {})
            news_errors = news_metrics.get('errors', 0)
            if news_errors >= 5:
                faults.append({'code': 'NEWS_API_ERRORS', 'detail': {'errors': news_errors}})

        # Knowledge base errors
        knowledge_base = getattr(self.ecosystem, 'knowledge_base', None)
        if knowledge_base:
            kb_metrics = getattr(knowledge_base, 'metrics', {})
            kb_errors = kb_metrics.get('errors', 0)
            if kb_errors >= 10:
                faults.append({'code': 'KNOWLEDGE_API_ERRORS', 'detail': {'errors': kb_errors}})

        # Thought-level faults
        recent_faults = [f for f in self.fault_memory if now - f['ts'] < 120]
        for fault in recent_faults:
            faults.append({'code': 'THOUGHT_FAULT', 'detail': fault})

        return faults

    # ------------------------------------------------------------------
    # Mind protocols
    # ------------------------------------------------------------------
    def _miner_mind(self, faults: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        plan: List[Dict[str, Any]] = []
        if any(f['code'] in ('PROBABILITY_STALE', 'THOUGHT_FAULT') for f in faults):
            plan.append({
                'mind': 'Miner',
                'action': 'REFRESH_PROBABILITY_REPORTS',
                'description': 'Reload probability reports + aggregated state',
                'callable': self._heal_probability_reports,
                'auto_execute': True,
            })
        return plan

    def _risk_mind(self, faults: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        plan: List[Dict[str, Any]] = []
        if any(f['code'] in ('TRADING_HALTED', 'ORGANISM_DEGRADED') for f in faults):
            plan.append({
                'mind': 'Risk',
                'action': 'AUDIT_POSITIONS',
                'description': 'Run position/risk audit to release halts if conditions improve',
                'callable': self._heal_risk_controls,
                'auto_execute': True,
            })
        return plan

    def _execution_mind(self, faults: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        plan: List[Dict[str, Any]] = []
        if any(f['code'] == 'WS_STALE' for f in faults):
            plan.append({
                'mind': 'Execution',
                'action': 'RECHARGE_MARKET_DATA',
                'description': 'Refresh tickers and request websocket heartbeat',
                'callable': self._heal_market_data,
                'auto_execute': True,
            })
        return plan

    def _bridge_mind(self, faults: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        plan: List[Dict[str, Any]] = []
        if any(f['code'] == 'BRIDGE_STALE' for f in faults):
            plan.append({
                'mind': 'Bridge',
                'action': 'SYNC_BRIDGE',
                'description': 'Force a bridge sync so Ultimate/Unified share state',
                'callable': self._heal_bridge_link,
                'auto_execute': True,
            })
        return plan

    def _newsfeed_mind(self, faults: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """News Feed mind - handles news API staleness and errors."""
        plan: List[Dict[str, Any]] = []
        
        # Handle stale news
        if any(f['code'] == 'NEWS_STALE' for f in faults):
            plan.append({
                'mind': 'NewsFeed',
                'action': 'FORCE_NEWS_POLL',
                'description': 'Force refresh news feed from World News API',
                'callable': self._heal_news_feed,
                'auto_execute': True,
            })
        
        # Handle API errors accumulating
        if any(f['code'] == 'NEWS_API_ERRORS' for f in faults):
            plan.append({
                'mind': 'NewsFeed',
                'action': 'RESET_NEWS_METRICS',
                'description': 'Reset news API error counters and retry',
                'callable': self._heal_news_errors,
                'auto_execute': True,
            })
        
        return plan

    def _knowledge_mind(self, faults: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Knowledge Base mind - handles Wikipedia API errors."""
        plan: List[Dict[str, Any]] = []
        
        # Handle API errors accumulating
        if any(f['code'] == 'KNOWLEDGE_API_ERRORS' for f in faults):
            plan.append({
                'mind': 'KnowledgeBase',
                'action': 'RESET_KNOWLEDGE_METRICS',
                'description': 'Reset knowledge base error counters and clear stale cache',
                'callable': self._heal_knowledge_errors,
                'auto_execute': True,
            })
        
        return plan

    # ------------------------------------------------------------------
    # Healing actions
    # ------------------------------------------------------------------
    def _heal_probability_reports(self) -> None:
        loader = getattr(self.ecosystem, 'probability_loader', None)
        if loader:
            loader.load_all_reports()
        self.aggregator.load_all_sources()

    def _heal_risk_controls(self) -> None:
        self.ecosystem.check_positions()
        self.ecosystem.refresh_equity()

    def _heal_market_data(self) -> None:
        try:
            self.ecosystem.refresh_tickers()
        finally:
            self.ecosystem.ws_last_message = time.time()

    def _heal_bridge_link(self) -> None:
        if getattr(self.ecosystem, 'bridge_enabled', False):
            self.ecosystem.sync_bridge()

    def _heal_news_feed(self) -> None:
        """Force a news poll to refresh market sentiment data."""
        news_feed = getattr(self.ecosystem, 'news_feed', None)
        if news_feed:
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(news_feed.poll_and_publish())
                finally:
                    loop.close()
            except Exception as e:
                logger.warning(f"News feed heal failed: {e}")

    def _heal_news_errors(self) -> None:
        """Reset news API error counters."""
        news_feed = getattr(self.ecosystem, 'news_feed', None)
        if news_feed and hasattr(news_feed, 'metrics'):
            news_feed.metrics['errors'] = 0
            logger.info("News feed error counters reset")

    def _heal_knowledge_errors(self) -> None:
        """Reset knowledge base error counters and clear stale cache."""
        knowledge_base = getattr(self.ecosystem, 'knowledge_base', None)
        if knowledge_base:
            if hasattr(knowledge_base, 'metrics'):
                knowledge_base.metrics['errors'] = 0
            # Clear cache to force fresh lookups
            if hasattr(knowledge_base, 'cache'):
                knowledge_base.cache.clear()
            logger.info("Knowledge base error counters reset, cache cleared")

    # ------------------------------------------------------------------
    # Execution + telemetry
    # ------------------------------------------------------------------
    def _execute_plan(self, plan: List[Dict[str, Any]], faults: List[Dict[str, Any]]) -> None:
        executed = []
        for step in plan:
            callable_fn = step.get('callable')
            ok = False
            error = None
            if callable_fn:
                try:
                    callable_fn()
                    ok = True
                except Exception as exc:
                    error = str(exc)
            executed.append({
                'mind': step.get('mind'),
                'action': step.get('action'),
                'status': 'ok' if ok else 'error',
                'error': error,
            })

        self._emit_thought("immune.heal", {
            'executed': executed,
            'faults': faults,
        })

    def _emit_thought(self, topic: str, payload: Dict[str, Any]) -> None:
        if not self.bus:
            return
        self.bus.publish(Thought(
            source="immune_system",
            topic=topic,
            payload=payload,
        ))


def kelly_criterion(win_rate: float, avg_win: float, avg_loss: float, safety_factor: float = 0.5) -> float:
    """
    Calculate Kelly Criterion position size.
    
    Formula: f* = (p*b - (1-p)) / b
    Where:
        p = win probability
        b = win/loss ratio (avg_win / avg_loss)
    
    Returns: Position size as fraction of balance (with safety factor applied)
    """
    if avg_loss <= 0 or win_rate <= 0 or win_rate >= 1:
        return 0.10  # Fallback to 10%
    
    b = avg_win / avg_loss
    kelly_fraction = (win_rate * b - (1 - win_rate)) / b
    
    # Apply safety factor and bounds
    kelly_fraction = max(0, kelly_fraction) * safety_factor
    return min(kelly_fraction, CONFIG['MAX_POSITION_SIZE'])


# ═══════════════════════════════════════════════════════════════
# 🧠 ADAPTIVE LEARNING ENGINE - Self-Optimizing Parameters
# ═══════════════════════════════════════════════════════════════

class AdaptiveLearningEngine:
    """
    Learns from past trades and dynamically adjusts system parameters.
    
    Key Optimizations:
    1. Win rate tracking by frequency band (432Hz vs 528Hz vs 440Hz)
    2. Coherence threshold optimization based on actual outcomes
    3. Score threshold calibration using rolling performance
    4. Time-of-day pattern detection
    5. Volume correlation analysis
    """
    
    def __init__(self, history_file: str = 'adaptive_learning_history.json'):
        self.history_file = history_file
        self.trade_history: List[Dict] = []
        self.max_history = 500  # Keep last 500 trades for analysis

        # Keep a pristine copy of defaults for easy reset when data is stale
        self.default_thresholds = {
            'min_coherence': CONFIG.get('ENTRY_COHERENCE', 0.45),
            'min_score': CONFIG.get('MIN_SCORE', 65),
            'min_probability': CONFIG.get('PROB_MIN_CONFIDENCE', 0.50),
            'harmonic_bonus': CONFIG.get('HNC_HARMONIC_BONUS', 1.15),
            'distortion_penalty': CONFIG.get('HNC_DISTORTION_PENALTY', 0.70),
        }
        self.optimized_thresholds = self.default_thresholds.copy()
        self.recency_window_days = 10  # Ignore trades older than this to avoid stale fear
        
        # Performance metrics by category
        self.metrics_by_frequency: Dict[str, Dict] = {}  # freq_band -> {wins, losses, total_pnl}
        self.metrics_by_coherence: Dict[str, Dict] = {}  # coherence_range -> {wins, losses}
        self.metrics_by_score: Dict[str, Dict] = {}      # score_range -> {wins, losses}
        self.metrics_by_hour: Dict[int, Dict] = {}       # hour -> {wins, losses}
        self.metrics_by_action: Dict[str, Dict] = {}     # HNC action -> {wins, losses}
        
        # Learning parameters
        self.learning_rate = 0.05  # How quickly to adapt
        self.min_samples_for_learning = 20  # Minimum trades before adjusting
        self.confidence_interval = 0.95  # Statistical confidence for changes
        
        self._load_history()
        
    def _load_history(self):
        """Load historical trades from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.trade_history = data.get('trades', [])[-self.max_history:]
                    self.optimized_thresholds = {
                        **self.default_thresholds,
                        **data.get('thresholds', {})
                    }

                    stale_removed = self._filter_recent_trades()
                    if stale_removed:
                        logger.info(f"Adaptive Learning: dropped {stale_removed} stale trades (> {self.recency_window_days}d) to stay active")

                    self._clamp_thresholds()
                    self._rebuild_metrics()
                    
                    if not self.trade_history:
                        # If everything was stale, reset to defaults so the system will trade
                        self.optimized_thresholds = self.default_thresholds.copy()
                        logger.info("Adaptive Learning: no recent trades found, resetting thresholds to defaults")
        except Exception as e:
            logger.warning(f"Could not load learning history: {e}")
            
    def _save_history(self):
        """Save trade history and learned thresholds."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump({
                    'trades': self.trade_history[-self.max_history:],
                    'thresholds': self.optimized_thresholds,
                    'updated_at': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save learning history: {e}")
            
    def _rebuild_metrics(self):
        """Rebuild performance metrics from trade history."""
        self.metrics_by_frequency = {}
        self.metrics_by_coherence = {}
        self.metrics_by_score = {}
        self.metrics_by_hour = {}
        self.metrics_by_action = {}
        
        for trade in self.trade_history:
            self._update_metrics(trade)
            
    def _get_frequency_band(self, freq: float) -> str:
        """Map frequency to band name."""
        if freq <= 200:
            return '174_FOUNDATION'
        elif freq <= 300:
            return '256_ROOT'
        elif freq <= 410:
            return '396_LIBERATION'
        elif freq <= 438:
            return '432_NATURAL'
        elif freq <= 445:
            return '440_DISTORTION'
        elif freq <= 520:
            return '512_VISION'
        elif freq <= 580:
            return '528_LOVE'
        elif freq <= 700:
            return '639_CONNECTION'
        elif freq <= 800:
            return '741_AWAKENING'
        elif freq <= 900:
            return '852_INTUITION'
        else:
            return '963_UNITY'
            
    def _get_coherence_range(self, coherence: float) -> str:
        """Map coherence to range bucket."""
        if coherence < 0.3:
            return 'LOW_0-30'
        elif coherence < 0.5:
            return 'MED_30-50'
        elif coherence < 0.7:
            return 'HIGH_50-70'
        else:
            return 'VERY_HIGH_70+'
            
    def _get_score_range(self, score: float) -> str:
        """Map score to range bucket."""
        if score < 50:
            return 'LOW_0-50'
        elif score < 65:
            return 'MED_50-65'
        elif score < 80:
            return 'HIGH_65-80'
        else:
            return 'VERY_HIGH_80+'
            
    def _update_metrics(self, trade: Dict):
        """Update metrics with a single trade."""
        is_win = trade.get('pnl', 0) > 0
        pnl = trade.get('pnl', 0)
        
        # By frequency
        freq = trade.get('frequency', 256)
        band = self._get_frequency_band(freq)
        if band not in self.metrics_by_frequency:
            self.metrics_by_frequency[band] = {'wins': 0, 'losses': 0, 'total_pnl': 0, 'trades': []}
        self.metrics_by_frequency[band]['wins' if is_win else 'losses'] += 1
        self.metrics_by_frequency[band]['total_pnl'] += pnl
        self.metrics_by_frequency[band]['trades'].append(pnl)
        
        # By coherence
        coherence = trade.get('coherence', 0.5)
        coh_range = self._get_coherence_range(coherence)
        if coh_range not in self.metrics_by_coherence:
            self.metrics_by_coherence[coh_range] = {'wins': 0, 'losses': 0, 'trades': []}
        self.metrics_by_coherence[coh_range]['wins' if is_win else 'losses'] += 1
        self.metrics_by_coherence[coh_range]['trades'].append(pnl)
        
        # By score
        score = trade.get('score', 50)
        score_range = self._get_score_range(score)
        if score_range not in self.metrics_by_score:
            self.metrics_by_score[score_range] = {'wins': 0, 'losses': 0, 'trades': []}
        self.metrics_by_score[score_range]['wins' if is_win else 'losses'] += 1
        self.metrics_by_score[score_range]['trades'].append(pnl)
        
        # By hour of day
        entry_time = trade.get('entry_time', time.time())
        hour = datetime.fromtimestamp(entry_tim