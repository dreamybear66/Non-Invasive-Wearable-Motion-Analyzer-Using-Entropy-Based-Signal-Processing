import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

// Custom Tooltip with glassmorphism style
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="glass-panel p-3 border border-[#1a2840] shadow-xl">
        <p className="label mb-2 text-gray-400">{label}</p>
        <div className="flex flex-col gap-1">
          {payload.map((entry, index) => (
            <div key={`item-${index}`} className="flex items-center gap-2">
              <div 
                className="w-2 h-2 rounded-full" 
                style={{ backgroundColor: entry.color }}
              />
              <span className="text-gray-300 text-sm font-medium w-16">{entry.name}:</span>
              <span className="mono text-white text-sm font-bold">{Number(entry.value).toFixed(2)}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

export default function EntropyChart({ data, threshold = 1.0 }) {
  return (
    <div className="w-full h-72 relative">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorApEn" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorSampEn" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
            </linearGradient>
          </defs>
          
          <XAxis 
            dataKey="time" 
            tick={{ fill: '#475569', fontSize: 11, fontFamily: 'JetBrains Mono' }}
            stroke="#1a2840"
            tickMargin={10}
            minTickGap={30}
          />
          <YAxis 
            domain={['auto', 'auto']}
            tick={{ fill: '#475569', fontSize: 11, fontFamily: 'JetBrains Mono' }}
            stroke="#1a2840"
            tickFormatter={(val) => val.toFixed(1)}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#3b82f6', strokeWidth: 1, strokeDasharray: '4 4' }} />
          
          {/* Fatigue Threshold Line */}
          <ReferenceLine 
            y={threshold} 
            stroke="#ef4444" 
            strokeDasharray="3 3" 
            opacity={0.5} 
            label={{ position: 'insideTopLeft', value: 'Fatigue Threshold', fill: '#ef4444', fontSize: 10, opacity: 0.8 }} 
          />
          
          <Area 
            type="monotone" 
            dataKey="apen" 
            name="ApEn"
            stroke="#3b82f6" 
            strokeWidth={2.5}
            fillOpacity={1} 
            fill="url(#colorApEn)" 
            isAnimationActive={false} // Disable recharts animation to prevent lag on streaming
          />
          <Area 
            type="monotone" 
            dataKey="sampen" 
            name="SampEn"
            stroke="#8b5cf6" 
            strokeWidth={2.5}
            fillOpacity={1} 
            fill="url(#colorSampEn)" 
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}