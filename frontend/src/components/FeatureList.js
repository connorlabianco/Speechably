import React from 'react';
import Card from './layout/Card';
import '../styles/components/FeatureList.css';

function FeatureList() {
  const features = [
    {
      icon: '🎥',
      title: 'Video Upload',
      description: 'Upload a video of yourself speaking to get personalized feedback.'
    },
    {
      icon: '🔊',
      title: 'Speech Emotion Recognition',
      description: 'Detects tone, mood, and speaking style using advanced AI models.'
    },
    {
      icon: '📊',
      title: 'Speaking Rate Analysis',
      description: 'Measures your words-per-second rate and identifies optimal pacing.'
    },
    {
      icon: '🧠',
      title: 'AI-Powered Feedback',
      description: 'Get personalized insights and tips to improve your delivery.'
    },
    {
      icon: '💬',
      title: 'AI Speech Coach',
      description: 'Chat with an AI coach for specific advice on improving your speech.'
    },
    {
      icon: '📈',
      title: 'Interactive Visualizations',
      description: 'View detailed timelines of your emotion patterns and speaking rate.'
    }
  ];

  return (
    <div className="feature-list">
      {features.map((feature, index) => (
        <Card key={index} className="feature-card">
          <div className="feature-icon">{feature.icon}</div>
          <h3 className="feature-title">{feature.title}</h3>
          <p className="feature-description">{feature.description}</p>
        </Card>
      ))}
    </div>
  );
}

export default FeatureList;