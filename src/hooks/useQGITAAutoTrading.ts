import { useEffect, useRef, useState } from 'react';
import { QGITASignal } from '@/core/qgitaSignalGenerator';
import { supabase } from '@/integrations/supabase/client';
import { useToast } from '@/hooks/use-toast';

interface QGITAAutoTradingProps {
  signal: QGITASignal | null;
  symbol: string;
  currentPrice: number;
  enabled: boolean;
}

const STORAGE_KEY = 'qgita-auto-trading-enabled';

export function useQGITAAutoTrading({ signal, symbol, currentPrice, enabled }: QGITAAutoTradingProps) {
  const { toast } = useToast();
  const [isExecuting, setIsExecuting] = useState(false);
  const lastExecutedSignalRef = useRef<string | null>(null);

  useEffect(() => {
    if (!enabled || !signal || !currentPrice) return;

    // Only execute Tier 1 or Tier 2 signals
    if (signal.tier === 3 || signal.signalType === 'HOLD') return;

    // Prevent duplicate executions
    const signalKey = `${signal.timestamp}-${signal.signalType}-${signal.confidence}`;
    if (lastExecutedSignalRef.current === signalKey) return;

    executeQGITATrade();

    async function executeQGITATrade() {
      if (isExecuting) return;

      try {
        setIsExecuting(true);
        lastExecutedSignalRef.current = signalKey;

        toast({
          title: "🎯 QGITA Auto-Trading",
          description: `Executing ${signal.signalType} signal (Tier ${signal.tier}, ${signal.confidence.toFixed(1)}% confidence)`,
        });

        const { data, error } = await supabase.functions.invoke('execute-trade', {
          body: {
            symbol,
            signalType: signal.signalType,
            price: currentPrice,
            coherence: signal.coherence.crossScaleCoherence,
            lighthouseValue: signal.lighthouse.L,
            lighthouseConfidence: signal.lighthouse.confidence,
            prismLevel: 5, // QGITA signals are high-quality
            signalStrength: signal.confidence,
            signalReasoning: signal.reasoning,
            // QGITA-specific metadata
            qgitaTier: signal.tier,
            qgitaCurvature: signal.curvature,
            qgitaFTCP: signal.ftcpDetected,
            qgitaGoldenRatio: signal.goldenRatioScore,
          },
        });

        if (error) throw error;

        toast({
          title: "✅ Trade Executed",
          description: `${signal.signalType} order placed successfully via QGITA auto-trading`,
        });

        console.log('QGITA Auto-Trade executed:', data);

      } catch (error) {
        console.error('QGITA Auto-Trading error:', error);
        toast({
          title: "❌ Auto-Trade Failed",
          description: error instanceof Error ? error.message : 'Failed to execute QGITA trade',
          variant: "destructive",
        });
      } finally {
        setIsExecuting(false);
      }
    }
  }, [enabled, signal, symbol, currentPrice, toast, isExecuting]);

  return {
    isExecuting,
  };
}

export function useQGITAAutoTradingToggle() {
  const [isEnabled, setIsEnabled] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored === 'true';
    } catch {
      return false;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, String(isEnabled));
    } catch (error) {
      console.error('Failed to save QGITA auto-trading state:', error);
    }
  }, [isEnabled]);

  return {
    isEnabled,
    setIsEnabled,
  };
}
