// Trading Signals - Combines Lighthouse + High Coherence for optimal entry points
// Trade signal confirmed when:
// 1. Lighthouse Event (LHE) detected
// 2. Coherence Γ > 0.945
// 3. Prism state is CONVERGING or MANIFEST

import type { LighthouseState } from './lighthouseConsensus';
import type { LambdaState } from './masterEquation';
import type { PrismOutput } from './prism';

export type TradingSignal = {
  timestamp: number;
  type: 'LONG' | 'SHORT' | 'HOLD';
  strength: number;        // 0-1, confidence in signal
  lighthouse: number;      // L(t) value
  coherence: number;       // Γ value
  prismLevel: number;      // 1-5
  reason: string;
};

export class TradingSignalGenerator {
  private readonly COHERENCE_THRESHOLD = 0.945;
  private lastSignal: TradingSignal | null = null;
  private signalHistory: TradingSignal[] = [];
  private readonly maxHistory = 50;
  
  generateSignal(
    lambda: LambdaState,
    lighthouse: LighthouseState,
    prism: PrismOutput
  ): TradingSignal {
    const timestamp = Date.now();
    
    // Check conditions for optimal trading moment
    const highCoherence = lambda.coherence >= this.COHERENCE_THRESHOLD;
    const lighthouseEvent = lighthouse.isLHE;
    const prismReady = prism.state === 'CONVERGING' || prism.state === 'MANIFEST';
    
    // Determine signal type and strength
    let type: 'LONG' | 'SHORT' | 'HOLD' = 'HOLD';
    let strength = 0;
    let reason = '';
    
    if (lighthouseEvent && highCoherence && prismReady) {
      // Perfect conditions - strongest signal
      type = 'LONG';
      strength = Math.min(
        lighthouse.confidence * lambda.coherence * (prism.level / 5),
        1
      );
      reason = `🎯 OPTIMAL: LHE + Γ=${lambda.coherence.toFixed(3)} + Prism L${prism.level}`;
      
    } else if (lighthouseEvent && highCoherence) {
      // Strong signal - lighthouse + coherence
      type = 'LONG';
      strength = lighthouse.confidence * lambda.coherence * 0.8;
      reason = `✨ STRONG: LHE + High Coherence Γ=${lambda.coherence.toFixed(3)}`;
      
    } else if (highCoherence && prismReady) {
      // Moderate signal - coherence + prism alignment
      type = 'LONG';
      strength = lambda.coherence * (prism.level / 5) * 0.6;
      reason = `📊 MODERATE: High Γ + Prism ${prism.state}`;
      
    } else if (lambda.coherence < 0.3 && lighthouse.L < lighthouse.threshold * 0.5) {
      // Weak conditions - consider short
      type = 'SHORT';
      strength = (1 - lambda.coherence) * 0.4;
      reason = `⚠️ WEAK: Low Γ=${lambda.coherence.toFixed(3)} + Low L(t)`;
      
    } else {
      // Hold - conditions not met
      type = 'HOLD';
      strength = 0.5;
      reason = `⏸️ HOLD: Γ=${lambda.coherence.toFixed(3)}, L(t)=${lighthouse.L.toFixed(2)}`;
    }
    
    const signal: TradingSignal = {
      timestamp,
      type,
      strength,
      lighthouse: lighthouse.L,
      coherence: lambda.coherence,
      prismLevel: prism.level,
      reason,
    };
    
    this.lastSignal = signal;
    this.signalHistory.push(signal);
    
    if (this.signalHistory.length > this.maxHistory) {
      this.signalHistory.shift();
    }
    
    return signal;
  }
  
  getLastSignal(): TradingSignal | null {
    return this.lastSignal;
  }
  
  getSignalHistory(): TradingSignal[] {
    return [...this.signalHistory];
  }
  
  // Get trade signal statistics
  getStatistics() {
    if (this.signalHistory.length === 0) {
      return {
        totalSignals: 0,
        longSignals: 0,
        shortSignals: 0,
        holdSignals: 0,
        averageStrength: 0,
        optimalSignals: 0,
      };
    }
    
    const longSignals = this.signalHistory.filter(s => s.type === 'LONG').length;
    const shortSignals = this.signalHistory.filter(s => s.type === 'SHORT').length;
    const holdSignals = this.signalHistory.filter(s => s.type === 'HOLD').length;
    const optimalSignals = this.signalHistory.filter(s => 
      s.reason.startsWith('🎯 OPTIMAL')
    ).length;
    
    const averageStrength = this.signalHistory.reduce((sum, s) => sum + s.strength, 0) / this.signalHistory.length;
    
    return {
      totalSignals: this.signalHistory.length,
      longSignals,
      shortSignals,
      holdSignals,
      averageStrength,
      optimalSignals,
    };
  }
  
  reset() {
    this.lastSignal = null;
    this.signalHistory = [];
  }
}
