import { useState, useEffect } from 'react';
import { qgitaSignalGenerator, QGITASignal } from '@/core/qgitaSignalGenerator';
import { useBinanceMarketData } from './useBinanceMarketData';
import { useBinanceMarginData } from './useBinanceMarginData';
import { MasterEquation } from '@/core/masterEquation';
import { useQGITAConfig } from './useQGITAConfig';
import { AureonDataPoint } from '@/components/AureonChart';

export function useQGITASignals(symbol: string) {
  const [signals, setSignals] = useState<QGITASignal[]>([]);
  const [latestSignal, setLatestSignal] = useState<QGITASignal | null>(null);
  const [aureonData, setAureonData] = useState<AureonDataPoint[]>([]);
  const [masterEq] = useState(() => new MasterEquation());
  const { config } = useQGITAConfig();
  
  const { marketData } = useBinanceMarketData(symbol);
  const { marginData } = useBinanceMarginData(symbol.replace('USDT', ''));
  
  // Update signal generator config when it changes
  useEffect(() => {
    qgitaSignalGenerator.updateConfig(config);
  }, [config]);
  
  useEffect(() => {
    if (!marketData) return;
    
    const interval = setInterval(() => {
      // Step the Master Equation with current market data
      const marketSnapshot = {
        timestamp: marketData.timestamp,
        price: marketData.price,
        volume: marketData.volume,
        volatility: marketData.volatility,
        momentum: marketData.momentum,
        spread: marketData.spread,
      };
      
      const lambdaState = masterEq.step(marketSnapshot);
      
      // Generate QGITA signal
      let signal = qgitaSignalGenerator.generateSignal(
        Date.now(),
        marketData.price,
        marketData.volume,
        lambdaState.lambda,
        lambdaState.coherence,
        lambdaState.substrate,
        lambdaState.observer,
        lambdaState.echo
      );
      
      // Apply margin sentiment adjustment
      if (marginData) {
        const { marketHealth, leverageRisk, liquidationPressure } = marginData.sentiment;
        
        // Boost confidence when market is healthy and low risk
        if (marketHealth > 0.7 && leverageRisk < 0.3) {
          signal = {
            ...signal,
            confidence: Math.min(100, signal.confidence * 1.1),
            reasoning: signal.reasoning + ' [Margin boost: Healthy market conditions]'
          };
        }
        // Reduce confidence when high risk or liquidation pressure
        else if (marketHealth < 0.4 || leverageRisk > 0.7 || liquidationPressure > 0.6) {
          signal = {
            ...signal,
            confidence: signal.confidence * 0.85,
            reasoning: signal.reasoning + ' [Margin caution: Elevated risk detected]'
          };
        }
      }
      
      setLatestSignal(signal);
      
      // Collect Aureon chart data (G_eff, Q_sig, sentiment, data integrity)
      const gEff = qgitaSignalGenerator['ftcpDetector'].computeGeff();
      const dataPoint: AureonDataPoint = {
        time: new Date().toLocaleTimeString(),
        crystalCoherence: gEff, // Geometric Anomaly (G_eff)
        inerchaVector: signal.anomalyPointer, // Anomaly Pointer (Q_sig)
        sentiment: signal.coherence.linearCoherence, // Market Sentiment (using linear coherence as proxy)
        dataIntegrity: signal.coherence.crossScaleCoherence, // Data Integrity (cross-scale coherence)
      };
      
      setAureonData(prev => {
        const updated = [...prev, dataPoint];
        // Keep only last 50 data points for the chart
        return updated.slice(-50);
      });
      
      // Only keep signals that are actionable (BUY/SELL with min confidence)
      if (signal.signalType !== 'HOLD' && signal.confidence >= config.minConfidenceForSignal) {
        setSignals(prev => {
          const updated = [...prev, signal];
          // Keep only last 50 signals
          return updated.slice(-50);
        });
      }
    }, 5000); // Check every 5 seconds
    
    return () => clearInterval(interval);
  }, [marketData, masterEq]);
  
  const stats = {
    totalSignals: signals.length,
    buySignals: signals.filter(s => s.signalType === 'BUY').length,
    sellSignals: signals.filter(s => s.signalType === 'SELL').length,
    avgConfidence: signals.length > 0 
      ? signals.reduce((sum, s) => sum + s.confidence, 0) / signals.length 
      : 0,
    tier1Signals: signals.filter(s => s.tier === 1).length,
    tier2Signals: signals.filter(s => s.tier === 2).length,
  };
  
  return {
    signals,
    latestSignal,
    aureonData,
    stats,
  };
}
