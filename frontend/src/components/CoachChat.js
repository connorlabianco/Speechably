import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';
import Card from './layout/Card';
import '../styles/components/CoachChat.css';

function CoachChat({ emotionSegments }) {
  const [chatHistory, setChatHistory] = useState([
    { role: 'ai', content: "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?" }
  ]);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);
  
  // Auto-scroll to bottom when chat history changes
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);
  
  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!message.trim()) return;
    
    // Add user message to chat
    const userMessage = { role: 'user', content: message };
    setChatHistory(prev => [...prev, userMessage]);
    setMessage('');
    setIsLoading(true);
    
    try {
      // Send message to backend
      const response = await sendChatMessage({
        message,
        emotion_segments: emotionSegments
      });
      
      // Add AI response to chat
      const aiMessage = { role: 'ai', content: response.response };
      setChatHistory(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message to chat
      const errorMessage = { 
        role: 'ai', 
        content: "I'm having trouble connecting right now. Please try again later.",
        isError: true
      };
      setChatHistory(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };
  
  const resetChat = () => {
    setChatHistory([
      { role: 'ai', content: "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?" }
    ]);
  };
  
  // Suggested questions for the user
  const suggestedQuestions = [
    "How can I improve my speaking pace?",
    "What should I do to sound more confident?",
    "How can I better control my emotions while speaking?",
    "What vocal exercises would help me?",
    "How can I eliminate filler words?"
  ];
  
  const handleSuggestedQuestion = (question) => {
    setMessage(question);
  };
  
  return (
    <Card className="coach-chat-card">
      <div className="chat-container">
        <div className="chat-messages">
          {chatHistory.map((msg, index) => (
            <div 
              key={index} 
              className={`chat-message ${msg.role === 'user' ? 'user-message' : 'ai-message'} ${msg.isError ? 'error-message' : ''}`}
            >
              {msg.role === 'ai' && <div className="ai-avatar">🧠</div>}
              <div className="message-content">{msg.content}</div>
              {msg.role === 'user' && <div className="user-avatar">👤</div>}
            </div>
          ))}
          {isLoading && (
            <div className="chat-message ai-message loading-message">
              <div className="ai-avatar">🧠</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
        
        <div className="suggested-questions">
          <h4>Try asking:</h4>
          <div className="question-buttons">
            {suggestedQuestions.map((question, index) => (
              <button 
                key={index} 
                className="question-button"
                onClick={() => handleSuggestedQuestion(question)}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
        
        <div className="chat-input-container">
          <form onSubmit={handleSendMessage}>
            <textarea
              className="chat-input"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask your AI coach a question..."
              disabled={isLoading}
              rows={2}
            />
            <div className="chat-buttons">
              <button 
                type="button" 
                className="reset-button"
                onClick={resetChat}
              >
                Reset
              </button>
              <button 
                type="submit" 
                className="send-button"
                disabled={isLoading || !message.trim()}
              >
                Send
              </button>
            </div>
          </form>
        </div>
      </div>
    </Card>
  );
}

export default CoachChat;