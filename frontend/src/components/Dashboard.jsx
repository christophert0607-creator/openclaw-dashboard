import React, { useState } from 'react';
import Badge from './Badge';
import ProgressBar from './ProgressBar';

const Dashboard = () => {
  const [tasks, setTasks] = useState([
    { id: 1, name: 'Design Wireframe', completed: true },
    { id: 2, name: 'Build Frontend', completed: true },
    { id: 3, name: 'Develop Backend', completed: true },
    { id: 4, name: 'Integrate APIs', completed: true },
    { id: 5, name: 'Test & Deploy', completed: false },
  ]);

  const completedTasks = tasks.filter(task => task.completed).length;
  const totalTasks = tasks.length;
  const progress = (completedTasks / totalTasks) * 100;

  const badges = [
    { type: 'achievement', text: 'Wireframe Master' },
    { type: 'achievement', text: 'Code Ninja' },
    { type: 'progress', text: `Project Progress: ${Math.round(progress)}%` },
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">OpenClaw Dashboard</h1>
      
      {/* Gamification Section */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Achievements & Progress</h2>
        <div className="flex flex-wrap gap-2 mb-4">
          {badges.map((badge, index) => (
            <Badge key={index} type={badge.type} text={badge.text} />
          ))}
        </div>
        
        <ProgressBar progress={progress} label="Overall Project Completion" color="green" />
      </div>

      {/* Tasks List */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Task Tracker</h2>
        <ul className="space-y-2">
          {tasks.map(task => (
            <li key={task.id} className={`p-2 rounded ${task.completed ? 'bg-green-100' : 'bg-gray-100'}`}>
              {task.name} - {task.completed ? 'Completed' : 'Pending'}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
