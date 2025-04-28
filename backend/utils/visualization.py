import pandas as pd
from typing import List, Dict, Tuple, Any, Optional

class VisualizationHelper:
    """
    Helper class for preparing data for visualization in the UI.
    Transforms raw data into formats suitable for visualization libraries.
    """
    
    def __init__(self):
        """Initialize the visualization helper"""
        pass
    
    def prepare_emotion_timeline_data(self, emotion_segments: List[Tuple[str, str]]) -> pd.DataFrame:
        """
        Convert emotion segment data to DataFrame for visualization.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            
        Returns:
            DataFrame with preprocessed emotion data
        """
        # Convert emotion data to DataFrame for analysis
        emotion_df = pd.DataFrame(emotion_segments, columns=["Time Range", "Emotion"])
        
        # Create new columns with numeric start time for plotting
        emotion_df["Start Time"] = emotion_df["Time Range"].apply(lambda x: x.split(" - ")[0])
        emotion_df["End Time"] = emotion_df["Time Range"].apply(lambda x: x.split(" - ")[1])
        
        # Add time in seconds for plotting
        emotion_df["Start Seconds"] = emotion_df["Start Time"].apply(self._time_to_seconds)
        emotion_df["End Seconds"] = emotion_df["End Time"].apply(self._time_to_seconds)
        emotion_df["Mid Seconds"] = (emotion_df["Start Seconds"] + emotion_df["End Seconds"]) / 2
        
        return emotion_df
    
    def calculate_emotion_metrics(self, emotion_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate metrics about the emotion distribution.
        
        Args:
            emotion_df: DataFrame with preprocessed emotion data
            
        Returns:
            Dictionary with calculated emotion metrics
        """
        # Count occurrences of each emotion
        emotion_counts = emotion_df["Emotion"].value_counts().to_dict()
        
        # Calculate diversity of emotions
        emotion_diversity = len(emotion_counts)
        
        # Calculate main emotion percentage
        if len(emotion_df) > 0:
            main_emotion = next(iter(emotion_counts)) if emotion_counts else "None"
            main_emotion_percentage = (emotion_counts[main_emotion] / len(emotion_df)) * 100
        else:
            main_emotion = "None"
            main_emotion_percentage = 0
        
        # Calculate emotional versatility
        versatility_score = min(emotion_diversity / 5 * 100, 100)  # Normalize to 100%
        
        # Create emotion transitions list
        transitions = []
        if len(emotion_df) > 1:
            for i in range(len(emotion_df) - 1):
                from_emotion = emotion_df.iloc[i]["Emotion"]
                to_emotion = emotion_df.iloc[i+1]["Emotion"]
                if from_emotion != to_emotion:
                    transitions.append(f"{from_emotion} → {to_emotion}")
        
        return {
            "emotion_counts": emotion_counts,
            "emotion_diversity": emotion_diversity,
            "main_emotion": main_emotion,
            "main_emotion_percentage": round(main_emotion_percentage, 1),
            "versatility_score": round(versatility_score, 1),
            "transitions": transitions
        }
    
    def prepare_wps_data(self, transcription_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Prepare words-per-second data for visualization.
        
        Args:
            transcription_data: List of transcription segment dictionaries
            
        Returns:
            DataFrame with WPS data
        """
        if not transcription_data:
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=["Time", "WPS", "Optimal Min", "Optimal Max", "Emotion"])
        
        # Extract data points
        data_points = []
        
        for segment in transcription_data:
            # Use midpoint of segment for time
            time = (segment["start"] + segment["end"]) / 2
            wps = segment["wps"]
            emotion = segment["emotion"]
            
            data_points.append({
                "Time": time,
                "WPS": wps,
                "Optimal Min": 2.0,  # Optimal minimum WPS
                "Optimal Max": 3.0,   # Optimal maximum WPS
                "Emotion": emotion    # Include emotion for combined visualization
            })
        
        return pd.DataFrame(data_points)
    
    def prepare_combined_timeline_data(
        self, 
        emotion_df: pd.DataFrame, 
        wps_data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Prepare combined emotion and WPS data for timeline visualization.
        
        Args:
            emotion_df: DataFrame with emotion data
            wps_data: DataFrame with WPS data
            
        Returns:
            DataFrame with combined data for visualization
        """
        # Create a combined dataset for timeline visualization
        combined_data = []
        
        # Add emotion data points
        for _, row in emotion_df.iterrows():
            combined_data.append({
                "Time": row["Mid Seconds"],
                "Type": "Emotion",
                "Value": row["Emotion"],
                "Start": row["Start Seconds"],
                "End": row["End Seconds"]
            })
        
        # Add WPS data points
        for _, row in wps_data.iterrows():
            # Determine speed category
            if row["WPS"] > 3.0:
                speed_category = "Too Fast"
            elif row["WPS"] < 1.0:
                speed_category = "Too Slow"
            else:
                speed_category = "Optimal"
                
            combined_data.append({
                "Time": row["Time"],
                "Type": "WPS",
                "Value": row["WPS"],
                "Category": speed_category,
                "Emotion": row["Emotion"]
            })
        
        return pd.DataFrame(combined_data)
    
    def prepare_emotion_distribution_data(self, emotion_segments: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Prepare data for emotion distribution pie chart.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            
        Returns:
            Dictionary with emotion distribution data
        """
        # Count emotions
        emotion_counts = {}
        for _, emotion in emotion_segments:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Calculate percentages
        total = sum(emotion_counts.values())
        emotion_percentages = {emotion: (count / total) * 100 for emotion, count in emotion_counts.items()}
        
        # Prepare data for pie chart
        labels = list(emotion_counts.keys())
        values = list(emotion_counts.values())
        percentages = [emotion_percentages[emotion] for emotion in labels]
        
        return {
            "labels": labels,
            "values": values,
            "percentages": percentages
        }
    
    def prepare_speech_clarity_data(self, transcription_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepare speech clarity data for visualization.
        
        Args:
            transcription_data: List of transcription segment dictionaries
            
        Returns:
            Dictionary with speech clarity metrics
        """
        if not transcription_data:
            return {
                "avg_words_per_segment": 0,
                "avg_wps": 0,
                "clarity_score": 0,
                "issues": []
            }
        
        # Calculate metrics
        total_words = sum(len(segment["text"].split()) for segment in transcription_data)
        avg_words_per_segment = total_words / len(transcription_data)
        
        wps_values = [segment["wps"] for segment in transcription_data]
        avg_wps = sum(wps_values) / len(wps_values) if wps_values else 0
        
        # Simplified clarity score calculation
        clarity_score = min(100, max(0, (avg_words_per_segment / 20) * 100))
        
        # Identify potential clarity issues
        issues = []
        for i, segment in enumerate(transcription_data):
            text = segment["text"]
            words = text.split()
            
            # Check for very short segments (potentially unclear speech)
            if len(words) < 3 and segment["end"] - segment["start"] > 2:
                issues.append(f"Segment {i+1} has very few words for its duration")
            
            # Check for segments with too many filler words (simplified)
            filler_words = ["um", "uh", "like", "you know", "sort of", "kind of"]
            filler_count = sum(text.lower().count(word) for word in filler_words)
            if filler_count > len(words) * 0.2:  # If more than 20% are filler words
                issues.append(f"Segment {i+1} has many filler words")
        
        return {
            "avg_words_per_segment": round(avg_words_per_segment, 1),
            "avg_wps": round(avg_wps, 2),
            "clarity_score": round(clarity_score, 1),
            "issues": issues
        }
    
    def _time_to_seconds(self, time_str: str) -> float:
        """
        Convert MM:SS format to seconds.
        
        Args:
            time_str: Time string in MM:SS format
            
        Returns:
            Time in seconds
        """
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds
    
    def get_emotion_color_map(self) -> Dict[str, str]:
        """
        Get a mapping of emotions to colors for consistent visualization.
        
        Returns:
            Dictionary mapping emotion names to color codes
        """
        return {
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
        }
    
    def get_emotion_icon_map(self) -> Dict[str, str]:
        """
        Get a mapping of emotions to text labels for visualization.
        
        Returns:
            Dictionary mapping emotion names to text labels
        """
        return {
            "angry": "ANGRY",
            "calm": "CALM",
            "sad": "SAD",
            "surprised": "SURP",
            "happy": "HAPPY",
            "neutral": "NEUT",
            "anxious": "ANX",
            "disappointed": "DISAP",
            "fearful": "FEAR",
            "excited": "EXCIT",
            "unknown": "UNK"
        }