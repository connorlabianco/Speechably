import os
import subprocess
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

class DataProcessor:
    """
    Handles data processing operations for the application including
    audio file handling, duration detection, and formatting.
    """
    
    def __init__(self, ffmpeg_path: str):
        """
        Initialize the DataProcessor with the path to FFmpeg.
        
        Args:
            ffmpeg_path: Path to the FFmpeg executable
        """
        self.ffmpeg_path = ffmpeg_path
        # Ensure FFmpeg path is in the environment PATH
        os.environ['PATH'] = os.path.dirname(self.ffmpeg_path) + os.pathsep + os.environ['PATH']
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get the duration of an audio file using FFmpeg.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Duration of the audio file in seconds
        """
        cmd = [
            self.ffmpeg_path,
            '-i', audio_path,
            '-f', 'null',
            '-'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Extract duration using regex
        duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2}', result.stderr)
        if duration_match:
            hours, minutes, seconds = map(int, duration_match.groups())
            return hours * 3600 + minutes * 60 + seconds
        return 0.0
    
    def format_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to MM:SS format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string in MM:SS format
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def process_emotion_data(
        self, 
        emotion_results: Dict[str, str], 
        total_duration: float, 
        segment_durations: List[float]
    ) -> List[Tuple[str, str]]:
        """
        Process emotion analysis results into time-based segments.
        
        Args:
            emotion_results: Dictionary mapping segment filenames to emotions
            total_duration: Total duration of the audio in seconds
            segment_durations: List of durations for each segment
            
        Returns:
            List of (time_range, emotion) tuples
        """
        current_time = 0
        emotion_segments = []
        
        for i, (filename, emotion) in enumerate(emotion_results.items()):
            segment_duration = segment_durations[i] if i < len(segment_durations) else 0
            
            start_time = self.format_timestamp(current_time)
            # For the last segment, use the total duration instead of current_time + segment_duration
            if i == len(emotion_results) - 1:
                end_time = self.format_timestamp(total_duration)
            else:
                end_time = self.format_timestamp(current_time + segment_duration)
            
            time_range = f"{start_time} - {end_time}"
            emotion_segments.append((time_range, emotion))
            
            current_time += segment_duration
        
        return emotion_segments
    
    def save_transcription_data(self, output_dir: str, transcription_data: List[Dict[str, Any]]) -> str:
        """
        Save transcription data to JSON file.
        
        Args:
            output_dir: Directory to save the JSON file
            transcription_data: List of transcription segment dictionaries
            
        Returns:
            Path to the saved JSON file
        """
        json_path = os.path.join(output_dir, "transcripts.json")
        with open(json_path, "w") as f:
            json.dump(transcription_data, f, indent=4)
        return json_path
    
    def save_analysis_results(
        self, 
        output_dir: str, 
        emotion_segments: List[Tuple[str, str]], 
        transcription_data: List[Dict[str, Any]],
        gemini_analysis: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save all analysis results to a single JSON file.
        
        Args:
            output_dir: Directory to save the JSON file
            emotion_segments: List of (time_range, emotion) tuples
            transcription_data: List of transcription segment dictionaries
            gemini_analysis: Optional dictionary containing Gemini analysis results
            
        Returns:
            Path to the saved JSON file
        """
        # Convert emotion segments to dictionary format
        emotion_data = [{"time_range": time_range, "emotion": emotion} 
                       for time_range, emotion in emotion_segments]
        
        # Create the complete results dictionary
        results = {
            "emotion_segments": emotion_data,
            "transcription_data": transcription_data
        }
        
        # Add Gemini analysis if available
        if gemini_analysis:
            results["gemini_analysis"] = gemini_analysis
        
        # Save to file
        json_path = os.path.join(output_dir, "analysis_results.json")
        with open(json_path, "w") as f:
            json.dump(results, f, indent=4)
        
        return json_path
    
    def load_analysis_results(self, json_path: str) -> Dict[str, Any]:
        """
        Load analysis results from a JSON file.
        
        Args:
            json_path: Path to the JSON file
            
        Returns:
            Dictionary containing the loaded analysis results
        """
        if not os.path.exists(json_path):
            return {"error": f"File not found: {json_path}"}
        
        try:
            with open(json_path, "r") as f:
                results = json.load(f)
            
            # Convert emotion data back to tuple format if needed
            if "emotion_segments" in results:
                emotion_segments = [(item["time_range"], item["emotion"]) 
                                   for item in results["emotion_segments"]]
                results["emotion_segments"] = emotion_segments
            
            return results
        except Exception as e:
            return {"error": f"Error loading results: {str(e)}"}
    
    def extract_segment_emotions(self, emotion_results: Dict[str, str]) -> List[str]:
        """
        Extract a list of emotions from the analysis results.
        
        Args:
            emotion_results: Dictionary mapping segment filenames to emotions
            
        Returns:
            List of emotions in segment order
        """
        return list(emotion_results.values())
    
    def calculate_emotion_stats(self, emotion_segments: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Calculate statistics about the emotion distribution.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            
        Returns:
            Dictionary containing emotion statistics
        """
        if not emotion_segments:
            return {
                "emotion_counts": {},
                "dominant_emotion": "none",
                "dominant_percentage": 0,
                "emotion_diversity": 0,
                "emotion_transitions": 0
            }
        
        # Count occurrences of each emotion
        emotions = [emotion for _, emotion in emotion_segments]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Calculate statistics
        total_segments = len(emotion_segments)
        sorted_counts = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        dominant_emotion = sorted_counts[0][0] if sorted_counts else "none"
        dominant_count = sorted_counts[0][1] if sorted_counts else 0
        dominant_percentage = (dominant_count / total_segments) * 100 if total_segments > 0 else 0
        
        # Calculate emotion diversity (unique emotions)
        emotion_diversity = len(emotion_counts)
        
        # Count emotion transitions
        emotion_transitions = 0
        for i in range(1, len(emotions)):
            if emotions[i] != emotions[i-1]:
                emotion_transitions += 1
        
        return {
            "emotion_counts": emotion_counts,
            "dominant_emotion": dominant_emotion,
            "dominant_percentage": round(dominant_percentage, 1),
            "emotion_diversity": emotion_diversity,
            "emotion_transitions": emotion_transitions
        }


# Example usage
if __name__ == "__main__":
    # This allows testing the processor independently
    processor = DataProcessor("path/to/ffmpeg")
    
    # Example emotion results
    sample_emotion_results = {
        "segment_1.wav": "calm",
        "segment_2.wav": "happy",
        "segment_3.wav": "calm",
        "segment_4.wav": "surprised"
    }
    
    # Example durations
    total_duration = 60.0  # 1 minute
    segment_durations = [15.0, 15.0, 15.0, 15.0]  # 15 seconds each
    
    # Process emotion data
    emotion_segments = processor.process_emotion_data(
        sample_emotion_results, 
        total_duration, 
        segment_durations
    )
    
    print("Emotion segments:")
    for time_range, emotion in emotion_segments:
        print(f"  {time_range}: {emotion}")
    
    # Calculate emotion statistics
    stats = processor.calculate_emotion_stats(emotion_segments)
    print("\nEmotion statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")