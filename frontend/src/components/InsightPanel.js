import React from 'react';
import Card from './layout/Card';
import '../styles/components/InsightPanel.css';

function InsightPanel({ geminiAnalysis, emotionMetrics, speechClarity }) {
  // Ensure we have valid data
  const hasGeminiAnalysis = geminiAnalysis && 
                          Object.keys(geminiAnalysis).length > 0 && 
                          geminiAnalysis.summary !== "Gemini analysis not available. Please check your API key configuration.";
  const hasEmotionMetrics = emotionMetrics && Object.keys(emotionMetrics).length > 0;
  const hasSpeechClarity = speechClarity && Object.keys(speechClarity).length > 0;
  
  // Check for API configuration error
  const hasApiError = geminiAnalysis && 
                     geminiAnalysis.summary && 
                     geminiAnalysis.summary.includes("API key configuration");
  
  if (!hasGeminiAnalysis && !hasEmotionMetrics) {
    return (
      <div className="insights-placeholder">
        <p>No insight data available.</p>
      </div>
    );
  }
  
  return (
    <div className="insight-panel">
      {/* API Error Message */}
      {hasApiError && (
        <Card className="error-card">
          <h3>AI Analysis Unavailable</h3>
          <div className="error-message">
            <p>The AI analysis service is currently unavailable. This could be due to:</p>
            <ul>
              <li>Missing or invalid Google Gemini API key</li>
              <li>Network connectivity issues</li>
              <li>Service disruption with the AI provider</li>
            </ul>
            <p>Basic metrics are still available below. To enable AI analysis:</p>
            <ol>
              <li>Check that you have a valid Google Gemini API key</li>
              <li>Make sure the API key is correctly set in your .env file</li>
              <li>Restart the server to apply any changes</li>
            </ol>
          </div>
        </Card>
      )}
      
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
                  {speechClarity.wps_variation?.toFixed(2) || "0.00"} WPS
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
                <span className="metric-value">{speechClarity.total_words || 0}</span>
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
                  {Array.isArray(emotionMetrics.transitions) ? emotionMetrics.transitions.length : 0}
                </span>
              </div>
            </div>
          </Card>
        )}
      </div>
      
      {/* Coaching Tips */}
      {hasGeminiAnalysis && geminiAnalysis.coaching_tips && geminiAnalysis.coaching_tips.length > 0 ? (
        <Card className="coaching-tips-card">
          <h3>Coaching Tips</h3>
          <div className="coaching-tips">
            {geminiAnalysis.coaching_tips.map((tip, index) => (
              <div key={index} className="coaching-tip">
                <span className="tip-number">{index + 1}</span>
                <p className="tip-text">
                  {tip && typeof tip === 'object'
                    ? tip.tip || JSON.stringify(tip)
                    : tip}
                </p>
              </div>
            ))}
          </div>
        </Card>
      ) : !hasApiError && (
        <Card className="coaching-tips-card">
          <h3>Coaching Tips</h3>
          <div className="coaching-tips">
            <div className="coaching-tip">
              <span className="tip-number">1</span>
              <p className="tip-text">Practice maintaining a consistent speaking rate between 2-3 words per second for optimal clarity.</p>
            </div>
            <div className="coaching-tip">
              <span className="tip-number">2</span>
              <p className="tip-text">Record yourself regularly and review your emotional patterns to develop greater emotional range.</p>
            </div>
            <div className="coaching-tip">
              <span className="tip-number">3</span>
              <p className="tip-text">Join a speaking club or group to get regular feedback on your delivery and presentation skills.</p>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}

export default InsightPanel;