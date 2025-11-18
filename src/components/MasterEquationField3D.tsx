import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Text } from '@react-three/drei';
import { useRef, useMemo, useState } from 'react';
import * as THREE from 'three';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { LambdaState } from '@/core/masterEquation';
import fieldCavitySpacetime from '@/assets/research/field-cavity-spacetime.png';

interface MasterEquationField3DProps {
  lambda: LambdaState | null;
}

function FlowTube({ points, color, opacity }: { points: [number, number, number][]; color: string; opacity: number }) {
  const curve = useMemo(() => new THREE.CatmullRomCurve3(points.map(p => new THREE.Vector3(...p))), [points]);
  const geometry = useMemo(() => new THREE.TubeGeometry(curve, 64, 0.02, 8, false), [curve]);
  
  return (
    <mesh geometry={geometry}>
      <meshBasicMaterial color={color} transparent opacity={opacity} blending={THREE.AdditiveBlending} />
    </mesh>
  );
}

function SubstrateParticles({ substrate }: { substrate: number }) {
  const ref = useRef<THREE.Points>(null);
  const [trails, setTrails] = useState<Float32Array[]>([]);
  
  const { positions, colors } = useMemo(() => {
    const count = 1000;
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = 3 + Math.random() * 2, t = Math.random() * Math.PI * 2, p = Math.acos(2 * Math.random() - 1);
      pos[i * 3] = r * Math.sin(p) * Math.cos(t); pos[i * 3 + 1] = r * Math.sin(p) * Math.sin(t); pos[i * 3 + 2] = r * Math.cos(p);
      col[i * 3] = 0.2; col[i * 3 + 1] = 0.9; col[i * 3 + 2] = 0.3;
    }
    return { positions: pos, colors: col };
  }, []);
  
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime(), pos = ref.current.geometry.attributes.position.array as Float32Array;
    if (Math.floor(t * 60) % 5 === 0) setTrails(p => [...p, new Float32Array(pos)].slice(-10));
    for (let i = 0; i < 1000; i++) {
      const i3 = i * 3;
      pos[i3] += Math.sin(t * (0.2 + substrate * 0.5) + i) * 0.01 * substrate;
      pos[i3 + 1] += Math.cos(t * (0.2 + substrate * 0.5) + i) * 0.01 * substrate;
    }
    ref.current.geometry.attributes.position.needsUpdate = true;
  });
  
  return <>
    {trails.map((p, i) => <points key={i}><bufferGeometry><bufferAttribute attach="attributes-position" count={1000} array={p} itemSize={3} /><bufferAttribute attach="attributes-color" count={1000} array={colors} itemSize={3} /></bufferGeometry><pointsMaterial size={0.03} vertexColors transparent opacity={0.15 * (i / trails.length)} blending={THREE.AdditiveBlending} /></points>)}
    <points ref={ref}><bufferGeometry><bufferAttribute attach="attributes-position" count={1000} array={positions} itemSize={3} /><bufferAttribute attach="attributes-color" count={1000} array={colors} itemSize={3} /></bufferGeometry><pointsMaterial size={0.05} vertexColors transparent opacity={0.6} blending={THREE.AdditiveBlending} /></points>
  </>;
}

function ObserverParticles({ observer }: { observer: number }) {
  const ref = useRef<THREE.Points>(null);
  const { positions, colors } = useMemo(() => {
    const count = 500, pos = new Float32Array(count * 3), col = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const mr = 4, mnr = 1, u = Math.random() * Math.PI * 2, v = Math.random() * Math.PI * 2;
      pos[i * 3] = (mr + mnr * Math.cos(v)) * Math.cos(u); pos[i * 3 + 1] = (mr + mnr * Math.cos(v)) * Math.sin(u); pos[i * 3 + 2] = mnr * Math.sin(v);
      col[i * 3] = 0.3; col[i * 3 + 1] = 0.6; col[i * 3 + 2] = 1.0;
    }
    return { positions: pos, colors: col };
  }, []);
  
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const pos = ref.current.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < 500; i++) pos[i * 3 + 2] += Math.sin(clock.getElapsedTime() * 0.7 + i) * 0.02 * Math.abs(observer);
    ref.current.geometry.attributes.position.needsUpdate = true;
  });
  
  return <points ref={ref}><bufferGeometry><bufferAttribute attach="attributes-position" count={500} array={positions} itemSize={3} /><bufferAttribute attach="attributes-color" count={500} array={colors} itemSize={3} /></bufferGeometry><pointsMaterial size={0.06} vertexColors transparent opacity={0.5} blending={THREE.AdditiveBlending} /></points>;
}

function EchoParticles({ echo }: { echo: number }) {
  const ref = useRef<THREE.Points>(null);
  const { positions, colors } = useMemo(() => {
    const count = 300, pos = new Float32Array(count * 3), col = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const a = (i / count) * Math.PI * 4, r = 2 + (i / count) * 3;
      pos[i * 3] = r * Math.cos(a); pos[i * 3 + 1] = r * Math.sin(a); pos[i * 3 + 2] = (i / count) * 4 - 2;
      col[i * 3] = 0.8; col[i * 3 + 1] = 0.3; col[i * 3 + 2] = 1.0;
    }
    return { positions: pos, colors: col };
  }, []);
  
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const pos = ref.current.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < 300; i++) {
      const i3 = i * 3, p = clock.getElapsedTime() * 0.5 + (i / 300) * Math.PI * 2;
      pos[i3] += Math.sin(p) * 0.01 * Math.abs(echo); pos[i3 + 1] += Math.cos(p) * 0.01 * Math.abs(echo);
    }
    ref.current.geometry.attributes.position.needsUpdate = true;
  });
  
  return <points ref={ref}><bufferGeometry><bufferAttribute attach="attributes-position" count={300} array={positions} itemSize={3} /><bufferAttribute attach="attributes-color" count={300} array={colors} itemSize={3} /></bufferGeometry><pointsMaterial size={0.07} vertexColors transparent opacity={0.4} blending={THREE.AdditiveBlending} /></points>;
}

function LambdaCore({ lambda }: { lambda: number }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const s = 1 + Math.abs(lambda) * 0.3 + Math.sin(clock.getElapsedTime() * 2) * 0.1;
    ref.current.scale.set(s, s, s); ref.current.rotation.y += 0.005;
  });
  return <mesh ref={ref}><sphereGeometry args={[0.5, 32, 32]} /><meshStandardMaterial color="#ff3366" emissive="#ff1144" emissiveIntensity={0.7} metalness={0.8} roughness={0.2} /></mesh>;
}

function ComponentLabels() {
  return <><Text position={[0, 5, 0]} fontSize={0.4} color="#00ff88">S(t)</Text><Text position={[5.5, 0, 0]} fontSize={0.4} color="#4488ff">O(t)</Text><Text position={[-5.5, 0, 0]} fontSize={0.4} color="#cc44ff">E(t)</Text><Text position={[0, 0, 6]} fontSize={0.5} color="#ff3366">Λ(t)</Text></>;
}

function Scene({ lambda }: { lambda: LambdaState }) {
  const flow = (Math.abs(lambda.substrate) + Math.abs(lambda.observer) + Math.abs(lambda.echo)) / 3;
  return <>
    <ambientLight intensity={0.3} />
    <pointLight position={[10, 10, 10]} />
    <pointLight position={[0, 0, 0]} intensity={2} color="#ff3366" />
    <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} />
    <group><FlowTube points={[[0, 4, 0], [0.5, 2, 0.5], [0, 0, 0]]} color="#00ff88" opacity={0.3 + flow * 0.3} /><FlowTube points={[[4.5, 0, 0], [2.5, 0, 1], [0, 0, 0]]} color="#4488ff" opacity={0.3 + flow * 0.3} /><FlowTube points={[[-4.5, 0, 0], [-2.5, 0, -1], [0, 0, 0]]} color="#cc44ff" opacity={0.3 + flow * 0.3} /><FlowTube points={[[0, 4, 0], [3, 3, 0.5], [4.5, 0, 0], [3, -3, -0.5], [-4.5, 0, 0], [-3, 3, 0.5], [0, 4, 0]]} color="#ffffff" opacity={0.15} /></group>
    <SubstrateParticles substrate={lambda.substrate} />
    <ObserverParticles observer={lambda.observer} />
    <EchoParticles echo={lambda.echo} />
    <LambdaCore lambda={lambda.lambda} />
    <ComponentLabels />
    <OrbitControls autoRotate autoRotateSpeed={0.5} minDistance={5} maxDistance={30} />
  </>;
}

export const MasterEquationField3D = ({ lambda }: MasterEquationField3DProps) => {
  if (!lambda) return <Card className="p-6"><div className="text-center text-muted-foreground"><p>Start AUREON to visualize the Master Equation field</p></div></Card>;
  return (
    <div className="space-y-4">
      <Card className="p-6 bg-gradient-to-br from-primary/5 to-background border-2 border-primary/20">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xl font-bold">Master Equation 3D Field</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Λ(t) = S(t) + O(t) + E(t) with energy flow
            </p>
          </div>
          <div className="flex gap-2">
            <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">
              S: {lambda.substrate.toFixed(3)}
            </Badge>
            <Badge variant="outline" className="bg-blue-500/10 text-blue-500 border-blue-500/20">
              O: {lambda.observer.toFixed(3)}
            </Badge>
            <Badge variant="outline" className="bg-purple-500/10 text-purple-500 border-purple-500/20">
              E: {lambda.echo.toFixed(3)}
            </Badge>
          </div>
        </div>
        
        <div className="h-[600px] rounded-lg overflow-hidden bg-black/20 border border-border">
          <Canvas camera={{ position: [0, 0, 15], fov: 60 }}>
            <Scene lambda={lambda} />
          </Canvas>
        </div>
        
        <div className="grid grid-cols-3 gap-4 mt-4 text-sm">
          <div>
            <div className="font-semibold text-green-500">🟢 S(t)</div>
            <div className="text-xs text-muted-foreground mt-1">Green with trails - 9 Auris nodes</div>
          </div>
          <div>
            <div className="font-semibold text-blue-500">🔵 O(t)</div>
            <div className="text-xs text-muted-foreground mt-1">Blue with trails - Field awareness</div>
          </div>
          <div>
            <div className="font-semibold text-purple-500">🟣 E(t)</div>
            <div className="text-xs text-muted-foreground mt-1">Purple with trails - Memory</div>
          </div>
        </div>
        
        <div className="mt-4 p-3 rounded-lg bg-muted/30 text-center">
          <div className="text-lg font-semibold text-primary">Λ(t) = {lambda.lambda.toFixed(4)}</div>
          <div className="text-xs text-muted-foreground mt-1">Red core | White tubes show information flow</div>
        </div>
        
        {/* Field Cavity Research */}
        <div className="mt-4 border-t border-border/30 pt-4">
          <h4 className="text-sm font-semibold mb-3 text-muted-foreground">Research: Field Cavity Spacetime Structure</h4>
          <img 
            src={fieldCavitySpacetime}
            alt="Field cavity spacetime resonance geometry"
            className="w-full rounded-lg border border-border/50"
          />
          <p className="text-xs text-muted-foreground mt-2">
            Spacetime cavity resonance patterns showing how the Master Equation field creates standing waves in the temporal dimension. 
            The cavity structure enables coherent echo formation and phase-locking across substrate nodes.
          </p>
        </div>
      </Card>
    </div>
  );
};
