import React from 'react';
<<<<<<< HEAD
import Dashboard from './components/Dashboard';
import './App.css'; // Assume basic Tailwind or CSS setup
=======
import './App.css';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
>>>>>>> 1c3e546721c364cf4a9fb99da499236a1f53926a

function App() {
  return (
    <div className="App">
<<<<<<< HEAD
      <Dashboard />
=======
      <Sidebar />
      <main>
        <Dashboard />
      </main>
>>>>>>> 1c3e546721c364cf4a9fb99da499236a1f53926a
    </div>
  );
}

export default App;
