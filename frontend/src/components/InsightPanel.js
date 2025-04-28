import React from 'react';
import Card from './layout/Card';
import '../styles/components/InsightPanel.css';

function InsightPanel({ geminiAnalysis, emotionMetrics, speechClarity }) {
  // Ensure we have valid data
  const hasGeminiAnalysis = geminiAnalysis && Object.keys(geminiAnalysis).length > 0;
  const hasEmotionMetrics = emotionMetrics && Object.keys(emotionMetrics).length > 0;
  const hasSpeechClarity = speechClarity && Object.keys(speechClarity).length > 0;
  
  if (!hasGeminiAnalysis && !hasEmotionMetrics) {
    return (
      <div className="insights-placeholder">
        <p>No insight data available.</p>
      </div>
    );
  }
  
  return (
    <div className="insight-panel">
      {/* Summary Section */}
      {hasGeminiAnalysis && (
        <Card className="summary-card">
          <h3>Summary</h3>
          <p className="summary-text">{geminiAnalysis.summary}</p>
        </Card>
      )}
      
      {/* Strengths and Improvement Areas */}
      <div className="insights-grid">
        {hasGeminiAnalysis && (
          <>
            <Card className="strengths-card">
              <h3>Strengths</h3>
              <ul className="strength-list">
                {geminiAnalysis.strengths.map((strength, index) => (
                  <li key={index} className="strength-item">
                    <span className="strength-icon">🌟</span>
                    <span className="strength-text">{strength}</span>
                  </li>
                ))}
              </ul>
            </Card>
            
            <Card className="improvement-card">
              <h3>Areas for Improvement</h3>
              <ul className="improvement-list">
                {geminiAnalysis.improvement_areas.map((area, index) => (
                  <li key={index} className="improvement-item">
                    <span className="improvement-icon">🔍</span>
                    <span className="improvement-text">{area}</span>
                  </li>
                ))}
              </ul>
            </Card>
          </>
        )}
      </div>
      
      {/* Speech Metrics */}
      <div className="metrics-section">
        {hasSpeechClarity && (
          <Card className="metrics-card">
            <h3>Speech Metrics</h3>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-label">Average Speaking Rate</span>
                <span className="metric-value">
                  {speechClarity.avg_wps} WPS
                  <span className={`metric-indicator ${
                    speechClarity.avg_wps > 3.0 ? 'warning' : 
                    speechClarity.avg_wps < 1.5 ? 'caution' : 'good'
                  }`}>
                    {speechClarity.avg_wps > 3.0 ? '(Too Fast)' : 
                     speechClarity.avg_wps < 1.5 ? '(Too Slow)' : '(Good)'}
                  </span>
                </span>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Speaking Rate Variation</span>
                <span className="metric-value">
                  {speechClarity.wps_variation} WPS
                  <span className={`metric-indicator ${
                    speechClarity.wps_variation < 0.5 ? 'caution' :
                    speechClarity.wps_variation > 2.0 ? 'warning' : 'good'
                  }`}>
                    {speechClarity.wps_variation < 0.5 ? '(Low Variation)' : 
                     speechClarity.wps_variation > 2.0 ? '(High Variation)' : '(Good)'}
                  </span>
                </span>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Clarity Score</span>
                <span className="metric-value">
                  {speechClarity.clarity_score}/100
                  <span className={`metric-indicator ${
                    speechClarity.clarity_score < 50 ? 'caution' :
                    speechClarity.clarity_score > 80 ? 'good' : 'neutral'
                  }`}>
                    {speechClarity.clarity_score < 50 ? '(Needs Improvement)' : 
                     speechClarity.clarity_score > 80 ? '(Excellent)' : '(Good)'}
                  </span>
                </span>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Total Words</span>
                <span className="metric-value">{speechClarity.total_words}</span>
              </div>
            </div>
          </Card>
        )}
        
        {hasEmotionMetrics && (
          <Card className="emotion-metrics-card">
            <h3>Emotion Metrics</h3>
            <div className="metrics-grid">
              <div className="metric-item">
                <span className="metric-label">Dominant Emotion</span>
                <span className="metric-value">{emotionMetrics.main_emotion}</span>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Emotional Range</span>
                <span className="metric-value">
                  {emotionMetrics.emotion_diversity} emotions
                  <span className={`metric-indicator ${
                    emotionMetrics.emotion_diversity < 2 ? 'caution' :
                    emotionMetrics.emotion_diversity > 4 ? 'good' : 'neutral'
                  }`}>
                    {emotionMetrics.emotion_diversity < 2 ? '(Limited)' : 
                     emotionMetrics.emotion_diversity > 4 ? '(Diverse)' : '(Moderate)'}
                  </span>
                </span>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Emotion Consistency</span>
                <span className="metric-value">
                  {emotionMetrics.main_emotion_percentage}%
                  <span className={`metric-indicator ${
                    emotionMetrics.main_emotion_percentage > 80 ? 'caution' :
                    emotionMetrics.main_emotion_percentage < 40 ? 'warning' : 'good'
                  }`}>
                    {emotionMetrics.main_emotion_percentage > 80 ? '(Very Consistent)' : 
                     emotionMetrics.main_emotion_percentage < 40 ? '(Highly Variable)' : '(Balanced)'}
                  </span>
                </span>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Emotion Transitions</span>
                <span className="metric-value">
                  {emotionMetrics.transitions ? emotionMetrics.transitions.length : 0}
                </span>
              </div>
            </div>
          </Card>
        )}
      </div>
      
      {/* Coaching Tips */}
      {hasGeminiAnalysis && (
        <Card className="coaching-tips-card">
          <h3>Coaching Tips</h3>
          <div className="coaching-tips">
            {geminiAnalysis.coaching_tips.map((tip, index) => (
              <div key={index} className="coaching-tip">
                <span className="tip-number">{index + 1}</span>
                <p className="tip-text">{tip}</p>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

export default InsightPanel;