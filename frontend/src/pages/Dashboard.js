import React from 'react';

const Dashboard = () => {
  return (
    <div style={{marginLeft: '250px', padding: '20px'}}>
      <h1>Overview</h1>
      <div style={{display: 'flex', gap: '20px'}}>
        <div style={{background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)'}}>
          <h3>Users</h3>
          <p>1,234</p>
        </div>
        <div style={{background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)'}}>
          <h3>Projects</h3>
          <p>56</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
