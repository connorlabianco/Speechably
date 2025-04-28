import React from 'react';
import '../../styles/components/layout/Loading.css';

function Loading({ message = 'Processing...' }) {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p className="loading-message">{message}</p>
    </div>
  );
}

export default Loading;