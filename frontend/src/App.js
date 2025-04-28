import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Analysis from './pages/Analysis';
import NotFound from './pages/NotFound';
import './styles/App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  
  // Handler for setting analysis data from the VideoUploader component
  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
  };

  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route 
              path="/" 
              element={<Home onAnalysisComplete={handleAnalysisComplete} />} 
            />
            <Route 
              path="/analysis" 
              element={<Analysis analysisData={analysisData} />} 
            />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;