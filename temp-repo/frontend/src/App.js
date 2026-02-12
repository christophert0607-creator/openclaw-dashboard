import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  const [activePage, setActivePage] = useState('dashboard');

  return (
    <div className="App">
      <Sidebar activePage={activePage} setActivePage={setActivePage} />
      <main className="main-content">
        {activePage === 'dashboard' && <Dashboard />}
        {/* Add other pages */}
      </main>
    </div>
  );
}

export default App;
