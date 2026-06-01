import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, Search, LayoutDashboard, Activity, Users, FileText, Settings, Menu } from 'lucide-react';
import SessionStatusCard from '../components/SessionStatusCard';
import AthleteAvatarChip from '../components/AthleteAvatarChip';
import FatigueAlertBanner from '../components/FatigueAlertBanner';
import LiveBadge from '../components/LiveBadge';

// Mock Data for Demo
const MOCK_SESSIONS = [
  { id: '1', athleteName: 'Marcus Johnson', sport: 'Basketball', status: 'ACTIVE', fisValue: 82, duration: '01:14:22', state: 'HIGH_FATIGUE' },
  { id: '2', athleteName: 'Sarah Williams', sport: 'Track & Field', status: 'ACTIVE', fisValue: 45, duration: '00:32:10', state: 'MODERATE_FATIGUE' },
  { id: '3', athleteName: 'David Chen', sport: 'Soccer', status: 'ACTIVE', fisValue: 28, duration: '00:45:05', state: 'EARLY_FATIGUE' },
  { id: '4', athleteName: 'Elena Rodriguez', sport: 'Tennis', status: 'PAUSED', fisValue: 18, duration: '01:05:00', state: 'NORMAL' },
];

const MOCK_ALERTS = [
  { id: 'a1', severity: 'DANGER', title: 'Critical Fatigue Detected', message: 'Marcus Johnson exceeded FIS 80 threshold.', timestamp: '14:22:10', fisValue: 82 },
  { id: 'a2', severity: 'WARNING', title: 'Moderate Fatigue', message: 'Sarah Williams showing irregular ApEn patterns.', timestamp: '14:15:00', fisValue: 45 }
];

export default function Dashboard() {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState(MOCK_SESSIONS);
  const [alerts, setAlerts] = useState(MOCK_ALERTS);

  // Auto-sort sessions by FIS descending
  useEffect(() => {
    setSessions(prev => [...prev].sort((a, b) => b.fisValue - a.fisValue));
  }, []);

  const handleDismissAlert = (id) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  return (
    <div className="flex h-screen w-full bg-[#050912] overflow-hidden text-white">
      
      {/* Sidebar Navigation */}
      <div className="w-16 lg:w-64 bg-[#0d1424] border-r border-[#1a2840] flex flex-col justify-between py-6 transition-all duration-300">
        <div>
          <div className="px-4 lg:px-6 mb-10 flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center font-bold">
              EL
            </div>
            <span className="font-bold hidden lg:block">Sports EL</span>
          </div>

          <nav className="flex flex-col gap-2 px-2 lg:px-4">
            <button className="flex items-center gap-3 px-3 py-2 rounded-lg bg-[#111c30] text-blue-500 border-l-2 border-blue-500 w-full text-left">
              <LayoutDashboard size={20} />
              <span className="hidden lg:block font-medium">Dashboard</span>
            </button>
            <button onClick={() => navigate('/sessions/1')} className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-[#111c30] text-gray-400 hover:text-white transition-colors w-full text-left">
              <div className="flex items-center gap-3">
                <Activity size={20} />
                <span className="hidden lg:block font-medium">Live Sessions</span>
              </div>
              <div className="w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center text-[10px] text-white font-bold hidden lg:flex">3</div>
            </button>
            <button className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-[#111c30] text-gray-400 hover:text-white transition-colors w-full text-left">
              <Users size={20} />
              <span className="hidden lg:block font-medium">Athletes</span>
            </button>
            <button className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-[#111c30] text-gray-400 hover:text-white transition-colors w-full text-left">
              <FileText size={20} />
              <span className="hidden lg:block font-medium">Reports</span>
            </button>
          </nav>
        </div>

        <div className="px-2 lg:px-4">
          <button className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-[#111c30] text-gray-400 hover:text-white transition-colors w-full text-left">
            <Settings size={20} />
            <span className="hidden lg:block font-medium">Settings</span>
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        
        {/* Top Header */}
        <header className="h-20 border-b border-[#1a2840] flex items-center justify-between px-8 bg-[#050912]">
          <h1 className="text-2xl font-bold">Team Overview</h1>
          <div className="flex items-center gap-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
              <input type="text" placeholder="Search athletes..." className="bg-[#111c30] border border-[#1a2840] rounded-full pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-blue-500 transition-colors w-64" />
            </div>
            <button className="relative text-gray-400 hover:text-white transition-colors">
              <Bell size={20} />
              {alerts.length > 0 && <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-[#050912]"></span>}
            </button>
            <div className="flex items-center gap-3 pl-4 border-l border-[#1a2840]">
              <div className="w-9 h-9 rounded-full bg-blue-500 flex items-center justify-center font-bold text-sm">
                CO
              </div>
            </div>
          </div>
        </header>

        {/* Scrollable Dashboard */}
        <div className="flex-1 overflow-y-auto p-8">
          
          {/* Active Alerts Area */}
          <div className="w-full max-w-5xl mb-8">
            {alerts.map(alert => (
              <FatigueAlertBanner 
                key={alert.id}
                id={alert.id}
                severity={alert.severity}
                title={alert.title}
                message={alert.message}
                timestamp={alert.timestamp}
                fisValue={alert.fisValue}
                onDismiss={handleDismissAlert}
              />
            ))}
          </div>

          {/* Stats Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 max-w-5xl">
            <div className="card flex flex-col gap-2">
              <span className="label">Active Sessions</span>
              <div className="flex items-end gap-3">
                <span className="text-4xl font-black font-mono">3</span>
                <div className="mb-1"><LiveBadge /></div>
              </div>
            </div>
            <div className="card flex flex-col gap-2">
              <span className="label">Athletes Monitored Today</span>
              <div className="flex items-end gap-3">
                <span className="text-4xl font-black font-mono">12</span>
              </div>
            </div>
            <div className="card flex flex-col gap-2">
              <span className="label">Critical Events</span>
              <div className="flex items-end gap-3">
                <span className="text-4xl font-black font-mono text-red-500">1</span>
              </div>
            </div>
          </div>

          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            Live Monitoring Grid
            <span className="px-2 py-0.5 rounded bg-[#111c30] text-xs font-mono text-gray-400 border border-[#1a2840]">Sorted by FIS</span>
          </h2>

          {/* Live Sessions Grid */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 max-w-5xl">
            {sessions.map(session => (
              <SessionStatusCard 
                key={session.id}
                athleteName={session.athleteName}
                sport={session.sport}
                status={session.status}
                fisValue={session.fisValue}
                duration={session.duration}
                onClick={() => navigate(`/sessions/${session.id}`)}
              />
            ))}
          </div>

        </div>
      </div>
    </div>
  );
}