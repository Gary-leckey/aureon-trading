import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Text } from '@react-three/drei';
import { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { LambdaState } from '@/core/masterEquation';

interface MasterEquationField3DProps {
  lambda: LambdaState | null;
}

// Substrate particles (green) - representing 9 Auris nodes
function SubstrateParticles({ substrate, nodeResponses }: { substrate: number; nodeResponses: Record<string, number> }) {
  const particlesRef = useRef<THREE.Points>(null);
  const particleCount = 1000;
  
  const particles = useMemo(() => {
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
      // Distribute particles in a sphere around origin
      const radius = 3 + Math.random() * 2;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      
      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi);
      
      // Green color with variation
      colors[i * 3] = 0.1 + Math.random() * 0.3;
      colors[i * 3 + 1] = 0.8 + Math.random() * 0.2;
      colors[i * 3 + 2] = 0.2 + Math.random() * 0.3;
    }
    
    return { positions, colors };
  }, []);
  
  useFrame((state) => {
    if (!particlesRef.current) return;
    
    const time = state.clock.getElapsedTime();
    const positions = particlesRef.current.geometry.attributes.position.array as Float32Array;
    
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      
      // Orbital motion influenced by substrate strength
      const speed = 0.2 + substrate * 0.5;
      const radius = Math.sqrt(positions[i3] ** 2 + positions[i3 + 1] ** 2 + positions[i3 + 2] ** 2);
      const angle = time * speed;
      
      positions[i3] += Math.sin(angle + i) * 0.01 * substrate;
      positions[i3 + 1] += Math.cos(angle + i) * 0.01 * substrate;
      positions[i3 + 2] += Math.sin(angle * 0.5 + i) * 0.005 * substrate;
    }
    
    particlesRef.current.geometry.attributes.position.needsUpdate = true;
    particlesRef.current.rotation.y += 0.0005 * substrate;
  });
  
  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={particles.positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={particleCount}
          array={particles.colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        vertexColors
        transparent
        opacity={0.6}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

// Observer particles (blue) - self-referential awareness
function ObserverParticles({ observer }: { observer: number }) {
  const particlesRef = useRef<THREE.Points>(null);
  const particleCount = 500;
  
  const particles = useMemo(() => {
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
      // Distribute in a torus shape
      const majorRadius = 4;
      const minorRadius = 1;
      const u = Math.random() * Math.PI * 2;
      const v = Math.random() * Math.PI * 2;
      
      positions[i * 3] = (majorRadius + minorRadius * Math.cos(v)) * Math.cos(u);
      positions[i * 3 + 1] = (majorRadius + minorRadius * Math.cos(v)) * Math.sin(u);
      positions[i * 3 + 2] = minorRadius * Math.sin(v);
      
      // Blue color
      colors[i * 3] = 0.2 + Math.random() * 0.3;
      colors[i * 3 + 1] = 0.5 + Math.random() * 0.3;
      colors[i * 3 + 2] = 0.9 + Math.random() * 0.1;
    }
    
    return { positions, colors };
  }, []);
  
  useFrame((state) => {
    if (!particlesRef.current) return;
    
    const time = state.clock.getElapsedTime();
    const positions = particlesRef.current.geometry.attributes.position.array as Float32Array;
    
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      
      // Spiral motion influenced by observer
      const spiralSpeed = 0.3 + observer * 0.4;
      positions[i3 + 2] += Math.sin(time * spiralSpeed + i) * 0.02 * Math.abs(observer);
      
      // Keep within bounds
      if (Math.abs(positions[i3 + 2]) > 3) {
        positions[i3 + 2] *= -0.8;
      }
    }
    
    particlesRef.current.geometry.attributes.position.needsUpdate = true;
    particlesRef.current.rotation.z += 0.001 * observer;
  });
  
  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={particles.positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={particleCount}
          array={particles.colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.06}
        vertexColors
        transparent
        opacity={0.5}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

// Echo particles (purple) - memory and momentum
function EchoParticles({ echo }: { echo: number }) {
  const particlesRef = useRef<THREE.Points>(null);
  const particleCount = 300;
  
  const particles = useMemo(() => {
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
      // Distribute in trailing spiral
      const angle = (i / particleCount) * Math.PI * 4;
      const radius = 2 + (i / particleCount) * 3;
      
      positions[i * 3] = radius * Math.cos(angle);
      positions[i * 3 + 1] = radius * Math.sin(angle);
      positions[i * 3 + 2] = (i / particleCount) * 4 - 2;
      
      // Purple color
      colors[i * 3] = 0.7 + Math.random() * 0.3;
      colors[i * 3 + 1] = 0.2 + Math.random() * 0.3;
      colors[i * 3 + 2] = 0.9 + Math.random() * 0.1;
    }
    
    return { positions, colors };
  }, []);
  
  useFrame((state) => {
    if (!particlesRef.current) return;
    
    const time = state.clock.getElapsedTime();
    const positions = particlesRef.current.geometry.attributes.position.array as Float32Array;
    
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      
      // Wave motion influenced by echo
      const waveSpeed = 0.5 + Math.abs(echo) * 0.3;
      const phase = time * waveSpeed + (i / particleCount) * Math.PI * 2;
      
      positions[i3] += Math.sin(phase) * 0.01 * Math.abs(echo);
      positions[i3 + 1] += Math.cos(phase) * 0.01 * Math.abs(echo);
    }
    
    particlesRef.current.geometry.attributes.position.needsUpdate = true;
    particlesRef.current.rotation.x += 0.0008 * echo;
  });
  
  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={particles.positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={particleCount}
          array={particles.colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.07}
        vertexColors
        transparent
        opacity={0.4}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

// Central core representing Lambda
function LambdaCore({ lambda }: { lambda: number }) {
  const sphereRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (!sphereRef.current) return;
    
    const time = state.clock.getElapsedTime();
    const scale = 1 + Math.abs(lambda) * 0.3 + Math.sin(time * 2) * 0.1;
    sphereRef.current.scale.set(scale, scale, scale);
    sphereRef.current.rotation.y += 0.005;
    sphereRef.current.rotation.x += 0.003;
  });
  
  return (
    <mesh ref={sphereRef}>
      <sphereGeometry args={[0.5, 32, 32]} />
      <meshStandardMaterial
        color="#ff3366"
        emissive="#ff1144"
        emissiveIntensity={0.5 + Math.abs(lambda) * 0.5}
        metalness={0.8}
        roughness={0.2}
      />
    </mesh>
  );
}

// Component labels
function ComponentLabels() {
  return (
    <>
      <Text
        position={[0, 5, 0]}
        fontSize={0.4}
        color="#00ff88"
        anchorX="center"
        anchorY="middle"
      >
        S(t) Substrate
      </Text>
      <Text
        position={[5, 0, 0]}
        fontSize={0.4}
        color="#4488ff"
        anchorX="center"
        anchorY="middle"
      >
        O(t) Observer
      </Text>
      <Text
        position={[-5, 0, 0]}
        fontSize={0.4}
        color="#cc44ff"
        anchorX="center"
        anchorY="middle"
      >
        E(t) Echo
      </Text>
      <Text
        position={[0, 0, 6]}
        fontSize={0.5}
        color="#ff3366"
        anchorX="center"
        anchorY="middle"
      >
        Λ(t)
      </Text>
    </>
  );
}

// Main 3D Scene
function Scene({ lambda }: { lambda: LambdaState }) {
  return (
    <>
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <pointLight position={[-10, -10, -10]} intensity={0.5} />
      
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
      
      <SubstrateParticles substrate={lambda.substrate} nodeResponses={lambda.nodeResponses} />
      <ObserverParticles observer={lambda.observer} />
      <EchoParticles echo={lambda.echo} />
      <LambdaCore lambda={lambda.lambda} />
      <ComponentLabels />
      
      <OrbitControls
        enableZoom={true}
        enablePan={true}
        enableRotate={true}
        autoRotate={true}
        autoRotateSpeed={0.5}
        minDistance={5}
        maxDistance={30}
      />
    </>
  );
}

export const MasterEquationField3D = ({ lambda }: MasterEquationField3DProps) => {
  if (!lambda) {
    return (
      <Card className="p-6">
        <div className="text-center text-muted-foreground">
          <p>Start AUREON to visualize the Master Equation field</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <Card className="p-6 bg-gradient-to-br from-primary/5 to-background border-2 border-primary/20">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xl font-bold">Master Equation 3D Field</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Λ(t) = S(t) + O(t) + E(t)
            </p>
          </div>
          <div className="flex gap-2">
            <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">
              S(t): {lambda.substrate.toFixed(3)}
            </Badge>
            <Badge variant="outline" className="bg-blue-500/10 text-blue-500 border-blue-500/20">
              O(t): {lambda.observer.toFixed(3)}
            </Badge>
            <Badge variant="outline" className="bg-purple-500/10 text-purple-500 border-purple-500/20">
              E(t): {lambda.echo.toFixed(3)}
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
            <div className="font-semibold text-green-500">🟢 Substrate S(t)</div>
            <div className="text-xs text-muted-foreground mt-1">
              Green particles orbiting - Response from 9 Auris nodes
            </div>
          </div>
          <div>
            <div className="font-semibold text-blue-500">🔵 Observer O(t)</div>
            <div className="text-xs text-muted-foreground mt-1">
              Blue particles in torus - Self-referential field awareness
            </div>
          </div>
          <div>
            <div className="font-semibold text-purple-500">🟣 Echo E(t)</div>
            <div className="text-xs text-muted-foreground mt-1">
              Purple particles spiraling - Memory and momentum
            </div>
          </div>
        </div>

        <div className="mt-4 p-3 rounded-lg bg-muted/30 text-center">
          <div className="text-lg font-semibold text-primary">
            Λ(t) = {lambda.lambda.toFixed(4)}
          </div>
          <div className="text-xs text-muted-foreground mt-1">
            Central red core - Master field state
          </div>
        </div>
      </Card>
    </div>
  );
};
