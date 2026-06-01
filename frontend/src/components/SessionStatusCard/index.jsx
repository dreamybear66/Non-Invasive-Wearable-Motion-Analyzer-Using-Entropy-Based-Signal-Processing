import React from 'react';
import { Activity, Pause, CheckCircle, AlertOctagon } from 'lucide-react';
import FatigueGauge from '../FatigueGauge';
import LiveBadge from '../LiveBadge';

export default function SessionStatusCard({ 
  athleteName, 
  sport, 
  status, // ACTIVE, PAUSED, COMPLETED, INTERRUPTED
  fisValue, 
  duration,
  onClick 
}) {
  
  const config = {
    ACTIVE: {
      border: 'var(--primary-blue)',
      icon: <Activity size={36} color="var(--primary-blue)" />,
      showLive: true
    },
    PAUSED: {
      border: 'var(--fatigue-early)',
      icon: <Pause size={36} color="var(--fatigue-early)" />,
      showLive: false
    },
    COMPLETED: {
      border: 'var(--text-muted)',
      icon: <CheckCircle size={36} color="var(--text-muted)" />,
      showLive: false
    },
    INTERRUPTED: {
      border: 'var(--fatigue-high)',
      icon: <AlertOctagon size={36} color="var(--fatigue-high)" />,
      showLive: false
    }
  }[status] || config.COMPLETED;

  return (
    <div 
      className="card flex items-center justify-between cursor-pointer w-full"
      style={{ borderLeft: `4px solid ${config.border}` }}
      onClick={onClick}
    >
      <div className="flex items-center gap-4">
        {config.icon}
        <div className="flex flex-col">
          <div className="flex items-center gap-3">
            <h3 className="font-bold">{athleteName}</h3>
            {config.showLive && <LiveBadge />}
            {status === 'PAUSED' && <span className="label !text-yellow-500 bg-yellow-500/10 px-2 py-0.5 rounded">PAUSED</span>}
          </div>
          <span className="text-gray-400 text-sm">{sport} • {duration}</span>
        </div>
      </div>
      
      <div className="flex items-center gap-6">
        <FatigueGauge fisValue={fisValue} size="mini" />
      </div>
    </div>
  );
}
