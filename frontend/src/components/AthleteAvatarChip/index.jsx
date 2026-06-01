import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import gsap from 'full/gsap';

export default function AthleteAvatarChip({ 
  id, 
  name, 
  sport, 
  initials, 
  state = 'NORMAL',
  isActive = false
}) {
  const navigate = useNavigate();
  const cardRef = useRef(null);
  const [isHovered, setIsHovered] = useState(false);

  const stateColors = {
    NORMAL: 'var(--fatigue-normal)',
    EARLY_FATIGUE: 'var(--fatigue-early)',
    MODERATE_FATIGUE: 'var(--fatigue-moderate)',
    HIGH_FATIGUE: 'var(--fatigue-high)'
  };
  const color = stateColors[state] || stateColors.NORMAL;

  const handleMouseEnter = () => {
    setIsHovered(true);
    gsap.to(cardRef.current, {
      width: 240,
      duration: 0.3,
      ease: 'back.out(1.7)'
    });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    gsap.to(cardRef.current, {
      width: 60,
      duration: 0.2,
      ease: 'power2.in'
    });
  };

  return (
    <div 
      ref={cardRef}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={() => navigate(`/athletes/${id}`)}
      className="bg-[#111c30] rounded-full flex items-center p-1 relative cursor-pointer shadow-lg hover:bg-[#1a2840] transition-colors overflow-hidden"
      style={{ width: 60, height: 60 }}
    >
      <div className="w-[52px] h-[52px] rounded-full bg-[#1a2840] flex items-center justify-center font-bold text-white shrink-0 relative z-10">
        {initials}
        <div 
          className={`absolute top-0 right-0 w-3 h-3 rounded-full border-2 border-[#111c30] ${isActive ? 'live-pulse' : ''}`}
          style={{ backgroundColor: color }}
        />
      </div>
      
      <div className="flex flex-col ml-3 whitespace-nowrap opacity-0 transition-opacity duration-300" style={{ opacity: isHovered ? 1 : 0 }}>
        <span className="font-bold text-sm text-white">{name}</span>
        <span className="text-xs text-gray-400">{sport}</span>
      </div>
    </div>
  );
}
