import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import LiveSession from './pages/LiveSession';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/sessions/:id" element={<LiveSession />} />
      
      {/* Placeholders for future pages */}
      <Route path="/athletes" element={<div className="p-8 text-white">Athletes Page Stub</div>} />
      <Route path="/reports" element={<div className="p-8 text-white">Reports Page Stub</div>} />
      <Route path="/settings" element={<div className="p-8 text-white">Settings Page Stub</div>} />
    </Routes>
  );
}

export default App;
