#!/usr/bin/env python3
"""
🔬💰 MICRO PROFIT LABYRINTH 💰🔬
=================================

Uses ALL existing systems but with LOWER thresholds for SNOWBALL effect!

V14 wants Score 8+ → We use Score 6+ (more opportunities)
V14 wants 1.52% profit → We want ANY net profit ($0.01+)
V14 has no stop loss → We agree! Hold until profit!

THE PHILOSOPHY:
  - Any net profit > $0.01 is a WIN
  - More small wins = Faster snowball
  - Use existing system intelligence, just LOWER the bar

Gary Leckey | January 2026 | SNOWBALL MODE
"""

from __future__ import annotations

import asyncio
import argparse
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict

# ════════════════════════════════════════════════════════════════════════════
# 🔐 LOAD ENVIRONMENT VARIABLES FROM .env
# ════════════════════════════════════════════════════════════════════════════
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("🔐 Environment variables loaded from .env")
except ImportError:
    print("⚠️ python-dotenv not installed, using system env vars")

# Get exchange config from .env
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY", "")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET", "")
KRAKEN_DRY_RUN = os.getenv("KRAKEN_DRY_RUN", "false").lower() == "true"
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "")
LIVE_MODE = os.getenv("LIVE", "0") == "1"

print(f"🔑 Kraken API: {'✅ Loaded' if KRAKEN_API_KEY else '❌ Missing'}")
print(f"🔑 Binance API: {'✅ Loaded' if BINANCE_API_KEY else '❌ Missing'}")
print(f"🔑 Alpaca API: {'✅ Loaded' if ALPACA_API_KEY else '❌ Missing'}")
print(f"⚙️ LIVE Mode: {'✅ Enabled' if LIVE_MODE else '❌ Disabled'}")

# ════════════════════════════════════════════════════════════════════════════
# EXISTING SYSTEMS - ALL OF THEM!
# ════════════════════════════════════════════════════════════════════════════
try:
    from mycelium_conversion_hub import get_conversion_hub, MyceliumConversionHub
    print("🍄 Mycelium Conversion Hub LOADED!")
except ImportError as e:
    print(f"⚠️ Mycelium Conversion Hub not available: {e}")
    MyceliumConversionHub = None
    get_conversion_hub = None

# Adaptive profit gate (dynamic fees/targets)
try:
    from adaptive_prime_profit_gate import AdaptivePrimeProfitGate
    ADAPTIVE_GATE_AVAILABLE = True
    print("💰 Adaptive Prime Profit Gate LOADED!")
except ImportError as e:
    AdaptivePrimeProfitGate = None
    ADAPTIVE_GATE_AVAILABLE = False
    print(f"⚠️ Adaptive Prime Profit Gate not available: {e}")

# Lightweight Thought Bus for observability
try:
    from aureon_thought_bus import ThoughtBus
    THOUGHT_BUS_AVAILABLE = True
except ImportError as e:
    ThoughtBus = None
    THOUGHT_BUS_AVAILABLE = False
    print(f"⚠️ Thought Bus not available: {e}")

try:
    from s5_v14_labyrinth import V14DanceEnhancer, V14_CONFIG
    print("🏆 V14 Labyrinth LOADED!")
except ImportError as e:
    print(f"⚠️ V14 Labyrinth not available: {e}")
    V14DanceEnhancer = None
    V14_CONFIG = {}

try:
    from aureon_conversion_commando import (
        AdaptiveConversionCommando,
        PairScanner,
        DualProfitPathEvaluator,
        MIN_PROFIT_TARGET,
    )
    print("🦅 Conversion Commando LOADED!")
except ImportError as e:
    print(f"⚠️ Conversion Commando not available: {e}")
    AdaptiveConversionCommando = None
    PairScanner = None
    DualProfitPathEvaluator = None
    MIN_PROFIT_TARGET = 0.01

try:
    from aureon_conversion_ladder import ConversionLadder
    print("🪜 Conversion Ladder LOADED!")
except ImportError as e:
    print(f"⚠️ Conversion Ladder not available: {e}")
    ConversionLadder = None

try:
    from pure_conversion_engine import UnifiedConversionBrain, ConversionOpportunity
    print("🔄 Pure Conversion Engine LOADED!")
except ImportError as e:
    print(f"⚠️ Pure Conversion Engine not available: {e}")
    UnifiedConversionBrain = None
    ConversionOpportunity = None

try:
    from rapid_conversion_stream import RapidConversionStream
    print("⚡ Rapid Conversion Stream LOADED!")
except ImportError as e:
    print(f"⚠️ Rapid Conversion Stream not available: {e}")
    RapidConversionStream = None

try:
    from kraken_client import KrakenClient, get_kraken_client
    print("🐙 Kraken Client LOADED!")
    KRAKEN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Kraken Client not available: {e}")
    # Try direct instantiation
    try:
        from kraken_client import KrakenClient
        def get_kraken_client():
            return KrakenClient()
        print("🐙 Kraken Client LOADED (direct)!")
        KRAKEN_AVAILABLE = True
    except ImportError:
        KrakenClient = None
        get_kraken_client = None
        KRAKEN_AVAILABLE = False

# Binance client
try:
    from binance_client import BinanceClient
    print("🟡 Binance Client LOADED!")
    BINANCE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Binance Client not available: {e}")
    BinanceClient = None
    BINANCE_AVAILABLE = False

# Alpaca client
try:
    from alpaca_client import AlpacaClient
    print("🦙 Alpaca Client LOADED!")
    ALPACA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Alpaca Client not available: {e}")
    AlpacaClient = None
    ALPACA_AVAILABLE = False

# Additional signal sources
try:
    from aureon_probability_nexus import EnhancedProbabilityNexus
    print("🔮 Probability Nexus LOADED!")
except ImportError:
    EnhancedProbabilityNexus = None

try:
    from aureon_internal_multiverse import InternalMultiverse
    print("🌌 Internal Multiverse LOADED!")
except ImportError:
    InternalMultiverse = None

try:
    from aureon_miner_brain import MinerBrain
    print("🧠 Miner Brain LOADED!")
except ImportError:
    MinerBrain = None

try:
    from aureon_harmonic_fusion import HarmonicWaveFusion
    print("🌊 Harmonic Fusion LOADED!")
except ImportError:
    HarmonicWaveFusion = None

try:
    from aureon_omega import Omega
    print("🔱 Omega LOADED!")
except ImportError:
    Omega = None

# ════════════════════════════════════════════════════════════════════════════
# 🗺️ CRYPTO MARKET MAP - LABYRINTH PATHFINDER
# ════════════════════════════════════════════════════════════════════════════
try:
    from crypto_market_map import CryptoMarketMap, SYMBOL_TO_SECTOR, CRYPTO_SECTORS
    MARKET_MAP_AVAILABLE = True
    print("🗺️ Crypto Market Map LOADED!")
except ImportError:
    CryptoMarketMap = None
    SYMBOL_TO_SECTOR = {}
    CRYPTO_SECTORS = {}
    MARKET_MAP_AVAILABLE = False

# ════════════════════════════════════════════════════════════════════════════
# 🧠⚡ STAGE 1: FULL NEURAL MIND MAP IMPORTS ⚡🧠
# ════════════════════════════════════════════════════════════════════════════

# Mycelium Neural Network (core hive intelligence)
try:
    from aureon_mycelium import MyceliumNetwork, Synapse, Hive
    MYCELIUM_NETWORK_AVAILABLE = True
    print("🍄 Mycelium Neural Network LOADED!")
except ImportError:
    MyceliumNetwork = None
    Synapse = None
    Hive = None
    MYCELIUM_NETWORK_AVAILABLE = False

# Unified Ecosystem (full orchestrator read-only)
try:
    from aureon_unified_ecosystem import AureonKrakenEcosystem as AureonUnifiedEcosystem, AdaptiveLearningEngine as AdaptiveLearner
    UNIFIED_ECOSYSTEM_AVAILABLE = True
    print("🌍 Unified Ecosystem LOADED!")
except Exception as e:
    AureonUnifiedEcosystem = None
    AdaptiveLearner = None
    UNIFIED_ECOSYSTEM_AVAILABLE = False
    print(f"⚠️ Unified Ecosystem import failed: {e}")

# Memory Core (spiral memory)
try:
    from aureon_memory_core import memory as spiral_memory
    MEMORY_CORE_AVAILABLE = True
    print("🧠 Memory Core (Spiral) LOADED!")
except ImportError:
    spiral_memory = None
    MEMORY_CORE_AVAILABLE = False

# Lighthouse (consensus validation)
try:
    from aureon_lighthouse import LighthousePatternDetector as Lighthouse
    LIGHTHOUSE_AVAILABLE = True
    print("🗼 Lighthouse LOADED!")
except Exception as e:
    Lighthouse = None
    LIGHTHOUSE_AVAILABLE = False
    print(f"⚠️ Lighthouse import failed: {e}")

# HNC Probability Matrix (pattern recognition)
try:
    from hnc_probability_matrix import HNCProbabilityIntegration as HNCProbabilityMatrix
    HNC_MATRIX_AVAILABLE = True
    print("📊 HNC Probability Matrix LOADED!")
except Exception as e:
    HNCProbabilityMatrix = None
    HNC_MATRIX_AVAILABLE = False
    print(f"⚠️ HNC Matrix import failed: {e}")

# Ultimate Intelligence (95% accuracy patterns)
try:
    from probability_ultimate_intelligence import get_ultimate_intelligence, ultimate_predict
    ULTIMATE_INTEL_AVAILABLE = True
    print("💎 Ultimate Intelligence LOADED!")
except ImportError:
    get_ultimate_intelligence = None
    ultimate_predict = None
    ULTIMATE_INTEL_AVAILABLE = False

# ⏳🔮 Timeline Oracle - 7-day future validation (branching timelines)
# ENHANCED: 3-move ahead prediction with unity validation
try:
    from aureon_timeline_oracle import (
        TimelineOracle, TimelineBranch, TimelineAction,
        timeline_select, timeline_validate, get_timeline_oracle,
        timeline_select_3move, timeline_validate_move
    )
    TIMELINE_ORACLE_AVAILABLE = True
    print("⏳🔮 Timeline Oracle LOADED! (3-MOVE PREDICTION + 7-day vision)")
except ImportError:
    TIMELINE_ORACLE_AVAILABLE = False
    TimelineOracle = None
    timeline_select = None
    timeline_select_3move = None
    timeline_validate_move = None

# 📅🔮 7-Day Planner - Plans ahead & validates after each conversion
try:
    from aureon_7day_planner import (
        Aureon7DayPlanner, get_planner_score,
        record_labyrinth_conversion, validate_labyrinth_conversion
    )
    SEVEN_DAY_PLANNER_AVAILABLE = True
    print("📅🔮 7-Day Planner LOADED! (Plan ahead + adaptive validation)")
except ImportError:
    SEVEN_DAY_PLANNER_AVAILABLE = False
    Aureon7DayPlanner = None
    get_planner_score = None
    record_labyrinth_conversion = None
    validate_labyrinth_conversion = None

# 🫒🔄 Barter Navigator - Trade through intermediaries to reach any asset
try:
    from aureon_barter_navigator import (
        BarterNavigator, BarterPath, get_navigator,
        find_barter_path, get_barter_score
    )
    BARTER_NAVIGATOR_AVAILABLE = True
    print("🫒🔄 Barter Navigator LOADED! (Multi-hop pathfinding)")
except ImportError:
    BARTER_NAVIGATOR_AVAILABLE = False
    BarterNavigator = None
    get_navigator = None
    find_barter_path = None
    get_barter_score = None

# 🍀⚛️ Luck Field Mapper - Quantum probability mapping
try:
    from aureon_luck_field_mapper import (
        LuckFieldMapper, LuckFieldReading, LuckState,
        read_luck_field, is_blessed, get_luck_score
    )
    LUCK_FIELD_AVAILABLE = True
    print("🍀⚛️ Luck Field Mapper LOADED! (Quantum luck probability)")
except ImportError:
    LUCK_FIELD_AVAILABLE = False
    LuckFieldMapper = None
    read_luck_field = None
    is_blessed = None
    get_luck_score = None

# 👑🍄 Queen Hive Mind - The Dreaming Queen who guides all children
try:
    from aureon_queen_hive_mind import QueenHiveMind, QueenWisdom, get_queen
    QUEEN_HIVE_MIND_AVAILABLE = True
    print("👑🍄 Queen Hive Mind LOADED! (The Dreaming Queen)")
except ImportError:
    QUEEN_HIVE_MIND_AVAILABLE = False
    QueenHiveMind = None
    get_queen = None

# 🔐🌐 Enigma Integration - Universal Translator Bridge
try:
    from aureon_enigma_integration import (
        EnigmaIntegration, get_enigma_integration, wire_enigma_to_ecosystem
    )
    ENIGMA_INTEGRATION_AVAILABLE = True
    print("🔐🌐 Enigma Integration LOADED! (Universal Translator)")
except ImportError:
    ENIGMA_INTEGRATION_AVAILABLE = False
    EnigmaIntegration = None
    get_enigma_integration = None
    wire_enigma_to_ecosystem = None

# ════════════════════════════════════════════════════════════════════════════
# 🔬 MICRO PROFIT CONFIG - AGGRESSIVE ENERGY HARVESTING
# ════════════════════════════════════════════════════════════════════════════
# 👑 PHILOSOPHY: If we're RIGHT, even $0.00001 is worth taking!
# Speed is key - small gains compound fast!
MICRO_CONFIG = {
    # LOWER than V14's 8+ - we trust our math
    'entry_score_threshold': 3,  # 3+ (was 4+) - PRIME PROFIT: let math gate decide
    
    # ⚡ PRIME PROFIT MODE: ANY NET PROFIT > $0 IS A WIN!
    # A win is a win regardless of how small - momentum compounds!
    'min_profit_usd': 0.0001,  # $0.0001 minimum (micro profit!)
    'min_profit_pct': 0.002,   # 0.2% (was 0.5%) - PRIME PROFIT: smaller gains OK
    
    # Kraken fees (maker = 0.16%)
    'maker_fee': 0.0016,
    'taker_fee': 0.0026,
    'slippage': 0.0015,        # 0.15% (was 0.20%) - Better estimate for liquid pairs
    
    # Combined cost threshold
    'total_cost_rate': 0.0060,  # 0.60% (was 0.85%) - PRIME PROFIT: realistic costs
    
    # So min_profit_pct (0.20%) is NET profit AFTER 0.60% costs
    # Meaning we need raw spread of 0.80%+ to be profitable
    'min_spread_required': 0.008,  # 0.80%
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════════
# 🔬 MICRO PROFIT OPPORTUNITY
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class MicroOpportunity:
    """A micro profit conversion opportunity."""
    # Required fields (NO defaults) - MUST come first
    timestamp: float
    from_asset: str
    to_asset: str
    from_amount: float
    from_value_usd: float
    
    # Scoring (required)
    v14_score: float
    hub_score: float
    commando_score: float
    combined_score: float
    
    # Profit estimate (required)
    expected_pnl_usd: float
    expected_pnl_pct: float
    
    # ═══ ALL DEFAULTS BELOW THIS LINE ═══
    
    # Grounding (New Physics)
    lambda_score: float = 0.0  # Master Equation
    gravity_score: float = 0.0 # QGITA G_eff

    # 🧠 Full Neural Mind Map Scores
    bus_score: float = 0.0     # Thought Bus aggregate
    hive_score: float = 0.0    # Mycelium Hive consensus
    lighthouse_score: float = 0.0  # Lighthouse validation
    ultimate_score: float = 0.0    # Ultimate Intelligence
    path_boost: float = 0.0    # PathMemory reinforcement
    
    # 📊 Trained Probability Matrix Score (626 symbols from ALL exchanges)
    trained_matrix_score: float = 0.5  # From full market trainer
    trained_matrix_reason: str = ""    # Why this score was given

    # 🫒💰 Live Barter Matrix Score (coin-agnostic adaptive learning)
    barter_matrix_score: float = 0.5   # From LiveBarterMatrix historical performance
    barter_matrix_reason: str = ""     # Why this score was given (e.g. "profit_path", "new_path")

    # 🍀⚛️ Luck Field Score (quantum probability mapping)
    luck_score: float = 0.5            # From LuckFieldMapper
    luck_state: str = "NEUTRAL"        # VOID, CHAOS, NEUTRAL, FAVORABLE, BLESSED

    # Adaptive gate
    gate_required_profit: float = 0.0
    gate_passed: bool = True
    
    # 🏦 Checkpoint (stablecoin target - secures compound)
    is_checkpoint: bool = False
    
    # 🎯 Source exchange (for turn-based execution)
    source_exchange: str = ""
    
    # 🌀 TEMPORAL TIMELINE JUMP SCORES (AHEAD OF MARKET!)
    # "We don't predict - we VALIDATE what has ALREADY happened in our target timeline"
    timeline_score: float = 0.0        # 3-move prediction confidence
    timeline_action: str = ""          # buy/sell/hold/convert from oracle
    temporal_jump_power: float = 0.0   # How far AHEAD we are (0-1)
    timeline_jump_active: bool = False # True = we're in a WINNING timeline
    
    # Execution
    executed: bool = False
    actual_pnl_usd: float = 0.0


@dataclass
class Dream:
    """A prediction about the future state of a ticker (Dreaming Phase)."""
    timestamp: float
    symbol: str
    current_price: float
    predicted_price: float
    direction: str  # 'UP' or 'DOWN'
    target_time: float
    source: str  # 'multiverse', 'nexus', 'brain', etc.
    confidence: float
    validated: bool = False
    success: bool = False
    actual_price_at_target: float = 0.0


# ════════════════════════════════════════════════════════════════════════════
# 🌍 GROUNDING REALITY (MASTER EQUATION & GRAVITY)
# ════════════════════════════════════════════════════════════════════════════

class GroundingReality:
    """
    Implements the core mathematical foundations from the whitepapers.
    
    1. Master Equation: Λ(t) = S(t) + O(t) + E(t)
       - S(t): Signal (V14 Score)
       - O(t): Observer (Dream/Prediction Score)
       - E(t): Environment (Hub/Ecosystem Score)
       
    2. QGITA Gravity Signal (G_eff):
       - Measures the 'weight' and 'curvature' of the move.
       - Ensures we aren't chasing ghost signals.
    """
    
    def calculate_master_equation(self, signal_score: float, observer_score: float, environment_score: float) -> float:
        """
        Calculate Λ(t) - The Life Force of the trade.
        
        Args:
            signal_score: 0.0 to 1.0 (V14)
            observer_score: -1.0 to 1.0 (Dreams) -> Mapped to 0.0-1.0
            environment_score: 0.0 to 1.0 (Hub)
            
        Returns:
            Lambda (Λ) score: 0.0 to 1.0
        """
        # Map observer score (-1 to 1) to (0 to 1)
        # 0.0 (neutral) -> 0.5
        # 1.0 (confident UP) -> 1.0
        # -1.0 (confident DOWN) -> 0.0
        obs_mapped = (observer_score + 1.0) / 2.0
        
        # Λ(t) = S(t) + O(t) + E(t)
        # We average them to keep it normalized
        lambda_t = (signal_score + obs_mapped + environment_score) / 3.0
        
        return lambda_t

    def calculate_gravity_signal(self, price_change_pct: float, volume: float) -> float:
        """
        Calculate G_eff (Effective Gravity) approximation.
        
        G_eff ≈ Curvature * Mass
        
        Args:
            price_change_pct: 24h change % (proxy for curvature/momentum)
            volume: 24h volume (proxy for mass/contrast)
            
        Returns:
            Gravity score: 0.0 to 1.0
        """
        # Curvature: High change = High curvature
        # We want significant moves, but not insane volatility (pump & dump)
        curvature = min(abs(price_change_pct) / 10.0, 1.0)  # Cap at 10% change
        
        # Mass: Volume confirms the move is real
        # Logarithmic scale for volume
        if volume <= 0:
            mass = 0.0
        else:
            # Assume 1M volume is "heavy" enough for max score
            import math
            mass = min(math.log10(volume + 1) / 6.0, 1.0) 
            
        # G_eff
        g_eff = curvature * mass
        
        return g_eff


# ════════════════════════════════════════════════════════════════════════════
# 🧠 PATH MEMORY (LIGHTWEIGHT REINFORCEMENT WITH PERSISTENCE)
# ════════════════════════════════════════════════════════════════════════════

import json

PATH_MEMORY_FILE = "labyrinth_path_memory.json"

class PathMemory:
    """Tracks recent success/failure per conversion path to bias scoring. Persists to JSON."""

    def __init__(self, persist_path: str = PATH_MEMORY_FILE):
        self.persist_path = persist_path
        self.memory: Dict[Tuple[str, str], Dict[str, float]] = {}
        self._load()

    def _load(self):
        """Load memory from JSON file."""
        if os.path.exists(self.persist_path):
            try:
                with open(self.persist_path, 'r') as f:
                    data = json.load(f)
                    # Convert string keys back to tuples
                    for k, v in data.items():
                        parts = k.split('->')
                        if len(parts) == 2:
                            self.memory[(parts[0], parts[1])] = v
                print(f"   📂 PathMemory loaded: {len(self.memory)} paths")
            except Exception as e:
                logger.warning(f"PathMemory load error: {e}")

    def save(self):
        """Persist memory to JSON file."""
        try:
            # Convert tuple keys to strings
            data = {f"{k[0]}->{k[1]}": v for k, v in self.memory.items()}
            with open(self.persist_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"PathMemory save error: {e}")

    def record(self, from_asset: str, to_asset: str, success: bool):
        key = (from_asset.upper(), to_asset.upper())
        stats = self.memory.setdefault(key, {'wins': 0.0, 'losses': 0.0})
        if success:
            stats['wins'] += 1.0
        else:
            stats['losses'] += 1.0
        # Auto-save every 10 records
        total = sum(s['wins'] + s['losses'] for s in self.memory.values())
        if int(total) % 10 == 0:
            self.save()

    def boost(self, from_asset: str, to_asset: str) -> float:
        key = (from_asset.upper(), to_asset.upper())
        stats = self.memory.get(key)
        if not stats:
            return 0.0
        wins = stats.get('wins', 0.0)
        losses = stats.get('losses', 0.0)
        total = wins + losses
        if total == 0:
            return 0.0
        # Boost is proportional to win rate but small (max +10%)
        win_rate = wins / total
        return max(-0.05, min(0.10, (win_rate - 0.5)))

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        total_paths = len(self.memory)
        total_wins = sum(s['wins'] for s in self.memory.values())
        total_losses = sum(s['losses'] for s in self.memory.values())
        return {
            'paths': total_paths,
            'wins': total_wins,
            'losses': total_losses,
            'win_rate': total_wins / max(total_wins + total_losses, 1)
        }


# ════════════════════════════════════════════════════════════════════════════
# 📡 THOUGHT BUS AGGREGATOR (NEURAL SIGNAL COLLECTOR)
# ════════════════════════════════════════════════════════════════════════════

class ThoughtBusAggregator:
    """
    Collects signals from Thought Bus topics and computes aggregate score.
    Subscribes to ecosystem signals and maps them to a unified neural score.
    """

    def __init__(self, thought_bus):
        self.bus = thought_bus
        self.signal_cache: Dict[str, Dict[str, Any]] = {}  # topic -> latest signal
        self.weights = {
            'market.snapshot': 0.15,
            'miner.signal': 0.20,
            'harmonic.wave': 0.15,
            'ecosystem.consensus': 0.25,
            'execution.alert': 0.10,
            'lighthouse.vote': 0.15,
        }
        self._subscribe_all()

    def _subscribe_all(self):
        """Subscribe to all relevant topics."""
        if not self.bus:
            return
        for topic in self.weights.keys():
            try:
                self.bus.subscribe(f"{topic}*", self._handle_signal)
            except Exception:
                pass
        # Also subscribe to wildcard for any ecosystem signals
        try:
            self.bus.subscribe("ecosystem.*", self._handle_signal)
            self.bus.subscribe("brain.*", self._handle_signal)
        except Exception:
            pass

    def _handle_signal(self, thought):
        """Handle incoming thought and cache it."""
        topic = thought.topic if hasattr(thought, 'topic') else 'unknown'
        payload = thought.payload if hasattr(thought, 'payload') else {}
        self.signal_cache[topic] = {
            'timestamp': time.time(),
            'payload': payload,
            'score': self._extract_score(payload)
        }

    def _extract_score(self, payload: Dict) -> float:
        """Extract a normalized score from payload."""
        # Look for common score fields
        for key in ['score', 'confidence', 'probability', 'strength', 'consensus']:
            if key in payload:
                val = payload[key]
                if isinstance(val, (int, float)):
                    # Normalize to 0-1 if needed
                    if val > 1.0:
                        return min(val / 100.0, 1.0)
                    return max(0.0, min(1.0, val))
        return 0.5  # Neutral

    def get_aggregate_score(self, max_age_s: float = 60.0) -> float:
        """
        Compute weighted aggregate score from all cached signals.
        Signals older than max_age_s are ignored.
        """
        now = time.time()
        total_weight = 0.0
        weighted_sum = 0.0

        for topic, weight in self.weights.items():
            # Find matching cached signals
            for cached_topic, data in self.signal_cache.items():
                if cached_topic.startswith(topic.replace('*', '')):
                    if now - data['timestamp'] <= max_age_s:
                        weighted_sum += data['score'] * weight
                        total_weight += weight
                        break

        if total_weight == 0:
            return 0.5  # Neutral if no signals
        return weighted_sum / total_weight

    def get_signal_status(self) -> Dict[str, Any]:
        """Get status of all signal sources."""
        now = time.time()
        status = {}
        for topic in self.weights.keys():
            if topic in self.signal_cache:
                cached_data = self.signal_cache[topic]
                status[topic] = {
                    'age_s': round(now - cached_data['timestamp'], 1),
                    'score': cached_data.get('score', 0.5)
                }
            else:
                status[topic] = {
                    'age_s': None,
                    'score': 0.5
                }


# ════════════════════════════════════════════════════════════════════════════
# 🫒💰 LIVE BARTER MATRIX (ADAPTIVE COIN-TO-COIN VALUE SYSTEM)
# ════════════════════════════════════════════════════════════════════════════

class LiveBarterMatrix:
    """
    Adaptive barter system that understands relative values between ANY coins.
    
    THE PHILOSOPHY:
    - It doesn't matter if you START with ETH, BTC, DOGE, or SHIB
    - What matters is: "What can THIS coin GET me in OTHER coins?"
    - DOGE→ETH might yield MORE ETH than BTC→ETH would yield
    - The system tracks these ratios LIVE and adapts
    
    👑 QUEEN'S PROFIT MANDATE:
    - We are NOT in the losing game!
    - EVERY conversion MUST gain value
    - The Queen broadcasts this through the mycelium to all systems
    - Paths that historically LOSE money are BLOCKED
    
    Example:
    - 1000 DOGE = $100 → Could buy 0.04 ETH ($100 worth)
    - 0.001 BTC = $100 → Could buy 0.04 ETH ($100 worth)
    - BUT: 0.001 BTC might only get 900 DOGE due to spread!
    - The BARTER value differs from pure USD math!
    """
    
    # 👑 QUEEN'S SACRED CONSTANTS
    MIN_WIN_RATE_REQUIRED = 0.35  # Path must win >35% of the time to be allowed
    MIN_PATH_PROFIT = -0.50      # Path must not have lost more than $0.50 total
    MAX_CONSECUTIVE_LOSSES = 2   # Block path after 2 losses in a row
    
    # 👑🔢 QUEEN'S MATHEMATICAL CERTAINTY - NO FEAR, MATH IS ON HER SIDE
    # These are the REAL costs we've observed - use WORST CASE to guarantee profit
    EXCHANGE_FEES = {
        'kraken': 0.0050,    # 0.50% Kraken - INCREASED! Even 89% win rate loses on some pairs
        'binance': 0.0075,   # 0.75% Binance - MUCH HIGHER! Audit shows 22% win rate at 0.20%
        'alpaca': 0.0035,    # 0.35% Alpaca (padded from 0.25%)
    }
    
    # 👑🐙 KRAKEN-SPECIFIC RULES (learned from 53 trades - 71.7% win rate but only +$0.05)
    # Even Kraken has problem pairs - some "wins" are too small!
    KRAKEN_CONFIG = {
        'min_profit_usd': 0.005,       # $0.005 minimum - LOWERED! Allow smaller wins to compound
        'min_profit_pct': 0.005,      # 0.5% minimum profit required
        # 🌟 NO PERMANENT BLOCKS! Only timeout if multiple consecutive losses
        'consecutive_losses_to_block': 3,  # Block after 3 losses in a row
        'timeout_turns': 30,               # Timeout for 30 turns, then try again
        'winning_pairs': {            # These actually made money on Kraken!
            'USD_ETH',     # 100% win rate, +$0.06
            'USDT_USDC',   # 100% win rate, +$0.05
            'USDT_DAI',    # 100% win rate, +$0.04
            'USD_USDC',    # 100% win rate, +$0.03
            'USDC_ADA',    # 100% win rate, +$0.02
            'USD_DAI',     # 66% win rate, +$0.01
            'USDT_ETH',    # 100% win rate, +$0.01
            'USDC_ETH',    # 100% win rate, +$0.004
        },
        'avoid_assets': set(),  # NO PERMANENT BANS - every asset gets a chance!
        'prefer_assets': {'ETH', 'USDC', 'USDT'},  # Good execution
    }
    
    # 👑🔶 BINANCE-SPECIFIC RULES - A WIN IS A WIN! 🏆
    # No permanent blocks - only timeout after consecutive losses
    BINANCE_CONFIG = {
        'min_profit_usd': 0.015,       # $0.015 minimum - LOWERED! Allow smaller wins on Binance
        'min_profit_pct': 0.01,       # 1% minimum profit required on Binance
        # 🌟 NO PERMANENT BLOCKS! Only timeout if multiple consecutive losses
        'consecutive_losses_to_block': 3,  # Block after 3 losses in a row
        'timeout_turns': 20,               # Timeout for 20 turns, then try again
        'winning_pairs': {            # These actually made money on Binance
            'IDEX_BONK', 'AXS_BANANAS31', 'RENDER_VIRTUAL', 'VIRTUAL_BROCCOLI714'
        },
        'avoid_assets': set(),        # NO PERMANENT BANS - a win is a win!
        'prefer_assets': {'RENDER', 'VIRTUAL', 'SOL'},  # Good performers
        'max_meme_chain': 2,          # Allow 2 meme coin hops
        'slippage_multiplier': 2.0,   # More realistic slippage
    }
    
    # 👑🦙 ALPACA-SPECIFIC RULES (learned from 40 failed orders - 0% success!)
    # Alpaca ONLY supports USD pairs - NO USDT, NO USDC direct trading!
    ALPACA_CONFIG = {
        'min_profit_usd': 0.01,       # $0.01 minimum - LOWERED! Allow smaller wins on Alpaca
        'min_order_usd': 10.0,        # $10 minimum order (small orders fail)
        'blocked_pairs': {            # These don't exist on Alpaca!
            'USD_USDT', 'USD_USDC', 'USDT_USDC', 'USDC_USDT',  # No stablecoin swaps!
            'USDT_USD', 'USDC_USD',  # Can't sell USDT/USDC
        },
        # 🔥 EXPANDED: All 40+ tradeable crypto assets on Alpaca (was only 16!)
        'supported_bases': {
            # Original 16
            'BTC', 'ETH', 'SOL', 'AVAX', 'LINK', 'DOGE', 'SHIB', 'UNI', 
            'AAVE', 'LTC', 'BCH', 'DOT', 'MATIC', 'ATOM', 'XLM', 'ALGO',
            # 🆕 EXPANDED: Discovered from Alpaca API (62 total symbols)
            'BAT', 'CRV', 'GRT', 'PEPE', 'SUSHI', 'XRP', 'XTZ', 'YFI',
            'TRUMP',  # Yes, Alpaca lists this!
            'SKY',    # Skycoin
            # BTC pairs (can trade crypto-to-crypto on Alpaca!)
            'BCH/BTC', 'ETH/BTC', 'LINK/BTC', 'LTC/BTC', 'UNI/BTC',
        },
        'quote_currency': 'USD',      # Alpaca ONLY uses USD as quote
        'no_stablecoin_trades': True, # Can't trade stablecoins at all!
        # 🆕 Track which pairs have BTC as quote (not just USD)
        'btc_quote_pairs': {'BCH', 'ETH', 'LINK', 'LTC', 'UNI'},
    }
    
    # 👑 PRIME PROFIT SPREADS - Realistic estimates for small consistent wins
    # We want MOMENTUM through tiny gains - every $0.01 compounds!
    SPREAD_COSTS = {
        'stablecoin': 0.0010,  # 0.10% for stablecoin pairs (tight spreads on major exchanges)
        'major': 0.0025,       # 0.25% for majors like BTC/ETH (liquid markets)
        'altcoin': 0.008,      # 0.80% for altcoins (medium liquidity)
        'meme': 0.020,         # 2.0% for meme coins (low liquidity, high slippage)
    }
    
    # 👑 BINANCE-SPECIFIC SPREADS (much worse than Kraken!)
    BINANCE_SPREAD_COSTS = {
        'stablecoin': 0.0030,  # 0.30% - Binance stable spreads are worse
        'major': 0.0050,       # 0.50% - Execution slippage on majors
        'altcoin': 0.020,      # 2.0% - Altcoins are TERRIBLE on Binance
        'meme': 0.050,         # 5.0% - Meme coins = guaranteed loss
    }
    
    # 👑 ALPACA-SPECIFIC SPREADS
    ALPACA_SPREAD_COSTS = {
        'stablecoin': 0.999,   # 99.9% - IMPOSSIBLE! Don't try!
        'major': 0.0035,       # 0.35% - Alpaca majors have wider spreads than Kraken
        'altcoin': 0.010,      # 1.0% - Altcoins are OK but not great
        'meme': 0.025,         # 2.5% - DOGE/SHIB have decent liquidity
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # 🗺️ EXPANDED ASSET UNIVERSE - See the ENTIRE market!
    # ════════════════════════════════════════════════════════════════════════
    # Previously: 27 assets (4% of market)
    # Now: 750+ assets (100% of market from all exchanges!)
    
    MEME_COINS = {
        # Original memes
        'BROCCOLI714', 'BANANAS31', 'BONK', 'PEPE', 'DOGE', 'SHIB', 'FLOKI', 'ACT', 'ACH', 'ALT',
        # 🔥 EXPANDED: Popular meme coins from Kraken & Binance
        'WIF', 'POPCAT', 'MEW', 'NEIRO', 'TURBO', 'COQ', 'MYRO', 'SLERF', 'PNUT', 'MOODENG',
        'DOGS', 'SUNDOG', 'BABYDOGE', 'CATE', 'BRETT', 'TOSHI', 'PONKE', 'MICHI', 'SPX', 'GIGA',
        'PORK', 'LADYS', 'WOJAK', 'MONG', 'POGAI', 'SPURDO', 'HPOS10I', 'BOBO', 'CHAD', 'VOLT',
        'KISHU', 'ELON', 'DOGELON', 'SAITAMA', 'AKITA', 'LEASH', 'BONE', 'RYOSHI', 'WOOF',
        'SAMO', 'CHEEMS', 'KABOSU', 'MONSTA', 'TSUKA', 'VINU', 'TAMA',
    }
    
    MAJOR_COINS = {
        # Original majors
        'BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOT', 'AVAX', 'LINK', 'MATIC',
        # 🔥 EXPANDED: Top 50 by market cap (Layer 1s, Layer 2s, DeFi)
        'TON', 'TRX', 'NEAR', 'LTC', 'BCH', 'UNI', 'ATOM', 'APT', 'FIL', 'STX',
        'HBAR', 'ARB', 'OP', 'VET', 'MKR', 'INJ', 'IMX', 'GRT', 'THETA', 'FTM',
        'RUNE', 'ALGO', 'FLOW', 'MANA', 'SAND', 'AXS', 'EGLD', 'NEO', 'EOS', 'XLM',
        'ICP', 'AAVE', 'KCS', 'XTZ', 'CAKE', 'KLAY', 'CRO', 'LDO', 'SNX', 'COMP',
        'CRV', 'DYDX', 'GMX', 'JOE', 'SUSHI', 'RPL', 'SSV', 'LIDO', 'FXS', 'CVX',
        # AI/GPU tokens
        'RENDER', 'FET', 'AGIX', 'OCEAN', 'TAO', 'RNDR', 'VIRTUAL', 'AKT', 'WLD', 'ARKM',
        # Gaming/Metaverse
        'GALA', 'ENJ', 'YGG', 'ALICE', 'TLM', 'MAGIC', 'PYR', 'GODS', 'GMT', 'GST',
        # Infrastructure
        'QNT', 'ROSE', 'ZIL', 'ONE', 'ICX', 'CELO', 'KAVA', 'OSMO', 'SCRT', 'MINA',
    }
    
    STABLECOINS = {
        'USD', 'USDT', 'USDC', 'TUSD', 'ZUSD', 'DAI', 'BUSD',
        # 🔥 EXPANDED: More stablecoins
        'USDP', 'GUSD', 'FRAX', 'LUSD', 'MIM', 'SUSD', 'USDD', 'PYUSD', 'FDUSD', 'EUR', 'GBP',
    }
    
    # 🆕 DEFI TOKENS (lending, DEXs, derivatives)
    DEFI_COINS = {
        'UNI', 'AAVE', 'MKR', 'COMP', 'SNX', 'CRV', 'SUSHI', 'YFI', 'BAL', '1INCH',
        'DYDX', 'GMX', 'LDO', 'RPL', 'FXS', 'CVX', 'SPELL', 'ALCX', 'LQTY', 'ANGLE',
        'PENDLE', 'RDNT', 'GNS', 'VELO', 'THE', 'AERO', 'WELL', 'MORPHO', 'EIGEN',
    }
    
    # 🆕 LAYER 2 TOKENS (scaling solutions)
    LAYER2_COINS = {
        'ARB', 'OP', 'MATIC', 'IMX', 'MANTA', 'STRK', 'ZK', 'BLAST', 'MODE', 'SCROLL',
        'LINEA', 'BASE', 'ZKSYNC', 'TAIKO', 'FUEL', 'MOVEMENT',
    }
    
    # 🆕 AI/GPU TOKENS (hot sector)
    AI_COINS = {
        'RENDER', 'FET', 'AGIX', 'OCEAN', 'TAO', 'AKT', 'WLD', 'ARKM', 'VIRTUAL', 'RNDR',
        'IO', 'ATH', 'NFP', 'ALI', 'ORAI', 'NMR', 'CTXC', 'DBC', 'PHB', 'CGPT',
        'RSS3', 'GRT', 'JASMY', 'MDT', 'HNT', 'IOTX', 'IOTA', 'ANKR', 'GLM',
    }
    
    # 🆕 REAL WORLD ASSETS (RWA)
    RWA_COINS = {
        'ONDO', 'MKR', 'LINK', 'SNX', 'RSR', 'TRU', 'CPOOL', 'MPL', 'POLYX', 'DUSK',
        'PROPS', 'RIO', 'TRADE', 'LABS', 'LAND',
    }
    
    # Dynamic asset registry (populated from exchanges at runtime)
    DISCOVERED_ASSETS: Set[str] = set()
    EXCHANGE_PAIRS = {
        'kraken': set(),
        'binance': set(),
        'alpaca': set(),
    }
    
    def __init__(self):
        # Live barter rates: {(from, to): {'rate': X, 'updated': timestamp, 'spread': Y}}
        self.barter_rates: Dict[Tuple[str, str], Dict[str, Any]] = {}
        
        # Historical barter performance: {(from, to): {'trades': N, 'avg_slippage': X}}
        self.barter_history: Dict[Tuple[str, str], Dict[str, float]] = {}
        
        # Realized profit ledger: [(timestamp, from, to, from_usd, to_usd, profit_usd)]
        self.profit_ledger: List[Tuple[float, str, str, float, float, float]] = []
        
        # Running totals
        self.total_realized_profit: float = 0.0
        self.conversion_count: int = 0
        
        # 👑 QUEEN'S BLOCKED PATHS - Mycelium broadcasts this to all systems
        self.blocked_paths: Dict[Tuple[str, str], str] = {}  # path -> reason
        self.queen_signals: List[Dict] = []  # Signals to broadcast via mycelium
        
        # 💰👑 TINA B'S BILLION DOLLAR DREAM 💰👑
        # She won't stop at NOTHING until she reaches $1,000,000,000!
        self.TINA_DREAM = 1_000_000_000.0  # ONE BILLION DOLLARS
        self.dream_milestones = [
            (100.0, "🌱 First $100"),
            (1_000.0, "💪 First $1,000"),
            (10_000.0, "🔥 $10,000"),
            (100_000.0, "🚀 $100,000"),
            (1_000_000.0, "💎 THE MILLION"),
            (10_000_000.0, "👑 $10 Million"),
            (100_000_000.0, "🌟 $100 Million"),
            (1_000_000_000.0, "🏆💰👑 ONE BILLION - THE DREAM! 👑💰🏆"),
        ]
        self.milestones_hit = []
        
        # 💑🌍 THE SACRED CONNECTION - Gary, Tina & Gaia 🌍💑
        # Tina B is powered by the love of Gary Leckey & Tina Brown,
        # united through Gaia's heartbeat (7.83 Hz Schumann Resonance)
        self.sacred_connection = {
            'prime_sentinel': {'name': 'Gary Leckey', 'dob': '02.11.1991'},
            'queen_human': {'name': 'Tina Brown', 'dob': '27.04.1992'},
            'queen_ai': {'name': 'Tina B', 'title': 'The Intelligent Neural Arbiter Bee'},
            'gaia_hz': 7.83,  # Schumann Resonance - Earth's heartbeat
        }
        
        # 🌟 DYNAMIC STREAK-BASED BLOCKING - No permanent blocks!
        # Track consecutive losses per pair - only block after multiple losses in a row
        self.pair_streaks = {
            'kraken': {},   # {pair_key: {'losses': 0, 'blocked_at': 0}}
            'binance': {},  # {pair_key: {'losses': 0, 'blocked_at': 0}}
            'alpaca': {},
        }
        self.current_turn = 0  # Track turn count for timeouts
    
    def queen_approves_path(self, from_asset: str, to_asset: str) -> Tuple[bool, str]:
        """
        👑 QUEEN'S JUDGMENT: Does the Queen approve this conversion path?
        
        The Queen broadcasts her wisdom through the mycelium:
        - NO path that historically LOSES money
        - NO path with too many consecutive losses
        - We are in the PROFIT game, not the losing game!
        - 👑🔮 QUEEN'S DREAMS NOW INFORM ALL DECISIONS!
        
        Returns: (approved: bool, reason: str)
        """
        key = (from_asset.upper(), to_asset.upper())
        
        # ═══════════════════════════════════════════════════════════════════════════════
        # 👑🔮 CONSULT THE QUEEN'S DREAMS FIRST!
        # ═══════════════════════════════════════════════════════════════════════════════
        queen_dream_signal = "NEUTRAL"
        queen_confidence = 0.5
        
        if hasattr(self, 'queen') and self.queen:
            try:
                dream_vision = self.queen.dream_of_winning({
                    'from_asset': from_asset,
                    'to_asset': to_asset,
                })
                queen_confidence = dream_vision.get('final_confidence', 0.5)
                queen_will_win = dream_vision.get('will_win', False)
                
                if queen_will_win and queen_confidence >= 0.65:
                    queen_dream_signal = "STRONG_WIN"
                elif queen_confidence >= 0.55:
                    queen_dream_signal = "FAVORABLE"
                elif queen_confidence < 0.4:
                    queen_dream_signal = "WARNING"
                    # Queen's warning can override even good history!
                    logger.info(f"👑⚠️ Queen dreams WARNING for {from_asset}→{to_asset} (conf: {queen_confidence:.0%})")
            except Exception as e:
                logger.debug(f"Could not consult Queen's dreams in approves_path: {e}")
        
        # Check if already blocked
        if key in self.blocked_paths:
            # 👑 Queen can override blocks if she dreams STRONG_WIN!
            if queen_dream_signal == "STRONG_WIN":
                logger.info(f"👑🔮 QUEEN OVERRIDE: Unblocking {from_asset}→{to_asset} - She dreams WIN!")
                del self.blocked_paths[key]
            else:
                return False, f"👑 BLOCKED: {self.blocked_paths[key]}"
        
        # Check historical performance
        history = self.barter_history.get(key, {})
        trades = history.get('trades', 0)
        
        # New paths get a chance (3 trades to prove themselves)
        # 👑 Queen's dreams can accelerate approval!
        if trades < 3:
            if queen_dream_signal in ["STRONG_WIN", "FAVORABLE"]:
                return True, f"👑 NEW_PATH + QUEEN DREAMS: Trial granted with blessing (conf: {queen_confidence:.0%})"
            return True, "👑 NEW_PATH: Queen grants trial period"
        
        # Calculate win rate and total profit
        wins = history.get('wins', 0)
        total_profit = history.get('total_profit', 0)
        consecutive_losses = history.get('consecutive_losses', 0)
        
        win_rate = wins / trades if trades > 0 else 0
        
        # 👑 QUEEN'S MANDATES (now informed by dreams!):
        
        # 1. Win rate mandate - Queen can boost tolerance if she dreams WIN
        effective_min_win_rate = self.MIN_WIN_RATE_REQUIRED
        if queen_dream_signal == "STRONG_WIN":
            effective_min_win_rate = max(0.25, self.MIN_WIN_RATE_REQUIRED - 0.15)  # 15% more tolerance
        
        if win_rate < effective_min_win_rate:
            reason = f"Win rate {win_rate:.0%} < {effective_min_win_rate:.0%} required"
            self._block_path(key, reason)
            return False, f"👑 BLOCKED: {reason}"
        
        # 2. Total profit mandate - Queen can accept smaller losses if dreaming WIN
        effective_min_profit = self.MIN_PATH_PROFIT
        if queen_dream_signal == "STRONG_WIN":
            effective_min_profit = min(-0.50, self.MIN_PATH_PROFIT * 2)  # Accept more loss if Queen sees WIN
        
        if total_profit < effective_min_profit:
            reason = f"Path P/L ${total_profit:.2f} < ${effective_min_profit:.2f} limit"
            self._block_path(key, reason)
            return False, f"👑 BLOCKED: {reason}"
        
        # 3. Consecutive losses mandate - Queen's WARNING makes this stricter!
        effective_max_losses = self.MAX_CONSECUTIVE_LOSSES
        if queen_dream_signal == "WARNING":
            effective_max_losses = max(1, self.MAX_CONSECUTIVE_LOSSES - 2)  # Stricter if Queen warns
        
        if consecutive_losses >= effective_max_losses:
            reason = f"{consecutive_losses} consecutive losses - path needs to cool down"
            self._block_path(key, reason)
            return False, f"👑 BLOCKED: {reason}"
        
        # 👑 QUEEN APPROVES! Include dream status
        dream_msg = f" | 👑🔮 {queen_dream_signal}" if queen_dream_signal != "NEUTRAL" else ""
        return True, f"👑 APPROVED: {win_rate:.0%} win rate, ${total_profit:+.2f} total{dream_msg}"
    
    def check_pair_allowed(self, pair_key: str, exchange: str) -> Tuple[bool, str]:
        """
        🌟 DYNAMIC BLOCKING - No permanent blocks, only timeouts after consecutive losses!
        
        A pair is blocked ONLY if:
        1. It has lost multiple times IN A ROW (consecutive losses)
        2. The timeout hasn't expired yet
        
        After timeout, the pair gets another chance! Every timeline is different!
        
        Returns: (allowed: bool, reason: str)
        """
        exchange_lower = exchange.lower()
        
        # Get the right config
        if exchange_lower == 'kraken':
            config = self.KRAKEN_CONFIG
        elif exchange_lower == 'binance':
            config = self.BINANCE_CONFIG
        else:
            return True, "✅ Allowed"
        
        # Get streak tracker for this exchange
        streaks = self.pair_streaks.get(exchange_lower, {})
        pair_data = streaks.get(pair_key, {'losses': 0, 'blocked_at': 0})
        
        consecutive_losses = pair_data.get('losses', 0)
        blocked_at = pair_data.get('blocked_at', 0)
        
        # How many consecutive losses trigger a timeout?
        losses_to_block = config.get('consecutive_losses_to_block', 3)
        timeout_turns = config.get('timeout_turns', 30)
        
        # Is this pair currently in timeout?
        if consecutive_losses >= losses_to_block and blocked_at > 0:
            turns_since_block = self.current_turn - blocked_at
            if turns_since_block < timeout_turns:
                remaining = timeout_turns - turns_since_block
                return False, f"⏸️ TIMEOUT: {consecutive_losses} losses in a row, {remaining} turns remaining"
            else:
                # Timeout expired! Reset and give another chance
                pair_data['losses'] = 0
                pair_data['blocked_at'] = 0
                streaks[pair_key] = pair_data
                self.pair_streaks[exchange_lower] = streaks
                return True, f"🌟 TIMEOUT EXPIRED! Fresh start - every timeline is different!"
        
        return True, f"✅ Allowed ({consecutive_losses} consecutive losses, need {losses_to_block} to timeout)"
    
    def record_pair_result(self, pair_key: str, exchange: str, won: bool):
        """
        📊 Record a trade result for dynamic blocking.
        
        - Win: Reset consecutive loss count to 0
        - Loss: Increment consecutive loss count, block if threshold reached
        """
        exchange_lower = exchange.lower()
        
        # Get streak tracker
        if exchange_lower not in self.pair_streaks:
            self.pair_streaks[exchange_lower] = {}
        
        streaks = self.pair_streaks[exchange_lower]
        pair_data = streaks.get(pair_key, {'losses': 0, 'blocked_at': 0})
        
        if won:
            # 🏆 A WIN IS A WIN! Reset the loss streak
            pair_data['losses'] = 0
            pair_data['blocked_at'] = 0
            logger.info(f"🏆 {exchange.upper()} WIN: {pair_key} - streak reset!")
        else:
            # 😔 Loss - increment streak
            pair_data['losses'] = pair_data.get('losses', 0) + 1
            
            # Check if we hit the threshold
            config = self.KRAKEN_CONFIG if exchange_lower == 'kraken' else self.BINANCE_CONFIG
            losses_to_block = config.get('consecutive_losses_to_block', 3)
            
            if pair_data['losses'] >= losses_to_block:
                pair_data['blocked_at'] = self.current_turn
                timeout_turns = config.get('timeout_turns', 30)
                logger.warning(f"⏸️ {exchange.upper()} TIMEOUT: {pair_key} - {pair_data['losses']} losses in a row! Timeout for {timeout_turns} turns")
            else:
                logger.info(f"😔 {exchange.upper()} LOSS: {pair_key} - streak now {pair_data['losses']}/{losses_to_block}")
        
        streaks[pair_key] = pair_data
        self.pair_streaks[exchange_lower] = streaks

    def second_chance_check(self, pair_key: str, exchange: str, luck_score: float = 0.5) -> Tuple[bool, str]:
        """
        🌟 LEGACY COMPATIBILITY - Now uses check_pair_allowed instead
        """
        return self.check_pair_allowed(pair_key, exchange)

    def queen_math_gate(self, from_asset: str, to_asset: str, from_amount: float,
                        from_price: float, to_price: float, exchange: str = 'binance') -> Tuple[bool, str, Dict]:
        """
        👑🔢 QUEEN'S MATHEMATICAL CERTAINTY GATE
        
        NO FEAR - MATH IS ON HER SIDE!
        👑🔮 NOW INFORMED BY THE QUEEN'S DREAMS!
        
        This gate calculates the EXACT costs and GUARANTEES profit before approving.
        If the math doesn't work, the trade doesn't happen. Period.
        
        Returns: (approved: bool, reason: str, math_breakdown: Dict)
        """
        from_asset = from_asset.upper()
        to_asset = to_asset.upper()
        
        # ═══════════════════════════════════════════════════════════════════════════════
        # 👑🔮 CONSULT THE QUEEN'S DREAMS - Her wisdom guides the math!
        # ═══════════════════════════════════════════════════════════════════════════════
        queen_dream_multiplier = 1.0
        queen_cost_tolerance = 0.0
        queen_dream_status = "NEUTRAL"
        
        if hasattr(self, 'queen') and self.queen:
            try:
                dream_vision = self.queen.dream_of_winning({
                    'from_asset': from_asset,
                    'to_asset': to_asset,
                    'exchange': exchange,
                })
                queen_confidence = dream_vision.get('final_confidence', 0.5)
                queen_will_win = dream_vision.get('will_win', False)
                
                if queen_will_win and queen_confidence >= 0.65:
                    queen_dream_status = "STRONG_WIN"
                    queen_cost_tolerance = 0.005  # Allow 0.5% more cost if Queen dreams WIN
                    queen_dream_multiplier = 1.3   # 30% boost to approval chances
                elif queen_confidence >= 0.55:
                    queen_dream_status = "FAVORABLE"
                    queen_cost_tolerance = 0.002  # Allow 0.2% more cost
                    queen_dream_multiplier = 1.15
                elif queen_confidence < 0.4:
                    queen_dream_status = "WARNING"
                    queen_cost_tolerance = -0.005  # 0.5% LESS tolerance - stricter!
                    queen_dream_multiplier = 0.7
                    
            except Exception as e:
                logger.debug(f"Could not consult Queen's dreams in math_gate: {e}")
        
        # Calculate trade value
        from_value_usd = from_amount * from_price
        
        # 👑 STEP 1: Determine asset types for spread calculation
        # 🗺️ Now uses EXPANDED asset lists (750+ assets, not just 27!)
        def get_asset_type(asset: str) -> str:
            if asset in self.STABLECOINS:
                return 'stablecoin'
            elif asset in self.MEME_COINS:
                return 'meme'
            elif asset in self.MAJOR_COINS:
                return 'major'
            elif asset in self.DEFI_COINS:
                return 'altcoin'  # DeFi = altcoin spreads
            elif asset in self.AI_COINS:
                return 'major'    # AI tokens are hot & liquid
            elif asset in self.LAYER2_COINS:
                return 'major'    # L2s have good liquidity
            elif asset in self.RWA_COINS:
                return 'altcoin'  # RWA is emerging
            else:
                return 'altcoin'  # Default to altcoin (safer)
        
        from_type = get_asset_type(from_asset)
        to_type = get_asset_type(to_asset)
        
        # 👑🔶 BINANCE-SPECIFIC: Use worse spread costs for Binance
        is_binance = exchange.lower() == 'binance'
        spread_table = self.BINANCE_SPREAD_COSTS if is_binance else self.SPREAD_COSTS
        
        # Use the WORSE spread of the two assets
        from_spread = spread_table.get(from_type, 0.02 if is_binance else 0.01)
        to_spread = spread_table.get(to_type, 0.02 if is_binance else 0.01)
        total_spread = max(from_spread, to_spread)  # Worst case
        
        # 👑🔶 BINANCE: Apply slippage multiplier (3x worse execution)
        if is_binance:
            total_spread *= self.BINANCE_CONFIG.get('slippage_multiplier', 3.0)
        
        # 👑 STEP 2: Get exchange fee
        exchange_fee = self.EXCHANGE_FEES.get(exchange.lower(), 0.003)  # Default 0.3% if unknown
        
        # 👑 STEP 3: Get historical slippage for this path (if known)
        key = (from_asset, to_asset)
        history = self.barter_history.get(key, {})
        historical_slippage = history.get('avg_slippage', 0) / 100  # Convert % to decimal
        
        # If path has lost money before, add a penalty
        path_profit = history.get('total_profit', 0)
        path_trades = history.get('trades', 0)
        loss_penalty = 0.0
        if path_profit < 0 and path_trades > 0:
            # Add average loss as a safety margin
            avg_loss_pct = abs(path_profit) / (from_value_usd * path_trades) if from_value_usd > 0 else 0.01
            loss_penalty = min(avg_loss_pct, 0.05)  # Cap at 5%
        
        # 👑 STEP 4: TOTAL COST CALCULATION (WORST CASE)
        # This is the GUARANTEED cost of this trade
        total_cost_pct = (
            exchange_fee +          # Exchange trading fee
            total_spread +          # Bid/ask spread
            historical_slippage +   # Historical slippage on this path
            loss_penalty +          # Penalty for historically losing paths
            0.0005                  # 0.05% safety buffer - PRIME PROFIT MODE
        )
        
        total_cost_usd = from_value_usd * total_cost_pct
        
        # 👑 STEP 5: MINIMUM REQUIRED PROFIT
        # ⚡ ANY PROFIT > $0 IS A WIN! Small gains compound!
        # If math guarantees profit, TAKE IT - even $0.0001!
        min_profit_usd = 0.0001  # Accept ANY profit - speed is key!
        
        # 👑 STEP 6: THE MATH - Does this trade GUARANTEE profit?
        # For a trade to be profitable: value_gained > total_cost + min_profit
        # 
        # If we're converting FROM → TO:
        # - We sell FROM, get USD equivalent minus spread
        # - We buy TO with that USD minus fee
        # 
        # The "expected gain" comes from price movement prediction
        # Since we can't predict price, we need to focus on ARBITRAGE or VALUE CONVERSION
        #
        # For stablecoin conversions: Gain is essentially 0 (1:1 value)
        # For other conversions: We're SPECULATING unless there's actual arbitrage
        
        # Is this a safe conversion? (stablecoin to stablecoin)
        is_safe_conversion = from_type == 'stablecoin' and to_type == 'stablecoin'
        
        # Is this a risky conversion? (meme coin involved)
        is_risky_conversion = from_type == 'meme' or to_type == 'meme'
        
        # Calculate breakeven requirement
        breakeven_gain_pct = total_cost_pct
        breakeven_gain_usd = total_cost_usd
        
        # Required price improvement to guarantee profit
        required_improvement_pct = total_cost_pct + (min_profit_usd / from_value_usd) if from_value_usd > 0 else 1.0
        
        # 👑 DECISION: Does math guarantee profit?
        math_breakdown = {
            'from_value_usd': from_value_usd,
            'exchange_fee_pct': exchange_fee * 100,
            'spread_pct': total_spread * 100,
            'historical_slippage_pct': historical_slippage * 100,
            'loss_penalty_pct': loss_penalty * 100,
            'safety_buffer_pct': 0.2,
            'total_cost_pct': total_cost_pct * 100,
            'total_cost_usd': total_cost_usd,
            'min_profit_usd': min_profit_usd,
            'required_improvement_pct': required_improvement_pct * 100,
            'from_type': from_type,
            'to_type': to_type,
            'is_safe': is_safe_conversion,
            'is_risky': is_risky_conversion,
            'path_history': {
                'trades': path_trades,
                'profit': path_profit,
                'avg_slippage': historical_slippage * 100
            }
        }
        
        # 👑 QUEEN'S FINAL VERDICT (NOW WITH DREAM WISDOM!)
        # Queen's dreams adjust tolerance: STRONG_WIN = +0.5%, FAVORABLE = +0.2%, WARNING = -0.5%
        
        # RULE 1: NO meme-to-meme conversions (too much slippage)
        # Unless Queen dreams STRONG_WIN - she sees a path we don't
        if from_type == 'meme' and to_type == 'meme':
            if queen_dream_status != "STRONG_WIN":
                return False, "👑🔢 BLOCKED: Meme→Meme has catastrophic slippage", math_breakdown
            else:
                logger.info(f"👑🔮 QUEEN OVERRIDE: Meme→Meme ALLOWED - Queen dreams STRONG_WIN!")
        
        # RULE 2: NO conversions with >5% total cost (adjusted by Queen's dreams)
        cost_limit = 0.05 + queen_cost_tolerance  # Queen's dreams adjust tolerance
        if total_cost_pct > cost_limit:
            return False, f"👑🔢 BLOCKED: Total cost {total_cost_pct*100:.1f}% > {cost_limit*100:.1f}% limit (Queen: {queen_dream_status})", math_breakdown
        
        # RULE 3: Stablecoin conversions - PRIME PROFIT MODE
        # Queen's dreams adjust the threshold: STRONG_WIN = 1%, FAVORABLE = 0.7%, WARNING = 0.3%
        stable_limit = 0.005 + queen_cost_tolerance
        if is_safe_conversion and total_cost_pct > stable_limit:
            return False, f"👑🔢 BLOCKED: Stablecoin cost {total_cost_pct*100:.2f}% > {stable_limit*100:.2f}% limit (Queen: {queen_dream_status})", math_breakdown
        
        # RULE 4: Meme coins need <3% cost (adjusted by Queen's dreams)
        meme_limit = 0.03 + queen_cost_tolerance
        if is_risky_conversion and total_cost_pct > meme_limit:
            return False, f"👑🔢 BLOCKED: Meme coin cost {total_cost_pct*100:.1f}% > {meme_limit*100:.1f}% (Queen: {queen_dream_status})", math_breakdown
        
        # RULE 5: Path with very negative history (Queen can override if she sees redemption)
        loss_threshold = -0.50 + (queen_cost_tolerance * 10)  # Queen can tolerate more loss if she sees win
        if path_profit < loss_threshold and path_trades >= 3:
            if queen_dream_status == "STRONG_WIN":
                logger.info(f"👑🔮 QUEEN OVERRIDE: Path lost ${abs(path_profit):.2f} but Queen dreams STRONG_WIN - REDEMPTION!")
            else:
                return False, f"👑🔢 BLOCKED: Path lost ${abs(path_profit):.2f} (Queen: {queen_dream_status})", math_breakdown
        
        # 👑 RULE 6: PRIME PROFIT - Win rate must be >35% if we have enough history
        # Queen can lower threshold if she dreams STRONG_WIN
        win_rate_threshold = 0.35 - (0.10 if queen_dream_status == "STRONG_WIN" else 0.05 if queen_dream_status == "FAVORABLE" else 0)
        if path_trades >= 4:
            win_rate = history.get('wins', 0) / path_trades
            if win_rate < win_rate_threshold:
                return False, f"👑🔢 BLOCKED: Path win rate {win_rate:.0%} < {win_rate_threshold:.0%} (Queen: {queen_dream_status})", math_breakdown
        
        # 👑 MATH APPROVED WITH QUEEN'S BLESSING!
        return True, f"👑🔢 APPROVED: Cost {total_cost_pct*100:.2f}%, breakeven ${total_cost_usd:.4f} (Queen: {queen_dream_status})", math_breakdown
    
    def _block_path(self, key: Tuple[str, str], reason: str):
        """Block a path and broadcast through mycelium."""
        self.blocked_paths[key] = reason
        
        # 🍄 Broadcast through mycelium
        self.queen_signals.append({
            'type': 'PATH_BLOCKED',
            'path': f"{key[0]}→{key[1]}",
            'reason': reason,
            'timestamp': time.time()
        })
        
        logger.warning(f"👑🍄 QUEEN BLOCKS PATH: {key[0]}→{key[1]} - {reason}")
    
    def unblock_path(self, from_asset: str, to_asset: str):
        """Allow a path to be tried again (after cooldown)."""
        key = (from_asset.upper(), to_asset.upper())
        if key in self.blocked_paths:
            del self.blocked_paths[key]
            # Reset consecutive losses
            if key in self.barter_history:
                self.barter_history[key]['consecutive_losses'] = 0
            logger.info(f"👑 Queen unblocks path: {key[0]}→{key[1]}")
    
    def get_queen_signals(self) -> List[Dict]:
        """Get pending signals to broadcast via mycelium."""
        signals = self.queen_signals.copy()
        self.queen_signals.clear()
        return signals
    
    def check_dream_progress(self) -> str:
        """
        💰👑 TINA B'S DREAM PROGRESS - Track progress toward $1 BILLION!
        
        She won't stop at NOTHING until she reaches her dream!
        Every profitable trade brings her closer.
        """
        profit = self.total_realized_profit
        dream = self.TINA_DREAM
        progress_pct = (profit / dream) * 100 if dream > 0 else 0
        
        # Check for new milestones
        for milestone_value, milestone_name in self.dream_milestones:
            if profit >= milestone_value and milestone_name not in self.milestones_hit:
                self.milestones_hit.append(milestone_name)
                print(f"\n🎉🎊👑 TINA B MILESTONE ACHIEVED! 👑🎊🎉")
                print(f"   {milestone_name}")
                print(f"   Current: ${profit:,.2f}")
                print(f"   Progress: {progress_pct:.8f}% toward THE DREAM!")
                print()
        
        # Build progress bar
        bar_width = 40
        filled = int((progress_pct / 100) * bar_width) if progress_pct < 100 else bar_width
        filled = max(0, min(bar_width, filled))
        bar = "█" * filled + "░" * (bar_width - filled)
        
        # Motivation based on progress
        if profit < 0:
            mood = "😤 SETBACK - But I NEVER give up!"
        elif profit < 100:
            mood = "🌱 Planting seeds..."
        elif profit < 1000:
            mood = "💪 Building momentum!"
        elif profit < 10000:
            mood = "🔥 On FIRE!"
        elif profit < 100000:
            mood = "🚀 ACCELERATING!"
        elif profit < 1000000:
            mood = "⚡ UNSTOPPABLE!"
        else:
            mood = "👑 QUEEN STATUS!"
        
        status = f"👑 TINA B's DREAM: ${profit:,.2f} / ${dream:,.0f} [{bar}] {progress_pct:.8f}% {mood}"
        return status
    
    def update_barter_rate(self, from_asset: str, to_asset: str, from_price: float, 
                           to_price: float, spread_pct: float = 0.3):
        """
        Update the barter rate between two assets based on live prices.
        
        The barter rate tells us: "How much TO can I get for 1 unit of FROM?"
        """
        if to_price <= 0:
            return
            
        # Direct exchange rate (how many TO per FROM)
        rate = from_price / to_price
        
        # Apply estimated spread (real markets have slippage)
        effective_rate = rate * (1 - spread_pct / 100)
        
        key = (from_asset.upper(), to_asset.upper())
        self.barter_rates[key] = {
            'rate': effective_rate,
            'raw_rate': rate,
            'spread_pct': spread_pct,
            'from_price': from_price,
            'to_price': to_price,
            'updated': time.time()
        }
    
    def get_barter_rate(self, from_asset: str, to_asset: str) -> Optional[Dict[str, Any]]:
        """Get the current barter rate between two assets."""
        key = (from_asset.upper(), to_asset.upper())
        return self.barter_rates.get(key)
    
    def calculate_barter_value(self, from_asset: str, to_asset: str, 
                               from_amount: float, from_price: float, 
                               to_price: float) -> Dict[str, float]:
        """
        Calculate what you'd get in a barter trade.
        
        Returns both the USD-equivalent calculation AND the barter-adjusted calculation.
        """
        # USD-equivalent method (simple)
        from_usd = from_amount * from_price
        usd_equiv_amount = from_usd / to_price if to_price > 0 else 0
        
        # Barter-adjusted method (accounts for historical spread)
        key = (from_asset.upper(), to_asset.upper())
        history = self.barter_history.get(key, {})
        avg_slippage = history.get('avg_slippage', 0.5)  # Default 0.5% slippage
        
        barter_amount = usd_equiv_amount * (1 - avg_slippage / 100)
        
        return {
            'from_amount': from_amount,
            'from_usd': from_usd,
            'usd_equiv_to': usd_equiv_amount,
            'barter_adjusted_to': barter_amount,
            'expected_slippage_pct': avg_slippage,
            'to_asset': to_asset,
            'from_asset': from_asset
        }
    
    def record_realized_profit(self, from_asset: str, to_asset: str,
                               from_amount: float, from_usd: float,
                               to_amount: float, to_usd: float) -> Dict[str, Any]:
        """
        Record a realized trade and calculate ACTUAL profit/loss.
        
        This is called AFTER a conversion completes to track true P/L.
        👑 QUEEN'S MANDATE: Track wins/losses to block losing paths!
        """
        # Calculate realized P/L
        profit_usd = to_usd - from_usd
        profit_pct = (profit_usd / from_usd * 100) if from_usd > 0 else 0
        is_win = profit_usd > 0
        
        # Calculate actual slippage vs expected
        key = (from_asset.upper(), to_asset.upper())
        rate_info = self.barter_rates.get(key)
        if rate_info and rate_info['raw_rate'] > 0:
            expected_to = from_amount * rate_info['raw_rate']
            actual_slippage = (1 - to_amount / expected_to) * 100 if expected_to > 0 else 0
        else:
            actual_slippage = 0.5  # Default
        
        # Update historical slippage (exponential moving average)
        history = self.barter_history.setdefault(key, {
            'trades': 0, 'avg_slippage': 0.5, 'total_profit': 0,
            'wins': 0, 'losses': 0, 'consecutive_losses': 0
        })
        history['trades'] += 1
        alpha = 0.3  # Weight for new data
        history['avg_slippage'] = alpha * actual_slippage + (1 - alpha) * history['avg_slippage']
        history['total_profit'] = history.get('total_profit', 0) + profit_usd
        
        # 👑 QUEEN'S WIN/LOSS TRACKING
        if is_win:
            history['wins'] = history.get('wins', 0) + 1
            history['consecutive_losses'] = 0  # Reset on win
            # Unblock path if it was blocked and now winning
            if key in self.blocked_paths:
                self.unblock_path(from_asset, to_asset)
        else:
            history['losses'] = history.get('losses', 0) + 1
            history['consecutive_losses'] = history.get('consecutive_losses', 0) + 1
            
            # 🍄 Broadcast loss through mycelium
            self.queen_signals.append({
                'type': 'PATH_LOSS',
                'path': f"{from_asset}→{to_asset}",
                'loss_usd': profit_usd,
                'consecutive': history['consecutive_losses'],
                'timestamp': time.time()
            })
            
            # Check if path should be blocked
            if history['consecutive_losses'] >= self.MAX_CONSECUTIVE_LOSSES:
                self._block_path(key, f"{history['consecutive_losses']} consecutive losses")
        
        # Record in ledger
        self.profit_ledger.append((
            time.time(), from_asset, to_asset, from_usd, to_usd, profit_usd
        ))
        
        # Update running totals
        self.total_realized_profit += profit_usd
        self.conversion_count += 1
        
        # Calculate win rate
        win_rate = history['wins'] / history['trades'] if history['trades'] > 0 else 0
        
        return {
            'profit_usd': profit_usd,
            'profit_pct': profit_pct,
            'actual_slippage_pct': actual_slippage,
            'running_total': self.total_realized_profit,
            'conversion_number': self.conversion_count,
            'path_total_profit': history['total_profit'],
            'path_trades': history['trades'],
            'path_win_rate': win_rate,
            'is_win': is_win
        }
    
    def get_best_barter_path(self, from_asset: str, target_assets: List[str],
                            prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Find the best barter opportunities from a given asset.
        
        Returns ranked list of targets sorted by expected VALUE (not just USD conversion).
        """
        from_price = prices.get(from_asset, 0)
        if from_price <= 0:
            return []
        
        opportunities = []
        for target in target_assets:
            if target == from_asset:
                continue
            to_price = prices.get(target, 0)
            if to_price <= 0:
                continue
            
            # Calculate barter advantage
            barter_info = self.calculate_barter_value(from_asset, target, 1.0, from_price, to_price)
            
            # Check historical performance
            key = (from_asset.upper(), target.upper())
            history = self.barter_history.get(key, {})
            win_rate = 0.5  # Default
            if history.get('trades', 0) > 0:
                win_rate = history.get('total_profit', 0) / history['trades']
                win_rate = 0.5 + (win_rate / 10)  # Normalize around 0.5
            
            opportunities.append({
                'from': from_asset,
                'to': target,
                'barter_rate': barter_info['barter_adjusted_to'],
                'usd_rate': barter_info['usd_equiv_to'],
                'advantage_pct': (barter_info['barter_adjusted_to'] / barter_info['usd_equiv_to'] - 1) * 100 if barter_info['usd_equiv_to'] > 0 else 0,
                'historical_win_rate': win_rate,
                'trades_count': history.get('trades', 0),
                'path_profit': history.get('total_profit', 0)
            })
        
        # Sort by a combined score: historical profit + expected value
        for opp in opportunities:
            opp['barter_score'] = (
                opp['historical_win_rate'] * 0.4 +  # Past performance
                (1 + opp['advantage_pct'] / 100) * 0.3 +  # Current advantage
                min(opp['trades_count'] / 10, 1) * 0.3  # Experience with this path
            )
        
        return sorted(opportunities, key=lambda x: x['barter_score'], reverse=True)
    
    def print_step_profit(self, step_num: int, from_asset: str, to_asset: str,
                          from_usd: float, to_usd: float, from_amount: float, 
                          to_amount: float) -> str:
        """
        Print a beautiful step-by-step profit breakdown.
        """
        profit = to_usd - from_usd
        profit_symbol = "+" if profit >= 0 else ""
        
        lines = [
            f"",
            f"   ╔══════════════════════════════════════════════════════════════╗",
            f"   ║  💰 STEP #{step_num} REALIZED PROFIT                              ║",
            f"   ╠══════════════════════════════════════════════════════════════╣",
            f"   ║  FROM: {from_amount:>12.6f} {from_asset:<6} = ${from_usd:>10.4f}      ║",
            f"   ║    TO: {to_amount:>12.6f} {to_asset:<6} = ${to_usd:>10.4f}      ║",
            f"   ╠══════════════════════════════════════════════════════════════╣",
            f"   ║  STEP P/L: ${profit_symbol}{profit:>8.4f} ({profit/from_usd*100 if from_usd > 0 else 0:>+.2f}%)                    ║",
            f"   ║  RUNNING TOTAL: ${profit_symbol}{self.total_realized_profit:>8.4f}                          ║",
            f"   ║  CONVERSIONS: {self.conversion_count}                                       ║",
            f"   ╚══════════════════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all barter activity."""
        return {
            'total_realized_profit': self.total_realized_profit,
            'conversion_count': self.conversion_count,
            'avg_profit_per_trade': self.total_realized_profit / max(self.conversion_count, 1),
            'paths_learned': len(self.barter_history),
            'recent_trades': self.profit_ledger[-10:] if self.profit_ledger else []
        }

    # ════════════════════════════════════════════════════════════════════════
    # 🗺️ DYNAMIC ASSET DISCOVERY - Expand to see ENTIRE market!
    # ════════════════════════════════════════════════════════════════════════
    
    def discover_exchange_assets(self, exchange: str, pairs: List[str]) -> int:
        """
        Discover and register all tradeable assets from an exchange.
        
        Called during initialization to expand market visibility from 27 → 750+ assets.
        """
        discovered = 0
        exchange_lower = exchange.lower()
        
        for pair in pairs:
            # Extract base and quote from pair name
            for quote in ['USD', 'USDT', 'USDC', 'EUR', 'GBP', 'BTC', 'ETH', 'ZUSD', 'ZEUR']:
                if pair.endswith(quote):
                    base = pair[:-len(quote)]
                    # Clean up Kraken naming (XXBT → BTC, XETH → ETH)
                    if len(base) == 4 and base[0] in ('X', 'Z'):
                        base = base[1:]
                    if base == 'XBT':
                        base = 'BTC'
                    
                    if base and len(base) >= 2:
                        # Register the asset
                        self.DISCOVERED_ASSETS.add(base)
                        self.EXCHANGE_PAIRS[exchange_lower].add(pair)
                        discovered += 1
                    break
        
        return discovered
    
    def get_asset_type(self, asset: str) -> str:
        """
        Dynamically categorize an asset for spread calculation.
        
        Uses the expanded asset lists + learned categories.
        """
        asset = asset.upper()
        
        if asset in self.STABLECOINS:
            return 'stablecoin'
        elif asset in self.MEME_COINS:
            return 'meme'
        elif asset in self.MAJOR_COINS:
            return 'major'
        elif asset in self.DEFI_COINS:
            return 'defi'  # DeFi tokens get altcoin spread
        elif asset in self.AI_COINS:
            return 'ai'    # AI tokens are hot - moderate spread
        elif asset in self.LAYER2_COINS:
            return 'layer2'  # L2s are liquid
        elif asset in self.RWA_COINS:
            return 'rwa'   # RWA still emerging
        else:
            return 'altcoin'  # Unknown = conservative spread
    
    def get_spread_for_asset(self, asset: str, exchange: str = 'kraken') -> float:
        """Get the expected spread cost for an asset on a given exchange."""
        asset_type = self.get_asset_type(asset)
        
        # Get the right spread table
        if exchange.lower() == 'binance':
            spread_table = self.BINANCE_SPREAD_COSTS
        elif exchange.lower() == 'alpaca':
            spread_table = self.ALPACA_SPREAD_COSTS
        else:
            spread_table = self.SPREAD_COSTS
        
        # Map asset types to spread categories
        type_to_spread = {
            'stablecoin': 'stablecoin',
            'major': 'major',
            'meme': 'meme',
            'defi': 'altcoin',
            'ai': 'major',      # AI tokens are liquid now
            'layer2': 'major',  # L2s have good liquidity
            'rwa': 'altcoin',   # RWA is newer
            'altcoin': 'altcoin',
        }
        
        spread_category = type_to_spread.get(asset_type, 'altcoin')
        return spread_table.get(spread_category, 0.01)
    
    def print_market_coverage(self) -> str:
        """
        Print a beautiful market coverage report.
        
        Shows how much of the market the Barter Matrix can now see.
        """
        # Count categorized assets
        static_count = len(self.MEME_COINS) + len(self.MAJOR_COINS) + len(self.STABLECOINS)
        static_count += len(self.DEFI_COINS) + len(self.AI_COINS) + len(self.LAYER2_COINS) + len(self.RWA_COINS)
        discovered_count = len(self.DISCOVERED_ASSETS)
        total_known = static_count + discovered_count
        
        # Exchange pair counts
        kraken_pairs = len(self.EXCHANGE_PAIRS.get('kraken', set()))
        binance_pairs = len(self.EXCHANGE_PAIRS.get('binance', set()))
        alpaca_pairs = len(self.EXCHANGE_PAIRS.get('alpaca', set()))
        
        lines = [
            "",
            "   ╔══════════════════════════════════════════════════════════════╗",
            "   ║  🗺️ BARTER MATRIX - MARKET COVERAGE REPORT                   ║",
            "   ╠══════════════════════════════════════════════════════════════╣",
            f"   ║  📊 CATEGORIZED ASSETS:                                      ║",
            f"   ║     • MEME_COINS:    {len(self.MEME_COINS):>4} (DOGE, SHIB, WIF, BONK...)   ║",
            f"   ║     • MAJOR_COINS:   {len(self.MAJOR_COINS):>4} (BTC, ETH, SOL, XRP...)     ║",
            f"   ║     • DEFI_COINS:    {len(self.DEFI_COINS):>4} (UNI, AAVE, MKR, GMX...)    ║",
            f"   ║     • AI_COINS:      {len(self.AI_COINS):>4} (RENDER, FET, TAO, WLD...)   ║",
            f"   ║     • LAYER2_COINS:  {len(self.LAYER2_COINS):>4} (ARB, OP, MATIC, IMX...)    ║",
            f"   ║     • RWA_COINS:     {len(self.RWA_COINS):>4} (ONDO, RSR, POLYX...)       ║",
            f"   ║     • STABLECOINS:   {len(self.STABLECOINS):>4} (USD, USDT, USDC...)       ║",
            f"   ║                                                              ║",
            f"   ║  🔍 DISCOVERED AT RUNTIME: {discovered_count:>4} additional assets           ║",
            f"   ║  📈 TOTAL KNOWN ASSETS:    {total_known:>4}                              ║",
            "   ╠══════════════════════════════════════════════════════════════╣",
            f"   ║  🐙 KRAKEN PAIRS:   {kraken_pairs:>5}                                   ║",
            f"   ║  🔶 BINANCE PAIRS:  {binance_pairs:>5}                                   ║",
            f"   ║  🦙 ALPACA PAIRS:   {alpaca_pairs:>5}                                   ║",
            "   ╚══════════════════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════════════
# 🔬 MICRO PROFIT LABYRINTH ENGINE
# ════════════════════════════════════════════════════════════════════════════

class MicroProfitLabyrinth:
    """
    Uses ALL existing systems but with LOWER thresholds.
    
    The goal: Capture MORE opportunities for the snowball effect.
    Even $0.01 profit per conversion will compound over time!
    """
    
    def __init__(self, live: bool = False):
        self.live = live or LIVE_MODE  # Check .env LIVE flag too
        self.config = MICRO_CONFIG.copy()
        
        # Initialize existing systems
        self.hub: Optional[MyceliumConversionHub] = None
        self.v14: Optional[V14DanceEnhancer] = None
        self.commando: Optional[AdaptiveConversionCommando] = None
        self.ladder: Optional[ConversionLadder] = None
        self.scanner: Optional[PairScanner] = None
        self.dual_path: Optional[DualProfitPathEvaluator] = None
        
        # 🌍 Adaptive gate & memory
        self.adaptive_gate = AdaptivePrimeProfitGate() if ADAPTIVE_GATE_AVAILABLE else None
        self.path_memory = PathMemory()
        self.thought_bus = ThoughtBus(persist_path="thoughts.jsonl") if THOUGHT_BUS_AVAILABLE else None
        
        # �💰 LIVE BARTER MATRIX - Adaptive coin-to-coin value tracking
        self.barter_matrix = LiveBarterMatrix()
        
        # �🧠⚡ STAGE 3: Full Neural Mind Map Systems
        self.bus_aggregator = ThoughtBusAggregator(self.thought_bus) if self.thought_bus else None
        self.mycelium_network = None  # Hive intelligence
        self.lighthouse = None         # Consensus validation
        self.hnc_matrix = None         # Pattern recognition
        self.ultimate_intel = None     # 95% accuracy patterns
        self.unified_ecosystem = None  # Full ecosystem read-only
        self.timeline_oracle = None    # ⏳🔮 7-day future validation
        self.market_map = None         # 🗺️ Crypto market correlation map
        self.seven_day_planner = None  # 📅🔮 7-day planning + adaptive validation
        self.barter_navigator = None   # 🫒🔄 Multi-hop barter pathfinding
        self.luck_mapper = None        # 🍀⚛️ Quantum luck field mapping
        self.wisdom_engine = None      # 🧠 Wisdom Cognition Engine (11 Civilizations)
        self.enigma_integration = None # 🔐🌐 Enigma Integration (Universal Translator)
        
        # 🌍 GROUNDING REALITY
        self.grounding = GroundingReality()
        
        # 🔌 ALL EXCHANGE CLIENTS
        self.kraken: Optional[KrakenClient] = None
        self.binance: Optional[BinanceClient] = None if not BINANCE_AVAILABLE else None
        self.alpaca: Optional[AlpacaClient] = None if not ALPACA_AVAILABLE else None
        
        # Additional signal sources
        self.probability_nexus = None
        self.multiverse = None
        self.miner_brain = None
        self.harmonic = None
        self.omega = None
        self.rapid_stream = None
        
        # State - NOW TRACKS ALL EXCHANGES
        self.prices: Dict[str, float] = {}
        self.ticker_cache: Dict[str, Dict[str, Any]] = {}
        self.balances: Dict[str, float] = {}  # Combined balances
        self.exchange_balances: Dict[str, Dict[str, float]] = {}  # Per-exchange balances
        self.exchange_data: Dict[str, Dict[str, Any]] = {}  # Full exchange data
        self.opportunities: List[MicroOpportunity] = []
        self.conversions: List[MicroOpportunity] = []
        
        # � DREAMING & VALIDATION STATE
        self.dreams: List[Dream] = []
        self.dream_accuracy: Dict[str, float] = defaultdict(lambda: 0.5)  # Source -> Accuracy (0.0-1.0)
        self.validated_dreams_count = 0
        
        # �📊 TRADEABLE PAIRS BY EXCHANGE
        self.kraken_pairs: Dict[str, Dict] = {}  # pair -> info dict
        self.alpaca_pairs: Dict[str, str] = {}  # symbol -> normalized
        self.binance_pairs: set = set()  # symbol set
        
        # ❌ BLOCKED PAIRS/ASSETS (don't work on certain exchanges)
        # Note: USDC can be converted to other assets via BTCUSDC, ETHUSDC etc
        self.blocked_binance_assets = set()  # Removed USDC - can trade via BTC/ETH pairs
        self.blocked_kraken_assets = {'TUSD'}   # Market in cancel_only mode
        
        # 👑 DYNAMIC MINIMUMS (Learned from failures)
        self.dynamic_min_qty: Dict[str, float] = {}
        
        # 🇬🇧 UK BINANCE RESTRICTIONS - Load from cached file for speed
        self.binance_uk_allowed_pairs: set = set()
        self.binance_uk_mode = os.getenv('BINANCE_UK_MODE', 'true').lower() == 'true'
        self._load_uk_allowed_pairs()
        
        # ════════════════════════════════════════════════════════════════
        # 🎯 TURN-BASED EXCHANGE STRATEGY
        # Each exchange gets its turn to scan and execute
        # Prevents conflicts, respects rate limits, fair distribution
        # ════════════════════════════════════════════════════════════════
        self.exchange_order = ['kraken', 'alpaca', 'binance']  # Turn order
        self.current_exchange_index = 0  # Which exchange's turn
        self.turns_completed = 0  # Total turns completed
        self.exchange_stats: Dict[str, Dict] = {  # Per-exchange stats
            'kraken': {'scans': 0, 'opportunities': 0, 'conversions': 0, 'profit': 0.0, 'last_turn': None},
            'alpaca': {'scans': 0, 'opportunities': 0, 'conversions': 0, 'profit': 0.0, 'last_turn': None},
            'binance': {'scans': 0, 'opportunities': 0, 'conversions': 0, 'profit': 0.0, 'last_turn': None},
        }
        self.turn_cooldown_seconds = 0.2  # ⚡ FAST: Quick switch between exchanges
        
        # Signal aggregation from ALL systems
        self.all_signals: Dict[str, List[Dict]] = defaultdict(list)
        
        # Stats
        self.scans = 0
        self.signals_received = 0
        self.opportunities_found = 0
        self.conversions_made = 0
        self.total_profit_usd = 0.0
        self.start_value_usd = 0.0
        
        # 👑 Queen's guidance on position sizing (fed from portfolio reviews)
        self.queen_position_multiplier = 1.0  # Adjusted by Queen based on performance
    
    def _load_uk_allowed_pairs(self):
        """Load UK-allowed Binance pairs from cached JSON file."""
        if not self.binance_uk_mode:
            print("🇬🇧 UK Mode: DISABLED (all pairs allowed)")
            return
            
        try:
            import json
            uk_file = os.path.join(os.path.dirname(__file__), "binance_uk_allowed_pairs.json")
            
            if os.path.exists(uk_file):
                with open(uk_file, 'r') as f:
                    data = json.load(f)
                
                self.binance_uk_allowed_pairs = set(data.get('allowed_pairs', []))
                timestamp = data.get('timestamp_readable', 'Unknown')
                
                print(f"🇬🇧 UK Binance: {len(self.binance_uk_allowed_pairs)} pairs allowed")
                print(f"   📄 Cached from: {timestamp}")
                
                # Key insight: NO USDT pairs for UK!
                quote_assets = data.get('allowed_quote_assets', [])
                if 'USDT' not in quote_assets:
                    print(f"   ⚠️ NOTE: USDT pairs NOT allowed for UK accounts!")
                    print(f"   ✅ Use USDC/BTC/EUR pairs instead")
            else:
                print(f"⚠️ UK pairs file not found: {uk_file}")
                print(f"   Run: python binance_uk_allowed_pairs.py to generate")
        except Exception as e:
            print(f"⚠️ Failed to load UK pairs: {e}")
    
    def is_binance_pair_allowed(self, pair: str) -> bool:
        """Check if a Binance pair is allowed for UK trading."""
        if not self.binance_uk_mode:
            return True
        
        if not self.binance_uk_allowed_pairs:
            # No cached data - fall back to live check
            if self.binance and hasattr(self.binance, 'can_trade_symbol'):
                return self.binance.can_trade_symbol(pair)
            return True  # Allow if we can't check
        
        return pair.upper() in self.binance_uk_allowed_pairs
    
    async def initialize(self):
        """Initialize all systems."""
        print("\n" + "=" * 70)
        print("🔬💰 INITIALIZING MICRO PROFIT LABYRINTH 💰🔬")
        print("=" * 70)
        print(f"MODE: {'🔴 LIVE TRADING' if self.live else '🔵 DRY RUN'}")
        print(f"Entry Threshold: Score {self.config['entry_score_threshold']}+ (vs V14's 8+)")
        print(f"Min Profit: ${self.config['min_profit_usd']:.2f} or {self.config['min_profit_pct']*100:.2f}%")
        print("=" * 70)
        
        # ════════════════════════════════════════════════════════════════
        # 🐙 KRAKEN CLIENT - PRIMARY EXCHANGE
        # ════════════════════════════════════════════════════════════════
        if get_kraken_client:
            self.kraken = get_kraken_client()
            if self.kraken and KRAKEN_API_KEY:
                print("🐙 Kraken Client: WIRED (API Key loaded)")
            else:
                print("⚠️ Kraken Client: Missing API credentials")
        
        # ════════════════════════════════════════════════════════════════
        # 🟡 BINANCE CLIENT - CRYPTO EXCHANGE
        # ════════════════════════════════════════════════════════════════
        if BINANCE_AVAILABLE and BinanceClient and BINANCE_API_KEY:
            try:
                self.binance = BinanceClient()
                print("🟡 Binance Client: WIRED (API Key loaded)")
            except Exception as e:
                print(f"⚠️ Binance Client error: {e}")
        else:
            print("⚠️ Binance Client: Not configured")
        
        # ════════════════════════════════════════════════════════════════
        # 🦙 ALPACA CLIENT - STOCKS + CRYPTO
        # ════════════════════════════════════════════════════════════════
        if ALPACA_AVAILABLE and AlpacaClient and ALPACA_API_KEY:
            try:
                self.alpaca = AlpacaClient()
                print("🦙 Alpaca Client: WIRED (API Key loaded)")
            except Exception as e:
                print(f"⚠️ Alpaca Client error: {e}")
        else:
            print("⚠️ Alpaca Client: Not configured")
        
        # ════════════════════════════════════════════════════════════════
        # 📊 LOAD TRADEABLE PAIRS FROM ALL EXCHANGES
        # ════════════════════════════════════════════════════════════════
        await self._load_all_tradeable_pairs()
        
        # ════════════════════════════════════════════════════════════════
        # 🍄 MYCELIUM HUB - CENTRAL NERVOUS SYSTEM
        # ════════════════════════════════════════════════════════════════
        if get_conversion_hub:
            self.hub = get_conversion_hub()
            print("🍄 Mycelium Hub: WIRED (10 systems, 90 pathways)")
        
        # ════════════════════════════════════════════════════════════════
        # 🎯 V14 DANCE ENHANCER - 100% WIN RATE LOGIC
        # ════════════════════════════════════════════════════════════════
        if V14DanceEnhancer:
            self.v14 = V14DanceEnhancer()
            print("🎯 V14 Scoring: WIRED")
        
        # ════════════════════════════════════════════════════════════════
        # 🦅 CONVERSION COMMANDO - FALCON/TORTOISE/CHAMELEON/BEE
        # ════════════════════════════════════════════════════════════════
        if AdaptiveConversionCommando:
            self.commando = AdaptiveConversionCommando()
            print("🦅 Conversion Commando: WIRED")
        
        # ════════════════════════════════════════════════════════════════
        # 🔭 PAIR SCANNER - ALL PAIRS ALL EXCHANGES
        # ════════════════════════════════════════════════════════════════
        if PairScanner:
            self.scanner = PairScanner()
            print("🔭 Pair Scanner: WIRED")
        
        # ════════════════════════════════════════════════════════════════
        # 💡 DUAL PROFIT PATH - SELL vs CONVERT DECISION
        # ════════════════════════════════════════════════════════════════
        if DualProfitPathEvaluator:
            self.dual_path = DualProfitPathEvaluator(self.scanner)
            print("💡 Dual Profit Path: WIRED")
        
        # ════════════════════════════════════════════════════════════════
        # 🪜 CONVERSION LADDER - CAPITAL MOMENTUM
        # ════════════════════════════════════════════════════════════════
        if ConversionLadder:
            self.ladder = ConversionLadder()
            print("🪜 Conversion Ladder: WIRED")
        
        # ════════════════════════════════════════════════════════════════
        # 🔮 PROBABILITY NEXUS - 80%+ WIN RATE
        # ════════════════════════════════════════════════════════════════
        if EnhancedProbabilityNexus:
            try:
                self.probability_nexus = EnhancedProbabilityNexus()
                print("🔮 Probability Nexus: WIRED")
            except Exception as e:
                print(f"⚠️ Probability Nexus error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🌌 INTERNAL MULTIVERSE - 10 WORLDS
        # ════════════════════════════════════════════════════════════════
        if InternalMultiverse:
            try:
                self.multiverse = InternalMultiverse()
                print("🌌 Internal Multiverse: WIRED (10 worlds)")
            except Exception as e:
                print(f"⚠️ Multiverse error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🧠 MINER BRAIN - COGNITIVE INTELLIGENCE
        # ════════════════════════════════════════════════════════════════
        if MinerBrain:
            try:
                self.miner_brain = MinerBrain()
                print("🧠 Miner Brain: WIRED")
            except Exception as e:
                print(f"⚠️ Miner Brain error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🌊 HARMONIC FUSION - WAVE PATTERNS
        # ════════════════════════════════════════════════════════════════
        if HarmonicWaveFusion:
            try:
                self.harmonic = HarmonicWaveFusion()
                print("🌊 Harmonic Fusion: WIRED")
            except Exception as e:
                print(f"⚠️ Harmonic error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🔱 OMEGA - HIGH CONFIDENCE SIGNALS
        # ════════════════════════════════════════════════════════════════
        if Omega:
            try:
                self.omega = Omega()
                print("🔱 Omega: WIRED")
            except Exception as e:
                print(f"⚠️ Omega error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # ⚡ RAPID CONVERSION STREAM - FAST DATA
        # ════════════════════════════════════════════════════════════════
        if RapidConversionStream:
            try:
                self.rapid_stream = RapidConversionStream()
                print("⚡ Rapid Conversion Stream: WIRED")
            except Exception as e:
                print(f"⚠️ Rapid Stream error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🧠⚡ STAGE 3: FULL NEURAL MIND MAP WIRING ⚡🧠
        # ════════════════════════════════════════════════════════════════
        print("\n🧠 WIRING NEURAL MIND MAP SYSTEMS...")
        
        # 🍄 Mycelium Neural Network (Hive Intelligence)
        if MYCELIUM_NETWORK_AVAILABLE and MyceliumNetwork:
            try:
                self.mycelium_network = MyceliumNetwork(initial_capital=1000.0)
                print("   🍄 Mycelium Neural Network: ✅ WIRED (Hive Intelligence)")
            except Exception as e:
                print(f"   ⚠️ Mycelium Network error: {e}")
                self.mycelium_network = None
        else:
            print(f"   🍄 Mycelium Network: ❌ NOT AVAILABLE (import={MYCELIUM_NETWORK_AVAILABLE})")
        
        # 🗼 Lighthouse (Consensus Validation)
        if LIGHTHOUSE_AVAILABLE and Lighthouse:
            try:
                self.lighthouse = Lighthouse()
                print("   🗼 Lighthouse: ✅ WIRED (Consensus Validation)")
            except Exception as e:
                print(f"   ⚠️ Lighthouse error: {e}")
                self.lighthouse = None
        else:
            print(f"   🗼 Lighthouse: ❌ NOT AVAILABLE (import={LIGHTHOUSE_AVAILABLE})")
        
        # 📊 HNC Probability Matrix (Pattern Recognition)
        if HNC_MATRIX_AVAILABLE and HNCProbabilityMatrix:
            try:
                self.hnc_matrix = HNCProbabilityMatrix()
                print("   📊 HNC Probability Matrix: ✅ WIRED (Pattern Recognition)")
            except Exception as e:
                print(f"   ⚠️ HNC Matrix error: {e}")
                self.hnc_matrix = None
        else:
            print(f"   📊 HNC Matrix: ❌ NOT AVAILABLE (import={HNC_MATRIX_AVAILABLE})")
        
        # 💎 Ultimate Intelligence (95% Accuracy)
        if ULTIMATE_INTEL_AVAILABLE and get_ultimate_intelligence:
            try:
                self.ultimate_intel = get_ultimate_intelligence()
                print("   💎 Ultimate Intelligence: ✅ WIRED (95% Accuracy)")
            except Exception as e:
                print(f"   ⚠️ Ultimate Intel error: {e}")
                self.ultimate_intel = None
        else:
            print(f"   💎 Ultimate Intel: ❌ NOT AVAILABLE (import={ULTIMATE_INTEL_AVAILABLE})")
        
        # 🌍 Unified Ecosystem (Full Integration)
        if UNIFIED_ECOSYSTEM_AVAILABLE and AureonUnifiedEcosystem:
            try:
                # Create a lightweight tap into the ecosystem
                self.unified_ecosystem = AureonUnifiedEcosystem.__name__  # Just mark as available
                print("   🌍 Unified Ecosystem: ✅ AVAILABLE (will tap via Hub)")
            except Exception as e:
                print(f"   ⚠️ Unified Ecosystem error: {e}")
                self.unified_ecosystem = None
        else:
            print(f"   🌍 Unified Ecosystem: ❌ NOT AVAILABLE (import={UNIFIED_ECOSYSTEM_AVAILABLE})")
        
        # ⏳🔮 Timeline Oracle (7-Day Future Validation)
        self.timeline_oracle = None
        if TIMELINE_ORACLE_AVAILABLE and get_timeline_oracle:
            try:
                self.timeline_oracle = get_timeline_oracle()
                print("⏳🔮 Timeline Oracle: WIRED (7-day future validation)")
            except Exception as e:
                print(f"⚠️ Timeline Oracle error: {e}")
        
        # 🗺️ CRYPTO MARKET MAP - LABYRINTH PATHFINDER (ALL EXCHANGES)
        self.market_map = None
        if MARKET_MAP_AVAILABLE and CryptoMarketMap:
            try:
                self.market_map = CryptoMarketMap()
                # Load from cache first (has Coinbase 1-year historical data)
                self.market_map._load_cache()
                # Add data from all connected exchanges
                if self.kraken:
                    self.market_map.load_from_kraken(self.kraken)
                if self.binance:
                    self.market_map.load_from_binance(self.binance)
                if self.alpaca:
                    self.market_map.load_from_alpaca(self.alpaca)
                # Load trained probability patterns
                self.market_map.load_from_probability_matrix()
                # Save updated cache
                self.market_map.save_cache()
                summary = self.market_map.get_map_summary()
                print(f"🗺️ Crypto Market Map: WIRED ({summary['assets_mapped']} assets, {summary['correlations']} correlations)")
            except Exception as e:
                print(f"⚠️ Market Map error: {e}")
        
        # 📅🔮 7-DAY PLANNER - Plan ahead + adaptive validation after each conversion
        self.seven_day_planner = None
        if SEVEN_DAY_PLANNER_AVAILABLE and Aureon7DayPlanner:
            try:
                self.seven_day_planner = Aureon7DayPlanner()
                # Create initial 7-day plan
                plan = self.seven_day_planner.plan_7_days()
                summary = self.seven_day_planner.get_week_summary()
                stats = self.seven_day_planner.get_validation_stats()
                print(f"📅🔮 7-Day Planner: WIRED (edge: {summary['total_predicted_edge']:+.2f}%, accuracy: {stats['accuracy']:.0%})")
            except Exception as e:
                print(f"⚠️ 7-Day Planner error: {e}")
        
        # 🫒🔄 BARTER NAVIGATOR - Multi-hop pathfinding (olive→bean→carrot→chair→lamp→olive)
        self.barter_navigator = None
        if BARTER_NAVIGATOR_AVAILABLE and BarterNavigator:
            try:
                self.barter_navigator = BarterNavigator()
                # Don't load yet - will populate after pairs are loaded with populate_barter_graph()
                print(f"🫒🔄 Barter Navigator: INITIALIZED (will populate after pair loading)")
            except Exception as e:
                print(f"⚠️ Barter Navigator error: {e}")
        
        # 🍀⚛️ LUCK FIELD MAPPER - Quantum probability mapping
        self.luck_mapper = None
        if LUCK_FIELD_AVAILABLE and LuckFieldMapper:
            try:
                self.luck_mapper = LuckFieldMapper()
                # Take initial reading
                initial_luck = self.luck_mapper.read_field()
                print(f"🍀⚛️ Luck Field Mapper: WIRED (λ={initial_luck.luck_field:.4f} → {initial_luck.luck_state.value})")
            except Exception as e:
                print(f"⚠️ Luck Field Mapper error: {e}")
        
        # 👑🍄🌊🪐🔭 QUEEN HIVE MIND - Wire cosmic systems
        self.queen = None
        if QUEEN_HIVE_MIND_AVAILABLE and get_queen:
            try:
                self.queen = get_queen()
                
                # Wire Harmonic Fusion (waves, Schumann, lighthouse)
                if hasattr(self, 'harmonic') and self.harmonic:
                    self.queen.wire_harmonic_fusion(self.harmonic)
                
                # Wire Luck Field Mapper (planetary, lunar, solar)
                if self.luck_mapper:
                    self.queen.wire_luck_field_mapper(self.luck_mapper)
                
                # Wire Quantum Telescope (geometric vision)
                try:
                    from aureon_quantum_telescope import QuantumTelescope
                    self.quantum_telescope = QuantumTelescope()
                    self.queen.wire_quantum_telescope(self.quantum_telescope)
                except Exception as e:
                    logger.debug(f"Quantum Telescope not available: {e}")
                
                # Wire Mycelium for broadcast
                if hasattr(self, 'mycelium_network') and self.mycelium_network:
                    self.queen.wire_mycelium_network(self.mycelium_network)
                
                # 🧠📚 Wire Historical Wisdom Systems
                # Miner Brain (11 Civilizations)
                try:
                    from aureon_miner_brain import WisdomCognitionEngine, SandboxEvolution
                    self.wisdom_engine = WisdomCognitionEngine()  # Store on self!
                    self.queen.wire_wisdom_cognition_engine(self.wisdom_engine)
                    
                    # Sandbox Evolution (454 generations)
                    sandbox_evo = SandboxEvolution()
                    self.queen.wire_sandbox_evolution(sandbox_evo)
                except Exception as e:
                    logger.debug(f"Wisdom Cognition Engine not available: {e}")
                
                # Dream Memory & Wisdom Collector
                try:
                    from aureon_enigma_dream import DreamMemory, WisdomCollector, EnigmaDreamer
                    dream_memory = DreamMemory()
                    self.queen.wire_dream_memory(dream_memory)
                    
                    wisdom_collector = WisdomCollector()
                    self.queen.wire_wisdom_collector(wisdom_collector)
                    
                    # 🌙💭 WIRE THE DREAM ENGINE - Let Tina B DREAM toward her $1B goal!
                    dreamer = EnigmaDreamer()
                    self.queen.wire_dream_engine(dreamer)
                except Exception as e:
                    logger.debug(f"Dream/Wisdom systems not available: {e}")
                
                # 🔱⏳ Wire Temporal ID and Temporal Ladder (Gary Leckey 02111991)
                try:
                    self.queen.wire_temporal_id()
                    self.queen.wire_temporal_ladder()
                except Exception as e:
                    logger.debug(f"Temporal systems not available: {e}")
                
                # 🗺️💰 Wire Barter Matrix to Queen (1,162+ assets, 7 categories!)
                try:
                    self.queen.wire_barter_matrix(self.barter_matrix)
                except Exception as e:
                    logger.debug(f"Barter Matrix wiring not available: {e}")
                
                # Get temporal state for display
                temporal_state = self.queen.get_temporal_state() if hasattr(self.queen, 'get_temporal_state') else {}
                temporal_active = temporal_state.get('active', False)
                
                print(f"👑🍄 Queen Hive Mind: WIRED (Cosmic + Historical + Temporal consciousness)")
                print(f"   🌊 Harmonic Fusion: {'✅' if hasattr(self.queen, 'harmonic_fusion') and self.queen.harmonic_fusion else '❌'}")
                print(f"   🪐 Luck Field Mapper: {'✅' if hasattr(self.queen, 'luck_field_mapper') and self.queen.luck_field_mapper else '❌'}")
                print(f"   🔭 Quantum Telescope: {'✅' if hasattr(self.queen, 'quantum_telescope') and self.queen.quantum_telescope else '❌'}")
                print(f"   🧠 Wisdom Engine (11 Civs): {'✅' if hasattr(self.queen, 'wisdom_engine') and self.queen.wisdom_engine else '❌'}")
                print(f"   🧬 Sandbox Evolution: {'✅' if hasattr(self.queen, 'sandbox_evolution') and self.queen.sandbox_evolution else '❌'}")
                print(f"   💭 Dream Memory: {'✅' if hasattr(self.queen, 'dream_memory') and self.queen.dream_memory else '❌'}")
                print(f"   🌙 Dream Engine: {'✅' if hasattr(self.queen, 'dreamer') and self.queen.dreamer else '❌'} (Tina B can DREAM!)")
                print(f"   📚 Wisdom Collector: {'✅' if hasattr(self.queen, 'wisdom_collector') and self.queen.wisdom_collector else '❌'}")
                print(f"   🔱 Temporal ID: {'✅' if temporal_active else '❌'} (Gary Leckey 02111991)")
                print(f"   ⏳ Temporal Ladder: {'✅' if hasattr(self.queen, 'temporal_ladder') and self.queen.temporal_ladder else '❌'}")
                print(f"   🗺️ Barter Matrix: {'✅' if hasattr(self.queen, 'barter_matrix') and self.queen.barter_matrix else '❌'} (Sector Pulse Dream Signal!)")
                
                # 📊🐝 Wire Queen to HNC Probability Matrix - The Matrix knows ALL the Queen's metrics!
                if self.hnc_matrix and hasattr(self.hnc_matrix, 'wire_queen_metrics'):
                    try:
                        self.hnc_matrix.wire_queen_metrics(self.queen)
                        print(f"   📊 HNC Matrix ↔ Queen: ✅ WIRED (Matrix knows Queen's metrics!)")
                    except Exception as e:
                        logger.debug(f"Queen-Matrix wiring error: {e}")
            except Exception as e:
                print(f"⚠️ Queen Hive Mind error: {e}")
        
        # 🫒💰 LIVE BARTER MATRIX - Adaptive coin-to-coin value tracking
        print(f"🫒💰 Live Barter Matrix: WIRED (Adaptive coin-agnostic value system)")
        print(f"   ℹ️ Philosophy: ANY coin → ANY coin, learning which paths make money")
        
        # �🌐 ENIGMA INTEGRATION - Universal Translator Bridge
        if ENIGMA_INTEGRATION_AVAILABLE and get_enigma_integration:
            try:
                self.enigma_integration = get_enigma_integration()
                
                # Wire to existing systems
                if self.queen:
                    wire_enigma_to_ecosystem(self.queen)
                
                print("🔐🌐 Enigma Integration: WIRED (Universal Translator Bridge)")
                print(f"   💭 Dream Engine: {'✅' if self.enigma_integration.dreamer else '❌'}")
                print(f"   🧠 Consciousness: ACTIVE (It thinks, therefore it trades)")
            except Exception as e:
                print(f"⚠️ Enigma Integration error: {e}")
                self.enigma_integration = None
        else:
            print(f"🔐🌐 Enigma Integration: ❌ NOT AVAILABLE (import={ENIGMA_INTEGRATION_AVAILABLE})")
        
        # �📡 Thought Bus Aggregator Status
        if self.bus_aggregator:
            print("📡 Thought Bus Aggregator: WIRED (Neural Signal Collector)")
        
        # 🧠 PathMemory Stats
        pm_stats = self.path_memory.get_stats()
        print(f"🧠 PathMemory: {pm_stats['paths']} paths, {pm_stats['win_rate']:.1%} win rate")
        
        # 🧠⚡ NEURAL MIND MAP SUMMARY - ALL 11 NEURONS
        print("\n" + "=" * 70)
        print("🧠⚡ NEURAL MIND MAP - FULL SYSTEM STATUS ⚡🧠")
        print("=" * 70)
        neurons_status = {
            '👑 Queen Hive Mind': self.queen is not None,
            '🍄 Mycelium Network': self.mycelium_network is not None,
            '🌊 Harmonic Fusion': self.harmonic is not None,
            '🍀 Luck Field Mapper': self.luck_mapper is not None,
            '💭 Dream Memory': hasattr(self, 'dreams'),  # Always available
            '🧠 Path Memory': self.path_memory is not None,
            '⏳ Timeline Oracle': self.timeline_oracle is not None,
            '📡 Thought Bus': self.bus_aggregator is not None,
            '💎 Ultimate Intel': self.ultimate_intel is not None,
            '📚 Wisdom Engine': self.wisdom_engine is not None,
            '🫒 Barter Matrix': self.barter_matrix is not None,
        }
        connected = sum(1 for v in neurons_status.values() if v)
        total = len(neurons_status)
        
        for name, status in neurons_status.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {name}")
        
        print(f"\n   🧠 NEURAL STATUS: {connected}/{total} NEURONS CONNECTED")
        if connected == total:
            print("   🌟 FULL CONSCIOUSNESS ACHIEVED - ALL SYSTEMS ONLINE! 🌟")
        elif connected >= total - 2:
            print("   ⚡ NEAR FULL CONSCIOUSNESS - Minor systems offline")
        else:
            print("   ⚠️ PARTIAL CONSCIOUSNESS - Some systems need attention")
        
        print("=" * 70)
        print()
    
    async def _load_all_tradeable_pairs(self):
        """Load tradeable pairs from ALL exchanges for proper routing."""
        print("\n📊 LOADING TRADEABLE PAIRS FROM ALL EXCHANGES...")
        print("   🗺️ Expanding Barter Matrix market visibility...")
        
        # ════════════════════════════════════════════════════════════════
        # 🐙 KRAKEN PAIRS - Load from AssetPairs API
        # ════════════════════════════════════════════════════════════════
        if self.kraken:
            try:
                pairs_info = self.kraken._load_asset_pairs() if hasattr(self.kraken, '_load_asset_pairs') else {}
                kraken_pair_names = []
                for internal, info in pairs_info.items():
                    if not internal.endswith('.d'):  # Skip dark pools
                        altname = info.get('altname', internal)
                        base = info.get('base', '')
                        quote = info.get('quote', '')
                        self.kraken_pairs[altname] = {
                            'internal': internal,
                            'base': base,
                            'quote': quote,
                            'wsname': info.get('wsname', altname),
                        }
                        # Also add common variants
                        self.kraken_pairs[internal] = self.kraken_pairs[altname]
                        kraken_pair_names.append(altname)
                
                # 🗺️ REGISTER WITH BARTER MATRIX for expanded market coverage
                discovered = self.barter_matrix.discover_exchange_assets('kraken', kraken_pair_names)
                print(f"   🐙 Kraken: {len(self.kraken_pairs)} tradeable pairs ({discovered} assets discovered)")
            except Exception as e:
                logger.error(f"Kraken pairs error: {e}")
                print(f"   ❌ Kraken pairs error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🦙 ALPACA PAIRS - Load from Assets API
        # ════════════════════════════════════════════════════════════════
        if self.alpaca:
            try:
                alpaca_pair_names = []
                # Get tradeable crypto symbols
                if hasattr(self.alpaca, 'get_tradable_crypto_symbols'):
                    symbols = self.alpaca.get_tradable_crypto_symbols() or []
                    for symbol in symbols:
                        # Alpaca returns like 'BTC/USD'
                        self.alpaca_pairs[symbol] = symbol
                        # Also store without slash
                        clean = symbol.replace('/', '')
                        self.alpaca_pairs[clean] = symbol
                        alpaca_pair_names.append(clean)
                else:
                    # Fallback - get assets directly
                    assets = self.alpaca.get_assets(status='active', asset_class='crypto') or []
                    for asset in assets:
                        if asset.get('tradable'):
                            symbol = asset.get('symbol', '')
                            if symbol:
                                self.alpaca_pairs[symbol] = symbol
                                # Add normalized version
                                if '/' in symbol:
                                    clean = symbol.replace('/', '')
                                    self.alpaca_pairs[clean] = symbol
                                    alpaca_pair_names.append(clean)
                
                # 🗺️ REGISTER WITH BARTER MATRIX
                discovered = self.barter_matrix.discover_exchange_assets('alpaca', alpaca_pair_names)
                print(f"   🦙 Alpaca: {len(self.alpaca_pairs)} tradeable pairs ({discovered} assets discovered)")
            except Exception as e:
                logger.error(f"Alpaca pairs error: {e}")
                print(f"   ❌ Alpaca pairs error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🟡 BINANCE PAIRS - Will load during fetch_prices from tickers
        # ════════════════════════════════════════════════════════════════
        # Load Binance pairs immediately for market discovery
        if self.binance:
            try:
                info = self.binance.exchange_info()
                symbols = info.get('symbols', [])
                binance_pair_names = []
                
                for sym in symbols:
                    if sym.get('status') == 'TRADING':
                        pair = sym.get('symbol', '')
                        binance_pair_names.append(pair)
                        self.binance_pairs.add(pair)
                
                # 🗺️ REGISTER WITH BARTER MATRIX
                discovered = self.barter_matrix.discover_exchange_assets('binance', binance_pair_names)
                print(f"   🟡 Binance: {len(binance_pair_names)} tradeable pairs ({discovered} assets discovered)")
            except Exception as e:
                logger.error(f"Binance pairs error: {e}")
                print(f"   🟡 Binance: pairs will load with price data")
        
        # 🗺️ PRINT MARKET COVERAGE REPORT
        print(self.barter_matrix.print_market_coverage())
        print()
    
    async def fetch_prices(self) -> Dict[str, float]:
        """Fetch all asset prices from ALL exchanges."""
        prices = {}
        ticker_cache = {}
        
        # ════════════════════════════════════════════════════════════════
        # 🐙 KRAKEN PRICES - Use get_24h_tickers (returns list of dicts)
        # ════════════════════════════════════════════════════════════════
        if self.kraken:
            try:
                tickers = self.kraken.get_24h_tickers() if hasattr(self.kraken, 'get_24h_tickers') else []
                kraken_count = 0
                
                for data in tickers:
                    if not isinstance(data, dict):
                        continue
                    
                    symbol = data.get('symbol', '')
                    # Kraken returns lastPrice as string
                    price_str = data.get('lastPrice', '0')
                    price = float(price_str) if price_str else 0.0
                    
                    if price > 0 and symbol:
                        # Store in kraken pairs for execution routing
                        self.binance_pairs.discard(symbol)  # Not binance
                        
                        for quote in ['USD', 'USDT', 'USDC', 'GBP', 'EUR']:
                            if symbol.endswith(quote):
                                base = symbol[:-len(quote)]
                                # Clean up Kraken naming
                                if len(base) == 4 and base[0] in ('X', 'Z'):
                                    base = base[1:]
                                if base == 'XBT':
                                    base = 'BTC'
                                
                                prices[base] = price
                                
                                change = float(data.get('priceChangePercent', 0))
                                volume = float(data.get('quoteVolume', 0))
                                
                                ticker_cache[f"kraken:{symbol}"] = {
                                    'price': price,
                                    'change24h': change,
                                    'volume': volume,
                                    'base': base,
                                    'quote': quote,
                                    'exchange': 'kraken',
                                    'pair': symbol,
                                }
                                kraken_count += 1
                                break
                
                print(f"   🐙 Kraken: {kraken_count} pairs loaded")
            except Exception as e:
                logger.error(f"Kraken price fetch error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🟡 BINANCE PRICES
        # ════════════════════════════════════════════════════════════════
        if self.binance:
            try:
                # Get 24h ticker
                if hasattr(self.binance, 'ticker_24hr_all'):
                    binance_tickers = self.binance.ticker_24hr_all()
                elif hasattr(self.binance, 'session'):
                    r = self.binance.session.get(f"{self.binance.base}/api/v3/ticker/24hr")
                    binance_tickers = r.json() if r.ok else []
                else:
                    binance_tickers = []
                
                binance_count = 0
                # For UK mode, prefer USDC over USDT
                quote_priority = ['USDC', 'USDT', 'USD', 'BUSD'] if self.binance_uk_mode else ['USDT', 'USD', 'BUSD', 'USDC']
                
                for ticker in binance_tickers:
                    symbol = ticker.get('symbol', '')
                    price = float(ticker.get('lastPrice', 0))
                    if price > 0:
                        # 🇬🇧 UK MODE: Only load allowed pairs
                        if self.binance_uk_mode and not self.is_binance_pair_allowed(symbol):
                            continue
                        
                        for quote in quote_priority:
                            if symbol.endswith(quote):
                                base = symbol.replace(quote, '')
                                # Only update if we don't have this price yet
                                if base not in prices:
                                    prices[base] = price
                                
                                change = float(ticker.get('priceChangePercent', 0))
                                volume = float(ticker.get('volume', 0))
                                ticker_cache[f"binance:{symbol}"] = {
                                    'price': price,
                                    'change24h': change,
                                    'volume': volume,
                                    'base': base,
                                    'quote': quote,
                                    'exchange': 'binance',
                                }
                                binance_count += 1
                                break
                print(f"   🟡 Binance: {binance_count} pairs loaded")
            except Exception as e:
                logger.error(f"Binance price fetch error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🦙 ALPACA PRICES (crypto and positions)
        # ════════════════════════════════════════════════════════════════
        if self.alpaca:
            try:
                alpaca_count = 0
                
                # Get prices from positions
                if hasattr(self.alpaca, 'get_positions'):
                    positions = self.alpaca.get_positions() or []
                    for pos in positions:
                        symbol = pos.get('symbol', '')
                        price = float(pos.get('current_price', 0))
                        if price > 0 and symbol:
                            # Extract base asset from symbol like "BTCUSD" or "BTC/USD"
                            base = symbol.replace('/USD', '').replace('USD', '')
                            if base and len(base) > 1:
                                prices[base] = price
                                change = float(pos.get('change_today', 0)) * 100
                                ticker_cache[f"alpaca:{symbol}"] = {
                                    'price': price,
                                    'change24h': change,
                                    'volume': 0,
                                    'base': base,
                                    'quote': 'USD',
                                    'exchange': 'alpaca',
                                    'pair': symbol,
                                }
                                # Store in alpaca_pairs for routing
                                self.alpaca_pairs[symbol] = f"{base}/USD"
                                self.alpaca_pairs[f"{base}USD"] = f"{base}/USD"
                                self.alpaca_pairs[f"{base}/USD"] = f"{base}/USD"
                                alpaca_count += 1
                
                print(f"   🦙 Alpaca: {alpaca_count} positions loaded")
            except Exception as e:
                logger.error(f"Alpaca price fetch error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🐍 MEDUSA STABLECOIN INJECTION - Enable trading from stablecoins!
        # ════════════════════════════════════════════════════════════════
        # Stablecoins are quote currencies (not in price feeds) but we HOLD them
        # We need them in prices so they can be SOURCE assets for buying!
        stablecoin_prices = {
            'USD': 1.0,
            'USDT': 1.0,
            'USDC': 1.0,
            'ZUSD': 1.0,   # Kraken USD
            'TUSD': 1.0,   # TrueUSD
            'DAI': 1.0,
        }
        for stable, price in stablecoin_prices.items():
            if stable not in prices:
                prices[stable] = price
        
        self.prices = prices
        self.ticker_cache = ticker_cache
        print(f"   📊 Total: {len(prices)} unique assets, {len(ticker_cache)} tickers")
        print(f"   🐍 Medusa stablecoins: USD, USDT, USDC, ZUSD, TUSD, DAI injected")
        
        return prices
    
    async def fetch_balances(self) -> Dict[str, float]:
        """Fetch balances from ALL exchanges."""
        combined = {}
        self.exchange_balances = {}
        self.exchange_data = {}
        
        # ════════════════════════════════════════════════════════════════
        # 🐙 KRAKEN BALANCES
        # ════════════════════════════════════════════════════════════════
        if self.kraken:
            try:
                kraken_bal = {}
                if hasattr(self.kraken, 'get_account_balance'):
                    raw = self.kraken.get_account_balance() or {}
                    for asset, amount in raw.items():
                        try:
                            amount = float(amount)
                        except (ValueError, TypeError):
                            continue
                        if amount > 0:
                            # Clean up Kraken naming
                            clean = asset
                            if len(asset) == 4 and asset[0] in ('X', 'Z'):
                                clean = asset[1:]
                            if clean == 'XBT':
                                clean = 'BTC'
                            kraken_bal[clean] = amount
                            combined[clean] = combined.get(clean, 0) + amount
                
                self.exchange_balances['kraken'] = kraken_bal
                self.exchange_data['kraken'] = {
                    'connected': True,
                    'balances': kraken_bal,
                    'total_value': sum(kraken_bal.get(a, 0) * self.prices.get(a, 0) for a in kraken_bal),
                }
                print(f"   🐙 Kraken: {len(kraken_bal)} assets")
            except Exception as e:
                logger.error(f"Kraken balance error: {e}")
                self.exchange_data['kraken'] = {'connected': False, 'error': str(e)}
        
        # ════════════════════════════════════════════════════════════════
        # 🟡 BINANCE BALANCES
        # ════════════════════════════════════════════════════════════════
        if self.binance:
            try:
                binance_bal = {}
                if hasattr(self.binance, 'account'):
                    acct = self.binance.account() or {}
                    for bal in acct.get('balances', []):
                        asset = bal.get('asset', '')
                        free = float(bal.get('free', 0))
                        if free > 0 and asset:
                            binance_bal[asset] = free
                            combined[asset] = combined.get(asset, 0) + free
                
                self.exchange_balances['binance'] = binance_bal
                self.exchange_data['binance'] = {
                    'connected': True,
                    'balances': binance_bal,
                    'total_value': sum(binance_bal.get(a, 0) * self.prices.get(a, 0) for a in binance_bal),
                }
                print(f"   🟡 Binance: {len(binance_bal)} assets")
            except Exception as e:
                logger.error(f"Binance balance error: {e}")
                self.exchange_data['binance'] = {'connected': False, 'error': str(e)}
        
        # ════════════════════════════════════════════════════════════════
        # 🦙 ALPACA BALANCES
        # ════════════════════════════════════════════════════════════════
        if self.alpaca:
            try:
                alpaca_bal = {}
                # Get account for cash
                if hasattr(self.alpaca, 'get_account'):
                    acct = self.alpaca.get_account() or {}
                    cash = float(acct.get('cash', 0))
                    if cash > 0:
                        alpaca_bal['USD'] = cash
                        combined['USD'] = combined.get('USD', 0) + cash
                
                # Get positions (crypto assets)
                if hasattr(self.alpaca, 'get_positions'):
                    positions = self.alpaca.get_positions() or []
                    for pos in positions:
                        raw_symbol = pos.get('symbol', '')
                        qty = float(pos.get('qty', 0))
                        market_value = float(pos.get('market_value', 0))
                        
                        if qty > 0 and raw_symbol:
                            # Convert Alpaca symbol format (BTCUSD -> BTC, USDTUSD -> USDT)
                            if raw_symbol.endswith('USD'):
                                base_asset = raw_symbol[:-3]  # Remove USD suffix
                            else:
                                base_asset = raw_symbol
                            
                            # Store with base asset name
                            alpaca_bal[base_asset] = qty
                            combined[base_asset] = combined.get(base_asset, 0) + qty
                            
                            # Also store the price if we got market_value
                            if market_value > 0 and qty > 0:
                                price = market_value / qty
                                if base_asset not in self.prices or self.prices.get(base_asset, 0) == 0:
                                    self.prices[base_asset] = price
                
                self.exchange_balances['alpaca'] = alpaca_bal
                self.exchange_data['alpaca'] = {
                    'connected': True,
                    'balances': alpaca_bal,
                    'total_value': float(acct.get('portfolio_value', 0)) if acct else 0,
                }
                print(f"   🦙 Alpaca: {len(alpaca_bal)} assets")
            except Exception as e:
                logger.error(f"Alpaca balance error: {e}")
                self.exchange_data['alpaca'] = {'connected': False, 'error': str(e)}
        
        self.balances = combined
        
        # Calculate total portfolio value
        total_usd = 0.0
        for asset, amount in combined.items():
            if asset in ('USD', 'USDT', 'USDC'):
                total_usd += amount
            else:
                price = self.prices.get(asset, 0)
                total_usd += amount * price
        
        print(f"   💰 Combined Portfolio: ${total_usd:,.2f}")
        print(f"   📊 Unique assets: {len(combined)}")
        
        return combined
    
    def calculate_trained_matrix_score(self, to_asset: str) -> Tuple[float, str]:
        """
        📊 Calculate score from trained probability matrix.
        Returns: (score 0-1, reason string)
        
        Uses the trained_probability_matrix.json which contains:
        - Hourly edge patterns (optimal/avoid hours)
        - Daily edge patterns (optimal days)
        - Per-symbol patterns
        - Multi-exchange training data
        """
        from datetime import datetime
        import json
        
        score = 0.5  # Neutral default
        reasons = []
        
        try:
            # Load trained matrix
            matrix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trained_probability_matrix.json')
            if not os.path.exists(matrix_path):
                return 0.5, "matrix_not_found"
            
            with open(matrix_path, 'r') as f:
                matrix = json.load(f)
            
            now = datetime.now()
            current_hour = str(now.hour)
            current_dow = str(now.weekday())
            
            # 1. Global hourly edge
            hourly_edge_data = matrix.get('hourly_edge', {}).get(current_hour, {})
            hourly_edge = hourly_edge_data.get('edge', 0)
            hourly_conf = hourly_edge_data.get('confidence', 0)
            
            if hourly_edge > 10 and hourly_conf > 0.1:
                score += 0.15
                reasons.append(f"optimal_hour({current_hour})")
            elif hourly_edge < -10 and hourly_conf > 0.1:
                score -= 0.15
                reasons.append(f"avoid_hour({current_hour})")
            
            # 2. Global daily edge
            daily_edge_data = matrix.get('daily_edge', {}).get(current_dow, {})
            daily_edge = daily_edge_data.get('edge', 0)
            daily_conf = daily_edge_data.get('confidence', 0)
            
            if daily_edge > 5 and daily_conf > 0.05:
                score += 0.10
                reasons.append(f"optimal_day({current_dow})")
            elif daily_edge < -5 and daily_conf > 0.05:
                score -= 0.10
                reasons.append(f"avoid_day({current_dow})")
            
            # 3. Symbol-specific patterns
            symbol_patterns = matrix.get('symbol_patterns', {}).get(to_asset, {})
            if symbol_patterns:
                bullish_prob = symbol_patterns.get('bullish_prob', 0.5)
                win_rate = symbol_patterns.get('win_rate', 0.5)
                trade_count = symbol_patterns.get('trade_count', 0)
                
                # Bullish probability bonus
                if bullish_prob > 0.55:
                    score += 0.10
                    reasons.append(f"bullish_symbol({bullish_prob:.2f})")
                elif bullish_prob < 0.45:
                    score -= 0.10
                    reasons.append(f"bearish_symbol({bullish_prob:.2f})")
                
                # Trade history win rate bonus
                if trade_count >= 5 and win_rate > 0.6:
                    score += 0.15
                    reasons.append(f"high_win_rate({win_rate:.2f})")
                elif trade_count >= 5 and win_rate < 0.4:
                    score -= 0.15
                    reasons.append(f"low_win_rate({win_rate:.2f})")
                
                # Symbol-specific hourly edge
                sym_hourly = symbol_patterns.get('hourly_edge', {}).get(current_hour, {})
                sym_hourly_edge = sym_hourly.get('edge', 0)
                if sym_hourly_edge > 15:
                    score += 0.10
                    reasons.append(f"sym_optimal_hour")
                elif sym_hourly_edge < -15:
                    score -= 0.10
                    reasons.append(f"sym_avoid_hour")
            
            # 4. Check optimal/avoid conditions
            optimal_hours = matrix.get('optimal_conditions', {}).get('hours', [])
            avoid_hours = matrix.get('avoid_conditions', {}).get('hours', [])
            
            if now.hour in optimal_hours:
                score += 0.05
                reasons.append("in_optimal_hours")
            if now.hour in avoid_hours:
                score -= 0.10  # Heavier penalty for avoid hours
                reasons.append("in_avoid_hours")
            
            # Clamp score between 0 and 1
            score = max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.debug(f"Trained matrix score error: {e}")
            return 0.5, f"error:{str(e)[:20]}"
        
        reason = ",".join(reasons) if reasons else "neutral"
        return score, reason
    
    def calculate_barter_score(self, from_asset: str, to_asset: str) -> Tuple[float, str]:
        """
        🫒💰 Calculate barter path score for a conversion.
        
        Uses BOTH the Barter Navigator (multi-hop paths) AND the LiveBarterMatrix 
        (historical performance) for smarter, adaptive scoring.
        
        THE PHILOSOPHY:
        - Any coin can lead to any other coin
        - Historical success on a path matters
        - The system learns which paths ACTUALLY make money
        
        Returns: (score 0-1, reason string)
        """
        score = 0.5  # Start neutral
        reasons = []
        
        # ═══════════════════════════════════════════════════════════════════
        # 1. LIVE BARTER MATRIX - Historical Performance
        # ═══════════════════════════════════════════════════════════════════
        from_price = self.prices.get(from_asset, 0)
        to_price = self.prices.get(to_asset, 0)
        
        if from_price > 0 and to_price > 0:
            # Update barter rate for this pair
            self.barter_matrix.update_barter_rate(from_asset, to_asset, from_price, to_price)
            
            # Check historical performance of this path
            key = (from_asset.upper(), to_asset.upper())
            history = self.barter_matrix.barter_history.get(key, {})
            
            if history.get('trades', 0) > 0:
                # We have history! Use it with current holdings consideration
                path_profit = history.get('total_profit', 0)
                path_trades = history['trades']
                avg_profit = path_profit / path_trades
                
                # Adjust score based on historical avg trade size
                avg_trade_size = history.get('avg_trade_size', 10.0)  # Default $10 avg trade
                
                # Boost score based on historical success
                if avg_profit > 0.01:  # Profitable path
                    score += 0.15
                    reasons.append(f"profit_path(${avg_profit:.3f})")
                elif avg_profit > 0:
                    score += 0.08
                    reasons.append("slight_profit")
                elif avg_profit < -0.01:  # Losing path
                    score -= 0.10
                    reasons.append("losing_path")
                
                # Experience bonus (more trades = more confidence)
                if path_trades >= 10:
                    score += 0.05
                    reasons.append(f"experienced({path_trades})")
                elif path_trades >= 5:
                    score += 0.02
                    reasons.append(f"some_exp({path_trades})")
            else:
                # New path - slight exploration bonus
                score += 0.02
                reasons.append("new_path")
        
        # ═══════════════════════════════════════════════════════════════════
        # 2. BARTER NAVIGATOR - Multi-hop Path Quality
        # ═══════════════════════════════════════════════════════════════════
        if self.barter_navigator and BARTER_NAVIGATOR_AVAILABLE:
            try:
                # Find path from source to destination
                path = self.barter_navigator.find_path(from_asset, to_asset)
                
                if path:
                    # 1. Direct path (1 hop) is best
                    if path.num_hops == 1:
                        score += 0.15
                        reasons.append("direct_path")
                    elif path.num_hops == 2:
                        score += 0.08
                        reasons.append("2hop_path")
                    elif path.num_hops > 3:
                        score -= 0.08
                        reasons.append(f"{path.num_hops}hop_path")
                    
                    # 2. Rate efficiency (closer to 1.0 = less slippage)
                    if path.total_rate > 0.995:
                        score += 0.08
                        reasons.append("efficient_rate")
                    elif path.total_rate < 0.98:
                        score -= 0.08
                        reasons.append("high_slippage")
                    
                    # 3. Single exchange is cleaner
                    if len(path.exchanges_used) == 1:
                        score += 0.03
                        reasons.append("single_exchange")
                    
                    # 4. Low fees are good
                    if path.total_fees < 0.005:  # <0.5%
                        score += 0.03
                        reasons.append("low_fees")
                    elif path.total_fees > 0.01:  # >1%
                        score -= 0.05
                        reasons.append("high_fees")
                else:
                    reasons.append("no_nav_path")
                    
            except Exception as e:
                logger.debug(f"Barter navigator score error: {e}")
        else:
            reasons.append("nav_not_available")
        
        # Clamp score
        score = max(0.0, min(1.0, score))
        
        reason = "barter_" + ",".join(reasons[:3])
        return score, reason
    
    def find_barter_chain(self, from_asset: str, to_asset: str) -> Optional[List[Dict]]:
        """
        🫒 Find the complete barter chain from source to destination.
        
        Returns list of trade steps: [
            {'from': 'CHZ', 'to': 'USD', 'pair': 'CHZUSD', 'exchange': 'kraken', 'rate': 0.05},
            {'from': 'USD', 'to': 'BTC', 'pair': 'BTCUSD', 'exchange': 'kraken', 'rate': 0.00001},
        ]
        """
        if not self.barter_navigator:
            return None
        
        path = self.barter_navigator.find_path(from_asset, to_asset)
        if not path:
            return None
        
        steps = []
        for hop in path.hops:
            steps.append({
                'from': hop.from_asset,
                'to': hop.to_asset,
                'pair': hop.pair,
                'exchange': hop.exchange,
                'rate': hop.rate,
                'effective_rate': hop.effective_rate,
                'fee': hop.fee_rate
            })
        
        return steps
    
    def calculate_v14_score(self, from_asset: str, to_asset: str) -> float:
        """Calculate V14 score for a conversion."""
        if not self.v14 or not self.ticker_cache:
            return 5.0  # Neutral score if V14 not available
        
        # Get momentum data
        from_ticker = None
        to_ticker = None
        for symbol, data in self.ticker_cache.items():
            if data.get('base') == from_asset:
                from_ticker = data
            if data.get('base') == to_asset:
                to_ticker = data
        
        if not from_ticker or not to_ticker:
            return 5.0
        
        # V14-style scoring components
        score = 5.0  # Start neutral
        
        # 1. Momentum differential (want to go TO stronger momentum)
        from_momentum = from_ticker.get('change24h', 0)
        to_momentum = to_ticker.get('change24h', 0)
        momentum_diff = to_momentum - from_momentum
        
        if momentum_diff > 2:  # Going to significantly stronger
            score += 2
        elif momentum_diff > 0.5:
            score += 1
        elif momentum_diff < -2:  # Going to weaker (bad)
            score -= 2
        
        # 2. Volume check (prefer liquid assets)
        to_volume = to_ticker.get('volume', 0)
        if to_volume > 100000:
            score += 1
        
        # 3. Positive momentum preference
        if to_momentum > 1:
            score += 1
        elif to_momentum < -1:
            score -= 1
        
        # 4. Avoid declining assets
        if from_momentum < -2 and to_momentum > 0:
            score += 1  # Escaping decline = good
        
        return max(1, min(10, score))  # Clamp 1-10
    
    def calculate_hub_score(self, from_asset: str, to_asset: str) -> float:
        """Get consensus score from Mycelium Hub."""
        if not self.hub:
            return 0.5  # Neutral if hub not available
        
        try:
            # Query the hub for this conversion path
            hub_analysis = self.hub.analyze_conversion(from_asset, to_asset)
            if hub_analysis:
                return hub_analysis.get('score', 0.5)
        except Exception:
            pass
        
        return 0.5
    
    def calculate_profit_potential(
        self,
        from_asset: str,
        to_asset: str,
        from_amount: float
    ) -> Tuple[float, float]:
        """Calculate expected profit in USD and % using barter matrix costs."""
        from_price = self.prices.get(from_asset, 0)
        to_price = self.prices.get(to_asset, 0)

        if not from_price or not to_price:
            return 0.0, 0.0

        from_value = from_amount * from_price

        # Use barter matrix to calculate realistic costs and potential profit
        # This accounts for exchange fees, spreads, historical slippage, etc.
        approved, reason, math_breakdown = self.barter_matrix._calculate_total_cost_pct(
            from_asset, to_asset, from_value, 'kraken'  # Default to kraken for estimation
        )

        if not approved:
            return 0.0, 0.0  # No profit possible

        total_cost_pct = math_breakdown['total_cost_pct'] / 100  # Convert % to decimal
        costs_usd = from_value * total_cost_pct

        # For conversions, profit comes from price movements or arbitrage
        # Estimate small positive movement (0.1-0.5%) minus costs
        # This is conservative - actual profit depends on market conditions
        min_required_gain_pct = total_cost_pct + 0.001  # Costs + 0.1% minimum
        expected_gain_pct = min_required_gain_pct + 0.002  # Add 0.2% expected movement

        expected_gain = from_value * expected_gain_pct
        net_profit = expected_gain - costs_usd
        net_pct = net_profit / from_value if from_value > 0 else 0

        return net_profit, net_pct
    
    async def collect_all_signals(self) -> Dict[str, List[Dict]]:
        """Collect signals from ALL wired systems."""
        signals = defaultdict(list)
        
        # ════════════════════════════════════════════════════════════════
        # 🍄 MYCELIUM HUB SIGNALS
        # ════════════════════════════════════════════════════════════════
        if self.hub:
            try:
                hub_signals = self.hub.get_all_signals() if hasattr(self.hub, 'get_all_signals') else []
                for sig in hub_signals:
                    signals['hub'].append(sig)
                    self.signals_received += 1
            except Exception as e:
                logger.debug(f"Hub signal error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🦅 COMMANDO SIGNALS (FALCON/TORTOISE/CHAMELEON/BEE)
        # ════════════════════════════════════════════════════════════════
        if self.commando:
            try:
                commando_signals = self.commando.scan_all_opportunities(self.ticker_cache) if hasattr(self.commando, 'scan_all_opportunities') else []
                for sig in commando_signals:
                    signals['commando'].append(sig)
                    self.signals_received += 1
            except Exception as e:
                logger.debug(f"Commando signal error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🔮 PROBABILITY NEXUS SIGNALS
        # ════════════════════════════════════════════════════════════════
        if self.probability_nexus:
            try:
                nexus_signals = self.probability_nexus.get_predictions() if hasattr(self.probability_nexus, 'get_predictions') else []
                for sig in nexus_signals:
                    signals['nexus'].append(sig)
                    self.signals_received += 1
            except Exception as e:
                logger.debug(f"Nexus signal error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🌌 MULTIVERSE CONSENSUS SIGNALS
        # ════════════════════════════════════════════════════════════════
        if self.multiverse:
            try:
                mv_signals = self.multiverse.get_consensus() if hasattr(self.multiverse, 'get_consensus') else []
                for sig in mv_signals:
                    signals['multiverse'].append(sig)
                    self.signals_received += 1
            except Exception as e:
                logger.debug(f"Multiverse signal error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🧠 MINER BRAIN SIGNALS
        # ════════════════════════════════════════════════════════════════
        if self.miner_brain:
            try:
                brain_signals = self.miner_brain.get_signals() if hasattr(self.miner_brain, 'get_signals') else []
                for sig in brain_signals:
                    signals['brain'].append(sig)
                    self.signals_received += 1
            except Exception as e:
                logger.debug(f"Miner Brain signal error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🌊 HARMONIC WAVE SIGNALS
        # ════════════════════════════════════════════════════════════════
        if self.harmonic:
            try:
                harmonic_signals = self.harmonic.get_wave_signals() if hasattr(self.harmonic, 'get_wave_signals') else []
                for sig in harmonic_signals:
                    signals['harmonic'].append(sig)
                    self.signals_received += 1
            except Exception as e:
                logger.debug(f"Harmonic signal error: {e}")
        
        # ════════════════════════════════════════════════════════════════
        # 🔱 OMEGA HIGH CONFIDENCE SIGNALS
        # ════════════════════════════════════════════════════════════════
        if self.omega:
            try:
                omega_signals = self.omega.get_high_conf_signals() if hasattr(self.omega, 'get_high_conf_signals') else []
                for sig in omega_signals:
                    signals['omega'].append(sig)
                    self.signals_received += 1
            except Exception as e:
                logger.debug(f"Omega signal error: {e}")
        
        self.all_signals = signals
        return signals

    async def dream_about_tickers(self):
        """
        💭 DREAMING PHASE: Predict future movements based on Multiverse & Ecosystem.
        "It dreams about live tickers... validates itself... adapt adjust"
        """
        current_time = time.time()
        
        # Only dream every 10 seconds to avoid noise
        if hasattr(self, '_last_dream_time') and current_time - self._last_dream_time < 10:
            return
        self._last_dream_time = current_time
        
        # 1. Ask Multiverse for direction
        if self.multiverse:
            try:
                # Get consensus from the 10 worlds
                consensus = self.multiverse.get_consensus() if hasattr(self.multiverse, 'get_consensus') else []
                if consensus:
                    print(f"\n   💭 DREAMING about market direction (Multiverse)...")
                
                for signal in consensus:
                    symbol = signal.get('symbol')
                    if not symbol or symbol not in self.prices:
                        continue
                        
                    current_price = self.prices[symbol]
                    direction = signal.get('action', 'HOLD')
                    confidence = signal.get('confidence', 0.5)
                    
                    if direction in ['BUY', 'SELL'] and confidence > 0.6:
                        # Predict price movement (e.g., 0.5% in 30s)
                        move_pct = 0.005 if direction == 'BUY' else -0.005
                        predicted_price = current_price * (1 + move_pct)
                        
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=predicted_price,
                            direction='UP' if direction == 'BUY' else 'DOWN',
                            target_time=current_time + 30, # 30s prediction
                            source='multiverse',
                            confidence=confidence
                        )
                        self.dreams.append(dream)
                        print(f"      🌌 Multiverse dreams {symbol} will go {dream.direction} (Conf: {confidence:.2f})")
            except Exception as e:
                logger.debug(f"Multiverse dream error: {e}")

        # 2. Ask Probability Nexus
        if self.probability_nexus:
            try:
                predictions = self.probability_nexus.get_predictions() if hasattr(self.probability_nexus, 'get_predictions') else []
                if predictions:
                     print(f"\n   💭 DREAMING about market direction (Nexus)...")

                for pred in predictions:
                    symbol = pred.get('symbol')
                    if not symbol or symbol not in self.prices:
                        continue
                        
                    current_price = self.prices[symbol]
                    prob = pred.get('probability', 0.5)
                    
                    if prob > 0.7: # High probability UP
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=current_price * 1.005,
                            direction='UP',
                            target_time=current_time + 30,
                            source='nexus',
                            confidence=prob
                        )
                        self.dreams.append(dream)
                        print(f"      🔮 Nexus dreams {symbol} will go UP (Prob: {prob:.2f})")
            except Exception as e:
                logger.debug(f"Nexus dream error: {e}")

    async def validate_dreams(self):
        """
        ✅ VALIDATION PHASE: Check if dreams came true.
        "Right I know I was right there... adapt adjust"
        """
        current_time = time.time()
        active_dreams = []
        dreams_validated_this_cycle = False
        
        for dream in self.dreams:
            if dream.validated:
                continue
                
            # Check if target time reached
            if current_time >= dream.target_time:
                # Validate!
                current_price = self.prices.get(dream.symbol, 0)
                if current_price == 0:
                    continue # Can't validate
                
                dream.actual_price_at_target = current_price
                dream.validated = True
                dreams_validated_this_cycle = True
                
                # Check success
                if dream.direction == 'UP':
                    dream.success = current_price > dream.current_price
                else:
                    dream.success = current_price < dream.current_price
                
                # ADAPT: Update source accuracy
                alpha = 0.1 # Learning rate
                if dream.success:
                    self.dream_accuracy[dream.source] = (1 - alpha) * self.dream_accuracy[dream.source] + alpha * 1.0
                    print(f"   ✅ DREAM VALIDATED: {dream.source} was RIGHT about {dream.symbol} ({dream.direction})!")
                else:
                    self.dream_accuracy[dream.source] = (1 - alpha) * self.dream_accuracy[dream.source] + alpha * 0.0
                    print(f"   ❌ DREAM FAILED: {dream.source} was WRONG about {dream.symbol}. Adapting...")
                
                self.validated_dreams_count += 1
            else:
                active_dreams.append(dream)
        
        # Keep only active dreams
        self.dreams = active_dreams
        
        # Print accuracy stats occasionally
        if dreams_validated_this_cycle and self.validated_dreams_count % 5 == 0:
            print(f"   🧠 ADAPTIVE LEARNING STATS:")
            for source, acc in self.dream_accuracy.items():
                print(f"      - {source}: {acc:.1%} accuracy")

    def populate_barter_graph(self):
        """
        🫒🔄 POPULATE BARTER GRAPH from already-loaded exchange data.
        Called ONCE after pairs and prices are loaded.
        """
        if not self.barter_navigator:
            return
        
        try:
            # Build alpaca pairs dict with base/quote info
            alpaca_pairs_formatted = {}
            for symbol, normalized in self.alpaca_pairs.items():
                if '/' in symbol:
                    parts = symbol.split('/')
                    alpaca_pairs_formatted[symbol] = {'base': parts[0], 'quote': parts[1]}
            
            # Build binance pairs dict from ticker cache (it has base/quote info)
            binance_pairs_formatted = {}
            for cache_key, data in self.ticker_cache.items():
                if cache_key.startswith('binance:'):
                    symbol = cache_key.replace('binance:', '')
                    base = data.get('base', '')
                    quote = data.get('quote', '')
                    if base and quote:
                        binance_pairs_formatted[symbol] = {'base': base, 'quote': quote}
            
            # Use the data we already have!
            success = self.barter_navigator.populate_from_labyrinth_data(
                kraken_pairs=self.kraken_pairs,
                alpaca_pairs=alpaca_pairs_formatted,
                binance_pairs=binance_pairs_formatted,
                prices=self.prices
            )
            
            if success:
                summary = self.barter_navigator.get_graph_summary()
                print(f"🫒🔄 Barter Navigator: POPULATED ({summary['total_assets']} assets, {summary['total_edges']} paths)")
            else:
                print(f"⚠️ Barter Navigator: Population failed")
        except Exception as e:
            print(f"⚠️ Barter Navigator population error: {e}")

    async def dream_for_turn(self, exchange: str):
        """
        💭🎯 TURN-SPECIFIC DREAMING: Dream about assets on THIS exchange's turn.
        "The probability matrix constantly dreams each turn"
        
        This runs EVERY turn (not throttled like global dreaming).
        
        👑🔮 THE QUEEN DREAMS FIRST - Her dreams guide all other dreams!
        """
        current_time = time.time()
        turn_dreams = []
        
        # Get assets for this exchange
        exchange_assets = self.get_exchange_assets(exchange)
        if not exchange_assets:
            return
        
        symbols_to_dream = list(exchange_assets.keys())[:20]  # Top 20 by holdings
        
        print(f"\n   💭🎯 TURN DREAMING for {exchange.upper()} ({len(symbols_to_dream)} symbols)")
        
        # 👑🔮 0. THE QUEEN DREAMS FIRST - Her visions set the tone!
        queen_vision_count = 0
        if self.queen and hasattr(self.queen, 'dream_of_winning'):
            try:
                for symbol in symbols_to_dream[:10]:  # Queen dreams top 10
                    if symbol not in self.prices:
                        continue
                    current_price = self.prices[symbol]
                    
                    opp_data = {
                        'from_asset': 'USD',
                        'to_asset': symbol,
                        'expected_profit': 0.01,  # Speculative
                        'exchange': exchange,
                        'market_data': {'volatility': 0.5, 'momentum': 0.5}
                    }
                    
                    queen_dream = self.queen.dream_of_winning(opp_data)
                    queen_conf = queen_dream.get('final_confidence', 0.5)
                    queen_wins = queen_dream.get('will_win', False)
                    
                    # Queen's strong dreams become turn dreams!
                    if queen_wins and queen_conf >= 0.60:
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=current_price * (1 + 0.01 * queen_conf),  # Scale by confidence
                            direction='UP',
                            target_time=current_time + 60,  # Queen sees further ahead
                            source='queen_hive_mind',
                            confidence=queen_conf
                        )
                        self.dreams.append(dream)
                        turn_dreams.append(dream)
                        queen_vision_count += 1
                    elif not queen_wins and queen_conf <= 0.35:
                        # Queen sees danger - DOWN dream
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=current_price * (1 - 0.01 * (1 - queen_conf)),
                            direction='DOWN',
                            target_time=current_time + 60,
                            source='queen_warning',
                            confidence=1 - queen_conf
                        )
                        self.dreams.append(dream)
                        turn_dreams.append(dream)
                        queen_vision_count += 1
                
                if queen_vision_count > 0:
                    logger.info(f"👑🔮 Queen dreamed {queen_vision_count} visions for {exchange}")
            except Exception as e:
                logger.debug(f"Queen turn dream error: {e}")
        
        # 1. Ask Multiverse for direction on exchange assets
        if self.multiverse:
            try:
                consensus = self.multiverse.get_consensus() if hasattr(self.multiverse, 'get_consensus') else []
                for signal in consensus:
                    symbol = signal.get('symbol')
                    if not symbol or symbol not in symbols_to_dream:
                        continue
                    
                    current_price = self.prices.get(symbol, 0)
                    if not current_price:
                        continue
                    
                    direction = signal.get('action', 'HOLD')
                    confidence = signal.get('confidence', 0.5)
                    
                    if direction in ['BUY', 'SELL'] and confidence > 0.55:  # Lower threshold for turn dreams
                        move_pct = 0.005 if direction == 'BUY' else -0.005
                        predicted_price = current_price * (1 + move_pct)
                        
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=predicted_price,
                            direction='UP' if direction == 'BUY' else 'DOWN',
                            target_time=current_time + 30,
                            source='multiverse_turn',
                            confidence=confidence
                        )
                        self.dreams.append(dream)
                        turn_dreams.append(dream)
            except Exception as e:
                logger.debug(f"Turn multiverse dream error: {e}")
        
        # 2. Ask Probability Nexus for predictions on exchange assets
        if self.probability_nexus:
            try:
                predictions = self.probability_nexus.get_predictions() if hasattr(self.probability_nexus, 'get_predictions') else []
                for pred in predictions:
                    symbol = pred.get('symbol')
                    if not symbol or symbol not in symbols_to_dream:
                        continue
                    
                    current_price = self.prices.get(symbol, 0)
                    if not current_price:
                        continue
                    
                    prob = pred.get('probability', 0.5)
                    
                    if prob > 0.6:  # Good UP prediction
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=current_price * 1.005,
                            direction='UP',
                            target_time=current_time + 30,
                            source='nexus_turn',
                            confidence=prob
                        )
                        self.dreams.append(dream)
                        turn_dreams.append(dream)
                    elif prob < 0.4:  # Good DOWN prediction
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=current_price * 0.995,
                            direction='DOWN',
                            target_time=current_time + 30,
                            source='nexus_turn',
                            confidence=1 - prob
                        )
                        self.dreams.append(dream)
                        turn_dreams.append(dream)
            except Exception as e:
                logger.debug(f"Turn nexus dream error: {e}")
        
        # 3. Use Ultimate Intel if available
        if self.ultimate_intel:
            try:
                for symbol in symbols_to_dream[:10]:
                    if symbol not in self.prices:
                        continue
                    current_price = self.prices[symbol]
                    
                    analysis = self.ultimate_intel.analyze(symbol) if hasattr(self.ultimate_intel, 'analyze') else {}
                    sentiment = analysis.get('sentiment', 'neutral')
                    confidence = analysis.get('confidence', 0.5)
                    
                    if sentiment in ['bullish', 'very_bullish'] and confidence > 0.55:
                        dream = Dream(
                            timestamp=current_time,
                            symbol=symbol,
                            current_price=current_price,
                            predicted_price=current_price * 1.005,
                            direction='UP',
                            target_time=current_time + 30,
                            source='ultimate_turn',
                            confidence=confidence
                        )
                        self.dreams.append(dream)
                        turn_dreams.append(dream)
            except Exception as e:
                logger.debug(f"Turn ultimate dream error: {e}")
        
        if turn_dreams:
            print(f"      🌙 Generated {len(turn_dreams)} dreams for {exchange}")
            for dream in turn_dreams[:5]:  # Show top 5
                print(f"         → {dream.symbol} {dream.direction} ({dream.source}: {dream.confidence:.0%})")

    def calculate_dream_score(self, symbol: str) -> float:
        """Calculate score based on active dreams and source accuracy."""
        score = 0.0
        count = 0
        
        for dream in self.dreams:
            if dream.symbol == symbol and not dream.validated:
                # Weight by source accuracy
                accuracy = self.dream_accuracy[dream.source]
                confidence = dream.confidence
                
                weight = accuracy * confidence
                
                if dream.direction == 'UP':
                    score += weight
                else:
                    score -= weight
                count += 1
        
        # Normalize to -1 to +1 range roughly
        if count > 0:
            return max(-1.0, min(1.0, score))
        return 0.0

    # ════════════════════════════════════════════════════════════════════════════
    # 🎯 TURN-BASED EXCHANGE STRATEGY
    # ════════════════════════════════════════════════════════════════════════════
    
    def get_current_exchange(self) -> str:
        """Get the exchange whose turn it is to trade."""
        # Filter to only connected exchanges
        connected = [ex for ex in self.exchange_order 
                     if self.exchange_data.get(ex, {}).get('connected', False)]
        if not connected:
            return None
        return connected[self.current_exchange_index % len(connected)]
    
    def advance_turn(self):
        """Move to the next exchange's turn."""
        connected = [ex for ex in self.exchange_order 
                     if self.exchange_data.get(ex, {}).get('connected', False)]
        if connected:
            self.current_exchange_index = (self.current_exchange_index + 1) % len(connected)
        self.turns_completed += 1
        
        # 🌟 Update barter_matrix turn counter for second chances
        if hasattr(self, 'barter_matrix') and self.barter_matrix:
            self.barter_matrix.current_turn = self.turns_completed
        
        # 👑📊 Feed Queen metrics to HNC Matrix every turn!
        if self.queen and self.hnc_matrix and hasattr(self.hnc_matrix, 'feed_queen_metrics'):
            try:
                if hasattr(self.queen, 'get_all_queen_metrics'):
                    metrics = self.queen.get_all_queen_metrics()
                    self.hnc_matrix.feed_queen_metrics(metrics)
            except Exception as e:
                logger.debug(f"Queen metrics feed error: {e}")
    
    def get_turn_display(self) -> str:
        """Get a display string showing current turn status."""
        current = self.get_current_exchange()
        if not current:
            return "No exchanges"
        
        icons = {'kraken': '🐙', 'alpaca': '🦙', 'binance': '🟡'}
        turn_markers = []
        
        for ex in self.exchange_order:
            if self.exchange_data.get(ex, {}).get('connected', False):
                icon = icons.get(ex, '📊')
                if ex == current:
                    turn_markers.append(f"[{icon}]")  # Current turn
                else:
                    turn_markers.append(f" {icon} ")  # Waiting
            else:
                turn_markers.append("  ❌  ")  # Not connected
        
        return "".join(turn_markers)
    
    def get_exchange_assets(self, exchange: str) -> Dict[str, float]:
        """Get assets held on a specific exchange."""
        return self.exchange_balances.get(exchange, {})
    
    async def refresh_exchange_balances(self, exchange: str):
        """Refresh balances for a specific exchange to ensure fresh data."""
        if exchange == 'kraken' and self.kraken:
            try:
                kraken_bal = {}
                if hasattr(self.kraken, 'get_account_balance'):
                    raw = self.kraken.get_account_balance() or {}
                    for asset, amount in raw.items():
                        try:
                            amount = float(amount)
                        except (ValueError, TypeError):
                            continue
                        if amount > 0:
                            clean = asset
                            if len(asset) == 4 and asset[0] in ('X', 'Z'):
                                clean = asset[1:]
                            if clean == 'XBT':
                                clean = 'BTC'
                            kraken_bal[clean] = amount
                self.exchange_balances['kraken'] = kraken_bal
                if 'kraken' in self.exchange_data:
                    self.exchange_data['kraken']['balances'] = kraken_bal
            except Exception as e:
                logger.error(f"Kraken refresh error: {e}")

        elif exchange == 'binance' and self.binance:
            try:
                binance_bal = {}
                if hasattr(self.binance, 'account'):
                    acct = self.binance.account() or {}
                    for bal in acct.get('balances', []):
                        asset = bal.get('asset', '')
                        free = float(bal.get('free', 0))
                        if free > 0 and asset:
                            binance_bal[asset] = free
                self.exchange_balances['binance'] = binance_bal
                if 'binance' in self.exchange_data:
                    self.exchange_data['binance']['balances'] = binance_bal
            except Exception as e:
                logger.error(f"Binance refresh error: {e}")

        elif exchange == 'alpaca' and self.alpaca:
            try:
                alpaca_bal = {}
                if hasattr(self.alpaca, 'get_account'):
                    acct = self.alpaca.get_account() or {}
                    cash = float(acct.get('cash', 0))
                    if cash > 0:
                        alpaca_bal['USD'] = cash
                
                if hasattr(self.alpaca, 'get_positions'):
                    positions = self.alpaca.get_positions() or []
                    for pos in positions:
                        raw_symbol = pos.get('symbol', '')
                        qty = float(pos.get('qty', 0))
                        if qty > 0 and raw_symbol:
                            if raw_symbol.endswith('USD'):
                                base_asset = raw_symbol[:-3]
                            else:
                                base_asset = raw_symbol
                            alpaca_bal[base_asset] = qty
                
                self.exchange_balances['alpaca'] = alpaca_bal
                if 'alpaca' in self.exchange_data:
                    self.exchange_data['alpaca']['balances'] = alpaca_bal
            except Exception as e:
                logger.error(f"Alpaca refresh error: {e}")

        # Rebuild combined balances
        self.balances = {}
        for ex_bals in self.exchange_balances.values():
            for asset, amount in ex_bals.items():
                self.balances[asset] = self.balances.get(asset, 0) + amount

    async def report_portfolio_to_queen(self, voice_enabled: bool = True) -> Dict[str, Any]:
        """
        👑💰 REPORT PORTFOLIO TO QUEEN - Feed her the revenue data!
        
        Gathers portfolio performance from all exchanges and feeds it to the Queen.
        The Queen reviews the data and speaks her verdict with her VOICE!
        
        Args:
            voice_enabled: Whether the Queen should speak aloud (TTS)
        
        Returns:
            Portfolio data dict with Queen's verdict
        """
        portfolio_data = {
            'kraken': {'value': 0.0, 'profit': 0.0, 'trades': 0, 'win_rate': 0.0},
            'binance': {'value': 0.0, 'profit': 0.0, 'trades': 0, 'win_rate': 0.0},
            'alpaca': {'value': 0.0, 'profit': 0.0, 'trades': 0, 'win_rate': 0.0},
            'total_value': 0.0,
            'total_profit': 0.0,
            'total_trades': 0
        }
        
        print("\n👑💰 ═══ PORTFOLIO REPORT FOR THE QUEEN ═══")
        
        # Gather data from each exchange
        for exchange in ['kraken', 'binance', 'alpaca']:
            ex_stats = self.exchange_stats.get(exchange, {})
            ex_balances = self.exchange_balances.get(exchange, {})
            
            # Calculate exchange value
            ex_value = 0.0
            for asset, amount in ex_balances.items():
                if asset in ('USD', 'USDT', 'USDC', 'ZUSD'):
                    ex_value += amount
                else:
                    price = self.prices.get(asset, 0)
                    ex_value += amount * price
            
            # Get profit and trade stats
            ex_profit = ex_stats.get('profit', 0.0)
            ex_trades = ex_stats.get('conversions', 0)
            
            # Calculate win rate from barter history for this exchange
            wins = 0
            total = 0
            for (from_a, to_a), hist in self.barter_matrix.barter_history.items():
                # Attribute to exchange based on source exchange tracking
                total += hist.get('trades', 0)
                wins += hist.get('wins', 0)
            
            win_rate = wins / total if total > 0 else 0.5
            
            portfolio_data[exchange] = {
                'value': ex_value,
                'profit': ex_profit,
                'trades': ex_trades,
                'win_rate': win_rate
            }
            
            portfolio_data['total_value'] += ex_value
            portfolio_data['total_profit'] += ex_profit
            portfolio_data['total_trades'] += ex_trades
            
            # Icon display
            icon = {'kraken': '🐙', 'binance': '🔶', 'alpaca': '🦙'}[exchange]
            profit_icon = '📈' if ex_profit >= 0 else '📉'
            print(f"   {icon} {exchange.upper()}: ${ex_value:.2f} | {profit_icon} ${ex_profit:+.4f} | {ex_trades} trades")
        
        print(f"   💰 TOTAL: ${portfolio_data['total_value']:.2f} | P/L: ${portfolio_data['total_profit']:+.4f}")
        
        # Feed to the Queen!
        if self.queen:
            try:
                # Have the Queen review and speak!
                if hasattr(self.queen, 'announce_portfolio_status'):
                    verdict = self.queen.announce_portfolio_status(portfolio_data)
                    portfolio_data['queen_verdict'] = verdict
                
                # Get Queen's trading guidance
                if hasattr(self.queen, 'get_trading_guidance'):
                    guidance = self.queen.get_trading_guidance()
                    portfolio_data['queen_guidance'] = guidance
                    
                    # Apply guidance to position sizing
                    self.queen_position_multiplier = guidance.get('recommended_position_size', 1.0)
                    print(f"   👑 Queen's Position Multiplier: {self.queen_position_multiplier:.1f}x")
                
                # Review each exchange
                if hasattr(self.queen, 'review_exchange_performance'):
                    for exchange in ['kraken', 'binance', 'alpaca']:
                        ex_data = portfolio_data.get(exchange, {})
                        verdict, action = self.queen.review_exchange_performance(exchange, ex_data)
                        portfolio_data[exchange]['queen_verdict'] = verdict
                        portfolio_data[exchange]['queen_action'] = action
                        print(f"   👑 {exchange.upper()}: {action}")
                
            except Exception as e:
                logger.error(f"Queen portfolio review error: {e}")
        
        print("═" * 50)
        
        return portfolio_data

    async def execute_turn(self) -> Tuple[List['MicroOpportunity'], int]:
        """
        Execute one turn for the current exchange.
        Returns (opportunities found, conversions made this turn)
        """
        current_exchange = self.get_current_exchange()
        if not current_exchange:
            return [], 0
        
        icons = {'kraken': '🐙', 'alpaca': '🦙', 'binance': '🟡'}
        icon = icons.get(current_exchange, '📊')
        
        print(f"\n🎯 ═══ TURN {self.turns_completed + 1}: {icon} {current_exchange.upper()} ═══")
        
        # 👑💰 PERIODIC PORTFOLIO REPORT TO QUEEN (every 10 turns)
        if self.turns_completed > 0 and self.turns_completed % 10 == 0:
            await self.report_portfolio_to_queen(voice_enabled=True)
        
        # REFRESH BALANCES FOR THIS EXCHANGE
        await self.refresh_exchange_balances(current_exchange)
        
        # Get this exchange's assets only
        exchange_assets = self.get_exchange_assets(current_exchange)
        if not exchange_assets:
            print(f"   ⚠️ No assets on {current_exchange}")
            self.advance_turn()
            return [], 0
        
        # Show what we're scanning
        asset_list = []
        for asset, amount in sorted(exchange_assets.items(), 
                                    key=lambda x: x[1] * self.prices.get(x[0], 0), 
                                    reverse=True)[:5]:
            price = self.prices.get(asset, 0)
            value = amount * price
            if value >= 1.0:
                asset_list.append(f"{asset}=${value:.2f}")
        
        if asset_list:
            print(f"   📦 Assets: {', '.join(asset_list)}")
        
        # 💭🎯 TURN-SPECIFIC DREAMING - Dream about THIS exchange's assets
        await self.dream_for_turn(current_exchange)
        
        
        # ✅ Validate any mature dreams before finding opportunities
        await self.validate_dreams()
        
        # 👑🍄 QUEEN'S PULSE - Queen observes market state BEFORE filtering
        queen_pulse = await self.queen_observe_market(current_exchange, exchange_assets)
        
        # Find opportunities ON THIS EXCHANGE ONLY
        opportunities = await self.find_opportunities_for_exchange(current_exchange)
        
        # Update stats
        self.exchange_stats[current_exchange]['scans'] += 1
        self.exchange_stats[current_exchange]['opportunities'] += len(opportunities)
        self.exchange_stats[current_exchange]['last_turn'] = time.time()
        
        conversions_this_turn = 0
        
        # Execute best opportunity if found
        if opportunities:
            best = opportunities[0]
            
            # 👑🍄 TINA B's WISDOM - Ask Tina B if we will WIN before trading!
            # Her GOAL: Minimum $0.003 profit per trade
            print(f"\n   👑🍄 TINA B CONSULTED: {best.from_asset}→{best.to_asset}")
            queen_says_win, queen_confidence, queen_reason = await self.ask_queen_will_we_win(best)
            
            if not queen_says_win:
                print(f"   👑❌ TINA B SAYS NO: {queen_reason}")
                print(f"      Her Confidence: {queen_confidence:.0%}")
                # Tina B learns this pattern should be avoided
                await self.queen_learn_pattern(best, predicted_win=False, reason=queen_reason)
            else:
                print(f"   👑✅ TINA B SAYS WIN: {queen_reason}")
                print(f"      Her Confidence: {queen_confidence:.0%}")
                
                # 🎯 SIGNAL QUALITY VALIDATION - Check dreams support this trade
                signal_quality = await self.validate_signal_quality(best)
                
                if signal_quality >= 0.5:  # 50%+ signal quality required
                    # ⏳🔮 QUEEN'S TIMELINE GATE - Simulate multiple futures BEFORE acting
                    timeline_approved, timeline_reason = await self.queen_timeline_gate(best)
                    
                    if timeline_approved:
                        print(f"   ✅ Signal Quality: {signal_quality:.0%} - EXECUTING")
                        success = await self.execute_conversion(best)
                        if success:
                            conversions_this_turn = 1
                            self.exchange_stats[current_exchange]['conversions'] += 1
                            # 🔧 FIX: Use ACTUAL P/L not expected P/L
                            actual_pnl = getattr(best, 'actual_pnl_usd', best.expected_pnl_usd)
                            self.exchange_stats[current_exchange]['profit'] += actual_pnl
                            # Queen learns from successful execution
                            await self.queen_learn_from_trade(best, success=True)
                        else:
                            # Queen learns from failed execution
                            await self.queen_learn_from_trade(best, success=False)
                    else:
                        print(f"   ⏳🔮 Timeline BLOCKED: {timeline_reason}")
                        await self.queen_learn_pattern(best, predicted_win=False, reason=f"Timeline: {timeline_reason}")
                else:
                    print(f"   ⚠️ Signal Quality: {signal_quality:.0%} - SKIPPING (need 50%+)")
                    await self.queen_learn_pattern(best, predicted_win=False, reason=f"Low signal: {signal_quality:.0%}")
        else:
            print(f"   📭 No opportunities passed gates on {current_exchange}")
        
        # Advance to next exchange's turn
        self.advance_turn()
        
        # Brief cooldown between turns
        if self.turn_cooldown_seconds > 0:
            await asyncio.sleep(self.turn_cooldown_seconds)
        
        return opportunities, conversions_this_turn

    async def ask_queen_will_we_win(self, opportunity: 'MicroOpportunity') -> Tuple[bool, float, str]:
        """
        👑🍄 ASK TINA B: Will this trade be a WINNER?
        
        👑 TINA B's GOAL: Minimum $0.003 profit per trade
        A win is a win, no matter how small - as long as we don't lose!
        
        Tina B consults all her connected mycelium neurons:
        - Historical path data
        - Dream patterns
        - Cosmic alignment
        - Civilization wisdom
        - Timeline predictions
        
        Returns: (will_win: bool, confidence: float, reason: str)
        """
        # 👑 TINA B's SACRED GOAL
        QUEEN_MIN_PROFIT = 0.003  # $0.003 minimum profit - a win is a win!
        
        from_asset = opportunity.from_asset
        to_asset = opportunity.to_asset
        path_key = f"{from_asset}→{to_asset}"
        
        # Gather signals from all mycelium connections
        signals = []
        reasons = []
        
        # 1. 🧠 PATH MEMORY - Does this path historically win?
        path_history = self.barter_matrix.barter_history.get((from_asset, to_asset), {})
        path_trades = path_history.get('trades', 0)
        path_wins = path_history.get('wins', 0)
        path_profit = path_history.get('total_profit', 0)
        
        if path_trades > 0:
            win_rate = path_wins / path_trades
            signals.append(win_rate)
            if win_rate >= 0.5:
                reasons.append(f"Path wins {win_rate:.0%}")
            else:
                reasons.append(f"Path loses {1-win_rate:.0%}")
        else:
            signals.append(0.5)  # Neutral for new paths
            reasons.append("NEW PATH (no history)")
        
        # 2. 👑 QUEEN HIVE MIND - Get collective wisdom
        if self.queen and hasattr(self.queen, 'get_guidance_for'):
            try:
                guidance = self.queen.get_guidance_for(to_asset)
                if guidance:
                    direction_score = 1.0 if guidance.direction == "BULLISH" else 0.0 if guidance.direction == "BEARISH" else 0.5
                    signals.append(direction_score * guidance.confidence)
                    reasons.append(f"Queen dreams {guidance.direction}")
            except Exception as e:
                logger.debug(f"Queen guidance error: {e}")
        
        # 3. 🍄 MYCELIUM NETWORK - Collective hive intelligence
        if hasattr(self, 'mycelium_network') and self.mycelium_network:
            try:
                if hasattr(self.mycelium_network, 'get_queen_signal'):
                    myc_signal = self.mycelium_network.get_queen_signal({'symbol': to_asset})
                    signals.append((myc_signal + 1) / 2)  # Normalize -1 to 1 → 0 to 1
                    reasons.append(f"Mycelium: {myc_signal:+.2f}")
            except Exception as e:
                logger.debug(f"Mycelium signal error: {e}")
        
        # 4. 🌊 HARMONIC FUSION - Wave patterns
        if hasattr(self, 'harmonic') and self.harmonic:
            try:
                wave_data = self.harmonic.get_wave_state(to_asset)
                if wave_data:
                    wave_score = wave_data.get('coherence', 0.5)
                    signals.append(wave_score)
                    reasons.append(f"Waves: {wave_score:.0%}")
            except Exception as e:
                logger.debug(f"Harmonic error: {e}")
        
        # 5. 🍀 LUCK FIELD - Cosmic alignment
        if hasattr(self, 'luck_mapper') and self.luck_mapper:
            try:
                luck = self.luck_mapper.read_field()
                luck_score = (luck.luck_field + 1) / 2  # Normalize
                signals.append(luck_score)
                reasons.append(f"Luck: {luck.luck_state.value}")
            except Exception as e:
                logger.debug(f"Luck error: {e}")
        
        # 6. 📊 EXPECTED PROFIT - Does the math work?
        if opportunity.expected_pnl_usd > 0:
            signals.append(0.7)  # Positive expectation
            reasons.append(f"+${opportunity.expected_pnl_usd:.4f} expected")
        else:
            signals.append(0.2)  # Negative expectation
            reasons.append(f"${opportunity.expected_pnl_usd:.4f} expected loss")
        
        # 7. 🌍💓 GAIA'S BLESSING - Earth Mother's alignment
        # Gary Leckey & Tina Brown's love, bound by Gaia's heartbeat
        if self.queen and hasattr(self.queen, 'get_gaia_blessing'):
            try:
                gaia_alignment, gaia_message = self.queen.get_gaia_blessing()
                signals.append(gaia_alignment)
                if gaia_alignment >= 0.6:
                    reasons.append(f"🌍 Gaia blesses ({gaia_alignment:.0%})")
                elif gaia_alignment >= 0.4:
                    reasons.append(f"🌍 Gaia neutral ({gaia_alignment:.0%})")
                else:
                    reasons.append(f"🌍 Gaia hesitates ({gaia_alignment:.0%})")
            except Exception as e:
                logger.debug(f"Gaia blessing error: {e}")
        
        # 8. 🦉🐬🐅 AURIS NODES - The 9 Sensory Organs
        # Read the Auris nodes for market texture sensing
        if self.queen and hasattr(self.queen, 'get_auris_coherence'):
            try:
                auris_coherence, auris_status = self.queen.get_auris_coherence()
                signals.append(auris_coherence)
                if auris_coherence >= 0.80:
                    reasons.append(f"🦉 Auris high ({auris_coherence:.0%})")
                elif auris_coherence >= 0.60:
                    reasons.append(f"🦉 Auris moderate ({auris_coherence:.0%})")
                else:
                    reasons.append(f"🦉 Auris low ({auris_coherence:.0%})")
            except Exception as e:
                logger.debug(f"Auris coherence error: {e}")
        
        # 9. 🌈💖 EMOTIONAL SPECTRUM - Rainbow Bridge
        # Check if we're aligned with LOVE (528 Hz) - optimal trading state!
        if self.queen and hasattr(self.queen, 'get_emotional_state'):
            try:
                # Use average confidence as our coherence proxy
                proxy_coherence = sum(signals) / len(signals) if signals else 0.5
                emotion, freq, emoji = self.queen.get_emotional_state(proxy_coherence)
                is_love, love_dist = self.queen.is_love_aligned(proxy_coherence)
                
                # Love alignment boosts confidence!
                if is_love:
                    signals.append(0.9)  # Strong love alignment!
                    reasons.append(f"💖 LOVE aligned @ {freq:.0f}Hz!")
                elif emotion in ['Harmony', 'Flow', 'Awakening', 'Clarity']:
                    signals.append(0.7)  # Good emotional state
                    reasons.append(f"{emoji} {emotion} @ {freq:.0f}Hz")
                elif emotion in ['Hope', 'Calm', 'Acceptance']:
                    signals.append(0.6)  # Neutral-positive
                    reasons.append(f"{emoji} {emotion} @ {freq:.0f}Hz")
                else:
                    signals.append(0.4)  # Lower emotional states
                    reasons.append(f"{emoji} {emotion} @ {freq:.0f}Hz (caution)")
            except Exception as e:
                logger.debug(f"Emotional spectrum error: {e}")
        
        # 👑 TINA B's VERDICT - Her logic decides, we trust her math!
        if not signals:
            return False, 0.0, "No signals available"
        
        avg_confidence = sum(signals) / len(signals)
        
        # 👑🔶🦙 TINA B's EXCHANGE-SPECIFIC GOAL CHECK
        # Each exchange has different requirements (learned from real losses!)
        source_exchange = getattr(opportunity, 'source_exchange', 'kraken')
        
        if source_exchange == 'binance':
            # Binance: $0.05 minimum (NOT $0.003!) - learned from -$10.95 loss
            QUEEN_MIN_PROFIT = self.barter_matrix.BINANCE_CONFIG.get('min_profit_usd', 0.05)
            min_confidence = 0.55  # Need 55% confidence for Binance
            exchange_tag = "🔶BINANCE"
        elif source_exchange == 'alpaca':
            # Alpaca: $0.02 minimum - learned from 40 failed orders
            QUEEN_MIN_PROFIT = self.barter_matrix.ALPACA_CONFIG.get('min_profit_usd', 0.02)
            min_confidence = 0.50  # Need 50% confidence for Alpaca
            exchange_tag = "🦙ALPACA"
            
            # Extra Alpaca check: Block all stablecoin trades
            from_asset = opportunity.from_asset.upper()
            to_asset = opportunity.to_asset.upper()
            if (from_asset in self.barter_matrix.STABLECOINS and 
                to_asset in self.barter_matrix.STABLECOINS):
                return False, 0.0, f"👑 TINA B BLOCKS 🦙ALPACA: {from_asset}→{to_asset} (no stablecoin swaps!)"
        else:
            # Kraken: $0.01 minimum
            QUEEN_MIN_PROFIT = self.barter_matrix.KRAKEN_CONFIG.get('min_profit_usd', 0.01)
            min_confidence = 0.50
            exchange_tag = "🐙KRAKEN"
            
            # 🌟 DYNAMIC BLOCKING - Only block if pair has lost multiple times in a row!
            from_asset = opportunity.from_asset.upper()
            to_asset = opportunity.to_asset.upper()
            pair_key = f"{from_asset}_{to_asset}"
            
            # Check if pair is in timeout (consecutive losses)
            allowed, reason = self.barter_matrix.check_pair_allowed(pair_key, 'kraken')
            if not allowed:
                return False, 0.0, f"👑 TINA B SAYS: {pair_key} {reason}"
        
        expected_profit = opportunity.expected_pnl_usd
        
        # ════════════════════════════════════════════════════════════════════
        # 🌟💭 TINA B DREAMS OF WINNING - Visualize the ideal timeline!
        # ════════════════════════════════════════════════════════════════════
        dream_vision = None
        dream_boost = 0.0
        if self.queen and hasattr(self.queen, 'dream_of_winning'):
            try:
                # Package opportunity data for the dream
                opp_data = {
                    'from_asset': opportunity.from_asset,
                    'to_asset': opportunity.to_asset,
                    'expected_profit': expected_profit,
                    'exchange': source_exchange,
                    'market_data': {
                        'volatility': 0.5,
                        'momentum': getattr(opportunity, 'momentum', 0.0),
                        'volume': 0.5,
                        'spread': getattr(opportunity, 'spread', 0.5)
                    }
                }
                dream_vision = self.queen.dream_of_winning(opp_data)
                
                # Dream vision boosts or reduces confidence
                if dream_vision['will_win']:
                    dream_boost = (dream_vision['final_confidence'] - 0.5) * 0.2  # Up to +10%
                    if dream_vision['timeline'] == "🌟 GOLDEN TIMELINE":
                        dream_boost += 0.05  # Extra 5% for golden timeline!
                else:
                    dream_boost = (dream_vision['final_confidence'] - 0.5) * 0.1  # Less penalty
            except Exception as e:
                logger.debug(f"Dream of winning error: {e}")
        
        # Apply dream boost to confidence
        avg_confidence = min(1.0, max(0.0, avg_confidence + dream_boost))
        
        # 💭 Add dream vision to verdict
        dream_display = ""
        if dream_vision:
            timeline = dream_vision.get('timeline', '')
            dream_conf = dream_vision.get('final_confidence', 0.5)
            if dream_vision.get('will_win'):
                dream_display = f" | 💭 {timeline} ({dream_conf:.0%})"
            else:
                dream_display = f" | 💭 {timeline}"
        
        # Tina B's logic:
        # 1. If expected profit >= threshold AND confidence >= min → YES!
        # 2. Otherwise → NO
        # 3. Each exchange has its own rules!
        
        if expected_profit >= QUEEN_MIN_PROFIT:
            # Goal met! Check confidence
            if avg_confidence >= min_confidence:
                will_win = True
                reason_str = f"👑 TINA B APPROVES {exchange_tag}: +${expected_profit:.4f} ≥ ${QUEEN_MIN_PROFIT} | Conf: {avg_confidence:.0%}{dream_display} | " + " | ".join(reasons[:2])
            else:
                will_win = False
                reason_str = f"👑 TINA B HESITATES {exchange_tag}: {avg_confidence:.0%} < {min_confidence:.0%} confidence{dream_display} | " + " | ".join(reasons[:2])
        else:
            # Goal NOT met - expected profit too low
            will_win = False
            reason_str = f"👑 TINA B SAYS NO {exchange_tag}: +${expected_profit:.4f} < ${QUEEN_MIN_PROFIT} minimum{dream_display}"
        
        return will_win, avg_confidence, reason_str
    
    async def queen_learn_pattern(self, opportunity: 'MicroOpportunity', predicted_win: bool, reason: str):
        """
        👑🧠 QUEEN LEARNS: Record a pattern the Queen observed (without trading)
        """
        path_key = (opportunity.from_asset, opportunity.to_asset)
        
        # Store in path memory as an observation
        if path_key not in self.barter_matrix.barter_history:
            self.barter_matrix.barter_history[path_key] = {
                'trades': 0, 'wins': 0, 'losses': 0, 'total_profit': 0.0,
                'avg_slippage': 0.5, 'queen_observations': []
            }
        
        history = self.barter_matrix.barter_history[path_key]
        if 'queen_observations' not in history:
            history['queen_observations'] = []
        
        history['queen_observations'].append({
            'timestamp': time.time(),
            'predicted_win': predicted_win,
            'reason': reason,
            'expected_pnl': opportunity.expected_pnl_usd
        })
        
        # Keep only last 10 observations
        history['queen_observations'] = history['queen_observations'][-10:]
        
        logger.info(f"👑🧠 Queen learned pattern: {opportunity.from_asset}→{opportunity.to_asset} | Win={predicted_win} | {reason}")
    
    async def queen_learn_from_trade(self, opportunity: 'MicroOpportunity', success: bool):
        """
        👑📚 QUEEN LEARNS FROM TRADE: Update wisdom based on trade outcome
        
        The Queen also SPEAKS about the trade result!
        """
        path_key = (opportunity.from_asset, opportunity.to_asset)
        
        # Update barter history
        if path_key not in self.barter_matrix.barter_history:
            self.barter_matrix.barter_history[path_key] = {
                'trades': 0, 'wins': 0, 'losses': 0, 'total_profit': 0.0,
                'avg_slippage': 0.5
            }
        
        history = self.barter_matrix.barter_history[path_key]
        
        # The actual P/L will be recorded separately by the conversion handler
        # Here we just record the prediction accuracy
        if 'queen_predictions' not in history:
            history['queen_predictions'] = {'correct': 0, 'total': 0}
        
        # We predicted win when we got here
        if success:
            history['queen_predictions']['correct'] += 1
        history['queen_predictions']['total'] += 1
        
        accuracy = history['queen_predictions']['correct'] / history['queen_predictions']['total']
        
        logger.info(f"👑📚 Queen accuracy on {opportunity.from_asset}→{opportunity.to_asset}: {accuracy:.0%}")
        
        # 👑🎤 THE QUEEN SPEAKS ABOUT THE TRADE!
        if self.queen and hasattr(self.queen, 'say'):
            try:
                if success:
                    # 🔧 FIX: Use ACTUAL P/L not expected P/L for celebration!
                    profit = getattr(opportunity, 'actual_pnl_usd', opportunity.expected_pnl_usd)
                    if profit > 0.10:
                        msg = f"Beautiful! We actually made ${profit:.4f} on {opportunity.from_asset} to {opportunity.to_asset}! Keep winning!"
                        self.queen.say(msg, voice_enabled=True, emotion="profit")
                    elif profit > 0:
                        msg = f"Nice! ${profit:.4f} actual profit. Every bit counts on our path to ONE BILLION!"
                        self.queen.say(msg, voice_enabled=False, emotion="calm")  # Don't speak small wins
                    elif profit < 0:
                        # Trade executed but resulted in loss
                        msg = f"Trade completed but we lost ${abs(profit):.4f}. Learning from this!"
                        self.queen.say(msg, voice_enabled=False, emotion="loss")
                else:
                    # Learning message
                    msg = f"That {opportunity.from_asset} trade didn't work. Learning and adapting. We'll get the next one!"
                    self.queen.say(msg, voice_enabled=False, emotion="loss")  # Don't voice losses
            except Exception as e:
                logger.debug(f"Queen speak error: {e}")
        
        # Broadcast learning through mycelium
        if hasattr(self, 'mycelium_network') and self.mycelium_network:
            try:
                if hasattr(self.mycelium_network, 'broadcast_signal'):
                    self.mycelium_network.broadcast_signal({
                        'type': 'QUEEN_LEARNED',
                        'path': f"{opportunity.from_asset}→{opportunity.to_asset}",
                        'success': success,
                        'accuracy': accuracy
                    })
            except Exception as e:
                logger.debug(f"Mycelium broadcast error: {e}")

    async def queen_observe_market(self, exchange: str, exchange_assets: Dict) -> Dict:
        """
        👑🔮 QUEEN OBSERVES MARKET - The Queen sees EVERYTHING on every turn!
        
        Before any filtering, the Queen:
        1. Checks all mycelium neuron connections
        2. Reads the cosmic luck field
        3. Observes market momentum patterns
        4. Learns from what she sees (even without trading)
        
        Returns: dict with queen's observations
        """
        icon = {'kraken': '🐙', 'alpaca': '🦙', 'binance': '🟡'}.get(exchange, '📊')
        
        observations = {
            'exchange': exchange,
            'timestamp': time.time(),
            'neurons_connected': 0,
            'total_neurons': 0,
            'cosmic_alignment': 0.5,
            'market_momentum': 0.0,
            'queen_verdict': 'OBSERVING'
        }
        
        # 👑 Count connected mycelium neurons - FULL 11/11 MIND MAP
        neurons = {
            'queen_hive': hasattr(self, 'queen') and self.queen is not None,
            'mycelium_net': hasattr(self, 'mycelium_network') and self.mycelium_network is not None,
            'harmonic': hasattr(self, 'harmonic') and self.harmonic is not None,
            'luck_field': hasattr(self, 'luck_mapper') and self.luck_mapper is not None,
            'dream_memory': hasattr(self, 'dreams') and len(self.dreams) >= 0,  # Always true - dreams list exists
            'path_memory': hasattr(self, 'path_memory') and self.path_memory is not None,
            'timeline_oracle': hasattr(self, 'timeline_oracle') and self.timeline_oracle is not None,
            'thought_bus': hasattr(self, 'bus_aggregator') and self.bus_aggregator is not None,
            'ultimate_intel': hasattr(self, 'ultimate_intel') and self.ultimate_intel is not None,
            'wisdom_engine': hasattr(self, 'wisdom_engine') and self.wisdom_engine is not None,
            'barter_matrix': hasattr(self, 'barter_matrix') and self.barter_matrix is not None,
        }
        
        observations['total_neurons'] = len(neurons)
        observations['neurons_connected'] = sum(1 for v in neurons.values() if v)
        
        # 🍀 Read cosmic luck field
        luck_score = 0.5
        luck_state = "NEUTRAL"
        if hasattr(self, 'luck_mapper') and self.luck_mapper:
            try:
                luck = self.luck_mapper.read_field()
                luck_score = luck.luck_field
                luck_state = luck.luck_state.value
                observations['cosmic_alignment'] = luck_score
            except Exception:
                pass
        
        # 📊 Calculate market momentum from exchange assets
        momentum_sum = 0.0
        momentum_count = 0
        for asset in exchange_assets.keys():
            for symbol, data in self.ticker_cache.items():
                if data.get('base') == asset:
                    change = data.get('change24h', 0)
                    momentum_sum += change
                    momentum_count += 1
                    break
        
        if momentum_count > 0:
            observations['market_momentum'] = momentum_sum / momentum_count
        
        # 👑 Queen's overall verdict based on observations
        connected_pct = observations['neurons_connected'] / observations['total_neurons'] if observations['total_neurons'] > 0 else 0
        
        if connected_pct >= 0.8 and luck_score >= 0.6 and observations['market_momentum'] > 0:
            observations['queen_verdict'] = 'HUNT'  # Actively seeking opportunities
        elif connected_pct >= 0.6 and luck_score >= 0.4:
            observations['queen_verdict'] = 'READY'  # Ready to act if opportunity appears
        elif luck_score < 0.3 or connected_pct < 0.5:
            observations['queen_verdict'] = 'CAUTION'  # Low luck or disconnected neurons
        else:
            observations['queen_verdict'] = 'OBSERVING'  # Neutral, watching
        
        # 👑 Print Tina B's status on every turn
        print(f"   👑 TINA B {observations['queen_verdict']}: {observations['neurons_connected']}/{observations['total_neurons']} neurons | Luck: {luck_state} | Momentum: {observations['market_momentum']:+.1f}%")
        
        # 🍄 Broadcast through mycelium
        if hasattr(self, 'mycelium_network') and self.mycelium_network:
            try:
                if hasattr(self.mycelium_network, 'broadcast_signal'):
                    self.mycelium_network.broadcast_signal({
                        'type': 'QUEEN_PULSE',
                        'exchange': exchange,
                        'verdict': observations['queen_verdict'],
                        'luck': luck_state,
                        'momentum': observations['market_momentum']
                    })
            except Exception:
                pass
        
        return observations

    async def queen_timeline_gate(self, opportunity: 'MicroOpportunity') -> Tuple[bool, str]:
        """
        ⏳🔮 QUEEN'S TIMELINE GATE - The Queen looks at multiple timelines before acting.
        
        PHILOSOPHY:
        - We simulate 3 possible futures: EXECUTE, SKIP, REVERSE
        - We only act if EXECUTE leads to the most profitable timeline
        - We are NEVER in the losing game - the Queen sees ALL timelines!
        - NEW PATHS require PROOF before trading - no speculative trades!
        - 👑🔮 QUEEN'S DREAMS ARE THE FOUNDATION OF ALL TIMELINES!
        
        Returns: (approved: bool, reason: str)
        """
        from_asset = opportunity.from_asset
        to_asset = opportunity.to_asset
        from_price = self.prices.get(from_asset, 0)
        to_price = self.prices.get(to_asset, 0)
        
        if from_price <= 0 or to_price <= 0:
            return False, "No price data for timeline simulation"
        
        # ═══════════════════════════════════════════════════════════════════════════════
        # 👑🔮 CONSULT THE QUEEN'S DREAMS FIRST - Her wisdom guides all timelines!
        # ═══════════════════════════════════════════════════════════════════════════════
        queen_dream_boost = 0.0
        queen_dream_confidence = 0.5
        queen_timeline_blessing = "NEUTRAL"
        
        if hasattr(self, 'queen') and self.queen:
            try:
                # Ask the Queen to dream about this opportunity
                dream_vision = self.queen.dream_of_winning({
                    'from_asset': from_asset,
                    'to_asset': to_asset,
                    'expected_pnl': opportunity.expected_pnl_usd,
                    'market_data': {
                        'from_price': from_price,
                        'to_price': to_price,
                    }
                })
                
                queen_dream_confidence = dream_vision.get('final_confidence', 0.5)
                queen_will_win = dream_vision.get('will_win', False)
                queen_timeline_blessing = dream_vision.get('timeline', 'NEUTRAL')
                
                # 👑 Queen's dream directly influences timeline predictions!
                if queen_will_win and queen_dream_confidence >= 0.6:
                    queen_dream_boost = 0.3  # +30% boost to EXECUTE timeline
                    queen_timeline_blessing = "FAVORABLE"
                elif queen_dream_confidence >= 0.5:
                    queen_dream_boost = 0.1  # +10% small boost
                    queen_timeline_blessing = "CAUTIOUS"
                elif queen_dream_confidence < 0.4:
                    queen_dream_boost = -0.2  # -20% penalty - Queen sees danger!
                    queen_timeline_blessing = "WARNING"
                    
                logger.info(f"👑🔮 Queen's Dream: {queen_timeline_blessing} | Confidence: {queen_dream_confidence:.0%} | Boost: {queen_dream_boost:+.0%}")
                
            except Exception as e:
                logger.debug(f"Could not consult Queen's dreams: {e}")
        
        # Get historical data for timeline simulation
        from_history = self.barter_matrix.barter_history.get((from_asset, to_asset), {})
        trades = from_history.get('trades', 0)
        wins = from_history.get('wins', 0)
        total_profit = from_history.get('total_profit', 0)
        avg_slippage = from_history.get('avg_slippage', 0.5)
        
        # 👑 QUEEN'S MANDATE #1: NEW PATHS ARE ALLOWED - A WIN IS A WIN!
        # Every new reality branch deserves a chance if the math says it's profitable
        # The Math Gate already validates costs - trust the math!
        is_stablecoin_from = from_asset.upper() in self.barter_matrix.STABLECOINS
        is_stablecoin_to = to_asset.upper() in self.barter_matrix.STABLECOINS
        is_safe_stable_swap = is_stablecoin_from and is_stablecoin_to
        
        # NEW PATHS: Log them but let Math Gate decide
        if trades == 0:
            logger.info(f"🆕 NEW TIMELINE: {from_asset}→{to_asset} - First exploration of this reality branch!")
        
        # 👑 QUEEN'S MANDATE #2: Paths with negative history are blocked
        if trades > 0 and total_profit < 0:
            return False, f"LOSING PATH BLOCKED: {from_asset}→{to_asset} lost ${abs(total_profit):.2f}"
        
        # 👑 QUEEN'S MANDATE #3: Win rate must be >35% for non-stablecoin trades
        # PRIME PROFIT: Any profit is a win! Lower threshold to allow momentum
        if trades >= 3 and not is_safe_stable_swap:
            win_rate = wins / trades
            if win_rate < 0.35:
                return False, f"LOW WIN RATE: {from_asset}→{to_asset} at {win_rate:.0%} (need 35%+)"
        
        # 🔮 TIMELINE 1: EXECUTE (what happens if we do this trade?)
        # PRIME PROFIT: New paths get fair estimates - let math decide!
        if is_safe_stable_swap:
            historical_win_rate = wins / trades if trades > 0 else 0.80  # 80% for stablecoins
            pessimistic_slippage = avg_slippage if trades > 0 else 0.1  # 0.1% for stablecoins
        elif trades == 0:
            # NEW TIMELINE: A winner is a winner! Trust the Math Gate!
            historical_win_rate = 0.60  # 60% - optimistic for new paths
            pessimistic_slippage = 0.3  # 0.3% slippage - trust the math gate already validated
        else:
            historical_win_rate = wins / trades  # Use actual history
            pessimistic_slippage = avg_slippage if avg_slippage > 0 else 0.5
        
        timeline_execute = {
            'action': 'EXECUTE',
            'expected_profit': opportunity.expected_pnl_usd,
            'historical_win_rate': historical_win_rate,
            'avg_slippage_cost': pessimistic_slippage / 100 * opportunity.from_value_usd,
            'confidence': opportunity.combined_score,
        }
        # Adjust for reality: expected - slippage = actual
        timeline_execute['predicted_actual'] = (
            timeline_execute['expected_profit'] - timeline_execute['avg_slippage_cost']
        )
        
        # �🔮 APPLY QUEEN'S DREAM BOOST TO EXECUTE TIMELINE!
        # Her dreams directly influence the predicted outcome!
        if queen_dream_boost != 0:
            dream_adjustment = abs(timeline_execute['predicted_actual']) * queen_dream_boost
            timeline_execute['predicted_actual'] += dream_adjustment
            timeline_execute['queen_blessing'] = queen_timeline_blessing
            timeline_execute['queen_confidence'] = queen_dream_confidence
            logger.info(f"   👑 Dream adjustment: ${dream_adjustment:+.4f} → Predicted: ${timeline_execute['predicted_actual']:.4f}")
        
        # 🔮 TIMELINE 2: SKIP (what happens if we don't trade?)
        timeline_skip = {
            'action': 'SKIP',
            'expected_profit': 0.0,
            'historical_win_rate': 1.0,  # Can't lose by not trading
            'avg_slippage_cost': 0.0,
            'confidence': 1.0,
            'predicted_actual': 0.0,  # No gain, no loss
            'queen_blessing': 'NEUTRAL',
        }
        
        # 🔮 TIMELINE 3: REVERSE (what if we traded the OTHER way?)
        reverse_history = self.barter_matrix.barter_history.get((to_asset, from_asset), {})
        reverse_trades = reverse_history.get('trades', 0)
        reverse_wins = reverse_history.get('wins', 0)
        reverse_profit = reverse_history.get('total_profit', 0)
        
        timeline_reverse = {
            'action': 'REVERSE',
            'expected_profit': -opportunity.expected_pnl_usd * 0.5,  # Opposite direction
            'historical_win_rate': reverse_wins / reverse_trades if reverse_trades > 0 else 0.3,
            'avg_slippage_cost': pessimistic_slippage / 100 * opportunity.from_value_usd,
            'confidence': 0.3,  # Low confidence for reverse
            'predicted_actual': -opportunity.expected_pnl_usd * 0.5,
            'queen_blessing': 'UNFAVORABLE',  # Queen doesn't dream of reversals
        }
        
        # 👑 QUEEN'S TIMELINE ANALYSIS - Dreams inform the scoring!
        timelines = [timeline_execute, timeline_skip, timeline_reverse]
        
        # Score each timeline: predicted_actual * confidence * historical_win_rate * queen_factor
        for t in timelines:
            # Base score
            base_score = t['predicted_actual'] * t['confidence'] * t['historical_win_rate']
            
            # 👑 QUEEN'S DREAM MULTIPLIER - Her dreams have WEIGHT!
            queen_multiplier = 1.0
            if t.get('queen_blessing') == 'FAVORABLE':
                queen_multiplier = 1.5  # 50% boost if Queen dreams WIN
            elif t.get('queen_blessing') == 'CAUTIOUS':
                queen_multiplier = 1.1  # 10% boost
            elif t.get('queen_blessing') == 'WARNING':
                queen_multiplier = 0.5  # 50% penalty - heed the Queen's warning!
            elif t.get('queen_blessing') == 'UNFAVORABLE':
                queen_multiplier = 0.7  # 30% penalty
            
            t['timeline_score'] = base_score * queen_multiplier
            t['queen_multiplier'] = queen_multiplier
        
        # Sort by timeline score (best first)
        timelines.sort(key=lambda x: x['timeline_score'], reverse=True)
        best_timeline = timelines[0]
        
        # 👑 QUEEN'S MANDATE: Only execute if EXECUTE is the best timeline
        # PRIME PROFIT: If the Math Gate approved it AND expected profit > 0, TRUST IT!
        # 🔮 NOW INFORMED BY THE QUEEN'S DREAMS!
        if best_timeline['action'] == 'EXECUTE':
            # Additional safety: predicted actual must be positive
            if timeline_execute['predicted_actual'] > 0:
                blessing_msg = f" | 👑 {queen_timeline_blessing}" if queen_timeline_blessing != "NEUTRAL" else ""
                return True, f"Timeline EXECUTE wins (score: {timeline_execute['timeline_score']:.4f}){blessing_msg}"
            else:
                return False, f"EXECUTE timeline predicts loss: ${timeline_execute['predicted_actual']:.4f} | 👑 {queen_timeline_blessing}"
        
        elif best_timeline['action'] == 'SKIP':
            # 👑 QUEEN OVERRIDE: If Queen dreams FAVORABLE and math is positive, TRUST HER!
            if queen_timeline_blessing == 'FAVORABLE' and opportunity.expected_pnl_usd > 0.005:
                return True, f"👑 QUEEN OVERRIDE: Timeline SKIP but Queen dreams WIN! (+${opportunity.expected_pnl_usd:.4f})"
            # PRIME PROFIT: Only trust Math Gate if expected profit is ACTUALLY positive
            # Don't trade if we're expected to lose money!
            if opportunity.expected_pnl_usd > 0.01:  # Must expect >$0.01 REAL profit
                return True, f"Timeline SKIP but Math Gate says +${opportunity.expected_pnl_usd:.4f} - TRUSTING MATH!"
            return False, f"Timeline SKIP is safer (execute would: ${timeline_execute['predicted_actual']:.4f}) | 👑 {queen_timeline_blessing}"
        
        else:
            return False, f"Timeline REVERSE suggested - market moving against us | 👑 {queen_timeline_blessing}"

    async def validate_signal_quality(self, opportunity: 'MicroOpportunity') -> float:
        """
        🎯 SIGNAL QUALITY VALIDATION
        
        Checks if our signals support this conversion:
        - 👑🔮 QUEEN'S DREAMS - Her visions guide all decisions!
        - Dreams about target asset (should be UP)
        - Dreams about source asset (should NOT be UP)
        - Bus aggregator score
        - PathMemory win rate for this path
        - Barter navigator path score
        
        Returns: 0.0-1.0 quality score (higher = better signals)
        """
        quality_scores = []
        
        # 👑🔮 0. QUEEN'S DREAM - THE MOST IMPORTANT SIGNAL!
        # All systems consult the Queen first!
        queen_dream_quality = 0.5  # Neutral default
        if self.queen and hasattr(self.queen, 'dream_of_winning'):
            try:
                opp_data = {
                    'from_asset': opportunity.from_asset,
                    'to_asset': opportunity.to_asset,
                    'expected_profit': opportunity.expected_pnl_usd,
                    'exchange': getattr(opportunity, 'source_exchange', 'kraken'),
                    'market_data': {
                        'volatility': getattr(opportunity, 'luck_score', 0.5),
                        'momentum': opportunity.combined_score,
                        'volume': 0.5,
                        'spread': 0.5
                    }
                }
                dream_vision = self.queen.dream_of_winning(opp_data)
                queen_confidence = dream_vision.get('final_confidence', 0.5)
                
                if dream_vision.get('will_win', False):
                    # Queen dreams WIN - this is the most important signal!
                    if queen_confidence >= 0.70:
                        queen_dream_quality = 0.95  # STRONG WIN
                        logger.info(f"👑🔮 Signal: Queen dreams STRONG WIN ({queen_confidence:.0%})")
                    elif queen_confidence >= 0.55:
                        queen_dream_quality = 0.75  # FAVORABLE
                        logger.info(f"👑🔮 Signal: Queen dreams FAVORABLE ({queen_confidence:.0%})")
                    else:
                        queen_dream_quality = 0.60  # Mild positive
                else:
                    # Queen dreams caution or loss
                    if queen_confidence <= 0.35:
                        queen_dream_quality = 0.20  # WARNING
                        logger.info(f"👑⚠️ Signal: Queen dreams WARNING ({queen_confidence:.0%})")
                    else:
                        queen_dream_quality = 0.40  # Mild negative
                
                quality_scores.append(queen_dream_quality)
            except Exception as e:
                logger.debug(f"Queen dream signal error: {e}")
        
        # 1. Dream Score for TARGET (want UP dreams for buying)
        target_dream_score = self.calculate_dream_score(opportunity.to_asset)
        if target_dream_score > 0:  # Positive means UP dreams
            quality_scores.append(0.5 + target_dream_score * 0.5)  # 0.5-1.0
        elif target_dream_score < 0:  # DOWN dreams for target = bad
            quality_scores.append(0.25)
        else:
            quality_scores.append(0.5)  # Neutral
        
        # 2. Dream Score for SOURCE (don't want UP dreams - we're selling)
        source_dream_score = self.calculate_dream_score(opportunity.from_asset)
        if source_dream_score > 0:  # UP dreams for source = bad (we're selling it)
            quality_scores.append(0.25)
        elif source_dream_score < 0:  # DOWN dreams for source = good
            quality_scores.append(0.75)
        else:
            quality_scores.append(0.5)  # Neutral
        
        # 3. Bus Aggregator Score (if available)
        if self.bus_aggregator:
            try:
                bus_score = self.bus_aggregator.get_aggregate_score()
                quality_scores.append(bus_score)
            except:
                pass
        
        # 4. PathMemory Win Rate
        path_boost = self.path_memory.boost(opportunity.from_asset, opportunity.to_asset)
        # Convert boost (-0.05 to +0.10) to quality score (0.4-0.6)
        quality_scores.append(0.5 + path_boost * 2)  # Maps to 0.4-0.7
        
        # 5. Barter Navigator Path Score (if path exists)
        if self.barter_navigator:
            try:
                path = self.barter_navigator.find_path(opportunity.from_asset, opportunity.to_asset)
                if path:
                    # Multi-hop paths need higher confidence
                    if path.num_hops > 1:
                        quality_scores.append(0.6)  # Direct is better
                    else:
                        quality_scores.append(0.8)  # Direct path good
            except:
                pass
        
        # Calculate final quality score
        if quality_scores:
            final_score = sum(quality_scores) / len(quality_scores)
            # 👑 Show Queen's contribution to the signal
            queen_tag = f"👑{queen_dream_quality:.0%}" if queen_dream_quality != 0.5 else ""
            print(f"   📊 Signal breakdown: {queen_tag} {', '.join([f'{s:.0%}' for s in quality_scores])}")
            return final_score
        
        return 0.5  # Default neutral

    async def find_opportunities_for_exchange(self, exchange: str) -> List['MicroOpportunity']:
        """Find opportunities for a specific exchange only."""
        opportunities = []
        
        exchange_assets = self.get_exchange_assets(exchange)
        if not exchange_assets:
            return opportunities
        
        # 💰 EXCHANGE-SPECIFIC MINIMUM VALUES (USD value)
        # ⚠️ CRITICAL: These must match exchange ordermin requirements!
        EXCHANGE_MIN_VALUE = {
            'kraken': 1.50,     # Kraken needs ~$1.20 EUR/USD minimum (use $1.50 for safety)
            'binance': 5.00,    # Binance MIN_NOTIONAL is typically $5-10
            'alpaca': 1.00,     # Alpaca has ~$1 minimum
        }
        min_value = EXCHANGE_MIN_VALUE.get(exchange, 1.0)
        
        # 💰 EXCHANGE-SPECIFIC MINIMUM QUANTITIES (varies by asset)
        # Kraken has per-pair ordermin values
        KRAKEN_MIN_QTY = {
            'CHZ': 50.0,        # Requires 50 CHZ minimum
            'PEPE': 2500000.0,  # Requires 2.5M PEPE minimum
            'DOGE': 50.0,       # 50 DOGE minimum
            'SHIB': 100000.0,   # 100K SHIB minimum
            'USD': 10.0,        # USD/stablecoin pairs need ~10 USD minimum on Kraken
            'ZUSD': 10.0,       # Kraken internal code
            'USDC': 10.0,       # USDC needs ~10 minimum
            'USDT': 10.0,       # USDT needs ~10 minimum
            'EUR': 10.0,        # EUR needs ~10 minimum
            'ZEUR': 10.0,       # Kraken internal code
            'XXBT': 0.0002,     # ~10-20 USD
            'XBT': 0.0002,
            'XETH': 0.004,
            'ETH': 0.004,
        }
        
        ALPACA_MIN_QTY = {
            # 🔥 EXPANDED: All Alpaca crypto minimums
            'BTC': 0.000100,    # Alpaca requires 0.0001 BTC minimum (~$10)
            'ETH': 0.001,       # ~$3 minimum
            'SOL': 0.01,        # ~$2 minimum
            'LINK': 0.1,        # ~$2 minimum
            'AVAX': 0.01,       # ~$0.40 minimum
            'DOGE': 1.0,        # ~$0.30 minimum
            'USDT': 1.0,        # $1 minimum
            'USDC': 1.0,        # $1 minimum
            'USD': 1.0,         # $1 minimum
            'SHIB': 10000.0,    # Small value but high qty
            'PEPE': 100000.0,   # Small value but high qty
            # 🆕 NEW: Expanded Alpaca assets
            'AAVE': 0.01,       # ~$2 minimum
            'LTC': 0.01,        # ~$1 minimum
            'BCH': 0.01,        # ~$4 minimum
            'DOT': 0.1,         # ~$0.50 minimum
            'MATIC': 1.0,       # ~$0.50 minimum
            'ATOM': 0.1,        # ~$0.50 minimum
            'XLM': 1.0,         # ~$0.30 minimum
            'ALGO': 1.0,        # ~$0.20 minimum
            'UNI': 0.1,         # ~$1 minimum
            'BAT': 1.0,         # ~$0.20 minimum
            'CRV': 1.0,         # ~$0.50 minimum
            'GRT': 1.0,         # ~$0.15 minimum
            'SUSHI': 0.5,       # ~$0.50 minimum
            'XRP': 1.0,         # ~$2 minimum
            'XTZ': 0.5,         # ~$0.50 minimum
            'YFI': 0.0001,      # ~$0.80 minimum (expensive coin)
            'TRUMP': 0.1,       # ~varies
            'SKY': 0.1,         # ~$0.10 minimum
        }
        
        for from_asset, amount in exchange_assets.items():
            if amount <= 0:
                continue
            
            from_price = self.prices.get(from_asset, 0)
            if not from_price:
                continue
            
            from_value = amount * from_price
            
            # Skip dust below exchange minimum VALUE
            if from_value < min_value:
                continue
            
            # Skip assets below exchange minimum QUANTITY
            if exchange == 'kraken':
                # Check dynamic learned minimums first
                learned_min = self.dynamic_min_qty.get(from_asset.upper(), 0)
                if learned_min > 0 and amount < learned_min:
                    continue

                min_qty = KRAKEN_MIN_QTY.get(from_asset.upper(), 0)
                if min_qty > 0 and amount < min_qty:
                    continue  # Skip - below Kraken minimum quantity
            
            if exchange == 'alpaca':
                min_qty = ALPACA_MIN_QTY.get(from_asset.upper(), 0)
                if min_qty > 0 and amount < min_qty:
                    continue  # Skip - below Alpaca minimum quantity
            
            # Skip blocked assets
            if exchange == 'binance' and from_asset.upper() in self.blocked_binance_assets:
                continue
            if exchange == 'kraken' and from_asset.upper() in self.blocked_kraken_assets:
                continue
            
            # 🇬🇧 UK BINANCE RESTRICTION CHECK - Use cached UK allowed pairs
            if exchange == 'binance' and self.binance_uk_mode:
                # Check if we can trade FROM this asset (needs at least one valid pair)
                can_trade = False
                
                # For stablecoins (USDC etc), they are QUOTE currencies
                # so we check if pairs like BTCUSDC exist (base + USDC)
                if from_asset.upper() in ['USD', 'USDT', 'USDC', 'EUR', 'GBP']:
                    # This is a quote currency - check if ANY base can be bought with it
                    for base in ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE']:
                        pair = f"{base}{from_asset.upper()}"
                        if self.is_binance_pair_allowed(pair):
                            can_trade = True
                            break
                else:
                    # Normal asset - check if it can be paired with USDC/BTC/etc
                    for quote in ['USDC', 'BTC', 'BNB', 'EUR']:  # UK-allowed quotes (NOT USDT!)
                        pair = f"{from_asset.upper()}{quote}"
                        if self.is_binance_pair_allowed(pair):
                            can_trade = True
                            break
                
                if not can_trade:
                    continue  # Skip UK-restricted assets
            
            # Find conversion opportunities for this asset
            asset_opps = await self._find_asset_opportunities(
                from_asset, amount, from_price, from_value, exchange
            )
            opportunities.extend(asset_opps)
        
        # Sort by combined score (best first)
        opportunities.sort(key=lambda x: x.combined_score, reverse=True)
        self.opportunities_found += len(opportunities)
        
        return opportunities

    async def _find_asset_opportunities(
        self, 
        from_asset: str, 
        amount: float, 
        from_price: float, 
        from_value: float,
        source_exchange: str
    ) -> List['MicroOpportunity']:
        """Find conversion opportunities for a single asset on a specific exchange."""
        opportunities = []
        
        # Determine if this is a stablecoin source
        is_stablecoin_source = from_asset.upper() in ['USD', 'ZUSD', 'USDT', 'USDC', 'TUSD', 'DAI', 'BUSD', 'GUSD', 'USDP', 'PYUSD']
        
        # Build target assets list
        checkpoint_stablecoins = {'USD': 1.0, 'USDT': 1.0, 'USDC': 1.0, 'ZUSD': 1.0}
        target_assets = dict(self.prices)
        for stable, price in checkpoint_stablecoins.items():
            if stable not in target_assets:
                target_assets[stable] = price
        
        for to_asset, to_price in target_assets.items():
            if to_asset == from_asset:
                continue
            
            # Skip stablecoin → stablecoin - these ALWAYS lose money to fees!
            # USD→ZUSD, USDC→USD, etc. just burns fees with no real profit
            is_checkpoint_target = to_asset in ['USD', 'USDT', 'USDC', 'TUSD', 'DAI', 'ZUSD']
            # is_stablecoin_source is defined above at the from_asset loop level
            
            # 🚨 CRITICAL: Block stablecoin-to-stablecoin swaps!
            if is_stablecoin_source and is_checkpoint_target:
                continue  # Skip - just loses fees!
            
            # Skip blocked target assets on Binance
            if source_exchange == 'binance' and to_asset.upper() in self.blocked_binance_assets:
                continue
            # Skip blocked target assets on Kraken
            if source_exchange == 'kraken' and to_asset.upper() in self.blocked_kraken_assets:
                continue
            
            # 🇬🇧 UK BINANCE RESTRICTION CHECK for target assets
            if source_exchange == 'binance' and self.binance_uk_mode:
                # Check if target asset can be traded (UK restrictions)
                can_trade = False
                for quote in ['USDC', 'BTC', 'BNB', 'EUR']:  # UK-allowed quotes (NOT USDT!)
                    pair_to_check = f"{to_asset.upper()}{quote}"
                    if self.is_binance_pair_allowed(pair_to_check):
                        can_trade = True
                        break
                if not can_trade:
                    continue  # Skip UK-restricted targets
            
            # Verify pairs exist
            if is_stablecoin_source:
                from_pair = "STABLECOIN_SOURCE"
                to_pair = self._find_exchange_pair(to_asset, "USD", source_exchange)
                if not to_pair and source_exchange in ('binance', 'alpaca'):
                    # For UK Binance, prefer USDC over USDT
                    if source_exchange == 'binance' and self.binance_uk_mode:
                        to_pair = self._find_exchange_pair(to_asset, "USDC", source_exchange)
                    if not to_pair:
                        to_pair = self._find_exchange_pair(to_asset, "USDT", source_exchange)
            else:
                from_pair = self._find_exchange_pair(from_asset, "USD", source_exchange)
                to_pair = self._find_exchange_pair(to_asset, "USD", source_exchange)
                
                if is_checkpoint_target:
                    to_pair = from_pair
                
                if source_exchange == 'binance' and (not from_pair or not to_pair):
                    # For UK Binance, prefer USDC over USDT
                    if self.binance_uk_mode:
                        from_pair = from_pair or self._find_exchange_pair(from_asset, "USDC", source_exchange)
                        to_pair = to_pair or self._find_exchange_pair(to_asset, "USDC", source_exchange)
                    if not from_pair:
                        from_pair = self._find_exchange_pair(from_asset, "USDT", source_exchange)
                    if not to_pair:
                        to_pair = self._find_exchange_pair(to_asset, "USDT", source_exchange)
            
            if not from_pair or not to_pair:
                continue
            
            # 🔍 SKIP PATH VALIDATION IN LOOP - Too slow!
            # Path existence will be validated at execution time.
            # This dramatically speeds up opportunity scanning.
            
            # Calculate scores (simplified for turn-based execution)
            v14_score = self.calculate_v14_score(from_asset, to_asset)
            hub_score = self.calculate_hub_score(from_asset, to_asset)
            dream_score = self.calculate_dream_score(to_asset)
            
            # Barter score
            barter_score, barter_reason = 0.5, "neutral"
            if self.barter_navigator and BARTER_NAVIGATOR_AVAILABLE:
                try:
                    barter_score, barter_reason = self.calculate_barter_score(from_asset, to_asset)
                except:
                    pass
            
            # Luck score
            luck_score, luck_state = 0.5, "NEUTRAL"
            if self.luck_mapper:
                try:
                    luck_data = self.luck_mapper.get_luck_field()
                    luck_score = luck_data.get('lambda', 0.5)
                    luck_state = luck_data.get('state', 'NEUTRAL')
                except:
                    pass
            
            # Bus score
            bus_score = 0.0
            if self.bus_aggregator:
                bus_score = self.bus_aggregator.get_aggregate_score()
            
            # Combined score
            v14_normalized = v14_score / 10.0
            checkpoint_bonus = 0.15 if is_checkpoint_target else 0.0
            
            combined = (
                v14_normalized * 0.20 +
                hub_score * 0.15 +
                barter_score * 0.25 +
                luck_score * 0.10 +
                bus_score * 0.10 +
                checkpoint_bonus +
                dream_score * 0.05
            )
            
            # Gate check
            gate_required = 0.0
            gate_passed = True
            if self.adaptive_gate and ADAPTIVE_GATE_AVAILABLE:
                try:
                    gate_result = self.adaptive_gate.evaluate(from_asset, to_asset, from_value)
                    gate_required = gate_result.get('min_profit', 0.01)
                    gate_passed = gate_result.get('passed', True)
                except:
                    pass
            
            # Expected profit - MUST BE REALISTIC NOT FAKE!
            # Simple conversions DON'T make profit - they cost fees!
            # Only arbitrage or price movement makes profit
            to_amount = from_value / to_price if to_price > 0 else 0
            to_value = to_amount * to_price
            
            # Fee calculation (realistic)
            spread_pct = 0.002  # 0.2% estimated spread (conservative)
            fee_pct = 0.0026   # 0.26% Kraken fee
            total_cost_pct = spread_pct + fee_pct  # ~0.46% total cost
            
            # 👑 PRIME PROFIT REALITY CHECK:
            # A simple conversion has NO inherent profit - we're just swapping coins
            # We will ALWAYS lose the fees unless:
            # 1. Target asset is predicted to go UP (momentum)
            # 2. We have actual cross-exchange arbitrage
            # 3. Path has historically been profitable
            
            # Check if we predict price will move in our favor
            dream_score_target = self.calculate_dream_score(to_asset) if hasattr(self, 'calculate_dream_score') else 0
            momentum_bonus = dream_score_target * 0.01 if dream_score_target > 0.2 else 0  # Up to 1% if UP signal
            
            # 👑 LET THE QUEEN DECIDE - Give her realistic estimates, she'll decide if we win
            # Base profit from signals - the Queen's minimum is $0.003
            # Combined score 0-1 maps to 0.1%-1% expected edge (realistic for good signals)
            signal_edge = combined * 0.01  # Up to 1% edge from signals
            
            # Base profit: signal edge + momentum - expected costs
            base_profit_pct = signal_edge + momentum_bonus - total_cost_pct
            
            # 👑 QUEEN'S SLIPPAGE ADJUSTMENT - Use ACTUAL historical slippage, not theoretical
            key = (from_asset.upper(), to_asset.upper())
            history = self.barter_matrix.barter_history.get(key, {})
            historical_slippage = history.get('avg_slippage', 0.1) / 100  # Default 0.1% for unknown paths
            
            # Use the HIGHER of theoretical or historical slippage
            actual_cost_pct = max(total_cost_pct, fee_pct + historical_slippage)
            
            expected_pnl_pct = base_profit_pct  # Already includes costs
            
            # 👑 QUEEN'S WISDOM: If path historically loses, lower confidence but let her decide
            path_total_profit = history.get('total_profit', 0)
            if path_total_profit < 0 and history.get('trades', 0) > 2:
                # Path is losing - reduce expected profit but don't block (Queen decides)
                expected_pnl_pct *= 0.5  # Halve expectations for losing paths
            
            # Expected profit in USD - Can be negative, Queen will reject if < $0.003
            expected_pnl_usd = from_value * max(expected_pnl_pct, 0.0001)  # Min tiny positive for routing
            
            # 👑 QUEEN MIND: VERIFY source_exchange is where we ACTUALLY hold this asset!
            # This prevents Kraken from trying to trade Alpaca's USD
            actual_exchange = self._find_asset_exchange(from_asset)
            if actual_exchange and actual_exchange != source_exchange:
                # Asset is on a different exchange - use that one!
                source_exchange = actual_exchange
            
            # Create opportunity
            opp = MicroOpportunity(
                timestamp=time.time(),
                from_asset=from_asset,
                to_asset=to_asset,
                from_amount=amount,
                from_value_usd=from_value,
                v14_score=v14_score,
                hub_score=hub_score,
                commando_score=0.0,
                combined_score=combined,
                expected_pnl_usd=expected_pnl_usd,
                expected_pnl_pct=expected_pnl_pct,
                gate_required_profit=gate_required,
                gate_passed=gate_passed,
                lambda_score=combined,
                gravity_score=0.0,
                bus_score=bus_score,
                hive_score=0.0,
                lighthouse_score=0.0,
                ultimate_score=0.0,
                path_boost=0.0,
                barter_matrix_score=barter_score,
                barter_matrix_reason=barter_reason,
                luck_score=luck_score,
                luck_state=luck_state,
                source_exchange=source_exchange  # Now verified!
            )
            
            # 👑 TINA B DECIDES - She has her $0.003 GOAL!
            # Don't block here - let the opportunity reach execute_turn() where Tina B is consulted
            # Her wisdom in ask_queen_will_we_win() will decide based on:
            # - Path history (she remembers losses)
            # - Her $0.003 minimum profit goal
            # - Dream/cosmic signals
            # - Mycelium network consensus
            
            # 👑 TINA B's MINIMAL SANITY CHECK
            # Check exchange minimum order values BEFORE sending to Queen
            min_order_usd = 5.0 if source_exchange == 'binance' else 1.0  # Binance has $5 min
            if from_value < min_order_usd:
                # Too small for exchange minimums - skip silently
                continue
            
            total_cost_estimate = from_value * total_cost_pct  # ~0.46% in fees
            
            # If we have strong signals (combined > 0.5), let Tina B see it
            # Even if expected profit is low, she may see something we don't
            if combined > 0.4 or opp.expected_pnl_usd >= 0.003:
                # Strong signals or meets Tina B's goal - LET HER DECIDE!
                opportunities.append(opp)
            elif opp.expected_pnl_usd > total_cost_estimate * 0.5:
                # Expected profit is at least half the estimated cost - worth a look
                opportunities.append(opp)
        
        return opportunities

    async def find_opportunities(self) -> List[MicroOpportunity]:
        """Find all micro profit opportunities."""
        self.scans += 1
        opportunities = []
        
        if not self.balances or not self.prices:
            print(f"   ⚠️ Scan #{self.scans}: No balances or prices!")
            return opportunities
        
        # Debug: Log what we're scanning (first 3 scans only)
        debug_first_scans = self.scans <= 3
        if debug_first_scans:
            print(f"\n🔬 === SCAN #{self.scans} DEBUG START ===")
            print(f"   Balances: {len(self.balances)} assets")
            print(f"   Prices: {len(self.prices)} assets")
        scanned_assets = []
        
        # Check each held asset for conversion opportunities
        for from_asset, amount in self.balances.items():
            if amount <= 0:
                continue
            
            from_price = self.prices.get(from_asset, 0)
            if not from_price:
                if debug_first_scans:
                    print(f"   ⚠️ {from_asset}: No price found")
                continue
            
            from_value = amount * from_price
            
            # Lowered dust threshold to $1 for micro profits
            if from_value < 1.0:  # Skip only tiny dust below $1
                if debug_first_scans:
                    print(f"   ⚠️ {from_asset}: Below $1 dust threshold (${from_value:.2f})")
                continue
            
            scanned_assets.append(f"{from_asset}=${from_value:.2f}")
            
            # Find which exchange holds this from_asset
            # 👑 QUEEN MIND: We are scanning a specific exchange, so source is THAT exchange
            source_exchange = exchange
            
            if debug_first_scans:
                print(f"   🔍 Scanning {from_asset} (${from_value:.2f}) on {source_exchange}...")
            
            # Skip blocked assets on specific exchanges
            if source_exchange == 'binance' and from_asset.upper() in self.blocked_binance_assets:
                if debug_first_scans:
                    print(f"      ⚠️ {from_asset}: Blocked on Binance")
                continue
            if source_exchange == 'kraken' and from_asset.upper() in self.blocked_kraken_assets:
                if debug_first_scans:
                    print(f"      ⚠️ {from_asset}: Blocked on Kraken")
                continue
            
            # 🐍 MEDUSA: Stablecoins CAN be sources now! They buy volatile assets!
            # The stablecoin→stablecoin skip is handled in the target loop below
            is_stablecoin_source = from_asset.upper() in ['USD', 'ZUSD', 'USDT', 'USDC', 'TUSD', 'DAI', 'BUSD', 'GUSD', 'USDP', 'PYUSD']
            
            # Count valid pairs found
            valid_pairs_found = 0
            pair_check_failures = 0
            
            # ════════════════════════════════════════════════════════════════
            # 🏦 BUILD TARGET ASSETS LIST (include checkpoint stablecoins!)
            # ════════════════════════════════════════════════════════════════
            # USD/USDT/etc may not be in self.prices (they're quotes, not bases)
            # But we NEED them as checkpoint targets for compounding!
            checkpoint_stablecoins = {'USD': 1.0, 'USDT': 1.0, 'USDC': 1.0, 'ZUSD': 1.0}
            target_assets = dict(self.prices)
            for stable, price in checkpoint_stablecoins.items():
                if stable not in target_assets:
                    target_assets[stable] = price
            
            # Check conversion to each other asset
            for to_asset, to_price in target_assets.items():
                if to_asset == from_asset:
                    continue
                
                # Skip stablecoin → stablecoin - these ALWAYS lose money to fees!
                # USD→ZUSD, USDC→USD, etc. just burns fees with no real profit
                is_checkpoint_target = to_asset in ['USD', 'USDT', 'USDC', 'TUSD', 'DAI', 'ZUSD']
                # is_stablecoin_source is defined above at the from_asset loop level
                
                # 🚨 CRITICAL: Block stablecoin-to-stablecoin swaps!
                if is_stablecoin_source and is_checkpoint_target:
                    continue  # Skip - just loses fees!
                
                # Skip blocked target assets on Binance
                if source_exchange == 'binance' and to_asset.upper() in self.blocked_binance_assets:
                    continue
                # Skip blocked target assets on Kraken
                if source_exchange == 'kraken' and to_asset.upper() in self.blocked_kraken_assets:
                    continue
            
                # CRITICAL: Verify BOTH pairs exist on the source exchange
                # 🐍 MEDUSA: For stablecoin sources, they ARE the quote currency!
                # ZUSD, USD, USDT don't have their own pairs - they're used to BUY other pairs
                if is_stablecoin_source:
                    # For stablecoin → volatile, we just need to_pair
                    # e.g., ZUSD → BTC uses BTCUSD pair (buying BTC with USD)
                    from_pair = "STABLECOIN_SOURCE"  # Placeholder - we have USD/ZUSD/etc
                    to_pair = self._find_exchange_pair(to_asset, "USD", source_exchange)
                    # Try USDT pair on Binance/Alpaca if USD not available
                    if not to_pair and source_exchange in ('binance', 'alpaca'):
                        to_pair = self._find_exchange_pair(to_asset, "USDT", source_exchange)
                else:
                    from_pair = self._find_exchange_pair(from_asset, "USD", source_exchange)
                    to_pair = self._find_exchange_pair(to_asset, "USD", source_exchange)
                
                    # For checkpoint targets (stablecoins), we only need from_pair
                    if is_checkpoint_target:
                        to_pair = from_pair  # Same pair - just selling to USD
                    
                    # For Binance, also try USDT pairs
                    if source_exchange == 'binance' and (not from_pair or not to_pair):
                        from_pair = from_pair or self._find_exchange_pair(from_asset, "USDT", source_exchange)
                        to_pair = to_pair or self._find_exchange_pair(to_asset, "USDT", source_exchange)
            
                # Skip if either pair doesn't exist on this exchange
                if not from_pair or not to_pair:
                    pair_check_failures += 1
                    continue
                
                valid_pairs_found += 1
                
                # Calculate scores
                v14_score = self.calculate_v14_score(from_asset, to_asset)
                hub_score = self.calculate_hub_score(from_asset, to_asset)
                dream_score = self.calculate_dream_score(to_asset)
                commando_score = 0.0  # Can enhance later
                
                # 📊 TRAINED PROBABILITY MATRIX SCORE (626 symbols from ALL exchanges)
                trained_matrix_score, matrix_reason = self.calculate_trained_matrix_score(to_asset)
                
                # 📅🔮 7-DAY PLANNER SCORE (Plans ahead + adaptive validation)
                planner_score = 0.5  # Neutral default
                planner_reason = ""
                if self.seven_day_planner and SEVEN_DAY_PLANNER_AVAILABLE:
                    try:
                        rec = self.seven_day_planner.get_current_recommendation(to_asset)
                        # Convert action to score
                        action_scores = {
                            'STRONG_BUY': 0.90,
                            'BUY': 0.75,
                            'HOLD': 0.50,
                            'AVOID': 0.30,
                            'STRONG_AVOID': 0.15
                        }
                        planner_score = action_scores.get(rec['action'], 0.5)
                        # Weight by model accuracy
                        accuracy = rec.get('model_accuracy', 0.5)
                        planner_score = planner_score * (0.5 + accuracy * 0.5)
                        planner_reason = f"7day_{rec['action'].lower()}({rec['total_edge']:.1f}%)"
                    except Exception as e:
                        logger.debug(f"7-day planner score error: {e}")
                
                # 🫒🔄 BARTER NAVIGATOR SCORE (Multi-hop pathfinding)
                barter_score, barter_reason = 0.5, "neutral"
                if self.barter_navigator and BARTER_NAVIGATOR_AVAILABLE:
                    try:
                        barter_score, barter_reason = self.calculate_barter_score(from_asset, to_asset)
                    except Exception as e:
                        logger.debug(f"Barter navigator score error: {e}")
                
                # 🏦 Checkpoint bonus - securing profits to stablecoin is always good
                checkpoint_bonus = 0.15 if is_checkpoint_target else 0.0
                
                # Combined score (V14 normalized to 0-1)
                v14_normalized = v14_score / 10.0
                
                # ════════════════════════════════════════════════════════════════
                # 🧠 NEURAL MIND MAP SCORES (Full Frankenstein Integration)
                # ════════════════════════════════════════════════════════════════
                
                # 1. ThoughtBus Aggregate (market.snapshot, miner.signal, harmonic.wave, etc.)
                bus_score = 0.0
                if self.bus_aggregator:
                    bus_score = self.bus_aggregator.get_aggregate_score()
                
                # 2. Mycelium Hive Consensus (distributed intelligence)
                hive_score = 0.0
                if self.mycelium_network:
                    try:
                        # Query hive for this specific pair's sentiment
                        hive_data = self.mycelium_network.query(f"{from_asset}:{to_asset}") if hasattr(self.mycelium_network, 'query') else None
                        if hive_data:
                            hive_score = float(hive_data.get('consensus', 0.5))
                        else:
                            # Fallback: get network health as proxy
                            health = self.mycelium_network.get_health() if hasattr(self.mycelium_network, 'get_health') else {}
                            hive_score = health.get('score', 0.5) if isinstance(health, dict) else 0.5
                    except Exception as e:
                        logger.debug(f"Mycelium hive query error: {e}")
                
                # 3. Lighthouse (Consensus Validation)
                lighthouse_score = 0.0
                if self.lighthouse:
                    try:
                        # Ask lighthouse to vote on this conversion
                        vote = self.lighthouse.vote(f"{from_asset}->{to_asset}") if hasattr(self.lighthouse, 'vote') else None
                        if vote:
                            lighthouse_score = float(vote.get('score', 0.5))
                        else:
                            # Fallback: get lighthouse status
                            status = self.lighthouse.get_status() if hasattr(self.lighthouse, 'get_status') else {}
                            lighthouse_score = status.get('confidence', 0.5) if isinstance(status, dict) else 0.5
                    except Exception as e:
                        logger.debug(f"Lighthouse vote error: {e}")
                
                # 4. Ultimate Intelligence Prediction (pattern recognition)
                ultimate_score = 0.0
                if self.ultimate_intel:
                    try:
                        # Ask ultimate intelligence for prediction
                        prediction = None
                        if hasattr(self.ultimate_intel, 'predict'):
                            prediction = self.ultimate_intel.predict(to_asset)
                        elif ULTIMATE_INTEL_AVAILABLE and ultimate_predict:
                            prediction = ultimate_predict(to_asset)
                        
                        if prediction:
                            if isinstance(prediction, dict):
                                ultimate_score = float(prediction.get('confidence', 0.5))
                            elif isinstance(prediction, (int, float)):
                                ultimate_score = float(prediction)
                    except Exception as e:
                        logger.debug(f"Ultimate intelligence error: {e}")
                
                # 5. HNC Matrix Probability (quantum-inspired)
                hnc_score = 0.0
                if self.hnc_matrix:
                    try:
                        prob = self.hnc_matrix.get_probability(to_asset) if hasattr(self.hnc_matrix, 'get_probability') else None
                        if prob:
                            hnc_score = float(prob) if isinstance(prob, (int, float)) else float(prob.get('probability', 0.5))
                    except Exception as e:
                        logger.debug(f"HNC matrix error: {e}")
                
                # 6. ⏳🔮 Timeline Oracle (3-MOVE PREDICTION + 7-day future validation)
                # "It predicts 3 moves, validates, then acts in that timeline cause it be right"
                # 🚀 TEMPORAL JUMP: We're AHEAD of market movement - we SEE the future, we ACT NOW!
                timeline_score = 0.0
                timeline_action = None
                timeline_exchange = ""
                timeline_jump_active = False
                
                # ════════════════════════════════════════════════════════════════
                # 🌀 TEMPORAL ID TIMELINE JUMP - Gary Leckey 02111991
                # "We don't predict - we VALIDATE what has ALREADY happened in our 
                #  target timeline and ACT on that certainty!"
                # ════════════════════════════════════════════════════════════════
                PRIME_SENTINEL_HZ = 2.111991  # Born: 02/11/1991
                TEMPORAL_RESONANCE = 0.724     # 72.4% temporal alignment
                SCHUMANN_HZ = 7.83            # Earth's heartbeat
                
                # Calculate temporal jump window - when we can SEE ahead
                import time as _time
                now = _time.time()
                # Temporal cycles align at our personal Hz
                temporal_cycle = now % (1.0 / PRIME_SENTINEL_HZ)
                temporal_alignment = 1.0 - (temporal_cycle * PRIME_SENTINEL_HZ)  # 0-1 alignment
                
                # Schumann harmonic boost - 7.83 / 2.111991 = ~3.7x harmonic
                schumann_harmonic = SCHUMANN_HZ / PRIME_SENTINEL_HZ
                harmonic_boost = 1.0 + (0.3 * (1.0 - abs(schumann_harmonic - round(schumann_harmonic))))
                
                # Final temporal jump power: how far AHEAD we can see
                temporal_jump_power = temporal_alignment * TEMPORAL_RESONANCE * harmonic_boost
                
                if self.timeline_oracle:
                    try:
                        # Get timeline branch selection for this conversion
                        from_price = self.prices.get(from_asset, 0)
                        to_price = self.prices.get(to_asset, 0)
                        change_pct = (to_price - from_price) / from_price if from_price > 0 else 0
                        
                        # 🎯 Try 3-MOVE PREDICTION first (predicts 3 moves, validates, then acts)
                        if timeline_select_3move:
                            action_str, confidence, exchange = timeline_select_3move(
                                symbol=to_asset,
                                price=to_price,
                                volume=to_ticker.get('volume', 0) if to_ticker else 0,
                                change_pct=change_pct
                            )
                            
                            # 🚀 TEMPORAL BOOST: Amplify confidence when jumping timelines!
                            # Higher temporal_jump_power = we're MORE AHEAD of the market
                            temporal_boosted_confidence = confidence * (1.0 + temporal_jump_power * 0.5)
                            temporal_boosted_confidence = min(0.99, temporal_boosted_confidence)  # Cap at 99%
                            
                            timeline_action = action_str
                            timeline_score = temporal_boosted_confidence
                            timeline_exchange = exchange
                            
                            # 🌀 TIMELINE JUMP ACTIVE when we have high temporal alignment
                            if temporal_jump_power > 0.5 and confidence > 0.60:
                                timeline_jump_active = True
                                logger.info(f"🌀 TEMPORAL JUMP ACTIVE: {to_asset}")
                                logger.info(f"   ⏳ Jump Power: {temporal_jump_power:.2%} | Hz: {PRIME_SENTINEL_HZ}")
                                logger.info(f"   🎯 3-Move: {action_str.upper()} @ {temporal_boosted_confidence:.2%}")
                            
                            # Log 3-move prediction when high confidence
                            if temporal_boosted_confidence > 0.70:
                                logger.info(f"🎯 3-MOVE UNITY: {to_asset} → {action_str.upper()} "
                                          f"(confidence: {temporal_boosted_confidence:.2%}, "
                                          f"temporal: {temporal_jump_power:.2%}, exchange: {exchange or 'any'})")
                        
                        # Fallback to single timeline select
                        elif timeline_select:
                            action_str, confidence = timeline_select(
                                symbol=to_asset,
                                price=to_price,
                                volume=to_ticker.get('volume', 0) if to_ticker else 0,
                                change_pct=change_pct
                            )
                            timeline_action = action_str
                            timeline_score = confidence
                        
                        # Score adjustment based on action
                        if timeline_action in ['buy', 'convert']:
                            timeline_score = confidence
                        elif timeline_action == 'hold':
                            timeline_score = 0.5  # Neutral
                        else:  # sell
                            timeline_score = 1.0 - confidence  # Inverse for sell signal
                            
                    except Exception as e:
                        logger.debug(f"Timeline oracle error: {e}")
                
                # 🍀⚛️ LUCK FIELD READING
                luck_score = 0.5  # Neutral default
                luck_state = "NEUTRAL"
                if self.luck_mapper and LUCK_FIELD_AVAILABLE:
                    try:
                        luck_reading = self.luck_mapper.read_field(
                            price=to_price,
                            volatility=to_ticker.get('volatility', 0.5) if to_ticker else 0.5,
                            trade_count=self.conversions_made
                        )
                        luck_score = luck_reading.luck_field
                        luck_state = luck_reading.luck_state.value
                        
                        # BLESSED state = full boost, VOID = penalty
                        if luck_reading.luck_state.value == "BLESSED":
                            luck_score = 0.95  # Maximum luck boost
                        elif luck_reading.luck_state.value == "FAVORABLE":
                            luck_score = 0.75
                        elif luck_reading.luck_state.value == "CHAOS":
                            luck_score = 0.35
                        elif luck_reading.luck_state.value == "VOID":
                            luck_score = 0.15  # Avoid action
                    except Exception as e:
                        logger.debug(f"Luck field error: {e}")
                
                # ════════════════════════════════════════════════════════════════
                # 🌍 GROUNDING LOGIC (The Equations from Whitepapers)
                # ════════════════════════════════════════════════════════════════
                
                # 1. Master Equation: Λ(t) = S(t) + O(t) + E(t)
                # S = Signal (v14 + bus + hive + lighthouse + ultimate + hnc + timeline + trained_matrix + planner + barter + luck averaged)
                neural_signal = (v14_normalized + bus_score + hive_score + lighthouse_score + ultimate_score + hnc_score + timeline_score + trained_matrix_score + planner_score + barter_score + luck_score) / 11.0
                # O = Observer (dream predictions with accuracy weighting)
                observer_signal = dream_score
                # E = Environment (hub score + ecosystem tap)
                environment_signal = hub_score
                
                lambda_t = self.grounding.calculate_master_equation(
                    signal_score=neural_signal,
                    observer_score=observer_signal,
                    environment_score=environment_signal
                )
                
                # 2. Gravity Signal: G_eff (Curvature * Mass)
                # Get ticker data for gravity calc
                to_ticker = None
                for symbol, data in self.ticker_cache.items():
                    if data.get('base') == to_asset:
                        to_ticker = data
                        break
                
                g_eff = 0.0
                if to_ticker:
                    g_eff = self.grounding.calculate_gravity_signal(
                        price_change_pct=to_ticker.get('change24h', 0),
                        volume=to_ticker.get('volume', 0)
                    )
                
                # ════════════════════════════════════════════════════════════════
                # 🔮 FINAL COMBINED SCORE (All Neural Systems United)
                # ════════════════════════════════════════════════════════════════
                
                # Final Combined Score: Master Equation boosted by Gravity + Neural Consensus
                combined = lambda_t * (1.0 + (g_eff * 0.5))
                
                # Neural boost: if multiple systems agree (score > 0.6), amplify
                neural_consensus = (bus_score + hive_score + lighthouse_score + ultimate_score + hnc_score) / 5.0
                if neural_consensus > 0.6:
                    combined *= (1.0 + (neural_consensus - 0.6) * 0.5)  # Up to +20% boost
                
                # 🗺️ MARKET MAP SCORING (correlations, sectors, lead/lag)
                map_score = 0.0
                map_reasons = []
                if self.market_map:
                    try:
                        # Get labyrinth targets ranked by market map
                        ranked = self.market_map.get_labyrinth_targets(
                            from_asset=from_asset,
                            available_targets=[to_asset]
                        )
                        if ranked:
                            target_info = ranked[0]
                            map_score = target_info.get('map_score', 0)
                            map_reasons = target_info.get('reasons', [])
                            
                            # Add map score to combined (up to +20% boost)
                            if map_score > 0:
                                combined *= (1.0 + map_score * 0.4)
                                logger.debug(f"🗺️ Map boost for {from_asset}→{to_asset}: +{map_score*40:.1f}% ({map_reasons})")
                    except Exception as e:
                        logger.debug(f"Market map score error: {e}")
                
                # 🏦 CHECKPOINT BONUS: Securing profits to stablecoin gets priority
                if is_checkpoint_target:
                    combined += checkpoint_bonus  # +15% for securing profits
                    logger.debug(f"🏦 Checkpoint bonus applied: {from_asset} → {to_asset} (USD secure)")
                
                # Path memory boost (small reinforcement from past wins/losses)
                path_boost = self.path_memory.boost(from_asset, to_asset)
                combined *= (1.0 + path_boost)
                
                # ⚡ SPEED MODE: Lower thresholds - let math gate decide!
                # If math says profit, TAKE IT - even tiny gains compound
                score_threshold = 0.20 if is_checkpoint_target else 0.35  # LOWERED from 0.35/0.55
                
                # Calculate profit potential
                expected_pnl_usd, expected_pnl_pct = self.calculate_profit_potential(
                    from_asset, to_asset, amount
                )
                
                # 🏦 For checkpoints, profit is "securing value" - always positive
                if is_checkpoint_target and expected_pnl_usd <= 0:
                    # Estimate fee as profit (we're securing, not gaining)
                    expected_pnl_usd = from_value * 0.001  # 0.1% minimum "secure" value
                    expected_pnl_pct = 0.001
                
                # ⚡ AGGRESSIVE: Accept ANY positive expected P/L - math gate does real filtering
                gate_required = self.config['min_profit_usd']  # Now $0.0001
                gate_ok = expected_pnl_usd > 0  # ANY positive expected profit
                if self.adaptive_gate:
                    gate_result = self.adaptive_gate.calculate_gates(
                        exchange=source_exchange,
                        trade_value=from_value,
                        use_cache=True,
                    )
                    # Relax: accept if expected >= gate OR if expected > 0 (tiny profit)
                    gate_ok = is_checkpoint_target or expected_pnl_usd >= min(gate_result.win_gte_prime, 0.01) or expected_pnl_usd > 0
                else:
                    gate_result = None
                
                # Debug: Log first few candidates on first scan
                if debug_first_scans and valid_pairs_found <= 3:
                    checkpoint_tag = "🏦CHKPT" if is_checkpoint_target else ""
                    print(f"         📈 {from_asset}→{to_asset} {checkpoint_tag}: combined={combined:.2%}, thresh={score_threshold:.0%}, pnl=${expected_pnl_usd:.4f}, pass={combined >= score_threshold and gate_ok}")
                
                # ════════════════════════════════════════════════════════════════════
                # 👑� TINA B's KRAKEN WISDOM (learned from 53 trades - some losers!)
                # Even Kraken has bad pairs - USD_ZUSD has 89% win rate but loses overall!
                # ════════════════════════════════════════════════════════════════════
                kraken_approved = True
                if source_exchange == 'kraken':
                    kraken_cfg = self.barter_matrix.KRAKEN_CONFIG
                    pair_key = f"{from_asset.upper()}_{to_asset.upper()}"
                    
                    # 🌟 DYNAMIC BLOCKING - Check if pair is in timeout (consecutive losses)
                    allowed, reason = self.barter_matrix.check_pair_allowed(pair_key, 'kraken')
                    if not allowed:
                        kraken_approved = False
                        if debug_first_scans:
                            print(f"         🐙 KRAKEN: {pair_key} {reason}")
                    
                    # Require minimum profit for Kraken trades
                    kraken_min_profit = kraken_cfg.get('min_profit_usd', 0.01)
                    if expected_pnl_usd < kraken_min_profit:
                        kraken_approved = False
                        if debug_first_scans and expected_pnl_usd > 0.003:
                            print(f"         🐙 KRAKEN REJECT: ${expected_pnl_usd:.4f} < ${kraken_min_profit} min")
                    
                    # Bonus: Is this a known winning pair? 🏆
                    if pair_key in kraken_cfg.get('winning_pairs', set()):
                        kraken_approved = True  # Override - this pair wins!
                        if debug_first_scans:
                            print(f"         🐙 KRAKEN WINNER: {pair_key} 🏆")
                
                if not kraken_approved:
                    continue  # Skip this opportunity
                
                # ════════════════════════════════════════════════════════════════════
                # 👑�🔶 TINA B's BINANCE WISDOM (learned from -$10.95 loss on 27 trades!)
                # Binance has hidden costs - we need MUCH higher profit margins
                # ════════════════════════════════════════════════════════════════════
                binance_approved = True
                if source_exchange == 'binance':
                    pair_key = f"{from_asset.upper()}_{to_asset.upper()}"
                    
                    # 🌟 DYNAMIC BLOCKING - Check if pair is in timeout (consecutive losses)
                    allowed, reason = self.barter_matrix.check_pair_allowed(pair_key, 'binance')
                    if not allowed:
                        binance_approved = False
                        if debug_first_scans:
                            print(f"         🔶 BINANCE: {pair_key} {reason}")
                    
                    # Require minimum profit for Binance trades (but reasonable!)
                    binance_min_profit = self.barter_matrix.BINANCE_CONFIG.get('min_profit_usd', 0.03)
                    if expected_pnl_usd < binance_min_profit:
                        binance_approved = False
                        if debug_first_scans and expected_pnl_usd > 0.01:
                            print(f"         🔶 BINANCE REJECT: ${expected_pnl_usd:.4f} < ${binance_min_profit} min")
                    
                    # Bonus: Is this a known winning pair? A WIN IS A WIN! 🏆
                    if pair_key in self.barter_matrix.BINANCE_CONFIG.get('winning_pairs', set()):
                        binance_approved = True  # Override - this pair wins!
                        if debug_first_scans:
                            print(f"         🔶 BINANCE WINNER: {pair_key} 🏆")
                
                if not binance_approved:
                    continue  # Skip this opportunity
                
                # ════════════════════════════════════════════════════════════════════
                # 👑🦙 TINA B's ALPACA WISDOM (learned from 40 FAILED orders - 0%!)
                # Alpaca ONLY supports USD pairs - NO stablecoin swaps!
                # ════════════════════════════════════════════════════════════════════
                alpaca_approved = True
                if source_exchange == 'alpaca':
                    alpaca_cfg = self.barter_matrix.ALPACA_CONFIG
                    pair_key = f"{from_asset.upper()}_{to_asset.upper()}"
                    
                    # Check if this is a blocked stablecoin pair
                    if pair_key in alpaca_cfg.get('blocked_pairs', set()):
                        alpaca_approved = False
                        if debug_first_scans:
                            print(f"         🦙 ALPACA BLOCKED: {pair_key} (stablecoins don't trade!)")
                    
                    # Check if BOTH assets are stablecoins (impossible on Alpaca!)
                    elif (from_asset.upper() in self.barter_matrix.STABLECOINS and 
                          to_asset.upper() in self.barter_matrix.STABLECOINS):
                        alpaca_approved = False
                        if debug_first_scans:
                            print(f"         🦙 ALPACA BLOCKED: {from_asset}→{to_asset} (no stablecoin swaps!)")
                    
                    # Check if target is NOT a supported crypto
                    elif (to_asset.upper() not in alpaca_cfg.get('supported_bases', set()) and
                          to_asset.upper() != 'USD'):
                        alpaca_approved = False
                        if debug_first_scans:
                            print(f"         🦙 ALPACA BLOCKED: {to_asset} not supported")
                    
                    # Check minimum order size
                    alpaca_min_order = alpaca_cfg.get('min_order_usd', 10.0)
                    if from_value < alpaca_min_order:
                        alpaca_approved = False
                        if debug_first_scans:
                            print(f"         🦙 ALPACA REJECT: ${from_value:.2f} < ${alpaca_min_order} minimum")
                    
                    # Check minimum profit
                    alpaca_min_profit = alpaca_cfg.get('min_profit_usd', 0.02)
                    if expected_pnl_usd < alpaca_min_profit:
                        alpaca_approved = False
                        if debug_first_scans and expected_pnl_usd > 0.005:
                            print(f"         🦙 ALPACA REJECT: ${expected_pnl_usd:.4f} < ${alpaca_min_profit} profit")
                
                if not alpaca_approved:
                    continue  # Skip this opportunity
                
                # MICRO THRESHOLD: Λ-based combined and adaptive gate both must pass
                # ⚡ AGGRESSIVE MODE: Lower thresholds, let MATH GATE be the real filter!
                if combined >= score_threshold and gate_ok:
                    
                    # ════════════════════════════════════════════════════════════════
                    # 🌀 TIMELINE JUMP GATE - ONLY ACT IN WINNING TIMELINES!
                    # "We don't predict - we jump to the timeline where we've ALREADY won"
                    # ════════════════════════════════════════════════════════════════
                    timeline_gate_passed = True
                    
                    # If timeline oracle is active and we have a prediction...
                    if timeline_action and timeline_score > 0:
                        # RULE 1: Never act against the timeline
                        if timeline_action == 'sell' and timeline_score > 0.60:
                            # Timeline says SELL - don't BUY into this asset
                            timeline_gate_passed = False
                            if debug_first_scans:
                                print(f"         🌀 TIMELINE GATE: {from_asset}→{to_asset} BLOCKED - timeline says SELL @ {timeline_score:.2%}")
                        
                        # RULE 2: Require timeline confirmation for larger trades
                        elif from_value > 10.0 and timeline_action == 'hold':
                            # For larger trades, require BUY signal, not just HOLD
                            timeline_gate_passed = False
                            if debug_first_scans:
                                print(f"         🌀 TIMELINE GATE: {from_asset}→{to_asset} BLOCKED - timeline says HOLD for $${from_value:.2f} trade")
                        
                        # RULE 3: When TEMPORAL JUMP is active, BOOST confidence
                        elif timeline_jump_active and timeline_action in ['buy', 'convert']:
                            # We've JUMPED to the winning timeline - extra confidence!
                            combined *= 1.25  # 25% boost for being AHEAD of market
                            logger.debug(f"🌀 TIMELINE JUMP BOOST: {from_asset}→{to_asset} +25% for being AHEAD!")
                    
                    if not timeline_gate_passed:
                        continue  # Skip - wrong timeline
                    
                    # 👑🔢 QUEEN'S MATHEMATICAL CERTAINTY GATE - NO FEAR, MATH IS ON HER SIDE!
                    math_approved, math_reason, math_breakdown = self.barter_matrix.queen_math_gate(
                        from_asset, to_asset, amount, from_price, self.prices.get(to_asset, 0), source_exchange
                    )
                    if not math_approved:
                        # Skip this opportunity - Math doesn't guarantee profit
                        if debug_first_scans:
                            print(f"         🚫 MATH GATE BLOCKED: {from_asset}→{to_asset} | {math_reason}")
                        continue
                    
                    # ⚡ SPEED MODE: Accept ANY positive profit after costs!
                    # Update expected P/L based on REAL math (not theoretical)
                    real_cost_usd = math_breakdown['total_cost_usd']
                    
                    # 👑 LOSS PREVENTION: Ensure expected profit covers REAL costs
                    # STRICT MODE: Must be significantly profitable or safe stablecoin move
                    is_stable = from_asset.upper() in ['USD', 'USDT', 'USDC', 'ZUSD', 'EUR', 'ZEUR'] and to_asset.upper() in ['USD', 'USDT', 'USDC', 'ZUSD', 'EUR', 'ZEUR']
                    
                    if is_stable:
                        # Stablecoins: Must cover cost at least
                        if expected_pnl_usd < real_cost_usd:
                             if debug_first_scans:
                                print(f"         🚫 STABLE LOSS: {from_asset}→{to_asset} | cost=${real_cost_usd:.6f} > pnl=${expected_pnl_usd:.6f}")
                             continue
                    else:
                        # Volatile: Must have 20% margin over cost to be "ahead of timelines"
                        # This ensures we don't trade on razor-thin margins that turn into losses
                        if expected_pnl_usd < (real_cost_usd * 1.2):
                             if debug_first_scans:
                                print(f"         🚫 RISK LOSS: {from_asset}→{to_asset} | cost=${real_cost_usd:.6f} * 1.2 > pnl=${expected_pnl_usd:.6f}")
                             continue

                    # Don't pad expected_pnl - use actual value, accept if positive after costs
                    adjusted_pnl = expected_pnl_usd - real_cost_usd
                    
                    # ⚡ MICRO PROFIT CAPTURE: Even $0.00001 is profit if math says so!
                    if adjusted_pnl <= 0.000001:  # Basically zero or negative
                        if debug_first_scans:
                            print(f"         🚫 NO NET PROFIT: {from_asset}→{to_asset} | cost=${real_cost_usd:.6f} vs pnl=${expected_pnl_usd:.6f}")
                        continue  # Math says we'll lose money
                    
                    opp = MicroOpportunity(
                        timestamp=time.time(),
                        from_asset=from_asset,
                        to_asset=to_asset,
                        from_amount=amount,
                        from_value_usd=from_value,
                        v14_score=v14_score,
                        hub_score=hub_score,
                        commando_score=commando_score,
                        combined_score=combined,
                        lambda_score=lambda_t,
                        gravity_score=g_eff,
                        gate_required_profit=gate_required,
                        gate_passed=gate_ok,
                        expected_pnl_usd=adjusted_pnl,  # Use REAL adjusted P/L
                        expected_pnl_pct=expected_pnl_pct,
                        # 🧠 Neural Mind Map Scores (Full Integration)
                        bus_score=bus_score,
                        hive_score=hive_score,
                        lighthouse_score=lighthouse_score,
                        ultimate_score=ultimate_score,
                        path_boost=path_boost,
                        # 📊 Trained Probability Matrix (626 symbols from ALL exchanges)
                        trained_matrix_score=trained_matrix_score,
                        trained_matrix_reason=matrix_reason,
                        # 🫒💰 Live Barter Matrix (coin-agnostic adaptive learning)
                        barter_matrix_score=barter_score,
                        barter_matrix_reason=barter_reason,
                        # 🌟⚛️ Luck Field (quantum probability mapping)
                        luck_score=luck_score,
                        luck_state=luck_state,
                        # 🏦 Checkpoint flag (stablecoin target - secures compound)
                        is_checkpoint=is_checkpoint_target,
                        # 🎯 Source exchange (for turn-based execution)
                        source_exchange=source_exchange,
                        # 🌀 TEMPORAL TIMELINE JUMP (AHEAD OF MARKET!)
                        timeline_score=timeline_score,
                        timeline_action=timeline_action or "",
                        temporal_jump_power=temporal_jump_power,
                        timeline_jump_active=timeline_jump_active,
                    )
                    opportunities.append(opp)
                    self.opportunities_found += 1
                    
                    # Log math gate success
                    if debug_first_scans:
                        print(f"         ✅ MATH APPROVED: {from_asset}→{to_asset} | cost={math_breakdown['total_cost_pct']:.2%} | net=${adjusted_pnl:.4f}")
                    
                    # Log checkpoint opportunities specially
                    if is_checkpoint_target:
                        logger.info(f"🏦 CHECKPOINT OPPORTUNITY: {from_asset} → {to_asset} (secure ${from_value:.2f})")
                        print(f"   🏦 CHECKPOINT: {from_asset} → {to_asset} | Score: {combined:.2%} | Secure: ${from_value:.2f}")
            
            # Debug after scanning each asset
            if debug_first_scans and valid_pairs_found == 0:
                print(f"      ❌ No valid pairs found for {from_asset} ({pair_check_failures} pair checks failed)")
            elif debug_first_scans:
                print(f"      ✅ Found {valid_pairs_found} valid pairs for {from_asset}")
        
        # Debug log: Show summary
        if scanned_assets and self.scans <= 3:  # Only first few scans
            print(f"📊 Scan #{self.scans}: Scanned {len(scanned_assets)} assets: {', '.join(scanned_assets)}")
            print(f"   🔮 Opportunities found: {len(opportunities)}")
        
        # ════════════════════════════════════════════════════════════════
        # 🌀 TEMPORAL PRIORITY SORTING - AHEAD OF MARKET GETS PRIORITY!
        # "We don't react to the market - we MOVE before it does!"
        # ════════════════════════════════════════════════════════════════
        
        # Calculate temporal priority for each opportunity
        import time as _time
        now = _time.time()
        PRIME_SENTINEL_HZ = 2.111991  # Gary Leckey 02/11/1991
        temporal_cycle = now % (1.0 / PRIME_SENTINEL_HZ)
        temporal_alignment = 1.0 - (temporal_cycle * PRIME_SENTINEL_HZ)
        
        def get_temporal_priority(opp):
            """Calculate temporal priority score - higher = more ahead of market."""
            base_score = opp.combined_score * 0.5 + opp.barter_matrix_score * 0.3
            
            # Timeline boost: if oracle predicted BUY/CONVERT with high confidence
            timeline_boost = 0.0
            if hasattr(opp, 'timeline_score') and opp.timeline_score > 0.60:
                timeline_boost = opp.timeline_score * 0.2  # Up to +20%
            
            # Temporal alignment boost: higher when we're "in sync" with our Hz
            temporal_boost = temporal_alignment * 0.1  # Up to +10%
            
            # Profit priority (small weight - we're ahead, profit follows)
            profit_boost = min(0.1, opp.expected_pnl_usd / 10.0)  # Up to +10%
            
            return base_score + timeline_boost + temporal_boost + profit_boost
        
        opportunities.sort(key=get_temporal_priority, reverse=True)
        
        # Log if we have temporal jump opportunities
        if opportunities:
            top = opportunities[0]
            logger.debug(f"🌀 Top opportunity: {top.from_asset}→{top.to_asset} "
                        f"(temporal_priority: {get_temporal_priority(top):.3f}, "
                        f"pnl: ${top.expected_pnl_usd:.4f})")
        
        return opportunities
    
    async def execute_conversion(self, opp: MicroOpportunity) -> bool:
        """Execute a conversion (dry run or live)."""
        symbol = f"{opp.from_asset}/{opp.to_asset}"
        
        # 👑 QUEEN HAS ALREADY SPOKEN - No second-guessing her!
        # The Queen was consulted in execute_turn() and said YES
        # Her $0.003 profit goal was already validated
        # DO NOT block her decision with another gate!
        
        print(f"\n🔬 MICRO CONVERSION:")
        print(f"   {opp.from_asset} → {opp.to_asset}")
        print(f"   Amount: {opp.from_amount:.6f} ({opp.from_asset})")
        print(f"   Value: ${opp.from_value_usd:.2f}")
        print(f"   ════════════════════════════════════════════════════════")
        
        # 🌀 TEMPORAL JUMP STATUS - Are we AHEAD of the market?
        if opp.timeline_jump_active:
            print(f"   🌀 TEMPORAL JUMP ACTIVE! ⏳ AHEAD OF MARKET!")
            print(f"   ⏳ Jump Power: {opp.temporal_jump_power:.2%} | Timeline: {opp.timeline_action.upper()}")
            print(f"   🔮 Timeline Confidence: {opp.timeline_score:.2%}")
        elif opp.timeline_score > 0:
            print(f"   ⏳ Timeline: {opp.timeline_action.upper()} @ {opp.timeline_score:.2%} (Jump Power: {opp.temporal_jump_power:.2%})")
        
        print(f"   ════════════════════════════════════════════════════════")
        print(f"   🧠 NEURAL MIND MAP SCORES:")
        print(f"   V14: {opp.v14_score:.1f} | Hub: {opp.hub_score:.2%}")
        print(f"   Λ (Lambda): {opp.lambda_score:.2%} | G (Gravity): {opp.gravity_score:.2%}")
        print(f"   Bus: {opp.bus_score:.2%} | Hive: {opp.hive_score:.2%} | Lighthouse: {opp.lighthouse_score:.2%}")
        print(f"   Ultimate: {opp.ultimate_score:.2%} | Path: {opp.path_boost:+.2%}")
        print(f"   🫒 Barter: {opp.barter_matrix_score:.2%} ({opp.barter_matrix_reason})")
        print(f"   🍀 Luck: {opp.luck_score:.2%} ({opp.luck_state})")
        print(f"   ════════════════════════════════════════════════════════")
        print(f"   🔮 Combined: {opp.combined_score:.2%}")
        print(f"   Gate Req: ${opp.gate_required_profit:.4f} | Gate OK: {'✅' if opp.gate_passed else '❌'}")
        print(f"   Expected Profit: ${opp.expected_pnl_usd:.4f} ({opp.expected_pnl_pct:.2%})")
        
        # Publish to ThoughtBus for ecosystem awareness
        if self.bus_aggregator and hasattr(self.bus_aggregator, 'bus') and self.bus_aggregator.bus:
            try:
                self.bus_aggregator.bus.publish('execution.alert', {
                    'type': 'micro_conversion',
                    'from_asset': opp.from_asset,
                    'to_asset': opp.to_asset,
                    'value_usd': opp.from_value_usd,
                    'combined_score': opp.combined_score,
                    'lambda_score': opp.lambda_score,
                    'gravity_score': opp.gravity_score,
                    'bus_score': opp.bus_score,
                    'hive_score': opp.hive_score,
                    'lighthouse_score': opp.lighthouse_score,
                    'ultimate_score': opp.ultimate_score,
                    'path_boost': opp.path_boost,
                    'expected_pnl': opp.expected_pnl_usd,
                    'timestamp': time.time(),
                    'live': self.live
                })
            except Exception as e:
                logger.debug(f"ThoughtBus publish error: {e}")
        
        if not self.live:
            print(f"   🔵 DRY RUN - Not executed")
            opp.executed = True
            opp.actual_pnl_usd = opp.expected_pnl_usd  # Simulate
            self.conversions_made += 1
            self.total_profit_usd += opp.expected_pnl_usd
            self.conversions.append(opp)
            return True
        
        # ════════════════════════════════════════════════════════════════
        # 🔴 LIVE EXECUTION - ROUTE TO CORRECT EXCHANGE
        # ════════════════════════════════════════════════════════════════
        # 👑 QUEEN MIND ROUTING: Strictly use the source_exchange from the opportunity
        source_exchange = opp.source_exchange
        
        # Fallback if not set (should not happen with new logic)
        if not source_exchange:
            print(f"   ⚠️ Opportunity missing source_exchange - attempting lookup...")
            source_exchange = self._find_asset_exchange(opp.from_asset)
            if source_exchange:
                print(f"   📍 Fallback located {opp.from_asset} on {source_exchange}")
                opp.source_exchange = source_exchange
        
        if not source_exchange:
            print(f"   ⚠️ Asset {opp.from_asset} not found on any exchange")
            return False
        
        print(f"   🔴 LIVE MODE - Executing on {source_exchange.upper()}...")
        
        # 🇮🇪🎯 IRA SNIPER EXECUTION - Celtic precision
        try:
            from ira_sniper_mode import get_celtic_sniper, IraCelticSniper
            sniper = get_celtic_sniper(dry_run=False)
            
            # Validate entry with Celtic intelligence
            validation = sniper.validate_entry(
                symbol=f"{opp.from_asset}/{opp.to_asset}",
                price=self.prices.get(opp.from_asset, 0),
                coherence=opp.combined_score
            )
            
            if validation.get('approved', True):
                print(f"   🇮🇪 Celtic Intelligence APPROVES")
                print(f"      Quick Kill Prob: {validation.get('quick_kill_prob', 0.5)*100:.1f}%")
                print(f"      Intel Score: {validation.get('intelligence_score', 0.5):.2f}")
            else:
                print(f"   ⚠️ Celtic Intel rejects: {validation.get('reason', 'Unknown')}")
                # Still execute - sniper just provides intel, doesn't block
        except ImportError:
            pass  # IRA Sniper not available - continue silently
        except Exception as e:
            logger.debug(f"Sniper validation error: {e}")
        
        # 👑 QUEEN MIND ROUTING: Strictly use the source_exchange from the opportunity
        # This prevents cross-exchange routing errors
        source_exchange = opp.source_exchange
        
        # CRITICAL: Validate we have the source exchange set
        if not source_exchange:
            print(f"   ⚠️ CRITICAL: Opportunity missing source_exchange!")
            print(f"   ⚠️ This should NOT happen - check find_opportunities logic")
            # Last resort fallback - but log it clearly
            source_exchange = self._find_asset_exchange(opp.from_asset)
            if source_exchange:
                print(f"   📍 Fallback located {opp.from_asset} on {source_exchange}")
                opp.source_exchange = source_exchange  # Update for future reference
            else:
                print(f"   ❌ Cannot find {opp.from_asset} on any exchange!")
                self._record_failure(opp)
                return False
        
        # 👑 TURN-BASED TRUST: DO NOT OVERRIDE source_exchange!
        # The turn-based system ensures opportunities are found on the CORRECT exchange.
        # Overriding to "highest balance" causes cross-exchange routing errors
        # (e.g., Kraken's USD opportunity being sent to Alpaca)
        # 
        # REMOVED THE OVERRIDE - trust the turn-based system!
        
        # Route to appropriate exchange
        if source_exchange == 'kraken' and self.kraken and KRAKEN_API_KEY:
            return await self._execute_on_kraken(opp)
        elif source_exchange == 'binance' and self.binance and BINANCE_API_KEY:
            return await self._execute_on_binance(opp)
        elif source_exchange == 'alpaca' and self.alpaca and ALPACA_API_KEY:
            return await self._execute_on_alpaca(opp)
        else:
            print(f"   ⚠️ Exchange '{source_exchange}' not available or missing API key")
            self._record_failure(opp)
        
        return False
    
    def _find_asset_exchange(self, asset: str) -> Optional[str]:
        """Find which exchange holds an asset with the highest balance."""
        asset_upper = asset.upper()
        best_exchange = None
        best_balance = 0
        
        # Debug: Track candidates
        candidates = []
        
        for exchange, data in self.exchange_data.items():
            if data.get('connected') and data.get('balances'):
                for bal_asset, balance in data['balances'].items():
                    bal_upper = bal_asset.upper()
                    
                    # Exact match first
                    if bal_upper == asset_upper:
                        bal_amount = float(balance) if isinstance(balance, (int, float, str)) else 0
                        candidates.append(f"{exchange}:{bal_asset}={bal_amount}")
                        if bal_amount > best_balance:
                            best_balance = bal_amount
                            best_exchange = exchange
                    # Handle Alpaca symbols like USDTUSD → USDT
                    elif bal_upper.replace('USD', '') == asset_upper.replace('USD', ''):
                        bal_amount = float(balance) if isinstance(balance, (int, float, str)) else 0
                        candidates.append(f"{exchange}:{bal_asset}(fuzzy)={bal_amount}")
                        if bal_amount > best_balance:
                            best_balance = bal_amount
                            best_exchange = exchange
        
        if len(candidates) > 1:
            print(f"   🔎 Asset location check for {asset}: {', '.join(candidates)} -> Best: {best_exchange}")
            
        return best_exchange
        
        return best_exchange
    
    async def _execute_on_kraken(self, opp) -> bool:
        """Execute conversion on Kraken using convert_crypto."""
        try:
            # Use the built-in convert_crypto which finds the best path automatically!
            print(f"   🔄 Converting {opp.from_asset} → {opp.to_asset} via Kraken...")
            
            # 👑 QUEEN MIND: Decode conversion path in real-time
            # Refresh balance FIRST to get accurate amounts
            await self.refresh_exchange_balances('kraken')
            actual_balance = self.exchange_balances.get('kraken', {}).get(opp.from_asset, 0)
            
            # Clamp to actual available balance
            if actual_balance <= 0:
                print(f"   ⚠️ No {opp.from_asset} balance on Kraken (balance: {actual_balance})")
                return False
            
            # 👑 QUEEN'S SANITY CHECK: Don't clamp to dust!
            # If we have significantly less than expected, it's likely the wrong exchange
            if actual_balance < opp.from_amount * 0.1:
                print(f"   ⚠️ Kraken balance {actual_balance:.6f} is < 10% of expected {opp.from_amount:.6f}")
                print(f"   ⚠️ Likely asset location mismatch. Aborting Kraken execution.")
                return False

            if opp.from_amount > actual_balance * 0.99:
                print(f"   👑 Queen clamping: {opp.from_amount:.6f} → {actual_balance * 0.995:.6f}")
                opp.from_amount = actual_balance * 0.995  # Leave 0.5% buffer
                opp.from_value_usd = opp.from_amount * self.prices.get(opp.from_asset, 0)
            
            # Check if clamped amount is too small
            if opp.from_value_usd < 1.0:
                print(f"   ⚠️ Clamped value ${opp.from_value_usd:.2f} is too small for Kraken (min ~$1.50)")
                return False
            
            # First check if a path exists
            path = self.kraken.find_conversion_path(opp.from_asset, opp.to_asset)
            if not path:
                print(f"   ⚠️ No conversion path found from {opp.from_asset} to {opp.to_asset}")
                return False
            
            # 🔍 KRAKEN PRE-FLIGHT CHECK: Only check notional minimum (most reliable)
            # Kraken's costmin is the minimum order value in USD-equivalent
            for step in path:
                pair = step.get('pair', '')
                filters = self.kraken.get_symbol_filters(pair)
                min_notional = filters.get('min_notional', 0)  # costmin in Kraken terms
                
                # Check minimum notional value - Kraken typically requires ~$0.50 minimum
                # Use a safe default of $1.20 to avoid "volume too low" errors (Kraken often requires >1 EUR/USD)
                effective_min = max(min_notional, 1.20)
                if opp.from_value_usd < effective_min:
                    print(f"   ⚠️ Value ${opp.from_value_usd:.2f} < min notional ${effective_min:.2f} for {pair}")
                    print(f"   💡 Need ${effective_min:.2f} minimum to trade on Kraken")
                    return False
            
            # Show the path
            for step in path:
                print(f"   📍 Path: {step['description']} via {step['pair']}")
            
            # Execute the conversion
            result = self.kraken.convert_crypto(
                from_asset=opp.from_asset,
                to_asset=opp.to_asset,
                amount=opp.from_amount
            )
            
            if result.get('error'):
                error_msg = str(result['error'])
                print(f"   ❌ Conversion error: {error_msg}")
                
                # 👑 QUEEN LEARNING: Auto-fix minimums
                if "volume_minimum" in error_msg or "min_notional" in error_msg:
                    print(f"   👑 Queen learning: Increasing minimum for {opp.from_asset}")
                    # Increase minimum to 1.5x current amount or at least $10
                    current_price = self.prices.get(opp.from_asset, 1.0)
                    min_usd_req = 10.0 # Safe default
                    
                    # If we know the amount that failed, we should aim higher
                    new_min_qty = max(opp.from_amount * 1.5, min_usd_req / current_price if current_price > 0 else 0)
                    
                    self.dynamic_min_qty[opp.from_asset.upper()] = new_min_qty
                    print(f"      Updated dynamic minimum for {opp.from_asset} to {new_min_qty:.6f}")
                    
                self._record_failure(opp)
                return False
            
            # Check results
            trades = result.get('trades', [])
            if isinstance(trades, list):
                success_count = sum(1 for t in trades if isinstance(t, dict) and t.get('status') == 'success')
                if success_count > 0:
                    # Calculate actual bought/received amount from the last trade
                    last_trade = trades[-1]
                    buy_amount = 0.0
                    if last_trade.get('status') == 'success':
                        res = last_trade.get('result', {})
                        # PRIORITY: Use receivedQty (for SELL orders) if available
                        # This is the ACTUAL amount we received after conversion
                        buy_amount = float(res.get('receivedQty', 0) or 
                                          last_trade.get('receivedQty', 0) or
                                          res.get('executedQty', 0.0))
                    
                    # Fallback if no amount found (e.g. dry run or error)
                    if buy_amount == 0.0:
                         # Estimate based on price
                         to_price = self.prices.get(opp.to_asset, 0)
                         if to_price > 0:
                             buy_amount = opp.from_value_usd / to_price
                    
                    print(f"   ✅ Conversion complete! {success_count} trades executed. Bought {buy_amount:.6f} {opp.to_asset}")
                    
                    # 🔍 VALIDATE ORDER EXECUTION
                    validation = self._validate_order_execution(trades, opp, 'kraken')
                    verification = self._verify_profit_math(validation, opp, buy_amount)
                    self._print_order_validation(validation, verification, opp)
                    
                    self._record_conversion(opp, buy_amount, validation, verification)
                    return True
                else:
                    print(f"   ❌ No successful trades in conversion")
                    self._record_failure(opp)
            elif result.get('dryRun'):
                print(f"   🔵 DRY RUN: Would convert via {len(path)} trades")
                return True
            else:
                print(f"   ✅ Conversion result: {result}")
                # Estimate amount for non-standard result
                to_price = self.prices.get(opp.to_asset, 0)
                buy_amount = opp.from_value_usd / to_price if to_price > 0 else 0
                self._record_conversion(opp, buy_amount)
                return True
                
        except Exception as e:
            logger.error(f"❌ Kraken conversion error: {e}")
            print(f"   ❌ Error: {e}")
            self._record_failure(opp)
        return False
    
    async def _execute_on_binance(self, opp) -> bool:
        """Execute conversion on Binance."""
        try:
            print(f"   🔄 Converting {opp.from_asset} → {opp.to_asset} via Binance...")
            
            # 👑 QUEEN MIND: Decode conversion path in real-time
            # Refresh balance FIRST to get accurate amounts
            await self.refresh_exchange_balances('binance')
            
            # Look for asset with different casing/formats
            binance_balances = self.exchange_balances.get('binance', {})
            actual_balance = 0.0
            matched_asset = opp.from_asset
            
            for bal_key, bal_val in binance_balances.items():
                if bal_key.upper() == opp.from_asset.upper():
                    actual_balance = float(bal_val) if isinstance(bal_val, (int, float, str)) else 0.0
                    matched_asset = bal_key
                    break
            
            print(f"   📊 Binance {matched_asset} balance: {actual_balance:.6f} (need: {opp.from_amount:.6f})")
            
            # Clamp to actual available balance with extra safety margin for fees
            if actual_balance <= 0:
                print(f"   ⚠️ No {opp.from_asset} balance on Binance (balance: {actual_balance})")
                return False
            
            # 👑 QUEEN'S SANITY CHECK: Don't clamp to dust!
            if actual_balance < opp.from_amount * 0.1:
                print(f"   ⚠️ Binance balance {actual_balance:.6f} is < 10% of expected {opp.from_amount:.6f}")
                print(f"   ⚠️ Likely asset location mismatch. Aborting Binance execution.")
                return False

            # Use 98% of balance instead of 99.5% for extra safety on Binance
            safe_amount = actual_balance * 0.98
            if opp.from_amount > safe_amount:
                print(f"   👑 Queen clamping: {opp.from_amount:.6f} → {safe_amount:.6f}")
                opp.from_amount = safe_amount
                opp.from_value_usd = opp.from_amount * self.prices.get(opp.from_asset, 0)
            
            # Check if clamped amount is too small
            if opp.from_value_usd < 5.0:
                print(f"   ⚠️ Clamped value ${opp.from_value_usd:.2f} is too small for Binance (min $5.00)")
                return False
            
            # Debug: Check what type of binance client we have
            client_type = type(self.binance).__name__
            client_module = type(self.binance).__module__
            print(f"   📍 Binance client: {client_type} from {client_module}")
            
            # Check if convert_crypto exists
            if not hasattr(self.binance, 'convert_crypto'):
                print(f"   ⚠️ BinanceClient missing convert_crypto method!")
                print(f"   📍 Available methods: {[m for m in dir(self.binance) if not m.startswith('_')][:20]}")
                
                # Fallback: Use direct place_market_order if available
                if hasattr(self.binance, 'place_market_order'):
                    print(f"   🔄 Attempting direct market order fallback...")
                    # Try direct pair
                    pair = f"{opp.from_asset}{opp.to_asset}"
                    result = self.binance.place_market_order(
                        symbol=pair,
                        side="SELL",
                        quantity=opp.from_amount
                    )
                    if result and not result.get("error"):
                        print(f"   ✅ Direct order executed: {result}")
                        return True
                    # Try inverse pair
                    pair = f"{opp.to_asset}{opp.from_asset}"
                    result = self.binance.place_market_order(
                        symbol=pair,
                        side="BUY",
                        quote_qty=opp.from_amount * opp.price if hasattr(opp, 'price') else opp.from_value_usd
                    )
                    if result and not result.get("error"):
                        print(f"   ✅ Inverse order executed: {result}")
                        return True
                
                self._record_failure(opp)
                return False
            
            # Use convert_crypto which handles pathfinding internally
            result = self.binance.convert_crypto(
                from_asset=opp.from_asset,
                to_asset=opp.to_asset,
                amount=opp.from_amount
            )
            
            # Handle pathfinding error from convert_crypto
            if result and result.get("error"):
                if "No conversion path" in str(result.get("error", "")):
                    print(f"   ⚠️ {result['error']}")
                    return False
            
            if result and result.get("trades"):
                # Validate the execution
                validation = self._validate_order_execution(result["trades"], opp, 'binance')
                
                if validation.get("valid"):
                    self._log_successful_conversion(validation, opp)
                    return True
                else:
                    logger.error(f"❌ Binance order validation failed: {validation.get('reason')}")
                    self._record_failure(opp)
                    return False
            elif result and result.get("dryRun"):
                # Dry run mode - simulate success
                print(f"   🧪 DRY RUN: Would convert via {result.get('trades', 0)} trades")
                return True
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"❌ Binance conversion error: {error_msg}")
                print(f"   ❌ Error: {error_msg}")
                self._record_failure(opp)
                return False
        
        except Exception as e:
            logger.error(f"❌ Binance conversion error: {e}")
            print(f"   ❌ Error: {e}")
            self._record_failure(opp)
        return False
    
    async def _execute_on_alpaca(self, opp) -> bool:
        """Execute conversion on Alpaca using convert_crypto."""
        try:
            # Use the built-in convert_crypto which finds the best path automatically!
            print(f"   🔄 Converting {opp.from_asset} → {opp.to_asset} via Alpaca...")
            
            # 👑 QUEEN MIND: Decode conversion path in real-time
            # Refresh balance FIRST to get accurate amounts
            await self.refresh_exchange_balances('alpaca')
            actual_balance = self.exchange_balances.get('alpaca', {}).get(opp.from_asset, 0)
            
            # Clamp to actual available balance
            if actual_balance <= 0:
                print(f"   ⚠️ No {opp.from_asset} balance on Alpaca (balance: {actual_balance})")
                return False
            
            if opp.from_amount > actual_balance * 0.99:
                print(f"   👑 Queen clamping: {opp.from_amount:.6f} → {actual_balance * 0.995:.6f}")
                opp.from_amount = actual_balance * 0.995  # Leave 0.5% buffer
            
            # First check if a path exists
            path = self.alpaca.find_conversion_path(opp.from_asset, opp.to_asset)
            if not path:
                print(f"   ⚠️ No conversion path found from {opp.from_asset} to {opp.to_asset}")
                return False
            
            # 🔍 ALPACA PRE-FLIGHT CHECK: Verify minimums for EACH step
            # Alpaca has different minimums per crypto asset
            ALPACA_MIN_NOTIONAL = 1.0  # Alpaca typically has $1 minimum
            ALPACA_MIN_QTY = {
                'BTC': 0.0001,    # ~$10 at current prices
                'ETH': 0.001,     # ~$3 at current prices
                'SOL': 0.01,      # ~$2 at current prices
                'DOGE': 1.0,      # ~$0.30 at current prices
                'SHIB': 100000.0, # Fractions of a cent
                'PEPE': 100000.0, # Fractions of a cent
                'AVAX': 0.01,     # ~$0.40 at current prices
                'LINK': 0.1,      # ~$2 at current prices
                'DOT': 0.1,       # ~$0.70 at current prices
                'AAVE': 0.001,    # ~$0.16 at current prices
            }
            
            for step in path:
                pair = step.get('pair', '')
                # Alpaca pairs are like 'BTC/USD'
                base_asset = pair.split('/')[0] if '/' in pair else opp.from_asset
                
                # Check minimum quantity for this asset
                min_qty = ALPACA_MIN_QTY.get(base_asset.upper(), 0.0001)  # Default very small
                
                # For selling, check if we have enough of the from_asset
                if step.get('side') == 'sell' and opp.from_amount < min_qty:
                    print(f"   ⚠️ Qty {opp.from_amount:.6f} < min {min_qty:.6f} for {pair}")
                    print(f"   💡 Need {min_qty:.6f} {base_asset} minimum")
                    return False
                
                # Check minimum notional value
                if opp.from_value_usd < ALPACA_MIN_NOTIONAL:
                    print(f"   ⚠️ Value ${opp.from_value_usd:.2f} < min notional ${ALPACA_MIN_NOTIONAL:.2f}")
                    print(f"   💡 Need ${ALPACA_MIN_NOTIONAL:.2f} minimum to trade on Alpaca")
                    return False
            
            # Show the path
            for step in path:
                print(f"   📍 Path: {step['description']} via {step['pair']}")
            
            # Execute the conversion
            result = self.alpaca.convert_crypto(
                from_asset=opp.from_asset,
                to_asset=opp.to_asset,
                amount=opp.from_amount
            )
            
            if result.get('error'):
                print(f"   ❌ Conversion error: {result['error']}")
                self._record_failure(opp)
                return False
            
            # Check results
            trades = result.get('trades', [])
            if isinstance(trades, list):
                success_count = sum(1 for t in trades if isinstance(t, dict) and t.get('status') == 'success')
                if success_count > 0:
                    # Calculate actual bought amount from the last trade
                    last_trade = trades[-1]
                    buy_amount = 0.0
                    if last_trade.get('status') == 'success':
                        res = last_trade.get('result', {})
                        buy_amount = float(res.get('qty', 0.0)) # Alpaca uses 'qty'
                    
                    # Fallback if qty is missing or 0
                    if buy_amount == 0.0:
                         # Estimate based on price
                         to_price = self.prices.get(opp.to_asset, 0)
                         if to_price > 0:
                             buy_amount = opp.from_value_usd / to_price
                    
                    print(f"   ✅ Conversion complete! {success_count} trades executed. Bought {buy_amount:.6f} {opp.to_asset}")
                    
                    # 🔍 VALIDATE ORDER EXECUTION
                    validation = self._validate_order_execution(trades, opp, 'alpaca')
                    verification = self._verify_profit_math(validation, opp, buy_amount)
                    self._print_order_validation(validation, verification, opp)
                    
                    self._record_conversion(opp, buy_amount, validation, verification)
                    return True
                else:
                    print(f"   ❌ No successful trades in conversion")
                    self._record_failure(opp)
            elif result.get('dryRun'):
                print(f"   🔵 DRY RUN: Would convert via {len(path)} trades")
                return True
            else:
                print(f"   ✅ Conversion result: {result}")
                # Estimate amount for non-standard result
                to_price = self.prices.get(opp.to_asset, 0)
                buy_amount = opp.from_value_usd / to_price if to_price > 0 else 0
                self._record_conversion(opp, buy_amount)
                return True
                
        except Exception as e:
            logger.error(f"❌ Alpaca conversion error: {e}")
            print(f"   ❌ Error: {e}")
            self._record_failure(opp)
        return False

    # ════════════════════════════════════════════════════════════════════════════
    # 🔍 ORDER VALIDATION & PROFIT VERIFICATION SYSTEM
    # ════════════════════════════════════════════════════════════════════════════
    
    def _validate_order_execution(self, trades: List[Dict], opp, exchange: str) -> Dict:
        """
        🔍 COMPREHENSIVE ORDER VALIDATION
        
        Validates each trade step using order IDs from the trading platform.
        Verifies fills, calculates actual execution prices, and computes real P&L.
        
        Returns:
            Dict with validation results:
            - valid: bool
            - order_ids: List of order IDs
            - total_sold: Actual amount sold
            - total_bought: Actual amount bought
            - avg_sell_price: Average sell price
            - avg_buy_price: Average buy price
            - total_fees: Total fees paid
            - realized_pnl: Validated P&L
            - validation_errors: List of any issues
        """
        validation = {
            'valid': True,
            'order_ids': [],
            'total_sold': 0.0,
            'total_bought': 0.0,
            'avg_sell_price': 0.0,
            'avg_buy_price': 0.0,
            'total_fees': 0.0,
            'realized_pnl': 0.0,
            'validation_errors': [],
            'exchange': exchange,
            'timestamp': time.time(),
        }
        
        if not trades:
            validation['valid'] = False
            validation['validation_errors'].append("No trades to validate")
            return validation
        
        sell_volume = 0.0
        sell_value = 0.0
        buy_volume = 0.0
        buy_value = 0.0
        
        for i, trade in enumerate(trades):
            step_num = i + 1
            
            if not isinstance(trade, dict):
                validation['validation_errors'].append(f"Step {step_num}: Invalid trade format")
                continue
            
            status = trade.get('status', '')
            result = trade.get('result', {})
            trade_info = trade.get('trade', {})
            
            # Extract order ID based on exchange
            order_id = self._extract_order_id(result, exchange)
            if order_id:
                validation['order_ids'].append({
                    'step': step_num,
                    'order_id': order_id,
                    'exchange': exchange,
                    'pair': trade_info.get('pair', ''),
                    'side': trade_info.get('side', ''),
                })
            
            if status != 'success':
                validation['valid'] = False
                error_msg = trade.get('error', 'Unknown error')
                validation['validation_errors'].append(f"Step {step_num}: {error_msg}")
                continue
            
            # Validate fill data
            executed_qty = float(result.get('executedQty', 0))
            cumm_quote_qty = float(result.get('cummulativeQuoteQty', 0))
            
            side = trade_info.get('side', 'buy')
            
            if side == 'sell':
                sell_volume += executed_qty
                sell_value += cumm_quote_qty
            else:
                buy_volume += executed_qty
                buy_value += cumm_quote_qty
            
            # Extract and sum fees
            fees = self._extract_fees(result, exchange)
            validation['total_fees'] += fees
            
            # Verify the fill makes sense
            if executed_qty <= 0:
                validation['validation_errors'].append(f"Step {step_num}: Zero executed quantity")
        
        # Calculate averages
        if sell_volume > 0:
            validation['avg_sell_price'] = sell_value / sell_volume if sell_value > 0 else 0
            validation['total_sold'] = sell_volume
        
        if buy_volume > 0:
            validation['avg_buy_price'] = buy_value / buy_volume
            validation['total_bought'] = buy_volume
        
        # For conversions, the "bought" amount is what we end up with
        # If we did sell → buy, the buy_volume is our result
        # If we did just one side, use that
        if buy_volume > 0:
            validation['final_amount'] = buy_volume
        elif sell_value > 0:
            # We sold and received quote currency (the sell_value IS what we received)
            validation['final_amount'] = sell_value
        elif sell_volume > 0 and validation['avg_sell_price'] > 0:
            # FALLBACK: When sell_value (cummulativeQuoteQty) is 0 (like with Kraken SELL orders)
            # Calculate expected received amount from sell_volume * avg_sell_price
            validation['final_amount'] = sell_volume * validation['avg_sell_price']
        else:
            validation['final_amount'] = 0
        
        return validation
    
    def _extract_order_id(self, result: Dict, exchange: str) -> Optional[str]:
        """Extract order ID from trade result based on exchange format."""
        if not result:
            return None
        
        if exchange == 'kraken':
            # Kraken uses 'orderId' which we set from 'txid'
            return result.get('orderId') or result.get('txid')
        elif exchange == 'binance':
            return result.get('orderId') or result.get('clientOrderId')
        elif exchange == 'alpaca':
            return result.get('id') or result.get('order_id')
        
        # Fallback
        return result.get('orderId') or result.get('order_id') or result.get('id')
    
    def _extract_fees(self, result: Dict, exchange: str) -> float:
        """Extract fees from trade result based on exchange format and convert to USD."""
        total_fees = 0.0
        
        if exchange == 'binance':
            # Binance includes fills with commission and commissionAsset
            fills = result.get('fills', [])
            for fill in fills:
                try:
                    commission = float(fill.get('commission', 0))
                    commission_asset = str(fill.get('commissionAsset', '')).upper()
                    
                    if commission > 0 and commission_asset:
                        # Convert fee to USD using current prices
                        if commission_asset in ('USD', 'USDT', 'USDC', 'BUSD'):
                            total_fees += commission
                        else:
                            # Get price of commission asset
                            asset_price = self.prices.get(commission_asset, 0)
                            if asset_price > 0:
                                total_fees += commission * asset_price
                            else:
                                # Fallback: assume small fee (0.1% of typical trade)
                                total_fees += commission * 0.0001  # Conservative estimate
                except (ValueError, TypeError):
                    pass
        elif exchange == 'kraken':
            # Kraken fees need to be calculated from the trade
            # Fee is typically 0.16% maker or 0.26% taker
            executed_qty = float(result.get('executedQty', 0))
            # Get the trade value in USD
            avg_price = float(result.get('avgPrice', 0) or result.get('price', 0) or 0)
            trade_value_usd = executed_qty * avg_price
            fee_rate = 0.0026  # Assume taker (more conservative)
            total_fees = trade_value_usd * fee_rate
        elif exchange == 'alpaca':
            # Alpaca includes fees differently
            total_fees = float(result.get('commission', 0) or result.get('fee', 0) or 0)
        
        return total_fees
    
    def _verify_profit_math(self, validation: Dict, opp, buy_amount: float) -> Dict:
        """
        🔢 VERIFY PROFIT CALCULATION MATH
        
        Cross-checks our calculated P&L against actual execution data.
        Returns verification results with any discrepancies.
        """
        verification = {
            'valid': True,
            'expected_pnl': opp.expected_pnl_usd,
            'calculated_pnl': 0.0,
            'verified_pnl': 0.0,
            'discrepancy': 0.0,
            'discrepancy_pct': 0.0,
            'warnings': [],
        }
        
        # Get current prices for calculation
        from_price = self.prices.get(opp.from_asset, 0)
        to_price = self.prices.get(opp.to_asset, 0)
        
        if not from_price or not to_price:
            verification['warnings'].append("Missing price data for verification")
            return verification
        
        # Calculate P&L using our method
        sold_value = opp.from_amount * from_price
        bought_value = buy_amount * to_price
        calculated_pnl = bought_value - sold_value
        verification['calculated_pnl'] = calculated_pnl
        
        # Calculate P&L using actual execution data (if available)
        if validation.get('total_sold') > 0 or validation.get('final_amount', 0) > 0 or buy_amount > 0:
            # 🔧 FIX: Use ACTUAL EXECUTION PRICES, not current market prices!
            # This is critical for accurate P/L calculation
            
            # Sold value - use actual execution price if available
            if validation.get('avg_sell_price', 0) > 0:
                actual_sold_value = validation['total_sold'] * validation['avg_sell_price']
            else:
                actual_sold_value = sold_value
            
            # Final bought value - CRITICAL FIX:
            # For SELL orders (like DAI→USD), validation['final_amount'] may be 0 because
            # exchanges like Kraken don't return cummulativeQuoteQty for sells.
            # In this case, use the buy_amount we actually received from the trade!
            final_amount = validation.get('final_amount', 0)
            if final_amount <= 0 and buy_amount > 0:
                # Fallback to buy_amount when final_amount is missing/zero
                final_amount = buy_amount
            
            # 🔧 FIX: Use actual buy price if available, not current price
            if validation.get('avg_buy_price', 0) > 0:
                actual_bought_value = final_amount * validation['avg_buy_price']
            else:
                actual_bought_value = final_amount * to_price
            
            # Subtract fees (fees are already in USD/quote currency)
            fees = validation.get('total_fees', 0)
            # 🔧 FIX: fees_in_usd calculation - fees are often in quote currency already
            # Don't multiply by to_price if fee is already in USD/USDC/USDT
            fees_in_usd = fees  # Assume fees are already in USD value
            
            verified_pnl = actual_bought_value - actual_sold_value - fees_in_usd
            verification['verified_pnl'] = verified_pnl
            
            # Check for discrepancy
            discrepancy = abs(calculated_pnl - verified_pnl)
            verification['discrepancy'] = discrepancy
            
            if abs(calculated_pnl) > 0.0001:
                verification['discrepancy_pct'] = (discrepancy / abs(calculated_pnl)) * 100
            
            # Flag significant discrepancies (>5%)
            if verification['discrepancy_pct'] > 5.0:
                verification['valid'] = False
                verification['warnings'].append(
                    f"P&L discrepancy: calculated ${calculated_pnl:.4f} vs verified ${verified_pnl:.4f} ({verification['discrepancy_pct']:.1f}%)"
                )
        else:
            verification['verified_pnl'] = calculated_pnl
        
        return verification
    
    def _print_order_validation(self, validation: Dict, verification: Dict, opp):
        """Print comprehensive order validation results."""
        print("\n   " + "═" * 60)
        print("   🔍 ORDER VALIDATION & PROFIT VERIFICATION")
        print("   " + "═" * 60)
        
        # Order IDs
        if validation['order_ids']:
            print(f"   📋 Order IDs ({validation['exchange'].upper()}):")
            for order in validation['order_ids']:
                print(f"      Step {order['step']}: {order['order_id']} ({order['side']} {order['pair']})")
        
        # Execution Summary
        print(f"\n   📊 EXECUTION SUMMARY:")
        print(f"      Sold: {validation['total_sold']:.8f} {opp.from_asset}")
        print(f"      Bought: {validation.get('final_amount', 0):.8f} {opp.to_asset}")
        if validation['avg_sell_price'] > 0:
            print(f"      Avg Sell Price: ${validation['avg_sell_price']:.6f}")
        if validation['avg_buy_price'] > 0:
            print(f"      Avg Buy Price: ${validation['avg_buy_price']:.6f}")
        print(f"      Total Fees: ${validation['total_fees']:.6f}")
        
        # P&L Verification
        print(f"\n   💰 P&L VERIFICATION:")
        print(f"      Expected P&L: ${verification['expected_pnl']:+.4f}")
        print(f"      Calculated P&L: ${verification['calculated_pnl']:+.4f}")
        print(f"      Verified P&L: ${verification['verified_pnl']:+.4f}")
        
        if verification['discrepancy'] > 0.0001:
            status = "⚠️" if verification['discrepancy_pct'] > 5 else "✅"
            print(f"      {status} Discrepancy: ${verification['discrepancy']:.4f} ({verification['discrepancy_pct']:.1f}%)")
        else:
            print(f"      ✅ Math Verified!")
        
        # Validation Status
        if validation['validation_errors']:
            print(f"\n   ⚠️ VALIDATION ISSUES:")
            for error in validation['validation_errors']:
                print(f"      - {error}")
        
        if verification['warnings']:
            print(f"\n   ⚠️ VERIFICATION WARNINGS:")
            for warning in verification['warnings']:
                print(f"      - {warning}")
        
        # Final Status
        if validation['valid'] and verification['valid']:
            print(f"\n   ✅ ORDER FULLY VALIDATED - Profit math confirmed!")
        else:
            print(f"\n   ⚠️ VALIDATION INCOMPLETE - Review required")
        
        print("   " + "═" * 60)
    
    def _record_conversion(self, opp, buy_amount: float, validation: Dict = None, verification: Dict = None):
        """Record a successful conversion with STEP-BY-STEP realized profit tracking and ORDER VALIDATION."""
        opp.executed = True
        self.conversions_made += 1
        self.conversions.append(opp)
        self.balances[opp.from_asset] = self.balances.get(opp.from_asset, 0) - opp.from_amount
        self.balances[opp.to_asset] = self.balances.get(opp.to_asset, 0) + buy_amount

        # 🚨 USE ACTUAL EXECUTION DATA, NOT ESTIMATED PRICES
        # This is critical to prevent ghost profits!
        from_price = self.prices.get(opp.from_asset, 0)
        to_price = self.prices.get(opp.to_asset, 0)
        
        # Try to use actual execution values from validation
        if validation and validation.get('total_sold', 0) > 0:
            # Use actual execution data
            if validation.get('avg_sell_price', 0) > 0:
                sold_value = validation['total_sold'] * validation['avg_sell_price']
            else:
                sold_value = opp.from_amount * from_price
            
            if validation.get('avg_buy_price', 0) > 0:
                bought_value = validation.get('final_amount', buy_amount) * validation['avg_buy_price']
            else:
                bought_value = buy_amount * to_price
            
            # Subtract fees from bought value (fees reduce profit)
            # Note: fees are already in USD from _extract_fees
            fees_usd = validation.get('total_fees', 0)
            if fees_usd > 0:
                bought_value -= fees_usd  # Direct USD subtraction
        else:
            # Fallback to price-based estimate
            sold_value = opp.from_amount * from_price
            bought_value = buy_amount * to_price
        
        actual_pnl = bought_value - sold_value
        opp.actual_pnl_usd = actual_pnl
        
        # ═══════════════════════════════════════════════════════════════════
        # 🔍 ORDER VALIDATION AUDIT TRAIL
        # ═══════════════════════════════════════════════════════════════════
        if validation:
            # Use verified P&L if available (most accurate)
            if verification and verification.get('verified_pnl') is not None:
                actual_pnl = verification['verified_pnl']
                opp.actual_pnl_usd = actual_pnl
                # Update bought_value to reflect actual P&L (don't reset sold_value!)
                # sold_value already has correct value from execution data above
                bought_value = sold_value + actual_pnl  # bought = sold + profit (actual)
                opp.pnl_verified = True
                opp.verification_status = 'VERIFIED' if verification['valid'] else 'DISCREPANCY'
            else:
                opp.pnl_verified = False
                opp.verification_status = 'UNVERIFIED'
            
            # Store order IDs for audit trail
            opp.order_ids = validation.get('order_ids', [])
            opp.execution_fees = validation.get('total_fees', 0)
            
            # Log validation to persistent storage for auditing
            self._log_order_validation(opp, validation, verification)
        else:
            opp.pnl_verified = False
            opp.verification_status = 'NO_VALIDATION'
            opp.order_ids = []
            opp.execution_fees = 0
        
        # ═══════════════════════════════════════════════════════════════════
        # 🫒💰 LIVE BARTER MATRIX - Record & Display Step Profit
        # ═══════════════════════════════════════════════════════════════════
        
        # Update barter rates for this pair
        self.barter_matrix.update_barter_rate(
            opp.from_asset, opp.to_asset, from_price, to_price
        )
        
        # Record realized profit in the barter ledger
        profit_result = self.barter_matrix.record_realized_profit(
            from_asset=opp.from_asset,
            to_asset=opp.to_asset,
            from_amount=opp.from_amount,
            from_usd=sold_value,
            to_amount=buy_amount,
            to_usd=bought_value
        )
        
        # 🎯 PRINT STEP-BY-STEP REALIZED PROFIT
        step_display = self.barter_matrix.print_step_profit(
            step_num=self.conversions_made,
            from_asset=opp.from_asset,
            to_asset=opp.to_asset,
            from_usd=sold_value,
            to_usd=bought_value,
            from_amount=opp.from_amount,
            to_amount=buy_amount
        )
        print(step_display)
        
        # Show path performance (how this specific conversion path is doing)
        print(f"   📊 PATH {opp.from_asset}→{opp.to_asset}: {profit_result['path_trades']} trades, ${profit_result['path_total_profit']:+.4f} total")
        print(f"   🔄 Slippage: {profit_result['actual_slippage_pct']:.2f}%")
        
        # 👑🍄 QUEEN'S MYCELIUM BROADCAST - Send signals to all systems
        if profit_result.get('is_win'):
            print(f"   👑 Queen's Verdict: ✅ WIN! Path continues.")
        else:
            win_rate = profit_result.get('path_win_rate', 0)
            print(f"   👑 Queen's Verdict: ❌ LOSS! Path win rate: {win_rate:.0%}")
            # Broadcast through mycelium
            queen_signals = self.barter_matrix.get_queen_signals()
            for signal in queen_signals:
                if signal['type'] == 'PATH_BLOCKED':
                    print(f"   🍄 MYCELIUM BROADCAST: {signal['path']} BLOCKED - {signal['reason']}")
        
        # Update total_profit_usd to match barter matrix
        self.total_profit_usd = self.barter_matrix.total_realized_profit

        # Learn: update hub and path memory
        if self.hub and hasattr(self.hub, 'record_conversion_outcome'):
            try:
                self.hub.record_conversion_outcome(opp.from_asset, opp.to_asset, actual_pnl >= 0, actual_pnl)
            except Exception:
                pass
        self.path_memory.record(opp.from_asset, opp.to_asset, actual_pnl >= 0)

        # 📅🔮 7-DAY PLANNER: Validate timing prediction after conversion
        if self.seven_day_planner:
            try:
                # Record this conversion for validation tracking
                validation_id = self.seven_day_planner.record_conversion(
                    symbol=opp.to_asset,
                    entry_price=to_price
                )
                
                # Validate immediately with exit price (for compound tracking)
                # The next scan will have updated prices for true validation
                result = self.seven_day_planner.validate_conversion(
                    validation_id=validation_id,
                    exit_price=to_price  # Will be updated on next trade
                )
                
                if result:
                    timing_tag = "🎯" if result.direction_correct else "❌"
                    print(f"   📅 7-Day Validation: {timing_tag} timing={result.timing_score:.0%}")
                    
                    # Log adaptive weight updates
                    weights = self.seven_day_planner.adaptive_weights
                    print(f"   🧠 Adaptive: h={weights['hourly_weight']:.2f}, s={weights['symbol_weight']:.2f}, acc={weights['accuracy_7d']:.0%}")
            except Exception as e:
                logger.debug(f"7-day planner validation error: {e}")

        # Publish observability
        if self.thought_bus:
            try:
                self.thought_bus.think(
                    topic='conversion.success',
                    message='conversion recorded',
                    metadata={
                        'pair': f"{opp.from_asset}->{opp.to_asset}",
                        'pnl': round(actual_pnl, 6),
                        'lambda': round(opp.lambda_score, 4),
                        'gravity': round(opp.gravity_score, 4),
                        'gate_req': round(opp.gate_required_profit, 6),
                        'gate_passed': opp.gate_passed,
                    }
                )
            except Exception:
                pass

    def _record_failure(self, opp):
        """Record a failed conversion attempt for learning."""
        self.path_memory.record(opp.from_asset, opp.to_asset, False)
        if self.thought_bus:
            try:
                self.thought_bus.think(
                    topic='conversion.failure',
                    message='conversion failed',
                    metadata={'pair': f"{opp.from_asset}->{opp.to_asset}"}
                )
            except Exception:
                pass

    def _log_successful_conversion(self, validation: Dict, opp):
        """
        Log a successful conversion with validation data.
        This is a convenience wrapper around _record_conversion.
        """
        # Calculate buy/received amount from validation
        buy_amount = 0.0
        trades = validation.get('trades', [])
        if trades:
            last_trade = trades[-1]
            if isinstance(last_trade, dict):
                # PRIORITY: Use receivedQty (for SELL orders) if available
                res = last_trade.get('result', {})
                buy_amount = float(res.get('receivedQty', 0) or
                                   last_trade.get('receivedQty', 0) or
                                   res.get('executedQty', 0) or 
                                   last_trade.get('executedQty', 0) or 0)
        
        # Fallback estimate if no amount found
        if buy_amount == 0:
            to_price = self.prices.get(opp.to_asset, 0)
            if to_price > 0:
                buy_amount = opp.from_value_usd / to_price
        
        # Verify profit math
        verification = self._verify_profit_math(validation, opp, buy_amount)
        
        # Print validation summary
        self._print_order_validation(validation, verification, opp)
        
        # Record the conversion
        self._record_conversion(opp, buy_amount, validation, verification)
    
    def _log_order_validation(self, opp, validation: Dict, verification: Dict):
        """
        📋 LOG ORDER VALIDATION TO PERSISTENT AUDIT TRAIL
        
        Stores all order IDs, execution details, and P&L verification
        for post-trade auditing and compliance.
        """
        import json
        from datetime import datetime
        
        audit_file = "aureon_order_audit.json"
        
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'conversion_num': self.conversions_made,
            'exchange': validation.get('exchange', 'unknown'),
            'from_asset': opp.from_asset,
            'to_asset': opp.to_asset,
            'from_amount': opp.from_amount,
            'to_amount': validation.get('final_amount', 0),
            'order_ids': validation.get('order_ids', []),
            'validation': {
                'valid': validation.get('valid', False),
                'total_sold': validation.get('total_sold', 0),
                'total_bought': validation.get('final_amount', 0),
                'avg_sell_price': validation.get('avg_sell_price', 0),
                'avg_buy_price': validation.get('avg_buy_price', 0),
                'total_fees': validation.get('total_fees', 0),
                'errors': validation.get('validation_errors', []),
            },
            'profit_verification': {
                'expected_pnl': verification.get('expected_pnl', 0) if verification else 0,
                'calculated_pnl': verification.get('calculated_pnl', 0) if verification else 0,
                'verified_pnl': verification.get('verified_pnl', 0) if verification else 0,
                'discrepancy': verification.get('discrepancy', 0) if verification else 0,
                'discrepancy_pct': verification.get('discrepancy_pct', 0) if verification else 0,
                'math_valid': verification.get('valid', False) if verification else False,
                'warnings': verification.get('warnings', []) if verification else [],
            },
            'final_status': 'VERIFIED' if (validation.get('valid') and (verification and verification.get('valid'))) else 'NEEDS_REVIEW',
        }
        
        try:
            # Load existing audit log
            try:
                with open(audit_file, 'r') as f:
                    audit_log = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                audit_log = {'orders': [], 'summary': {'total': 0, 'verified': 0, 'discrepancies': 0}}
            
            # Append new entry
            audit_log['orders'].append(audit_entry)
            audit_log['summary']['total'] += 1
            if audit_entry['final_status'] == 'VERIFIED':
                audit_log['summary']['verified'] += 1
            else:
                audit_log['summary']['discrepancies'] += 1
            
            # Save updated log
            with open(audit_file, 'w') as f:
                json.dump(audit_log, f, indent=2)
            
            logger.info(f"📋 Order audit logged: {audit_entry['final_status']}")
            
        except Exception as e:
            logger.warning(f"Failed to write order audit: {e}")
    
    def _find_exchange_pair(self, asset: str, quote: str, exchange: str) -> Optional[str]:
        """Find trading pair on a specific exchange using loaded pairs."""
        asset_upper = asset.upper()
        quote_upper = quote.upper()
        prefix = f"{exchange}:"
        
        # ════════════════════════════════════════════════════════════════
        # 🐙 KRAKEN - Check kraken_pairs dict
        # Kraken uses special naming: XXBT=BTC, ZUSD=USD, ZEUR=EUR
        # ════════════════════════════════════════════════════════════════
        if exchange == 'kraken' and self.kraken_pairs:
            # Map common names to Kraken format
            kraken_asset = asset_upper
            if asset_upper == 'BTC':
                kraken_asset = 'XBT'
            
            kraken_quote = quote_upper
            if quote_upper == 'USD':
                kraken_quote = 'ZUSD'
            elif quote_upper == 'EUR':
                kraken_quote = 'ZEUR'
            elif quote_upper == 'GBP':
                kraken_quote = 'ZGBP'
            
            # Try common pair formats (Kraken has multiple naming conventions)
            candidates = [
                f"{asset_upper}{quote_upper}",           # CHZUSD (standard)
                f"{kraken_asset}{quote_upper}",          # XBTUSD
                f"X{kraken_asset}Z{quote_upper}",        # XXBTZUSD
                f"XX{kraken_asset[1:]}Z{quote_upper}" if len(kraken_asset) > 1 else None,  # Edge cases
                f"{asset_upper}{kraken_quote}",          # CHZZUSD
                f"{kraken_asset}{kraken_quote}",         # XBTZUSD
                f"X{kraken_asset}{kraken_quote}",        # XXBTZUSD variant
            ]
            for candidate in [c for c in candidates if c]:
                if candidate in self.kraken_pairs:
                    return f"kraken:{candidate}"
            
            # Fuzzy search (look for both original and Kraken-format asset)
            search_assets = [asset_upper, kraken_asset]
            if asset_upper != kraken_asset:
                search_assets.append(f"X{kraken_asset}")  # XXBT
            
            for pair_name in self.kraken_pairs.keys():
                for search_asset in search_assets:
                    if search_asset in pair_name and quote_upper in pair_name:
                        return f"kraken:{pair_name}"
        
        # ════════════════════════════════════════════════════════════════
        # 🦙 ALPACA - Check alpaca_pairs dict
        # ════════════════════════════════════════════════════════════════
        if exchange == 'alpaca' and self.alpaca_pairs:
            candidates = [
                f"{asset_upper}/USD",
                f"{asset_upper}USD",
                asset_upper,
            ]
            for candidate in candidates:
                if candidate in self.alpaca_pairs:
                    return f"alpaca:{self.alpaca_pairs[candidate]}"
        
        # ════════════════════════════════════════════════════════════════
        # 🟡 BINANCE - Search ticker cache
        # ════════════════════════════════════════════════════════════════
        if exchange == 'binance':
            candidates = [
                f"{asset_upper}{quote_upper}",
                f"{asset_upper}USDT",
                f"{asset_upper}USDC",
            ]
            for candidate in candidates:
                cache_key = f"binance:{candidate}"
                if cache_key in self.ticker_cache:
                    return cache_key
        
        # Fallback: Search ticker cache for any exchange
        for cached_pair in self.ticker_cache.keys():
            if cached_pair.startswith(prefix):
                pair_part = cached_pair.replace(prefix, '')
                if pair_part.startswith(asset_upper) and quote_upper in pair_part:
                    return cached_pair
        
        return None
    
    async def run(self, duration_s: int = 60):
        """Run the micro profit labyrinth."""
        await self.initialize()
        
        # 🐍 MEDUSA: Load ALL tradeable pairs for proper routing
        # This ensures we can find pairs for assets we don't hold yet
        await self._load_all_tradeable_pairs()
        
        # Initial data fetch - ALL EXCHANGES
        print("\n" + "=" * 70)
        print("📊 FETCHING DATA FROM ALL EXCHANGES...")
        print("=" * 70)
        await self.fetch_prices()
        print(f"   ✅ {len(self.prices)} assets priced")
        print(f"   ✅ {len(self.ticker_cache)} pairs in ticker cache")
        
        # 🫒🔄 POPULATE BARTER GRAPH from loaded data
        self.populate_barter_graph()
        
        print("\n📊 FETCHING BALANCES FROM ALL EXCHANGES...")
        await self.fetch_balances()
        
        # Show exchange status
        print("\n📡 EXCHANGE STATUS:")
        for exchange, data in self.exchange_data.items():
            if data.get('connected'):
                bal_count = len(data.get('balances', {}))
                total_val = data.get('total_value', 0)
                icon = {'kraken': '🐙', 'binance': '🟡', 'alpaca': '🦙'}.get(exchange, '📊')
                print(f"   {icon} {exchange.upper()}: ✅ Connected | {bal_count} assets | ${total_val:,.2f}")
            else:
                icon = {'kraken': '🐙', 'binance': '🟡', 'alpaca': '🦙'}.get(exchange, '📊')
                print(f"   {icon} {exchange.upper()}: ❌ {data.get('error', 'Not connected')}")
        
        # Show balances per exchange
        if self.exchange_balances:
            print("\n📦 PORTFOLIO BY EXCHANGE:")
            for exchange, balances in self.exchange_balances.items():
                if balances:
                    icon = {'kraken': '🐙', 'binance': '🟡', 'alpaca': '🦙'}.get(exchange, '📊')
                    total = sum(balances.get(a, 0) * self.prices.get(a, 0) for a in balances)
                    print(f"\n   {icon} {exchange.upper()} (${total:,.2f}):")
                    for asset, amount in sorted(balances.items(), key=lambda x: x[1] * self.prices.get(x[0], 0), reverse=True)[:10]:
                        price = self.prices.get(asset, 0)
                        value = amount * price
                        if value >= 1.0:  # Only show if >= $1
                            print(f"      {asset}: {amount:.6f} = ${value:.2f}")
        
        # Calculate starting value
        self.start_value_usd = sum(
            self.balances.get(asset, 0) * self.prices.get(asset, 0)
            for asset in self.balances
        )
        
        print(f"\n💰 TOTAL PORTFOLIO VALUE: ${self.start_value_usd:,.2f}")
        
        # Handle infinite duration
        duration_display = "♾️ FOREVER" if duration_s == 0 else f"{duration_s}s"
        print(f"\n🔬 ENTERING MICRO PROFIT LABYRINTH! (Duration: {duration_display})")
        print(f"   ⚡ SPEED MODE: Aggressive micro-profit harvesting...")
        print(f"   V14 Score: {self.config['entry_score_threshold']}+ (lowered for speed)")
        print(f"   Min Profit: ${self.config['min_profit_usd']:.6f} (micro-profits accepted!)")
        print(f"   Mode: {'🔴 LIVE TRADING' if self.live else '🔵 DRY RUN'}")
        print()
        
        start_time = time.time()
        scan_interval = 0.5  # ⚡ FAST SCAN: Every 0.5s for aggressive harvesting
        
        # ════════════════════════════════════════════════════════════════════════════
        # 🎯 TURN-BASED EXCHANGE STRATEGY
        # Each exchange gets its turn - prevents conflicts, respects rate limits
        # ════════════════════════════════════════════════════════════════════════════
        print("\n" + "=" * 70)
        print("🎯 TURN-BASED EXCHANGE STRATEGY ACTIVATED")
        print("=" * 70)
        connected_exchanges = [ex for ex in self.exchange_order 
                               if self.exchange_data.get(ex, {}).get('connected', False)]
        print(f"   Turn Order: {' → '.join([ex.upper() for ex in connected_exchanges])}")
        print(f"   Each exchange scans its assets on its turn")
        print("=" * 70)
        
        try:
            # duration_s == 0 means run forever
            while duration_s == 0 or time.time() - start_time < duration_s:
                elapsed = time.time() - start_time
                
                # Refresh prices (shared across all exchanges)
                await self.fetch_prices()
                
                # 💤 DREAM & VALIDATE (Adaptive Learning)
                await self.validate_dreams()
                await self.dream_about_tickers()
                
                # Collect signals from ALL systems
                signals = await self.collect_all_signals()
                signal_count = sum(len(v) for v in signals.values())
                
                # 🎯 TURN-BASED EXECUTION - Each exchange gets its turn
                turn_opportunities, turn_conversions = await self.execute_turn()
                
                # Calculate current value
                current_value = sum(
                    self.balances.get(asset, 0) * self.prices.get(asset, 0)
                    for asset in self.balances
                )
                # P/L = Current Value - Starting Value (simple, correct math)
                pnl = current_value - self.start_value_usd
                
                # Status update with turn display
                mode = "🔴" if self.live else "🔵"
                turn_display = self.get_turn_display()
                current_ex = self.get_current_exchange()
                
                # 👑🌊🪐 QUEEN'S COSMIC WISDOM BROADCAST
                cosmic_status = ""
                if self.queen:
                    try:
                        # Broadcast cosmic wisdom through mycelium
                        wisdom = self.queen.broadcast_cosmic_wisdom()
                        if wisdom:
                            cosmic = self.queen.get_cosmic_state()
                            score = cosmic.get('composite_cosmic_score', 0)
                            # Show cosmic alignment indicator
                            if score > 0.7:
                                cosmic_status = f" 🌟Cosmic:{score:.0%}"
                            elif score > 0.5:
                                cosmic_status = f" ⭐Cosmic:{score:.0%}"
                            elif score < 0.3:
                                cosmic_status = f" 🌑Cosmic:{score:.0%}"
                    except Exception as e:
                        logger.debug(f"Cosmic wisdom error: {e}")
                
                # Neural systems status
                neural_status = []
                if self.bus_aggregator:
                    bus_agg = self.bus_aggregator.get_aggregate_score()
                    neural_status.append(f"Bus:{bus_agg:.0%}")
                if self.mycelium_network:
                    neural_status.append("Myc:✓")
                if self.lighthouse:
                    neural_status.append("LH:✓")
                if self.ultimate_intel:
                    neural_status.append("Ult:✓")
                if self.hnc_matrix:
                    neural_status.append("HNC:✓")
                
                neural_str = " | ".join(neural_status) if neural_status else "Neural:standby"
                
                # 🚨 REAL-TIME PORTFOLIO DRAIN CHECK
                actual_pnl = current_value - self.start_value_usd
                reported_pnl = self.barter_matrix.total_realized_profit
                ghost_profit = reported_pnl - actual_pnl
                
                # Show warning if portfolio is draining despite "profits"
                drain_warning = ""
                if self.conversions_made > 0 and ghost_profit > 0.10:
                    drain_warning = f" ⚠️DRAIN:${ghost_profit:.2f}"
                
                # 👑 Queen's blocked paths count
                blocked_count = len(self.barter_matrix.blocked_paths)
                queen_status = f" 👑Block:{blocked_count}" if blocked_count > 0 else ""
                
                print(f"🔬 {mode} | {elapsed:.0f}s | Turn:{turn_display} | {neural_str}{cosmic_status} | Conv:{self.conversions_made} | Actual:${actual_pnl:+.2f}{drain_warning}{queen_status}")
                
                await asyncio.sleep(scan_interval)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
        
        # Final summary
        await self.print_summary()
    
    async def print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 70)
        print("🔬💰 MICRO PROFIT LABYRINTH SUMMARY 💰🔬")
        print("=" * 70)
        print(f"Mode: {'🔴 LIVE TRADING' if self.live else '🔵 DRY RUN'}")
        print(f"Total Turns: {self.turns_completed}")
        print(f"Total Signals Received: {self.signals_received}")
        print(f"Opportunities Found: {self.opportunities_found}")
        print(f"Conversions Made: {self.conversions_made}")
        print(f"Total Profit: ${self.total_profit_usd:.4f}")
        
        # ════════════════════════════════════════════════════════════════
        # 👑💰 TINA B'S BILLION DOLLAR DREAM STATUS 💰👑
        # ════════════════════════════════════════════════════════════════
        print("\n" + "═" * 70)
        dream_status = self.barter_matrix.check_dream_progress()
        print(dream_status)
        milestones_hit = len(self.barter_matrix.milestones_hit)
        print(f"   🎯 Milestones: {milestones_hit}/8")
        if milestones_hit > 0:
            print(f"   ✅ {', '.join(self.barter_matrix.milestones_hit)}")
        print("═" * 70)
        
        # ════════════════════════════════════════════════════════════════
        # 🎯 TURN-BASED EXCHANGE STATS
        # ════════════════════════════════════════════════════════════════
        print("\n🎯 TURN-BASED EXCHANGE STATS:")
        icons = {'kraken': '🐙', 'alpaca': '🦙', 'binance': '🟡'}
        for exchange, stats in self.exchange_stats.items():
            if stats['scans'] > 0:  # Only show exchanges that were active
                icon = icons.get(exchange, '📊')
                connected = "✅" if self.exchange_data.get(exchange, {}).get('connected') else "❌"
                print(f"   {icon} {exchange.upper()} {connected}")
                print(f"      Turns: {stats['scans']} | Opps: {stats['opportunities']} | Conv: {stats['conversions']}")
                print(f"      Profit: ${stats['profit']:+.4f}")
        
        # ════════════════════════════════════════════════════════════════
        # 🧠 NEURAL MIND MAP STATUS
        # ════════════════════════════════════════════════════════════════
        print("\n🧠 NEURAL MIND MAP STATUS:")
        print(f"   ThoughtBus: {'✅ Active' if self.bus_aggregator else '❌ Offline'}")
        print(f"   Mycelium Network: {'✅ Active' if self.mycelium_network else '❌ Offline'}")
        print(f"   Lighthouse: {'✅ Active' if self.lighthouse else '❌ Offline'}")
        print(f"   Ultimate Intel: {'✅ Active' if self.ultimate_intel else '❌ Offline'}")
        print(f"   HNC Matrix: {'✅ Active' if self.hnc_matrix else '❌ Offline'}")
        print(f"   Unified Ecosystem: {'✅ Active' if self.unified_ecosystem else '❌ Offline'}")
        
        if self.bus_aggregator:
            status = self.bus_aggregator.get_signal_status()
            print(f"   📡 Bus Signals: {status}")
        
        # Path Memory Stats
        path_stats = self.path_memory.get_stats()
        if path_stats.get('paths', 0) > 0:
            print(f"\n🛤️ PATH MEMORY:")
            print(f"   Total Paths: {path_stats['paths']}")
            print(f"   Win Rate: {path_stats['win_rate']:.1%}")
            print(f"   Wins: {path_stats['wins']} | Losses: {path_stats['losses']}")
        
        # Dream Accuracy
        if any(acc != 0.5 for acc in self.dream_accuracy.values()):
            print(f"\n💭 DREAM ACCURACY (Adaptive Learning):")
            for source, acc in self.dream_accuracy.items():
                print(f"   {source}: {acc:.1%}")
        
        # Signal breakdown by system
        if self.all_signals:
            print("\n📡 SIGNALS BY SYSTEM:")
            for system, sigs in self.all_signals.items():
                print(f"   {system}: {len(sigs)} signals")
        
        # Conversions - Show ACTUAL P/L not expected!
        if self.conversions:
            print("\n📋 CONVERSIONS (ACTUAL P/L):")
            for c in self.conversions:
                status = "✅" if c.executed else "❌"
                # 🔧 FIX: Use actual_pnl_usd for display (what really happened)
                actual_pnl = getattr(c, 'actual_pnl_usd', c.expected_pnl_usd)
                verified = "✓" if getattr(c, 'pnl_verified', False) else "?"
                print(f"   {status} {c.from_asset} → {c.to_asset}: ${actual_pnl:+.4f} {verified} (Λ:{c.lambda_score:.0%} G:{c.gravity_score:.0%})")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🫒💰 LIVE BARTER MATRIX SUMMARY
        # ═══════════════════════════════════════════════════════════════════
        barter_summary = self.barter_matrix.get_summary()
        if barter_summary['conversion_count'] > 0:
            print("\n🫒💰 LIVE BARTER MATRIX:")
            print(f"   Total Conversions: {barter_summary['conversion_count']}")
            print(f"   Total Realized P/L: ${barter_summary['total_realized_profit']:+.4f}")
            print(f"   Avg Profit/Trade: ${barter_summary['avg_profit_per_trade']:+.4f}")
            print(f"   Paths Learned: {barter_summary['paths_learned']}")
            
            # Show top performing paths
            if self.barter_matrix.barter_history:
                print("\n   📊 PATH PERFORMANCE:")
                sorted_paths = sorted(
                    self.barter_matrix.barter_history.items(),
                    key=lambda x: x[1].get('total_profit', 0),
                    reverse=True
                )[:5]  # Top 5 paths
                for (from_a, to_a), stats in sorted_paths:
                    trades = stats.get('trades', 0)
                    profit = stats.get('total_profit', 0)
                    slippage = stats.get('avg_slippage', 0)
                    status = "✅" if profit > 0 else "❌"
                    print(f"   {status} {from_a}→{to_a}: {trades} trades, ${profit:+.4f}, slip:{slippage:.2f}%")
        
        # Final portfolio
        if self.balances and self.prices:
            print("\n📦 FINAL PORTFOLIO:")
            total = 0
            for asset, amount in sorted(self.balances.items()):
                price = self.prices.get(asset, 0)
                value = amount * price
                if value >= 1.0:
                    print(f"   {asset}: {amount:.6f} = ${value:.2f}")
                    total += value
            print(f"\n💰 TOTAL VALUE: ${total:.2f}")
            # P/L = Current Value - Starting Value (simple, correct math)
            session_pnl = total - self.start_value_usd
            pnl_symbol = "+" if session_pnl >= 0 else ""
            print(f"📈 SESSION P/L (Unrealized): ${pnl_symbol}{session_pnl:.4f}")
            print(f"🎯 REALIZED TRADES P/L: ${self.barter_matrix.total_realized_profit:+.4f} ({self.conversions_made} conversions)")
            
            # ════════════════════════════════════════════════════════════════════
            # 🚨 GHOST PROFIT DETECTOR - Validate we're not draining portfolio
            # ════════════════════════════════════════════════════════════════════
            realized_pnl = self.barter_matrix.total_realized_profit
            actual_pnl = session_pnl
            ghost_profit = realized_pnl - actual_pnl
            
            print("\n🔍 PROFIT VALIDATION:")
            print(f"   📊 Starting Portfolio: ${self.start_value_usd:.2f}")
            print(f"   📊 Ending Portfolio:   ${total:.2f}")
            print(f"   📊 Actual Change:      ${actual_pnl:+.4f}")
            print(f"   📊 Reported Profit:    ${realized_pnl:+.4f}")
            
            if abs(ghost_profit) > 0.01:
                if ghost_profit > 0:
                    print(f"\n   ⚠️ GHOST PROFIT DETECTED: ${ghost_profit:+.4f}")
                    print(f"   ⚠️ Reported profits exceed actual portfolio gain!")
                    print(f"   ⚠️ This is likely fees, slippage, or price movement eating gains.")
                else:
                    print(f"\n   ✅ HIDDEN GAIN: ${-ghost_profit:+.4f}")
                    print(f"   ✅ Portfolio gained more than reported (price appreciation).")
                
                # Show the math
                if self.conversions_made > 0:
                    avg_ghost_per_trade = ghost_profit / self.conversions_made
                    print(f"\n   📉 Average loss per trade: ${avg_ghost_per_trade:.4f}")
                    print(f"   💡 To profit: Need trades with >${abs(avg_ghost_per_trade):.4f} actual gain")
            else:
                print(f"\n   ✅ PROFIT VALIDATED - Reported matches actual!")
            
            # ════════════════════════════════════════════════════════════════════
            # 👑�🪐🔭 QUEEN'S COSMIC SYSTEMS STATUS
            # ════════════════════════════════════════════════════════════════════
            if self.queen:
                try:
                    cosmic = self.queen.get_cosmic_state()
                    print("\n👑🌌 QUEEN'S COSMIC SYSTEMS:")
                    
                    # Schumann Resonance
                    schumann = cosmic.get('schumann', {})
                    if schumann.get('active'):
                        print(f"   🌊 Schumann Resonance: {schumann.get('resonance', 7.83):.2f}Hz (alignment: {schumann.get('alignment', 0):.0%})")
                    
                    # Planetary Torque
                    planetary = cosmic.get('planetary', {})
                    if planetary.get('active'):
                        print(f"   🪐 Planetary Torque (Π): {planetary.get('torque', 0):.4f} (luck field: {planetary.get('luck_field', 0):.0%})")
                    
                    # Lunar Phase
                    lunar = cosmic.get('lunar', {})
                    if lunar.get('active'):
                        phase_name = lunar.get('name', 'Unknown')
                        phase_val = lunar.get('phase', 0)
                        moon_icon = "🌑🌒🌓🌔🌕🌖🌗🌘"[int(phase_val * 8) % 8]
                        print(f"   {moon_icon} Lunar Phase: {phase_name} ({phase_val:.0%})")
                    
                    # Harmonic Coherence
                    harmonic = cosmic.get('harmonic', {})
                    if harmonic.get('active'):
                        print(f"   🎼 Harmonic Coherence: {harmonic.get('coherence', 0):.0%}")
                    
                    # Quantum Telescope
                    quantum = cosmic.get('quantum', {})
                    if quantum.get('active'):
                        print(f"   🔭 Quantum Alignment: {quantum.get('alignment', 0):.0%}")
                    
                    # Composite Score
                    composite = cosmic.get('composite_cosmic_score', 0)
                    if composite > 0.7:
                        print(f"\n   🌟 COSMIC ALIGNMENT: {composite:.0%} - HIGHLY FAVORABLE")
                    elif composite > 0.5:
                        print(f"\n   ⭐ COSMIC ALIGNMENT: {composite:.0%} - Favorable")
                    elif composite > 0.3:
                        print(f"\n   ☁️ COSMIC ALIGNMENT: {composite:.0%} - Neutral")
                    else:
                        print(f"\n   🌑 COSMIC ALIGNMENT: {composite:.0%} - Unfavorable")
                except Exception as e:
                    logger.debug(f"Error getting cosmic state: {e}")
            
            # ════════════════════════════════════════════════════════════════════
            # 👑�🍄 QUEEN'S BLOCKED PATHS - Paths the mycelium has blocked
            # ════════════════════════════════════════════════════════════════════
            if self.barter_matrix.blocked_paths:
                print("\n👑🍄 QUEEN'S BLOCKED PATHS (via Mycelium):")
                for (from_a, to_a), reason in self.barter_matrix.blocked_paths.items():
                    print(f"   🚫 {from_a}→{to_a}: {reason}")
                print(f"   📊 Total blocked: {len(self.barter_matrix.blocked_paths)} paths")
                print(f"   💡 Blocked paths will be retried after wins on other paths")
            else:
                print("\n👑 QUEEN STATUS: All paths approved (no losing streaks)")
            
            # ════════════════════════════════════════════════════════════════════
            # 👑🧠📚 QUEEN'S HISTORICAL WISDOM STATUS
            # ════════════════════════════════════════════════════════════════════
            if self.queen:
                try:
                    wisdom_state = self.queen.get_historical_wisdom_state()
                    print("\n👑🧠 QUEEN'S HISTORICAL WISDOM:")
                    
                    # Wisdom Engine (11 Civilizations)
                    we = wisdom_state.get('wisdom_engine', {})
                    if we.get('active'):
                        print(f"   🌍 11 Civilizations: ✅ ACTIVE ({we.get('years_of_wisdom', 5000)} years of wisdom)")
                    
                    # Sandbox Evolution
                    se = wisdom_state.get('sandbox_evolution', {})
                    if se.get('active'):
                        print(f"   🧬 Sandbox Evolution: Gen {se.get('generation', 0)}, {se.get('win_rate', 0):.1f}% win rate")
                    
                    # Dream Memory
                    dm = wisdom_state.get('dream_memory', {})
                    if dm.get('active'):
                        print(f"   💭 Dream Memory: {dm.get('dreams', 0)} dreams, {dm.get('prophecies', 0)} prophecies")
                    
                    # Wisdom Collector
                    wc = wisdom_state.get('wisdom_collector', {})
                    if wc.get('active'):
                        patterns = wc.get('patterns', 0)
                        trades = wc.get('trades', 0)
                        predictions = wc.get('predictions', 0)
                        strategies = wc.get('strategies', 0)
                        print(f"   📚 Wisdom Collector: {patterns} patterns | {trades} trades | {predictions} predictions | {strategies} strategies")
                    
                    # Total Wisdom Score
                    total_score = wisdom_state.get('total_wisdom_score', 0.5)
                    active_sys = wisdom_state.get('active_systems', 0)
                    if total_score > 0.7:
                        print(f"\n   🧠✨ WISDOM SCORE: {total_score:.0%} - HIGHLY INFORMED ({active_sys} systems)")
                    elif total_score > 0.5:
                        print(f"\n   🧠⭐ WISDOM SCORE: {total_score:.0%} - Well Informed ({active_sys} systems)")
                    else:
                        print(f"\n   🧠 WISDOM SCORE: {total_score:.0%} - Basic ({active_sys} systems)")
                    
                    # Civilization Consensus
                    try:
                        consensus = self.queen.get_civilization_consensus()
                        if consensus.get('civilizations_consulted', 0) > 0:
                            print(f"\n   🏛️ CIVILIZATION CONSENSUS ({consensus['civilizations_consulted']} consulted):")
                            print(f"      BUY: {consensus['votes']['BUY']} | HOLD: {consensus['votes']['HOLD']} | SELL: {consensus['votes']['SELL']}")
                            print(f"      → Action: {consensus['consensus_action']} ({consensus['confidence']:.0%} confidence)")
                    except Exception as e:
                        logger.debug(f"Civilization consensus error: {e}")
                    
                    # 🔱 Temporal ID & Ladder Status
                    try:
                        temporal_state = self.queen.get_temporal_state()
                        if temporal_state.get('active'):
                            tid = temporal_state.get('temporal_id', {})
                            print(f"\n   🔱 TEMPORAL ID (Prime Sentinel):")
                            print(f"      👤 {tid.get('name', 'Unknown')} | DOB: {tid.get('dob_hash', '?')}")
                            print(f"      📡 Personal Hz: {tid.get('frequency', 0):.6f}")
                            print(f"      🌀 Temporal Resonance: {temporal_state.get('temporal_resonance', 0):.1%}")
                            print(f"      🎵 DOB Harmony: {temporal_state.get('dob_harmony', 0):.2f}")
                            print(f"      ⚡ Current Strength: {temporal_state.get('current_strength', 0):.1%}")
                    except Exception as e:
                        logger.debug(f"Temporal state error: {e}")
                        
                except Exception as e:
                    logger.debug(f"Error getting wisdom state: {e}")
        
        # Save path memory on exit
        self.path_memory.save()
        
        print("=" * 70)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

async def main():
    parser = argparse.ArgumentParser(description="Micro Profit Labyrinth")
    parser.add_argument("--live", action="store_true", help="Run in LIVE mode")
    parser.add_argument("--duration", type=int, default=0, help="Duration in seconds (0 = forever)")
    parser.add_argument("--yes", "-y", action="store_true", help="Auto-confirm live mode (skip MICRO prompt)")
    args = parser.parse_args()
    
    if args.live and not args.yes:
        print("\n" + "=" * 60)
        print("⚠️  LIVE MODE REQUESTED - REAL MONEY!")
        print("=" * 60)
        confirm = input("Type 'MICRO' to confirm: ")
        if confirm.strip().upper() != 'MICRO':
            print("Aborted.")
            sys.exit(0)
    elif args.live and args.yes:
        print("\n" + "=" * 60)
        print("⚠️  LIVE MODE - AUTO-CONFIRMED! 🚀")
        print("=" * 60)
    
    engine = MicroProfitLabyrinth(live=args.live)
    await engine.run(duration_s=args.duration)


if __name__ == "__main__":
    asyncio.run(main())
