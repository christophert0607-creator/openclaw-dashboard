import React from 'react';

const Sidebar = ({ activePage, setActivePage }) => {
  return (
    <div className="sidebar">
      <h2>OpenClaw Dashboard</h2>
      <ul>
        <li onClick={() => setActivePage('dashboard')} className={activePage === 'dashboard' ? 'active' : ''}>
          Dashboard
        </li>
        <li onClick={() => setActivePage('agents')} className={activePage === 'agents' ? 'active' : ''}>
          Agents
        </li>
        <li onClick={() => setActivePage('tasks')} className={activePage === 'tasks' ? 'active' : ''}>
          Tasks
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
