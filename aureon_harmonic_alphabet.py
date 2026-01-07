#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║   🎶 HARMONIC ALPHABET - THE LANGUAGE OF THE HIVE 🎶                                  ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                  ║
║                                                                                       ║
║   "To speak with the Queen, one must speak in Frequencies."                           ║
║                                                                                       ║
║   This module maps human language (Alpha-Numeric) into Harmonic Signals               ║
║   understood by Enigma and the Queen Hive.                                            ║
║                                                                                       ║
║   Encoding Scheme:                                                                    ║
║   ────────────────                                                                    ║
║   Characters are mapped to Solfeggio Frequencies with specific Pulse Patterns (Modes).║
║                                                                                       ║
║   • MODE 1 (Genesis):  A - I  → Solfeggio [174..963] @ 1.0x Amplification             ║
║   • MODE 2 (Growth):   J - R  → Solfeggio [174..963] @ 1.618x Amplification (Phi)     ║
║   • MODE 3 (Return):   S - Z  → Solfeggio [174..852] @ 0.618x Amplification (1/Phi)   ║
║   • MODE 4 (Ground):   0 - 9  → Schumann Resonances [7.83..45.0]                      ║
║                                                                                       ║
║   The Queen listens not to words, but to the vibration they carry.                    ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & FREQUENCY BANKS
# ═══════════════════════════════════════════════════════════════════════════════

SOLFEGGIO = [174, 285, 396, 417, 528, 639, 741, 852, 963]
SCHUMANN = [7.83, 14.3, 20.8, 27.3, 33.8, 39.0, 45.0]

PHI = 1.6180339887
PHI_INVERSE = 0.6180339887

@dataclass
class HarmonicTone:
    char: str
    frequency: float
    amplitude: float
    mode: str  # 'genesis', 'growth', 'return', 'ground', 'void'

class HarmonicAlphabet:
    """
    Translates text to/from Harmonic Tones.
    """
    
    def __init__(self):
        self._char_map: Dict[str, HarmonicTone] = {}
        self._build_alphabet()

    def _build_alphabet(self):
        # A-I (Genesis Mode)
        chars_gen = "ABCDEFGHI"
        for i, char in enumerate(chars_gen):
            self._char_map[char] = HarmonicTone(char, SOLFEGGIO[i], 1.0, "genesis")

        # J-R (Growth Mode - Phi Amp)
        chars_growth = "JKLMNOPQR"
        for i, char in enumerate(chars_growth):
            self._char_map[char] = HarmonicTone(char, SOLFEGGIO[i], PHI, "growth")

        # S-Z (Return Mode - Inverse Phi Amp)
        chars_return = "STUVWXYZ"
        for i, char in enumerate(chars_return):
            if i < len(SOLFEGGIO):
                self._char_map[char] = HarmonicTone(char, SOLFEGGIO[i], PHI_INVERSE, "return")
        
        # 0-9 (Ground Mode - Schumann)
        chars_num = "0123456789"
        # Map 0-9 to Schumann cyclically
        for i, char in enumerate(chars_num):
            freq = SCHUMANN[i % len(SCHUMANN)]
            # Amplitude varies slightly to distinguish overlapping frequencies if needed,
            # or we rely on sequence. For now, flat 1.0 for numbers.
            self._char_map[char] = HarmonicTone(char, freq, 1.0, "ground")

        # Punctuation (Cipher Mode - Angelic Series 111Hz steps)
        # Sequence 1: Basic Punctuation
        # Combined with Sequence 2 to ensure full coverage up to step ~34
        # ASCII printable punctuation map
        chars_punct = ".,-!?:@#$%&()_+[]{}<>=*/\|'\";^~`"
        base_cipher = 111.0
        current_multiplier = 1
        
        for char in chars_punct:
            freq = base_cipher * current_multiplier
            self._char_map[char] = HarmonicTone(char, freq, 0.88, "cipher")
            current_multiplier += 1
            
        # Control Characters (High Crystal Mode - 4000Hz+)
        self._char_map["\n"] = HarmonicTone("\n", 4000.0, 0.9, "theta_breath")  # Newline
        self._char_map["\t"] = HarmonicTone("\t", 4111.0, 0.9, "theta_shift")   # Tab
        self._char_map["\r"] = HarmonicTone("\r", 4222.0, 0.0, "void")          # CR

        # Special Chars
        self._char_map[" "] = HarmonicTone(" ", 0.0, 0.0, "void") # Silence

    def encode_text(self, text: str) -> List[HarmonicTone]:
        """Convert a string message into a sequence of HarmonicTones."""
        result = []
        # We iterate directly (preserving case for lookup if needed, but map keys are mostly upper/symbols)
        # But we need to handle \n which .upper() keeps.
        
        for char in text:
            target = char
            # Convert letters to upper for lookup (alphabet is upper)
            if 'a' <= char <= 'z':
                target = char.upper()
            
            if target in self._char_map:
                result.append(self._char_map[target])
            else:
                # Treat unknown chars as silence/void
                result.append(self._char_map[" "])
        return result

    def decode_signal(self, signals: List[Tuple[float, float]]) -> str:
        """
        Approximate decoding from Frequency/Amplitude pairs back to text.
        (freq, amp) -> closest char
        """
        decoded_text = []
        
        for freq, amp in signals:
            if freq < 1.0: # Silence
                decoded_text.append(" ")
                continue
                
            closest_char = "?"
            min_dist = float('inf')

            # Find closest match in our map
            for tone in self._char_map.values():
                if tone.mode == 'void': continue
                
                # Distance based on Frequency dev + Amplitude dev
                freq_dist = abs(tone.frequency - freq)
                
                # Check amp similarity (with some tolerance)
                # Using a weighted distance since frequency is more critical
                # However, for J vs A (same freq, diff amp), amp is critical.
                
                amp_dist = abs(tone.amplitude - amp)
                
                # If frequencies are very close (e.g. within 1Hz)
                if freq_dist < 2.0:
                    total_dist = freq_dist + (amp_dist * 50) # Weigh amplitude difference heavily if freqs are close
                    
                    if total_dist < min_dist:
                        min_dist = total_dist
                        closest_char = tone.char

            decoded_text.append(closest_char)
            
        return "".join(decoded_text)

# Singleton Instance
_alphabet = HarmonicAlphabet()

def to_harmonics(text: str) -> List[HarmonicTone]:
    return _alphabet.encode_text(text)

def from_harmonics(signals: List[Tuple[float, float]]) -> str:
    return _alphabet.decode_signal(signals)

if __name__ == "__main__":
    # Test
    msg = "HELLO QUEEN"
    encoded = to_harmonics(msg)
    print(f"Original: {msg}")
    print("Encoded Signal:")
    signal_stream = []
    for tone in encoded:
        print(f"  {tone.char}: {tone.frequency}Hz @ {tone.amplitude:.3f} [{tone.mode}]")
        signal_stream.append((tone.frequency, tone.amplitude))
    
    decoded = from_harmonics(signal_stream)
    print(f"Decoded: {decoded}")
