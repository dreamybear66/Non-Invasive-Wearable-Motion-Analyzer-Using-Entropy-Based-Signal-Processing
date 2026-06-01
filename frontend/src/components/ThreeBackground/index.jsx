import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';

const ParticleSystem = () => {
  const pointsRef = useRef();
  const { mouse, viewport } = useThree();
  const particleCount = 1200;

  // Generate particles
  const [positions, colors] = useMemo(() => {
    const pos = new Float32Array(particleCount * 3);
    const col = new Float32Array(particleCount * 3);

    const colorPalette = [
      new THREE.Color('#3b82f6'), // Electric Blue
      new THREE.Color('#8b5cf6'), // Purple
      new THREE.Color('#06b6d4'), // Cyan
      new THREE.Color('#22c55e'), // Green
      new THREE.Color('#1a3060')  // Dim Navy
    ];

    for (let i = 0; i < particleCount; i++) {
      // Random position in a 220x220x120 volume
      pos[i * 3] = (Math.random() - 0.5) * 220;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 220;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 120;

      // Random color from palette
      const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
      col[i * 3] = color.r;
      col[i * 3 + 1] = color.g;
      col[i * 3 + 2] = color.b;
    }

    return [pos, col];
  }, [particleCount]);

  useFrame((state) => {
    if (!pointsRef.current) return;
    
    // Base continuous slow rotation
    pointsRef.current.rotation.y += 0.0004;
    pointsRef.current.rotation.x += 0.0001;

    // Mouse parallax
    const targetX = (mouse.x * viewport.width) / 10;
    const targetY = (mouse.y * viewport.height) / 10;
    
    pointsRef.current.position.x += (targetX - pointsRef.current.position.x) * 0.03;
    pointsRef.current.position.y += (targetY - pointsRef.current.position.y) * 0.03;

    // Opacity pulse
    const time = state.clock.getElapsedTime();
    pointsRef.current.material.opacity = 0.5 + Math.sin(time * 0.5) * 0.15;
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={colors.length / 3}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={1.5}
        vertexColors={true}
        transparent={true}
        opacity={0.6}
        sizeAttenuation={true}
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
};

export default function ThreeBackground() {
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 0, overflow: 'hidden' }}>
      <Canvas
        camera={{ position: [0, 0, 80], fov: 60 }}
        dpr={[1, 2]} // Cap pixel ratio at 2 for performance
        gl={{ alpha: true, antialias: false }}
      >
        <ParticleSystem />
      </Canvas>
    </div>
  );
}
