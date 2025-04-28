// src/components/EmotionTimeline.js
import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, 
  Legend, ResponsiveContainer, ReferenceLine, Area, ComposedChart
} from 'recharts';
import Card from './layout/Card';
import '../styles/components/EmotionTimeline.css';

function EmotionTimeline({ emotionSegments, wpsData }) {
  const [viewMode, setViewMode] = useState('combined'); // 'combined', 'emotion', 'wps'
  
  // Helper function to convert time range to seconds for display
  const timeToSeconds = (timeRange) => {
    const [start] = timeRange.split(' - ');
    const [minutes, seconds] = start.split(':').map(Number);
    return minutes * 60 + seconds;
  };
  
  // Process emotion data for visualization
  const prepareEmotionData = () => {
    return emotionSegments.map((segment, index) => {
      const timeInSeconds = timeToSeconds(segment.time_range);
      return {
        name: segment.time_range,
        timeInSeconds,
        emotion: segment.emotion,
        // Add a numeric value for the emotion (for visualization)
        emotionValue: index + 1,
      };
    });
  };
  
  // Get emotion colors for consistent visualization
  const getEmotionColor = (emotion) => {
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
  };
  
  // Create the combined timeline data
  const prepareCombinedData = () => {
    const emotionData = prepareEmotionData();
    // If we don't have WPS data, just return emotion data
    if (!wpsData || wpsData.length === 0) return emotionData;
    
    // Merge the WPS data with emotion data
    return emotionData.map((item, index) => {
      // Find corresponding WPS data point
      const wpsPoint = wpsData.find(wp => {
        const wpTimeInSec = wp.Time;
        const itemStart = timeToSeconds(item.name.split(' - ')[0]);
        const itemEnd = timeToSeconds(item.name.split(' - ')[1]);
        return wpTimeInSec >= itemStart && wpTimeInSec <= itemEnd;
      });
      
      return {
        ...item,
        wps: wpsPoint ? wpsPoint.WPS : null,
        optimalMin: 2.0,
        optimalMax: 3.0
      };
    });
  };
  
  const combinedData = prepareCombinedData();
  
  // Custom tooltip for the chart
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip">
          <p className="label">{`Time: ${data.name}`}</p>
          <p className="emotion" style={{ color: getEmotionColor(data.emotion) }}>
            {`Emotion: ${data.emotion}`}
          </p>
          {data.wps !== null && (
            <p className="wps">
              {`Speaking Rate: ${data.wps.toFixed(2)} WPS`}
              {data.wps > 3.0 && " (too fast)"}
              {data.wps < 1.0 && " (too slow)"}
            </p>
          )}
        </div>
      );
    }
    return null;
  };
  
  return (
    <Card className="emotion-timeline-card">
      <div className="view-mode-selector">
        <button 
          className={`view-mode-btn ${viewMode === 'combined' ? 'active' : ''}`}
          onClick={() => setViewMode('combined')}
        >
          Combined View
        </button>
        <button 
          className={`view-mode-btn ${viewMode === 'emotion' ? 'active' : ''}`}
          onClick={() => setViewMode('emotion')}
        >
          Emotion Only
        </button>
        <button 
          className={`view-mode-btn ${viewMode === 'wps' ? 'active' : ''}`}
          onClick={() => setViewMode('wps')}
        >
          Speaking Rate Only
        </button>
      </div>
      
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={400}>
          {viewMode === 'combined' ? (
            <ComposedChart data={combinedData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timeInSeconds"
                type="number"
                domain={['dataMin', 'dataMax']}
                tickFormatter={(value) => `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')}`}
                label={{ value: 'Time (MM:SS)', position: 'insideBottom', offset: -5 }}
              />
              <YAxis yAxisId="emotion" orientation="left" label={{ value: 'Emotion', angle: -90, position: 'insideLeft' }} />
              <YAxis yAxisId="wps" orientation="right" domain={[0, 4]} label={{ value: 'WPS', angle: -90, position: 'insideRight' }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              
              {/* Emotion line */}
              <Line
                yAxisId="emotion"
                type="stepAfter"
                dataKey="emotionValue"
                stroke="#8884d8"
                name="Emotion"
                dot={{ fill: '#8884d8', r: 5 }}
                activeDot={{ r: 8 }}
                isAnimationActive={false}
              />
              
              {/* WPS line */}
              <Line
                yAxisId="wps"
                type="monotone"
                dataKey="wps"
                stroke="#82ca9d"
                name="Words Per Second"
                dot={{ fill: '#82ca9d', r: 5 }}
                isAnimationActive={false}
              />
              
              {/* Optimal WPS range */}
              <ReferenceLine yAxisId="wps" y={2.0} stroke="rgba(0, 255, 0, 0.5)" strokeDasharray="3 3" />
              <ReferenceLine yAxisId="wps" y={3.0} stroke="rgba(255, 0, 0, 0.5)" strokeDasharray="3 3" />
              <Area 
                yAxisId="wps"
                dataKey="optimalMin"
                stroke="transparent"
                fill="rgba(0, 255, 0, 0.1)"
                activeDot={false}
                name="Optimal Range (2-3 WPS)"
              />
            </ComposedChart>
          ) : viewMode === 'emotion' ? (
            <LineChart data={combinedData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timeInSeconds"
                type="number" 
                domain={['dataMin', 'dataMax']}
                tickFormatter={(value) => `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')}`}
                label={{ value: 'Time (MM:SS)', position: 'insideBottom', offset: -5 }}
              />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line
                type="stepAfter"
                dataKey="emotionValue"
                stroke="#8884d8"
                name="Emotion"
                dot={{ fill: '#8884d8', r: 5 }}
                activeDot={{ r: 8 }}
                isAnimationActive={false}
              />
            </LineChart>
          ) : (
            <LineChart data={combinedData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timeInSeconds"
                type="number"
                domain={['dataMin', 'dataMax']}
                tickFormatter={(value) => `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')}`}
                label={{ value: 'Time (MM:SS)', position: 'insideBottom', offset: -5 }}
              />
              <YAxis domain={[0, 4]} label={{ value: 'WPS', angle: -90, position: 'insideLeft' }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line
                type="monotone"
                dataKey="wps"
                stroke="#82ca9d"
                name="Words Per Second"
                dot={{ fill: '#82ca9d', r: 5 }}
                isAnimationActive={false}
              />
              <ReferenceLine y={2.0} stroke="rgba(0, 255, 0, 0.5)" strokeDasharray="3 3" label={{ value: 'Min Optimal', position: 'insideLeft' }} />
              <ReferenceLine y={3.0} stroke="rgba(255, 0, 0, 0.5)" strokeDasharray="3 3" label={{ value: 'Max Optimal', position: 'insideLeft' }} />
              <Area 
                dataKey="optimalMin"
                stroke="transparent"
                fill="rgba(0, 255, 0, 0.1)"
                activeDot={false}
              />
            </LineChart>
          )}
        </ResponsiveContainer>
      </div>
      
      <div className="emotion-legend">
        <h4>Emotion Legend</h4>
        <div className="emotion-legend-items">
          {[...new Set(emotionSegments.map(segment => segment.emotion))].map((emotion, index) => (
            <div key={index} className="emotion-legend-item">
              <span 
                className="emotion-color-indicator"
                style={{ backgroundColor: getEmotionColor(emotion) }}
              ></span>
              <span className="emotion-name">{emotion}</span>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

export default EmotionTimeline;