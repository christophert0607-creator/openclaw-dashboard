import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [sessions, setSessions] = useState([]);
  const [status, setStatus] = useState({});

  useEffect(() => {
    fetch('/api/session_status')
      .then(res => res.json())
      .then(data => setStatus(data));

    fetch('/api/sessions_list')
      .then(res => res.json())
      .then(data => setSessions(data.sessions || []));
  }, []);

  const chartData = {
    labels: sessions.slice(0, 5).map(s => s.key.slice(-10)),
    datasets: [{
      label: 'Token Usage',
      data: sessions.slice(0, 5).map(s => (s.tokens ? s.tokens.in + s.tokens.out : 0)),
      backgroundColor: 'rgba(75,192,192,0.6)',
    }],
  };

  return (
    <div>
      <h1>Overview</h1>
      <div className="cards">
        <div className="card">
          <h3>Active Sessions</h3>
          <p>{sessions.length}</p>
        </div>
        <div className="card">
          <h3>Model</h3>
          <p>{status.model || 'N/A'}</p>
        </div>
        <div className="card">
          <h3>Context Used</h3>
          <p>{status.contextUsed || 'N/A'}</p>
        </div>
      </div>
      <div className="chart">
        <h3>Sessions Token Usage</h3>
        <Bar data={chartData} />
      </div>
    </div>
  );
};

export default Dashboard;
