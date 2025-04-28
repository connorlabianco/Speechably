import React, { useState, useRef } from 'react';
import { uploadVideo } from '../services/api';
import Loading from './layout/Loading';
import '../styles/components/VideoUploader.css';

function VideoUploader({ onUploadStart, onUploadSuccess, onUploadError, isLoading }) {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);
  
  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };
  
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };
  
  const handleDragLeave = () => {
    setIsDragging(false);
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
    }
  };
  
  const handleUpload = async () => {
    if (!file) return;
    
    try {
      onUploadStart();
      
      const formData = new FormData();
      formData.append('file', file);
      
      const data = await uploadVideo(formData);
      onUploadSuccess(data);
    } catch (error) {
      onUploadError(error.message || 'Upload failed');
    }
  };
  
  const triggerFileInput = () => {
    fileInputRef.current.click();
  };
  
  return (
    <div className="video-uploader">
      {isLoading ? (
        <Loading message="Analyzing speech patterns and emotions..." />
      ) : (
        <>
          <div 
            className={`upload-area ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={triggerFileInput}
          >
            <input 
              type="file" 
              ref={fileInputRef}
              onChange={handleFileChange} 
              accept="video/mp4,video/x-m4v,video/*"
              className="file-input"
            />
            
            <div className="upload-content">
              {file ? (
                <>
                  <div className="file-info">
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">{(file.size / (1024 * 1024)).toFixed(2)} MB</span>
                  </div>
                </>
              ) : (
                <>
                  <div className="upload-icon">🎥</div>
                  <p className="upload-text">Drag and drop your video here or click to browse</p>
                  <p className="upload-hint">Supported formats: MP4, MOV, AVI, WebM</p>
                </>
              )}
            </div>
          </div>
          
          {file && (
            <button 
              className="btn-primary upload-button" 
              onClick={handleUpload}
            >
              Analyze Speech
            </button>
          )}
        </>
      )}
    </div>
  );
}

export default VideoUploader;