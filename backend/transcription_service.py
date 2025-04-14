import whisper
import os
import streamlit as st
from typing import List, Dict, Tuple, Any, Optional

class TranscriptionService:
    """
    Service for transcribing audio using the Whisper model.
    This handles the speech-to-text conversion for the application.
    """
    
    def __init__(self, model_size: str = "tiny"):
        """
        Initialize the transcription service with a Whisper model.
        
        Args:
            model_size: Size of the Whisper model to use ("tiny", "base", "small", "medium", "large")
        """
        self.model_size = model_size
        self.model = self.load_whisper_model(model_size)
    
    @st.cache_resource
    def load_whisper_model(_self, model_size: str):
        """
        Load and cache the Whisper model.
        
        Args:
            model_size: Size of the model to load
            
        Returns:
            Loaded Whisper model or None if loading fails
        """
        try:
            return whisper.load_model(model_size)
        except Exception as e:
            print(f"Error loading Whisper model: {str(e)}")
            return None
    
    def transcribe_segments(
        self, 
        segment_paths: List[str], 
        segment_duration: float,
        emotion_data: Optional[List[Tuple[str, str]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Transcribe audio segments using the Whisper model.
        
        Args:
            segment_paths: List of paths to audio segment files
            segment_duration: Approximate duration of each segment
            emotion_data: Optional list of (time_range, emotion) tuples
            
        Returns:
            List of dictionaries containing transcription data for each segment
        """
        if not self.model:
            print("Whisper model not loaded. Please check the error message above.")
            return []
            
        transcripts = []
        
        for i, segment_path in enumerate(segment_paths):
            if not os.path.exists(segment_path):
                print(f"Segment file not found: {segment_path}")
                continue
                
            try:
                # Get emotion from emotion_data if available
                emotion = emotion_data[i][1] if emotion_data and i < len(emotion_data) else "unknown"
                
                # Calculate segment times
                start_time = i * segment_duration
                end_time = (i + 1) * segment_duration
                
                # Transcribe with Whisper
                result = self.model.transcribe(segment_path)
                transcribed_text = result["text"].strip()
                
                # Count words and calculate WPS
                word_count = len(transcribed_text.split())
                wps = word_count / segment_duration if segment_duration > 0 else 0
                
                # Create segment data
                segment_data = {
                    "index": i,
                    "start": round(start_time, 2),
                    "end": round(end_time, 2),
                    "text": transcribed_text,
                    "wps": round(wps, 2),
                    "emotion": emotion
                }
                
                transcripts.append(segment_data)
                print(f"Transcribed segment {i+1}: {segment_data['text'][:50]}...")
            except Exception as e:
                print(f"Error transcribing segment {i+1}: {str(e)}")
                continue
        
        return transcripts
    
    def get_speech_metrics(self, transcription_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate speech metrics based on transcription data.
        
        Args:
            transcription_data: List of transcription segment dictionaries
            
        Returns:
            Dictionary containing calculated speech metrics
        """
        if not transcription_data:
            return {
                "avg_wps": 0,
                "wps_variation": 0,
                "total_words": 0,
                "speech_clarity": 0,
                "fast_segments": [],
                "slow_segments": []
            }
        
        # Extract WPS values
        wps_values = [segment["wps"] for segment in transcription_data]
        
        # Calculate metrics
        avg_wps = sum(wps_values) / len(wps_values)
        wps_variation = max(wps_values) - min(wps_values) if wps_values else 0
        total_words = sum(len(segment["text"].split()) for segment in transcription_data)
        
        # Identify segments that are too fast or too slow
        fast_segments = []
        slow_segments = []
        
        for i, segment in enumerate(transcription_data):
            if segment["wps"] > 3.0:
                fast_segments.append(i)
            elif segment["wps"] < 1.0:
                slow_segments.append(i)
        
        # Calculate speech clarity score (simplified)
        # Here we're estimating clarity based on word count vs. duration
        # A more sophisticated approach would analyze the actual content
        avg_words_per_segment = total_words / len(transcription_data)
        clarity_score = min(100, max(0, (avg_words_per_segment / 20) * 100))
        
        return {
            "avg_wps": round(avg_wps, 2),
            "wps_variation": round(wps_variation, 2),
            "total_words": total_words,
            "speech_clarity": round(clarity_score, 1),
            "fast_segments": fast_segments,
            "slow_segments": slow_segments
        }
    
    def format_transcript_for_display(self, transcription_data: List[Dict[str, Any]]) -> str:
        """
        Format the transcript data for display.
        
        Args:
            transcription_data: List of transcription segment dictionaries
            
        Returns:
            Formatted transcript string
        """
        if not transcription_data:
            return "No transcription data available."
        
        # Format time helper function
        def format_time(seconds: float) -> str:
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes:02d}:{seconds:02d}"
        
        # Build the formatted transcript
        formatted_lines = []
        
        for segment in transcription_data:
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])
            
            line = f"[{start_time} - {end_time}] ({segment['emotion']}) {segment['text']}"
            formatted_lines.append(line)
        
        return "\n\n".join(formatted_lines)


# Example usage
if __name__ == "__main__":
    # This allows testing the service independently
    transcription_service = TranscriptionService()
    
    # Test with sample data if needed
    print(f"Initialized transcription service with model: {transcription_service.model_size}")
    
    # Example of calculating metrics from sample data
    sample_data = [
        {"index": 0, "start": 0, "end": 5, "text": "This is a test sentence for the transcription service.", "wps": 2.4, "emotion": "neutral"},
        {"index": 1, "start": 5, "end": 10, "text": "The speech rate can vary across different segments.", "wps": 1.8, "emotion": "calm"},
        {"index": 2, "start": 10, "end": 15, "text": "Some segments might be too fast!", "wps": 3.2, "emotion": "excited"},
    ]
    
    metrics = transcription_service.get_speech_metrics(sample_data)
    print("Speech metrics:", metrics)
    
    # Display formatted transcript
    formatted = transcription_service.format_transcript_for_display(sample_data)
    print("\nFormatted transcript:\n")
    print(formatted)