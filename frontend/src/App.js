import React from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <div className="App">
      <Sidebar />
      <main>
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
