import React from 'react';

const Badge = ({ type, text, icon }) => {
  const badgeStyles = {
    achievement: 'bg-green-500 text-white px-3 py-1 rounded-full text-sm',
    progress: 'bg-blue-500 text-white px-3 py-1 rounded text-sm',
    warning: 'bg-yellow-500 text-white px-3 py-1 rounded text-sm',
  };

  const getIcon = () => {
    switch (type) {
      case 'achievement': return '🏆';
      case 'progress': return '📊';
      case 'warning': return '⚠️';
      default: return '🔹';
    }
  };

  return (
    <span className={badgeStyles[type] || badgeStyles.achievement}>
      {icon || getIcon()} {text}
    </span>
  );
};

export default Badge;
