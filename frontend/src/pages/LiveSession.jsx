import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Pause, Square, Activity, Bell } from 'lucide-react';
import FatigueGauge from '../components/FatigueGauge';
import EntropyChart from '../components/EntropyChart';
import LiveBadge from '../components/LiveBadge';
import FatigueAlertBanner from '../components/FatigueAlertBanner';
import DataTable from '../components/DataTable';
import { useWebSocket } from '../hooks/useWebSocket';

// Initial synthetic mock data for the chart
const generateMockData = () => {
  const data = [];
  let time = new Date();
  time.setMinutes(time.getMinutes() - 5);
  for(let i=0; i<60; i++) {
    data.push({
      time: time.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      apen: 1.5 - (i * 0.005) + (Math.random() * 0.1),
      sampen: 1.4 - (i * 0.006) + (Math.random() * 0.1)
    });
    time.setSeconds(time.getSeconds() + 5);
  }
  return data;
};

export default function LiveSession() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [fis, setFis] = useState(24); // Start at early fatigue
  const [chartData, setChartData] = useState(generateMockData());
  const [alerts, setAlerts] = useState([]);
  const [segments, setSegments] = useState([]);

  // Connect to the WebSocket using our custom hook
  const { isConnected, lastMessage } = useWebSocket(id, (msg) => {
    // Process incoming WebSocket message
    if (msg.type === 'UPDATE') {
      setFis(msg.fis);
      setChartData(prev => {
        const newData = [...prev.slice(1), {
          time: new Date(msg.timestamp).toLocaleTimeString([], { hour12: false }),
          apen: msg.apen,
          sampen: msg.sampen
        }];
        return newData;
      });
      setSegments(prev => [{ time: msg.timestamp, apen: msg.apen, sampen: msg.sampen, fis: msg.fis, state: msg.state }, ...prev].slice(0, 10));
    } else if (msg.type === 'ALERT') {
      setAlerts(prev => [msg.alert, ...prev]);
    }
  });

  // Simulator effect: If no real websocket data arrives, simulate incoming data for the demo
  useEffect(() => {
    if (isConnected) return; // Don't simulate if actually connected

    const interval = setInterval(() => {
      setFis(prev => {
        const next = prev + (Math.random() * 2 - 0.5);
        
        // Trigger a fake alert if crossing a threshold
        if (prev < 65 && next >= 65) {
          setAlerts(a => [{
            id: Date.now(), severity: 'DANGER', title: 'Critical Fatigue Detected', 
            message: 'FIS crossed 65 threshold rapidly.', timestamp: new Date().toLocaleTimeString(), fisValue: next
          }, ...a]);
        }
        
        return Math.min(100, Math.max(0, next));
      });

      setChartData(prev => {
        const time = new Date().toLocaleTimeString([], { hour12: false });
        const last = prev[prev.length - 1];
        return [...prev.slice(1), {
          time,
          apen: last.apen - (Math.random() * 0.02 - 0.005),
          sampen: last.sampen - (Math.random() * 0.02 - 0.005)
        }];
      });
    }, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, [isConnected]);

  const columns = [
    { key: 'time', label: 'Time', sortable: false },
    { key: 'apen', label: 'ApEn', sortable: false, render: (v) => <span className="mono text-cyan-400">{v?.toFixed(3)}</span> },
    { key: 'sampen', label: 'SampEn', sortable: false, render: (v) => <span className="mono text-purple-400">{v?.toFixed(3)}</span> },
    { key: 'fis', label: 'FIS', sortable: false, render: (v) => <span className="mono text-white">{v?.toFixed(1)}</span> },
    { key: 'state', label: 'State', sortable: false }
  ];

  return (
    <div className="flex flex-col h-screen w-full bg-[#050912] overflow-hidden text-white">
      
      {/* Header */}
      <header className="h-16 border-b border-[#1a2840] flex items-center justify-between px-6 bg-[#0d1424] shrink-0 z-20">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-[#111c30] rounded-lg transition-colors">
            <ArrowLeft size={20} />
          </button>
          <div className="h-6 w-[1px] bg-[#1a2840]"></div>
          <div>
            <h2 className="font-bold leading-tight">Marcus Johnson</h2>
            <span className="text-xs text-gray-400 tracking-wide uppercase">Basketball • Session #{id}</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 mr-4 bg-[#111c30] px-3 py-1.5 rounded-lg border border-[#1a2840]">
            <Activity size={16} className={isConnected ? "text-green-500" : "text-gray-500"} />
            <span className="text-sm font-mono text-gray-300">
              {isConnected ? 'WS CONNECTED' : 'WS SIMULATED'}
            </span>
          </div>
          <button className="btn-secondary h-9">
            <Pause size={16} /> Pause
          </button>
          <button className="btn-primary bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 h-9">
            <Square size={16} fill="currentColor" /> End Session
          </button>
        </div>
      </header>

      {/* Main Content (2 Columns) */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Left Column - Hero Gauge (40%) */}
        <div className="w-[40%] border-r border-[#1a2840] flex flex-col justify-between p-8 relative bg-gradient-to-b from-[#0d1424] to-[#050912]">
          
          <div className="flex justify-between items-start">
            <LiveBadge />
            <div className="text-right">
              <span className="label block mb-1">Duration</span>
              <span className="mono text-2xl font-bold">01:14:22</span>
            </div>
          </div>

          <div className="flex-1 flex items-center justify-center -mt-10">
            <FatigueGauge fisValue={fis} size="full" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-[#111c30] p-4 rounded-xl border border-[#1a2840]">
              <span className="label block mb-2">Current ApEn</span>
              <span className="mono text-xl text-cyan-400 font-bold">{chartData[chartData.length-1]?.apen.toFixed(3)}</span>
            </div>
            <div className="bg-[#111c30] p-4 rounded-xl border border-[#1a2840]">
              <span className="label block mb-2">Current SampEn</span>
              <span className="mono text-xl text-purple-400 font-bold">{chartData[chartData.length-1]?.sampen.toFixed(3)}</span>
            </div>
          </div>
        </div>

        {/* Right Column - Charts & Data (60%) */}
        <div className="w-[60%] flex flex-col overflow-y-auto p-8 gap-8">
          
          {/* Alerts Area */}
          <div className="flex flex-col gap-4 empty:hidden">
            {alerts.map(alert => (
              <FatigueAlertBanner 
                key={alert.id}
                id={alert.id}
                severity={alert.severity}
                title={alert.title}
                message={alert.message}
                timestamp={alert.timestamp}
                fisValue={alert.fisValue}
                onDismiss={(id) => setAlerts(a => a.filter(x => x.id !== id))}
              />
            ))}
          </div>

          {/* Chart Section */}
          <div className="card w-full">
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-semibold flex items-center gap-2">
                <Activity size={18} className="text-blue-500" /> Entropy Trend
              </h3>
              <div className="flex gap-4 label">
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500"></span> ApEn</span>
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-purple-500"></span> SampEn</span>
              </div>
            </div>
            <EntropyChart data={chartData} threshold={1.0} />
          </div>

          {/* Table Section */}
          <div className="mt-4">
            <DataTable 
              columns={columns}
              data={segments.length ? segments : [
                { time: '14:22:10', apen: 1.205, sampen: 1.102, fis: 82.5, state: 'HIGH_FATIGUE' },
                { time: '14:22:05', apen: 1.220, sampen: 1.115, fis: 78.2, state: 'HIGH_FATIGUE' },
                { time: '14:22:00', apen: 1.245, sampen: 1.130, fis: 64.0, state: 'MODERATE_FATIGUE' },
              ]}
              isLoading={false}
            />
          </div>

        </div>
      </div>
    </div>
  );
}