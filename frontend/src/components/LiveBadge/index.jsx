import React from 'react';
import '../styles/animations.css';

export default function LiveBadge() {
  return (
    <div className="flex items-center gap-2 bg-[#22c55e15] border border-[#22c55e40] px-3 py-1 rounded-full">
      <div className="relative flex items-center justify-center w-2 h-2">
        {/* Pulsing ring */}
        <div className="absolute w-full h-full rounded-full bg-green-500 live-pulse"></div>
        {/* Solid center dot */}
        <div className="absolute w-2 h-2 bg-green-500 rounded-full"></div>
      </div>
      <span className="label !text-green-500 m-0">LIVE</span>
    </div>
  );
}