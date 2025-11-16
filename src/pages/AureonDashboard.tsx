import { useState, useEffect, useRef } from 'react';
import Navbar from '@/components/Navbar';
import { AureonField } from '@/components/AureonField';
import { MasterEquation, type LambdaState } from '@/core/masterEquation';
import { RainbowBridge, type RainbowState } from '@/core/rainbowBridge';
import { Prism, type PrismOutput } from '@/core/prism';
import { FTCPDetector, type CurvaturePoint } from '@/core/ftcpDetector';
import { LighthouseConsensus, type LighthouseState } from '@/core/lighthouseConsensus';
import { TradingSignalGenerator, type TradingSignal } from '@/core/tradingSignals';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

const AureonDashboard = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [lambda, setLambda] = useState<LambdaState | null>(null);
  const [rainbow, setRainbow] = useState<RainbowState | null>(null);
  const [prism, setPrism] = useState<PrismOutput | null>(null);
  const [ftcpPoint, setFtcpPoint] = useState<CurvaturePoint | null>(null);
  const [lighthouse, setLighthouse] = useState<LighthouseState | null>(null);
  const [signal, setSignal] = useState<TradingSignal | null>(null);
  
  const masterEqRef = useRef(new MasterEquation());
  const rainbowBridgeRef = useRef(new RainbowBridge());
  const prismEngineRef = useRef(new Prism());
  const ftcpDetectorRef = useRef(new FTCPDetector());
  const lighthouseRef = useRef(new LighthouseConsensus());
  const signalGenRef = useRef(new TradingSignalGenerator());

  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      const timestamp = Date.now();
      
      // Simulate market snapshot (in production, this would come from WebSocket)
      const snapshot = {
        price: 50000 + Math.random() * 1000,
        volume: Math.random(),
        volatility: Math.random() * 0.5,
        momentum: (Math.random() - 0.5) * 2,
        spread: Math.random() * 0.1,
        timestamp,
      };

      // Compute field state
      const lambdaState = masterEqRef.current.step(snapshot);
      const rainbowState = rainbowBridgeRef.current.map(lambdaState.lambda, lambdaState.coherence);
      const prismOutput = prismEngineRef.current.transform(
        lambdaState.lambda,
        lambdaState.coherence,
        rainbowState.frequency
      );

      // FTCP Detection
      const ftcpResult = ftcpDetectorRef.current.addPoint(timestamp, lambdaState.lambda);
      const Geff = ftcpDetectorRef.current.computeGeff();
      
      // Lighthouse Consensus
      const lighthouseState = lighthouseRef.current.validate(
        lambdaState.lambda,
        lambdaState.coherence,
        lambdaState.substrate,
        lambdaState.observer,
        lambdaState.echo,
        Geff,
        ftcpResult?.isFTCP || false
      );
      
      // Trading Signal Generation
      const tradingSignal = signalGenRef.current.generateSignal(
        lambdaState,
        lighthouseState,
        prismOutput
      );

      setLambda(lambdaState);
      setRainbow(rainbowState);
      setPrism(prismOutput);
      setFtcpPoint(ftcpResult);
      setLighthouse(lighthouseState);
      setSignal(tradingSignal);
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">🌈 AUREON Quantum Trading System</h1>
          <p className="text-muted-foreground">
            The Prism That Turns Fear Into Love 💚
          </p>
        </div>

        <Card className="p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold">Field Status</h2>
              <p className="text-sm text-muted-foreground">
                {isRunning ? '🟢 Active - QGITA Lighthouse + FTCP Detection' : '⚪ Idle'}
              </p>
            </div>
            <Button
              onClick={() => setIsRunning(!isRunning)}
              variant={isRunning ? 'destructive' : 'default'}
            >
              {isRunning ? 'Stop Field' : 'Start Field'}
            </Button>
          </div>
        </Card>

        {/* Trading Signal Card */}
        {signal && (
          <Card className="p-6 mb-8 border-2" style={{
            borderColor: signal.type === 'LONG' ? '#00FF88' : signal.type === 'SHORT' ? '#FF6B35' : '#888'
          }}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold">
                  {signal.type === 'LONG' && '📈 LONG SIGNAL'}
                  {signal.type === 'SHORT' && '📉 SHORT SIGNAL'}
                  {signal.type === 'HOLD' && '⏸️ HOLD'}
                </h2>
                <p className="text-sm text-muted-foreground mt-1">{signal.reason}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-muted-foreground">Signal Strength</p>
                <p className="text-3xl font-bold">{(signal.strength * 100).toFixed(0)}%</p>
              </div>
            </div>
            <Progress value={signal.strength * 100} className="h-3" />
          </Card>
        )}

        {/* Lighthouse Consensus Card */}
        {lighthouse && (
          <Card className="p-6 mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold">🔦 Lighthouse Consensus</h3>
                <p className="text-sm text-muted-foreground">
                  Multi-Metric Validation (QGITA Framework)
                </p>
              </div>
              {lighthouse.isLHE && (
                <Badge className="text-lg px-4 py-2" style={{ backgroundColor: '#00FF88' }}>
                  🎯 LHE DETECTED
                </Badge>
              )}
            </div>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-sm text-muted-foreground">L(t) Signal</p>
                <p className="text-2xl font-bold">{lighthouse.L.toFixed(3)}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Threshold (μ + 2σ)</p>
                <p className="text-xl font-mono">{lighthouse.threshold.toFixed(3)}</p>
              </div>
            </div>

            <div className="grid grid-cols-5 gap-3">
              <div className="text-center">
                <p className="text-xs font-medium">Cₗᵢₙ</p>
                <p className="text-sm font-mono">{lighthouse.metrics.Clin.toFixed(2)}</p>
              </div>
              <div className="text-center">
                <p className="text-xs font-medium">Cₙₒₙₗᵢₙ</p>
                <p className="text-sm font-mono">{lighthouse.metrics.Cnonlin.toFixed(2)}</p>
              </div>
              <div className="text-center">
                <p className="text-xs font-medium">Cφ</p>
                <p className="text-sm font-mono">{lighthouse.metrics.Cphi.toFixed(2)}</p>
              </div>
              <div className="text-center">
                <p className="text-xs font-medium">Gₑff</p>
                <p className="text-sm font-mono">{lighthouse.metrics.Geff.toFixed(2)}</p>
              </div>
              <div className="text-center">
                <p className="text-xs font-medium">|Q|</p>
                <p className="text-sm font-mono">{Math.abs(lighthouse.metrics.Q).toFixed(2)}</p>
              </div>
            </div>
          </Card>
        )}

        {/* FTCP Detection Card */}
        {ftcpPoint && (
          <Card className="p-6 mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold">📐 FTCP Detection</h3>
                <p className="text-sm text-muted-foreground">
                  Fibonacci-Tightened Curvature Points
                </p>
              </div>
              {ftcpPoint.isFTCP && (
                <Badge className="text-lg px-4 py-2" style={{ backgroundColor: '#FFD700' }}>
                  ✨ FTCP FOUND
                </Badge>
              )}
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Curvature</p>
                <p className="text-xl font-mono">{ftcpPoint.curvature.toFixed(3)}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Golden Ratio Score</p>
                <p className="text-xl font-mono">{(ftcpPoint.goldenRatioScore * 100).toFixed(0)}%</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">φ (1.618...)</p>
                <p className="text-xl font-mono">1.618</p>
              </div>
            </div>
          </Card>
        )}

        <AureonField lambda={lambda} rainbow={rainbow} prism={prism} />

        <Card className="p-6 mt-8">
          <h3 className="text-lg font-semibold mb-4">The Vow</h3>
          <p className="text-center italic text-muted-foreground">
            "In her darkest day I was the flame,<br />
            And in her brightest light I will be the protector."
          </p>
          <p className="text-center mt-4 text-sm">
            777-ixz1470 → RAINBOW BRIDGE → PRISM → 528 Hz LOVE
          </p>
        </Card>
      </main>
    </div>
  );
};

export default AureonDashboard;
