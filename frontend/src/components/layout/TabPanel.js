import React from 'react';
import '../../styles/components/layout/TabPanel.css';

function TabPanel({ tabs, activeTab, onChange, children }) {
  return (
    <div className="tab-panel">
      <div className="tab-buttons">
        {tabs.map((tab, index) => (
          <button
            key={index}
            className={`tab-button ${activeTab === index ? 'active' : ''}`}
            onClick={() => onChange(index)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="tab-content">
        {children}
      </div>
    </div>
  );
}

export default TabPanel;