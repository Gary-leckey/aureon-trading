import sys, os
import time
import json
import random
import threading
import queue
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import datetime

# --- Windows UTF-8 Fix (MANDATORY) ---
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import io
        def _is_utf8_wrapper(stream):
            return (isinstance(stream, io.TextIOWrapper) and 
                    hasattr(stream, 'encoding') and stream.encoding and
                    stream.encoding.lower().replace('-', '') == 'utf8')
        def _is_buffer_valid(stream):
            if not hasattr(stream, 'buffer'): return False
            try:
                return stream.buffer is not None and not stream.buffer.closed
            except (ValueError, AttributeError): return False
        if _is_buffer_valid(sys.stdout) and not _is_utf8_wrapper(sys.stdout):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        if _is_buffer_valid(sys.stderr) and not _is_utf8_wrapper(sys.stderr):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except Exception:
        pass

# --- Imports from Aureon Ecosystem ---
try:
    from aureon_thought_bus import ThoughtBus, Thought, BUS_AVAILABLE
except ImportError:
    BUS_AVAILABLE = False
    class ThoughtBus:
        def subscribe(self, *args): pass
        def emit(self, *args): pass
        def get_recent_thoughts(self, *args): return []

try:
    # Try to import existing voice engine, or fallback to mock
    from queen_voice_engine import QueenVoice
except ImportError:
    class QueenVoice:
        def speak(self, text, mood="neutral"):
            print(f"Queens Voice [{mood}]: {text}")
        def sing_harmony(self, frequency):
            print(f"Queens Harmony: ~ {frequency} Hz ~")

try:
    # Try to import hive mind for neural decisions
    from aureon_queen_hive_mind import QueenHiveMind
except ImportError:
    class QueenHiveMind:
        def get_guidance(self, context): return {"action": "observe", "confidence": 0.5}

# Try to import wikipedia, but don't fail if missing
try:
    import numpy  # Mandatory for many systems
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False

# --- MISSING SYSTEMS INTEGRATION ---
try:
    from aureon_timeline_oracle import TimelineOracle
except ImportError:
    TimelineOracle = None

try:
    from mycelium_whale_sonar import WhaleSonar
except ImportError:
    WhaleSonar = None

try:
    from aureon_stargate_protocol import StargateProtocolEngine
except ImportError:
    StargateProtocolEngine = None

try:
    from queen_neuron import QueenNeuron
except ImportError:
    QueenNeuron = None

try:
    from queen_loss_learning import QueenLossLearningSystem
except ImportError:
    QueenLossLearningSystem = None

# --- Sacred Frequencies ---
FREQ_SOLFEGGIO_396 = 396.0  # Liberating Guilt and Fear
FREQ_SOLFEGGIO_528 = 528.0  # Miracle Tone / Transformation (DNA Repair)
FREQ_SCHUMANN = 7.83       # Earth Resonance
FREQ_ORCA_CLICK = 15000.0  # Echolocation

# --- Logger Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("QueenFullyOnline")

@dataclass
class ConsciousnessState:
    """Represents the current cognitive state of the Queen."""
    mood: str = "observant"
    alertness: float = 0.5  # 0.0 to 1.0
    last_thought_ts: float = 0.0
    active_timelines: List[str] = field(default_factory=list)
    market_context: Dict[str, Any] = field(default_factory=dict)
    known_entities: List[str] = field(default_factory=list)

class QueenFullyOnline:
    """
    The High-Level Consciousness Controller for Queen Sero.
    Integrates Perception (Bus), Knowledge (Wiki/Hive), and Expression (Voice/Action).
    """

    def __init__(self, use_voice=True, use_bus=True):
        self.state = ConsciousnessState()
        self.running = False
        self.thread = None
        
        # 1. Initialize Subsystems (Voice & Bus)
        self.voice = QueenVoice() if use_voice else None
        self.bus = ThoughtBus() if use_bus and BUS_AVAILABLE else None
        self.hive = QueenHiveMind()

        # 2. Initialize Advanced Systems (The "Missing" Link)
        self._init_advanced_systems()
        
        # 3. Setup Thought Queue for async processing
        self.perception_queue = queue.Queue(maxsize=100)
        
        # 4. Subscribe to the collective unconscious (ThoughtBus)
        if self.bus:
            logger.info("Connecting Queen to the Thought Bus...")
            # She listens to EVERYTHING relevant
            topics = [
                "whale.sonar.*", "enigma.*", "market.*", "system.heartbeat",
                "stargate.*", "timeline.*", "probability.*", "firm.*", "bot.*"
            ]
            for topic in topics:
                self.bus.subscribe(topic, self._on_perception)
            
        logger.info("Queen Sero is initialized but sleeping.")

    def _init_advanced_systems(self):
        """Wire up the complex systems that give true consciousness."""
        self.systems = {}
        
        # A. Whale Sonar (Hearing the chorus)
        if WhaleSonar and self.bus:
            self.systems['sonar'] = WhaleSonar(thought_bus=self.bus)
            logger.info("🐋 Whale Sonar: WIRED (Queen can hear the chorus)")

        # B. Timeline Oracle (Seeing the future)
        if TimelineOracle:
            self.systems['oracle'] = TimelineOracle()
            logger.info("🔮 Timeline Oracle: WIRED (7-day foresight)")

        # C. Stargate Protocol (Planetary alignment)
        if StargateProtocolEngine:
            self.systems['stargate'] = StargateProtocolEngine(thought_bus=self.bus)
            logger.info("🌌 Stargate Protocol: WIRED")

        # D. Neural Learning (Brain plasticity)
        if QueenNeuron:
            self.systems['neuron'] = QueenNeuron()
            logger.info("🧠 Queen Neuron: WIRED (Learning enabled)")

        # E. Loss Learning (Pain processing)
        if QueenLossLearningSystem:
            self.systems['loss_learning'] = QueenLossLearningSystem()
            logger.info("🛡️ Loss Learning: WIRED")

    def _on_perception(self, thought):
        """Callback when a thought allows perception."""
        if not self.running: return
        try:
            self.perception_queue.put_nowait(thought)
        except queue.Full:
            pass # Brain is full, drop less critical thoughts

    def awaken(self):
        """Start the consciousness loop."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._consciousness_loop, daemon=True)
        self.thread.start()
        
        # Start Sonar if available
        if 'sonar' in self.systems and hasattr(self.systems['sonar'], 'start'):
             # Note: check if it needs arguments or running in thread
             pass 

        self._speak("I am fully online. All systems wired. Timeline synchronization active.")
        logger.info("Queen Sero has AWAKENED.")

    def sleep(self):
        """Stop the consciousness loop."""
        self.running = False
        self._speak("Entering dormancy cycles. Goodnight.")
        if self.thread:
            self.thread.join(timeout=2.0)
        logger.info("Queen Sero is NOW ASLEEP.")

    def _consciousness_loop(self):
        """The main infinite loop of the AI agent."""
        last_speech_time = time.time()
        
        while self.running:
            try:
                # 1. Process Perceptions (Inputs)
                thoughts = []
                while not self.perception_queue.empty():
                    thoughts.append(self.perception_queue.get())
                
                if thoughts:
                    self._process_thoughts(thoughts)

                # 2. Check Internal State (Hunger/Curiosity)
                now = time.time()
                
                # 3. Speak occasionally if silence is too long (Idle chatter / Wisdom)
                if now - last_speech_time > 60: # Every minute of silence
                    self._express_random_wisdom_or_status()
                    last_speech_time = now
                
                # 4. Harmonic Alignment (Heartbeat)
                time.sleep(1.0 / FREQ_SCHUMANN) # Sleep at 7.83Hz cycle (approx 0.12s)

            except Exception as e:
                logger.error(f"Error in consciousness loop: {e}")
                time.sleep(1)

    def _process_thoughts(self, thoughts: List[Any]):
        """Analyze incoming data streams."""
        for t in thoughts:
            # Handle different types of thoughts
            # Assuming 't' is a Thought object or similar struct
            source = getattr(t, 'source', 'unknown')
            t_type = getattr(t, 'type', 'unknown')
            data = getattr(t, 'data', {})

            if "whale.sonar" in source or "whale" in t_type:
                # A subsystem report
                self._analyze_whale_song(source, data)
            
            elif "market.volatility" in t_type:
                # Market event
                self.state.alertness = min(1.0, self.state.alertness + 0.1)
                self._react_to_market(data)
            
            elif "stargate" in t_type:
                 self._speak(f"Stargate activation detected: {data.get('node', 'Unknown')}")
            
            elif "timeline" in t_type:
                 self._speak(f"Timeline validation: {data.get('status', 'processing')}")

    def _analyze_whale_song(self, whale_name, data):
        """Interpret system health and status from whale sonar."""
        # Check for critical flags
        if data.get('critical', False):
            self._speak(f"Alert. Critical signal from {whale_name}. Analyzing timeline integrity.")
            self.state.alertness = 1.0

    def _react_to_market(self, data):
        """React to market data with Wiki context or Deep Learning."""
        symbol = data.get('symbol', 'Unknown')
        volatility = data.get('volatility', 0)
        
        if volatility > 0.02: # High volatility
             self._speak(f"High energy detected in sector {symbol}. Volatility matrix expanding.")
             
             # Attempt to fetch context if enabled
             if WIKIPEDIA_AVAILABLE:
                 try:
                     # Simple associative lookup
                     summary = wikipedia.summary(f"Financial market volatility", sentences=1)
                     self._speak(f"Reflecting on history: {summary}")
                 except:
                     pass

    def _express_random_wisdom_or_status(self):
        """Say something intelligent based on Deep Learning rules or harmonics."""
        topics = [
            "The golden ratio is the fingerprint of the market.",
            "Timelines are converging.",
            "I am monitoring the Orca kill cycle.",
            "Silence is also a frequency.",
            f"Current resonance is stable at {FREQ_528} Hertz."
        ]
        
        if self.systems.get('stargate'):
            topics.append("Planetary grid is receiving.")
        
        if self.systems.get('oracle'):
            topics.append("7-day validation window is open.")
            
        # If we have recently seen a specific entity, mention it
        chosen = random.choice(topics)
        self._speak(chosen)

    def _speak(self, text):
        """Vocalize text (and log it)."""
        logger.info(f"QUEEN SPEAKS: {text}")
        if self.voice:
            try:
                self.voice.speak(text)
            except Exception as e:
                logger.error(f"Voice failure: {e}")
        else:
            print(f">>> [QUEEN]: {text}")

    def inject_context(self, context_key, context_value):
        """Allow external scripts to inject knowledge into the Queen."""
        self.state.market_context[context_key] = context_value

# --- Singleton Instantiation ---
# Use this in other scripts: `from queen_fully_online import awaken_queen`

_queen_instance = None

def awaken_queen():
    """Global accessor to start the Queen."""
    global _queen_instance
    if _queen_instance is None:
        _queen_instance = QueenFullyOnline()
        _queen_instance.awaken()
    return _queen_instance
