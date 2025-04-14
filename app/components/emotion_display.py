import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Tuple, Any, Optional

class EmotionDisplay:
    """
    Component for displaying emotion analysis visualizations and insights.
    """
    
    def __init__(self, visualization_helper):
        """
        Initialize the emotion display component.
        
        Args:
            visualization_helper: The VisualizationHelper instance for data preparation
        """
        self.viz_helper = visualization_helper
    
    def display_emotion_insights(self, emotion_data: List[Tuple[str, str]], transcription_data: Optional[List[Dict[str, Any]]] = None):
        """
        Display visualizations and insights about emotion patterns.
        
        Args:
            emotion_data: List of (time_range, emotion) tuples
            transcription_data: Optional list of transcription segment dictionaries
        """
        # Process emotion data for visualization
        emotion_df = self.viz_helper.prepare_emotion_timeline_data(emotion_data)
        
        # Calculate metrics about emotion distribution
        metrics = self.viz_helper.calculate_emotion_metrics(emotion_df)
        
        # Display visualizations
        st.subheader("Emotion Distribution")
        
        # Create emotion timeline chart
        fig = self._create_emotion_timeline_chart(emotion_df)
        
        # Display the plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # Display emotion diversity metrics
        st.markdown("### 🌟 Emotion Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Dominant Emotion", metrics["main_emotion"])
            
            # Display emotion consistency as a percentage
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {metrics['main_emotion_percentage']}%; background-color: rgba(255, 107, 107, 0.7);">
                    {metrics['main_emotion_percentage']:.1f}%
                </div>
            </div>
            <p>Consistency of dominant emotion</p>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Emotional Range", f"{metrics['emotion_diversity']} emotions")
            
            # Display emotional versatility score
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {metrics['versatility_score']}%; background-color: rgba(100, 149, 237, 0.7);">
                    {metrics['versatility_score']:.1f}%
                </div>
            </div>
            <p>Emotional versatility score</p>
            """, unsafe_allow_html=True)
        
        # Show emotion transitions
        st.markdown("### 🔄 Emotion Transitions")
        
        if metrics["transitions"]:
            for transition in metrics["transitions"]:
                st.markdown(f"- {transition}")
        else:
            st.write("No emotion transitions detected.")
            
        # Display transcription data if available
        if transcription_data:
            self.display_transcription(transcription_data)
    
    def display_transcription(self, transcription_data: List[Dict[str, Any]]):
        """
        Display transcribed speech segments with emotion and speed data.
        
        Args:
            transcription_data: List of transcription segment dictionaries
        """
        st.markdown("### 📝 Speech Transcription")
        
        for segment in transcription_data:
            # Helper function to format timestamp
            def format_timestamp(seconds: float) -> str:
                minutes = int(seconds // 60)
                seconds = int(seconds % 60)
                return f"{minutes:02d}:{seconds:02d}"
                
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            
            # Determine speed indicator
            speed_indicator = ""
            speed_color = "white"
            if segment["wps"] > 3.0:
                speed_indicator = " (too fast)"
                speed_color = "red"
            elif segment["wps"] < 1.0:
                speed_indicator = " (too slow)"
                speed_color = "orange"
                
            # Get emotion color
            emotion_colors = self.viz_helper.get_emotion_color_map()
            emotion_color = emotion_colors.get(segment["emotion"], "#ffffff")
            
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 4px solid {emotion_color};">
                <h4 style="margin: 0; padding: 0;">{start_time} - {end_time}</h4>
                <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                    <span style="color: white;">Emotion: <strong>{segment['emotion']}</strong></span>
                    <span style="color: {speed_color};">WPS: <strong>{segment['wps']}</strong>{speed_indicator}</span>
                </div>
                <p style="margin: 10px 0 0 0; font-size: 16px;">{segment['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    def display_wps_chart(self, transcription_data: List[Dict[str, Any]]):
        """
        Display a chart of words per second over time.
        
        Args:
            transcription_data: List of transcription segment dictionaries
        """
        if not transcription_data:
            st.write("No transcription data available for WPS analysis.")
            return
            
        # Prepare data for WPS chart
        wps_data = self.viz_helper.prepare_wps_data(transcription_data)
        
        # Create figure
        fig = go.Figure()
        
        # Add WPS line
        fig.add_trace(
            go.Scatter(
                x=wps_data["Time"],
                y=wps_data["WPS"],
                mode="lines+markers",
                name="Words Per Second",
                line=dict(color="#6495ed", width=3),
                marker=dict(size=8)
            )
        )
        
        # Add optimal range
        fig.add_trace(
            go.Scatter(
                x=wps_data["Time"],
                y=wps_data["Optimal Min"],
                mode="lines",
                name="Optimal Min (2.0)",
                line=dict(color="rgba(100, 255, 100, 0.5)", width=2, dash="dash")
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=wps_data["Time"],
                y=wps_data["Optimal Max"],
                mode="lines",
                name="Optimal Max (3.0)",
                line=dict(color="rgba(255, 100, 100, 0.5)", width=2, dash="dash"),
                fill="tonexty",
                fillcolor="rgba(100, 255, 100, 0.1)"
            )
        )
        
        # Customize layout
        fig.update_layout(
            title="Speaking Rate Over Time",
            xaxis_title="Time (seconds)",
            yaxis_title="Words Per Second",
            plot_bgcolor="#343D46",
            paper_bgcolor="#343D46",
            font=dict(color="white"),
            xaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)"),
            yaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)"),
            margin=dict(l=10, r=10, t=40, b=10),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _create_emotion_timeline_chart(self, emotion_df):
        """
        Create a plotly figure for emotion timeline.
        
        Args:
            emotion_df: DataFrame with preprocessed emotion data
            
        Returns:
            Plotly figure object
        """
        # Get emotion colors
        emotion_colors = self.viz_helper.get_emotion_color_map()
        
        # Create a color sequence based on the emotions in the data
        unique_emotions = emotion_df["Emotion"].unique()
        color_sequence = [emotion_colors.get(emotion, "#ffffff") for emotion in unique_emotions]
        
        # Create a plotly figure for emotion timeline
        fig = px.line(
            emotion_df, 
            x="Mid Seconds", 
            y="Emotion",
            markers=True,
            color_discrete_sequence=color_sequence,
            title="Emotion Timeline Throughout Speech"
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Time (seconds)",
            yaxis_title="Emotion",
            plot_bgcolor="#343D46",
            paper_bgcolor="#343D46",
            font=dict(color="white"),
            xaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)"),
            yaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)"),
            margin=dict(l=10, r=10, t=40, b=10),
            height=400
        )
        
        # Add range markers for each segment
        for i, row in emotion_df.iterrows():
            fig.add_shape(
                type="rect",
                x0=row["Start Seconds"],
                x1=row["End Seconds"],
                y0=row["Emotion"],
                y1=row["Emotion"],
                line=dict(width=0),
                fillcolor="rgba(255, 255, 255, 0.2)",
                layer="below"
            )
        
        return fig


# Example usage if run directly
if __name__ == "__main__":
    # This would be used for local testing
    import sys
    from pathlib import Path
    
    # Add project root to Python path
    project_root = Path(__file__).parent.parent.parent
    sys.path.append(str(project_root))
    
    from backend.visualization_helper import VisualizationHelper
    
    # Set up a simple Streamlit test page
    st.set_page_config(page_title="Emotion Display Test", layout="wide")
    st.title("Emotion Display Component Test")
    
    # Initialize components
    viz_helper = VisualizationHelper()
    emotion_display = EmotionDisplay(viz_helper)
    
    # Sample data
    sample_emotion_data = [
        ("00:00 - 00:15", "calm"),
        ("00:15 - 00:30", "happy"),
        ("00:30 - 00:45", "calm"),
        ("00:45 - 01:00", "surprised"),
        ("01:00 - 01:15", "angry")
    ]
    
    sample_transcription = [
        {
            "index": 0,
            "start": 0,
            "end": 15,
            "text": "This is a test of the emotion display component.",
            "wps": 2.2,
            "emotion": "calm"
        },
        {
            "index": 1,
            "start": 15,
            "end": 30,
            "text": "I'm feeling quite happy about how this is turning out!",
            "wps": 2.7,
            "emotion": "happy"
        },
        {
            "index": 2,
            "start": 30,
            "end": 45,
            "text": "Now I'll speak more calmly to demonstrate different emotions.",
            "wps": 1.8,
            "emotion": "calm"
        },
        {
            "index": 3,
            "start": 45,
            "end": 60,
            "text": "Wow! I can't believe how well this is working!",
            "wps": 3.2,
            "emotion": "surprised"
        },
        {
            "index": 4,
            "start": 60,
            "end": 75,
            "text": "This example is terrible! I hate it!",
            "wps": 2.5,
            "emotion": "angry"
        }
    ]
    
    # Display the emotion insights
    emotion_display.display_emotion_insights(sample_emotion_data, sample_transcription)
    
    # Display the WPS chart
    emotion_display.display_wps_chart(sample_transcription)