import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import EmotionTimeline from '../components/EmotionTimeline';
import TranscriptView from '../components/TranscriptView';
import InsightPanel from '../components/InsightPanel';
import CoachChat from '../components/CoachChat';
import TabPanel from '../components/layout/TabPanel';
import '../styles/pages/Analysis.css';

function Analysis({ analysisData }) {
  const [activeTab, setActiveTab] = useState(0);
  const navigate = useNavigate();

  // Redirect to home if no analysis data
  useEffect(() => {
    if (!analysisData) {
      navigate('/');
    }
  }, [analysisData, navigate]);

  if (!analysisData) {
    return <div className="loading">Loading...</div>;
  }

  const handleTabChange = (newValue) => {
    setActiveTab(newValue);
  };

  const tabs = [
    { label: "📊 Analysis", icon: "chart-bar" },
    { label: "🧠 Insights", icon: "brain" },
    { label: "💬 AI Coach", icon: "message" }
  ];

  return (
    <div className="analysis-page">
      <h1>Speech Analysis Results</h1>
      
      <TabPanel 
        tabs={tabs} 
        activeTab={activeTab} 
        onChange={handleTabChange}
      >
        {/* Tab 1: Analysis */}
        {activeTab === 0 && (
          <div className="analysis-tab">
            <div className="analysis-grid">
              <div className="analysis-section timeline-section">
                <h2>Emotion & Speaking Rate Timeline</h2>
                <EmotionTimeline 
                  emotionSegments={analysisData.emotion_segments}
                  wpsData={analysisData.wps_data}
                />
              </div>

              <div className="analysis-section transcript-section">
                <h2>Transcript</h2>
                <TranscriptView 
                  transcriptionData={analysisData.transcription_data}
                />
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Insights */}
        {activeTab === 1 && (
          <div className="insights-tab">
            <InsightPanel 
              geminiAnalysis={analysisData.gemini_analysis}
              emotionMetrics={analysisData.emotion_metrics}
              speechClarity={analysisData.speech_clarity}
            />
          </div>
        )}

        {/* Tab 3: AI Coach */}
        {activeTab === 2 && (
          <div className="coach-tab">
            <CoachChat emotionSegments={analysisData.emotion_segments} />
          </div>
        )}
      </TabPanel>
    </div>
  );
}

export default Analysis;