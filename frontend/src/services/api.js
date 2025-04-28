/**
 * API Service for Speechably
 * Handles all communication with the backend API
 */

// API base URL - set to the Flask backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Upload a video file for analysis
 * 
 * @param {FormData} formData - Form data containing the video file
 * @returns {Promise<Object>} - Analysis results
 */
export const uploadVideo = async (formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to upload video');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error uploading video:', error);
    throw error;
  }
};

/**
 * Send a chat message to the AI coach
 * 
 * @param {Object} data - Chat data containing message and emotion segments
 * @returns {Promise<Object>} - AI response
 */
export const sendChatMessage = async (data) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to send message');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Check API server health
 * 
 * @returns {Promise<boolean>} - True if API is healthy
 */
export const checkApiHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/healthcheck`);
    return response.ok;
  } catch (error) {
    console.error('API health check failed:', error);
    return false;
  }
};