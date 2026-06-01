import React, { useRef, useEffect, useState } from 'react';
import gsap from 'full/gsap'; // Assuming standard gsap import

export default function FatigueGauge({ fisValue, size = 'full' }) {
  const arcRef = useRef(null);
  const numberRef = useRef(null);
  const glowRef = useRef(null);
  const badgeRef = useRef(null);
  const [displayedFis, setDisplayedFis] = useState(0);
  
  // Size config
  const config = {
    full: { radius: 120, stroke: 16, fontSize: 64 },
    mini: { radius: 52, stroke: 8, fontSize: 24 },
    micro: { radius: 20, stroke: 4, fontSize: 0 } // No text for micro
  }[size];
  
  const center = config.radius + config.stroke * 2;
  const svgSize = center * 2;
  const circumference = Math.PI * config.radius; // Semicircle

  // State colors
  const getStateConfig = (fis) => {
    if (fis >= 65) return { color: 'var(--fatigue-high)', label: 'HIGH FATIGUE', icon: '🚨' };
    if (fis >= 40) return { color: 'var(--fatigue-moderate)', label: 'MODERATE FATIGUE', icon: '🔶' };
    if (fis >= 20) return { color: 'var(--fatigue-early)', label: 'EARLY FATIGUE', icon: '⚠' };
    return { color: 'var(--fatigue-normal)', label: 'NORMAL', icon: '●' };
  };

  const stateConfig = getStateConfig(fisValue);

  useEffect(() => {
    if (!arcRef.current || !numberRef.current || !glowRef.current) return;

    // Calculate dash offset based on percentage (0-100)
    const percentage = Math.min(Math.max(fisValue, 0), 100) / 100;
    const dashOffset = circumference * (1 - percentage);

    // Animate the arc fill
    gsap.to(arcRef.current, {
      strokeDashoffset: dashOffset,
      duration: 1.2,
      ease: 'power2.out'
    });
    
    // Animate glow arc to match the stroke
    gsap.to(glowRef.current, {
      strokeDashoffset: dashOffset,
      stroke: stateConfig.color,
      duration: 1.2,
      ease: 'power2.out'
    });

    // Animate the number counting up/down
    gsap.to(numberRef.current, {
      innerHTML: Math.round(fisValue),
      duration: 1.2,
      ease: 'power2.out',
      snap: { innerHTML: 1 },
      onUpdate: function() {
        setDisplayedFis(Math.round(this.targets()[0].innerHTML));
      }
    });

    // Animate the badge pop on state change
    if (badgeRef.current) {
      gsap.fromTo(badgeRef.current,
        { scale: 0.9 },
        { scale: 1, duration: 0.5, ease: 'back.out(1.7)' }
      );
    }

  }, [fisValue, circumference, stateConfig.color]);

  // Continuous glow pulse for full gauge
  useEffect(() => {
    if (size !== 'full' || !glowRef.current) return;
    
    const pulseAnim = gsap.to(glowRef.current, {
      opacity: 0.6,
      duration: 2.5,
      yoyo: true,
      repeat: -1,
      ease: 'sine.inOut'
    });
    
    return () => pulseAnim.kill();
  }, [size]);

  return (
    <div className="flex flex-col items-center justify-center relative">
      <svg width={svgSize} height={center + config.stroke} viewBox={`0 0 ${svgSize} ${center + config.stroke}`}>
        <defs>
          <linearGradient id="dataGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="var(--primary-blue)" />
            <stop offset="100%" stopColor="var(--cyan)" />
          </linearGradient>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Background Track */}
        <path
          d={`M ${config.stroke * 2} ${center} A ${config.radius} ${config.radius} 0 0 1 ${svgSize - config.stroke * 2} ${center}`}
          fill="none"
          stroke="var(--border)"
          strokeWidth={config.stroke}
          strokeLinecap="round"
        />

        {/* Glow Arc */}
        <path
          ref={glowRef}
          d={`M ${config.stroke * 2} ${center} A ${config.radius} ${config.radius} 0 0 1 ${svgSize - config.stroke * 2} ${center}`}
          fill="none"
          stroke={stateConfig.color}
          strokeWidth={config.stroke * 1.5}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          opacity={0.3}
          filter="url(#glow)"
        />

        {/* Active Arc */}
        <path
          ref={arcRef}
          d={`M ${config.stroke * 2} ${center} A ${config.radius} ${config.radius} 0 0 1 ${svgSize - config.stroke * 2} ${center}`}
          fill="none"
          stroke="url(#dataGrad)"
          strokeWidth={config.stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
        />
      </svg>

      {/* Center Value */}
      {size !== 'micro' && (
        <div className="absolute flex flex-col items-center bottom-6" style={{ bottom: size === 'full' ? '24px' : '12px' }}>
          <span 
            ref={numberRef} 
            className="mono gradient-text font-black"
            style={{ fontSize: `${config.fontSize}px`, lineHeight: 1 }}
          >
            0
          </span>
          {size === 'full' && <span className="label mt-1">Fatigue Index</span>}
        </div>
      )}

      {/* State Badge (Only for full size) */}
      {size === 'full' && (
        <div 
          ref={badgeRef}
          className="mt-4 px-4 py-1 rounded-full flex items-center gap-2 border border-opacity-30"
          style={{ 
            backgroundColor: `${stateConfig.color}15`, 
            borderColor: stateConfig.color,
            color: stateConfig.color 
          }}
        >
          <span className="text-sm">{stateConfig.icon}</span>
          <span className="label tracking-wider" style={{ color: stateConfig.color }}>
            {stateConfig.label}
          </span>
        </div>
      )}
    </div>
  );
}