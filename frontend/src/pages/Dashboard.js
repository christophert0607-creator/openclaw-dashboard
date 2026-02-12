import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [status, setStatus] = useState('');
  const [sessions, setSessions] = useState([]);
  const API_URL = 'http://localhost:3001';

  useEffect(() => {
    fetch(`${API_URL}/api/session_status`)
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(err => console.error(err));

    fetch(`${API_URL}/api/sessions_list`)
      .then(res => res.json())
      .then(data => {
        if (data.sessions) {
          setSessions(data.sessions.split('\n').filter(s => s.trim()));
        }
      })
      .catch(err => console.error(err));
  }, [API_URL]);

  return (
    <div style={{marginLeft: '250px', padding: '20px'}}>
      <h1>Overview</h1>
      <div style={{display: 'flex', gap: '20px'}}>
        <div style={{background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', flex: 1}}>
          <h3>Session Status</h3>
          <pre style={{whiteSpace: 'pre-wrap', fontSize: '12px'}}>{status}</pre>
        </div>
        <div style={{background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', flex: 1}}>
          <h3>Sessions</h3>
          <ul style={{listStyle: 'none', padding: 0}}>
            {sessions.map((s, i) => (
              <li key={i} style={{marginBottom: '5px'}}>{s}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
