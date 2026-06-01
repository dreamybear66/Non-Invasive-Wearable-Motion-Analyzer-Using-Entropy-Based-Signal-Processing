import React, { useRef, useState, useEffect } from 'react';
import gsap from 'full/gsap';
import { Info, AlertTriangle, AlertOctagon, X } from 'lucide-react';
import { useGSAP } from '../../hooks/useGSAP';

export default function FatigueAlertBanner({ 
  id,
  severity = 'INFO', // INFO, WARNING, DANGER
  title,
  message,
  timestamp,
  fisValue,
  onDismiss 
}) {
  const bannerRef = useRef(null);
  const [isVisible, setIsVisible] = useState(true);

  // Configuration mapping based on UI/UX specs
  const config = {
    INFO: {
      bgColor: '#06b6d415',
      borderColor: 'var(--cyan)',
      icon: <Info size={24} color="var(--cyan)" />,
      textColor: 'var(--cyan)',
      autoDismiss: 8000
    },
    WARNING: {
      bgColor: '#eab30815',
      borderColor: 'var(--fatigue-early)',
      icon: <AlertTriangle size={24} color="var(--fatigue-early)" />,
      textColor: 'var(--fatigue-early)',
      autoDismiss: 15000
    },
    DANGER: {
      bgColor: '#ef444415',
      borderColor: 'var(--fatigue-high)',
      icon: <AlertOctagon size={24} color="var(--fatigue-high)" />,
      textColor: 'var(--fatigue-high)',
      autoDismiss: null, // Requires manual dismiss
      containerClass: 'danger-alert' // Links to animations.css pulse
    }
  }[severity];

  useGSAP(() => {
    // Slide down entrance
    gsap.from(bannerRef.current, {
      y: -80,
      opacity: 0,
      duration: 0.5,
      ease: 'expo.out'
    });
  }, []);

  const handleDismiss = () => {
    gsap.to(bannerRef.current, {
      x: -100, // Slide out left
      opacity: 0,
      height: 0,
      marginTop: 0,
      marginBottom: 0,
      paddingTop: 0,
      paddingBottom: 0,
      duration: 0.3,
      ease: 'power2.in',
      onComplete: () => {
        setIsVisible(false);
        if (onDismiss) onDismiss(id);
      }
    });
  };

  // Auto-dismiss timer
  useEffect(() => {
    if (config.autoDismiss) {
      const timer = setTimeout(() => {
        handleDismiss();
      }, config.autoDismiss);
      return () => clearTimeout(timer);
    }
  }, [config.autoDismiss]);

  if (!isVisible) return null;

  return (
    <div 
      ref={bannerRef}
      className={`relative flex items-start gap-4 p-4 rounded-lg mb-4 glass-panel overflow-hidden ${config.containerClass || ''}`}
      style={{
        backgroundColor: config.bgColor,
        borderLeft: `4px solid ${config.borderColor}`
      }}
    >
      <div className="flex-shrink-0 mt-1">
        {config.icon}
      </div>
      
      <div className="flex-grow">
        <div className="flex justify-between items-start">
          <h3 className="text-sm font-bold" style={{ color: config.textColor }}>{title}</h3>
          <button 
            onClick={handleDismiss}
            className="text-gray-400 hover:text-white transition-colors p-1"
          >
            <X size={16} />
          </button>
        </div>
        
        <p className="text-sm text-gray-300 mt-1">{message}</p>
        
        <div className="flex items-center gap-4 mt-3 label">
          <span className="mono">{timestamp}</span>
          <span className="flex items-center gap-1">
            <span className="text-gray-500">FIS:</span>
            <span className="mono" style={{ color: config.textColor }}>{fisValue.toFixed(1)}</span>
          </span>
        </div>
      </div>
    </div>
  );
}
