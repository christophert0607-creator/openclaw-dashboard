import React from 'react';

const ProgressBar = ({ progress, label, color = 'blue' }) => {
  const barStyles = {
    width: '100%',
    height: '20px',
    backgroundColor: '#e5e7eb',
    borderRadius: '10px',
    overflow: 'hidden',
  };

  const fillStyles = {
    width: `${progress}%`,
    height: '100%',
    backgroundColor: color === 'green' ? '#10b981' : '#3b82f6',
    transition: 'width 0.3s ease',
  };

  return (
    <div className="w-full">
      <div className="flex justify-between mb-1">
        <span>{label}</span>
        <span>{progress}%</span>
      </div>
      <div style={barStyles}>
        <div style={fillStyles}></div>
      </div>
    </div>
  );
};

export default ProgressBar;
