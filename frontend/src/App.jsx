import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import LiveSession from './pages/LiveSession';
import History from './pages/History';
import AthleteList from './pages/AthleteList';
import AthleteProfile from './pages/AthleteProfile';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/sessions/:id" element={<LiveSession />} />
        <Route path="/sessions/:id/history" element={<History />} />
        <Route path="/athletes" element={<AthleteList />} />
        <Route path="/athletes/:id" element={<AthleteProfile />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
