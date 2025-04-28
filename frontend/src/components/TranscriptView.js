import React, { useState } from 'react';
import Card from './layout/Card';
import '../styles/components/TranscriptView.css';

function TranscriptView({ transcriptionData }) {
  const [viewMode, setViewMode] = useState('paragraph'); // 'paragraph', 'timeline'
  
  if (!transcriptionData || transcriptionData.length === 0) {
    return (
      <Card className="transcript-card">
        <div className="transcript-placeholder">
          <p>No transcription data available.</p>
        </div>
      </Card>
    );
  }
  
  // Sort segments by start time
  const sortedData = [...transcriptionData].sort((a, b) => a.start - b.start);
  
  // Format time helper function
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };
  
  // Format paragraph with speed indicators (bold for too fast, italic for too slow)
  const getParagraphText = () => {
    return sortedData.map((segment, index) => {
      const text = segment.text.trim();
      if (!text) return null;
      
      let formattedText;
      if (segment.wps > 3.0) {
        // Too fast - make bold
        formattedText = <strong key={index}>{text} </strong>;
      } else if (segment.wps < 1.0) {
        // Too slow - make italic
        formattedText = <em key={index}>{text} </em>;
      } else {
        // Normal speed - no formatting
        formattedText = <span key={index}>{text} </span>;
      }
      
      return formattedText;
    });
  };
  
  return (
    <Card className="transcript-card">
      <div className="transcript-header">
        <div className="view-mode-selector">
          <button 
            className={`view-mode-btn ${viewMode === 'paragraph' ? 'active' : ''}`}
            onClick={() => setViewMode('paragraph')}
          >
            Paragraph View
          </button>
          <button 
            className={`view-mode-btn ${viewMode === 'timeline' ? 'active' : ''}`}
            onClick={() => setViewMode('timeline')}
          >
            Timeline View
          </button>
        </div>
        
        {viewMode === 'paragraph' && (
          <div className="transcript-legend">
            <div className="legend-item">
              <span className="legend-indicator normal">Normal</span>
              <span className="legend-indicator fast">Too Fast</span>
              <span className="legend-indicator slow">Too Slow</span>
            </div>
          </div>
        )}
      </div>
      
      <div className="transcript-content">
        {viewMode === 'paragraph' ? (
          <div className="transcript-paragraph">
            {getParagraphText()}
          </div>
        ) : (
          <div className="transcript-timeline">
            {sortedData.map((segment, index) => (
              <div 
                key={index} 
                className={`transcript-segment ${
                  segment.wps > 3.0 ? 'too-fast' : 
                  segment.wps < 1.0 ? 'too-slow' : 'normal-speed'
                }`}
              >
                <div className="segment-header">
                  <span className="segment-time">
                    {formatTime(segment.start)} - {formatTime(segment.end)}
                  </span>
                  <div className="segment-metrics">
                    <span className="segment-emotion" style={{
                      backgroundColor: getEmotionColor(segment.emotion)
                    }}>
                      {segment.emotion}
                    </span>
                    <span className={`segment-wps ${
                      segment.wps > 3.0 ? 'too-fast' : 
                      segment.wps < 1.0 ? 'too-slow' : 'normal-speed'
                    }`}>
                      {segment.wps.toFixed(1)} WPS
                      {segment.wps > 3.0 && " (too fast)"}
                      {segment.wps < 1.0 && " (too slow)"}
                    </span>
                  </div>
                </div>
                <div className="segment-text">
                  {segment.text}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Card>
  );
}

// Helper function to get emotion color
function getEmotionColor(emotion) {
  const emotionColors = {
    "angry": "#ff6b6b",
    "calm": "#6495ed",
    "sad": "#9370db",
    "surprised": "#ffd700",
    "happy": "#7cfc00",
    "neutral": "#d3d3d3",
    "anxious": "#ff7f50",
    "disappointed": "#708090",
    "fearful": "#8a2be2",
    "excited": "#00ff7f",
    "unknown": "#ffffff"
  };
  return emotionColors[emotion] || "#d3d3d3";
}

export default TranscriptView;