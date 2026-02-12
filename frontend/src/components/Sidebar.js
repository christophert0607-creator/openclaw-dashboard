import React from 'react';

const Sidebar = () => {
  return (
    <aside style={{width: '250px', background: '#f4f4f4', height: '100vh', position: 'fixed'}}>
      <h2>Dashboard</h2>
      <ul>
        <li>Overview</li>
        <li>Projects</li>
        <li>Team</li>
        <li>Settings</li>
      </ul>
    </aside>
  );
};

export default Sidebar;
