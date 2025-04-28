// src/pages/Home.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import VideoUploader from '../components/VideoUploader';
import FeatureList from '../components/FeatureList';
import '../styles/pages/Home.css';

function Home({ onAnalysisComplete }) {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleUploadSuccess = (data) => {
    setIsLoading(false);
    onAnalysisComplete(data);
    navigate('/analysis');
  };

  const handleUploadStart = () => {
    setIsLoading(true);
  };

  const handleUploadError = (error) => {
    setIsLoading(false);
    console.error("Upload error:", error);
    // Show error state
  };

  return (
    <div className="home-page">
      <section className="hero">
        <h1>Speechably</h1>
        <p className="tagline">Creating confidence through user-driven feedback.</p>
        <p className="subtitle">Upload a video of yourself speaking to get personalized feedback on your speech emotion and delivery.</p>
        
        <VideoUploader 
          onUploadStart={handleUploadStart}
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
          isLoading={isLoading}
        />
      </section>
      
      <section className="features">
        <h2>Key Features</h2>
        <FeatureList />
      </section>
    </div>
  );
}

export default Home;