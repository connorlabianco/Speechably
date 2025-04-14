import streamlit as st

# This MUST be the first Streamlit command
st.set_page_config(
    page_title="Speechably - Speech Emotion Analysis",
    page_icon=None,
    layout="wide"
)

import tempfile
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import backend components
from backend.speech_analysis import SpeechAnalyzer
from backend.segment_and_extract import AudioSegmenter
from backend.transcription_service import TranscriptionService
from backend.gemini_service import GeminiService
from backend.data_processor import DataProcessor
from backend.visualization_helper import VisualizationHelper

# Import frontend components
from app.ui.style_manager import StyleManager
from app.components.emotion_display import EmotionDisplay
from app.components.gemini_insights import GeminiInsights
from app.components.coach_chat import CoachChat

# Set FFmpeg path - this should be configurable in a real application
FFMPEG_PATH = r"C:\Users\MCCLAB1200WL744\Downloads\ffmpeg-7.1.1-essentials_build (1)\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"

class SpeechablyApp:
    """
    Main application class for Speechably.
    Handles initialization of components and overall application flow.
    """
    
    def __init__(self):
        """Initialize the Speechably application"""
        # Initialize backend services
        self.speech_analyzer = SpeechAnalyzer()
        self.audio_segmenter = AudioSegmenter()
        self.transcription_service = TranscriptionService()
        self.gemini_service = GeminiService()
        self.data_processor = DataProcessor(FFMPEG_PATH)
        self.visualization_helper = VisualizationHelper()
        
        # Initialize UI components
        self.style_manager = StyleManager()
        self.emotion_display = EmotionDisplay(self.visualization_helper)
        self.gemini_insights = GeminiInsights(self.gemini_service)
        self.coach_chat = CoachChat(self.gemini_service)
        
        # Initialize session state if needed
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for storing analysis results"""
        if "emotion_segments" not in st.session_state:
            st.session_state.emotion_segments = None

        if "analysis_complete" not in st.session_state:
            st.session_state.analysis_complete = False

        if "transcription_data" not in st.session_state:
            st.session_state.transcription_data = None
    
    def run(self):
        """Run the Speechably application"""
        # Apply only custom styling
        self.style_manager.apply_custom_styling()
        
        # Render title and description
        st.title("Speechably - Speech Emotion Analysis")
        st.write("Upload an MP4 video to analyze speech emotions across different segments. Boost your delivery and launch your confidence.")
        
        # File upload and processing
        self._handle_file_upload()
    
    def _handle_file_upload(self):
        """Handle file upload and processing"""
        # File uploader
        uploaded_file = st.file_uploader("Choose an MP4 file to analyze", type=["mp4"])
        
        if uploaded_file is not None:
            # Reset analysis state if a new file is uploaded
            self._handle_new_file(uploaded_file.name)
            
            # Create a temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save the uploaded file temporarily
                temp_video_path = os.path.join(temp_dir, "uploaded_video.mp4")
                with open(temp_video_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process the video if analysis is not complete
                if not st.session_state.analysis_complete:
                    self._process_video(temp_video_path, temp_dir)
                else:
                    st.success("✅ Using cached analysis results!")
                
                # Display analysis results
                self._display_analysis_results(temp_video_path)
    
    def _handle_new_file(self, file_name):
        """
        Handle new file upload by resetting state.
        
        Args:
            file_name: Name of the uploaded file
        """
        if "current_file" not in st.session_state or st.session_state.current_file != file_name:
            st.session_state.current_file = file_name
            st.session_state.analysis_complete = False
            st.session_state.emotion_segments = None
            st.session_state.transcription_data = None
            
            # Reset chat history
            self.coach_chat.initialize_chat()
            
            # Reset Gemini analysis
            if "gemini_analysis" in st.session_state:
                del st.session_state.gemini_analysis
    
    def _process_video(self, video_path, temp_dir):
        """
        Process the uploaded video.
        
        Args:
            video_path: Path to the uploaded video file
            temp_dir: Temporary directory for storing outputs
        """
        # Create output directory for segments
        output_dir = os.path.join(temp_dir, "output_segments")
        os.makedirs(output_dir, exist_ok=True)
        
        # Show processing status
        with st.spinner("🛰️ Processing video and extracting audio segments..."):
            # Extract full audio and split into segments
            full_audio_path, segment_paths = self.audio_segmenter.extract_and_split_audio(video_path, output_dir)
            
            # Get total duration of the full audio
            total_duration = self.data_processor.get_audio_duration(full_audio_path)
            
            # Analyze the segments for emotions
            results = self.speech_analyzer.analyze_segments(output_dir)
            
            # Get segment durations
            segment_durations = [self.data_processor.get_audio_duration(path) for path in segment_paths]
            
            # Process emotion data into time-based segments
            emotion_segments = self.data_processor.process_emotion_data(results, total_duration, segment_durations)
            
            # Store emotion segments in session state
            st.session_state.emotion_segments = emotion_segments
            
            # Transcribe each segment using Whisper and analyze speech patterns
            with st.spinner("📝 Transcribing audio with Whisper..."):
                # Calculate average segment duration (for WPS)
                average_segment_duration = total_duration / len(segment_paths) if segment_paths else 0
                
                # Transcribe segments
                transcription_data = self.transcription_service.transcribe_segments(
                    segment_paths, 
                    average_segment_duration,
                    emotion_data=emotion_segments
                )
                
                # Store transcription data
                st.session_state.transcription_data = transcription_data
                
                # Save transcription data to JSON
                self.data_processor.save_transcription_data(output_dir, transcription_data)
            
            st.session_state.analysis_complete = True
        
        st.success("✅ Analysis complete! Here's your mission readout:")
    
    def _display_analysis_results(self, video_path):
        """
        Display analysis results in tabs.
        
        Args:
            video_path: Path to the video file for playback
        """
        # Get emotion segments and transcription data from session state
        emotion_segments = st.session_state.emotion_segments
        transcription_data = st.session_state.transcription_data
        
        # Create tabs for different analysis views
        tab1, tab2, tab3 = st.tabs(["📊 Basic Analysis", "🧠 Gemini Insights", "💬 AI Coach"])
        
        with tab1:
            # Create two columns for results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Emotion Analysis")
                # Display the emotion segments
                for time_range, emotion in emotion_segments:
                    st.write(f"**{time_range}**: {emotion}")
            
            with col2:
                st.subheader("🛰️ Video Playback")
                # Display the full video
                st.video(video_path)
        
        with tab2:
            # Display emotion analytics and Gemini insights
            self.emotion_display.display_emotion_insights(emotion_segments, transcription_data)
            self.gemini_insights.display_analysis(emotion_segments, transcription_data)
        
        with tab3:
            st.subheader("💬 Ask Your AI Speech Coach")
            st.write("Chat with your AI speech coach for personalized advice based on your speech analysis.")
            
            # Display interactive chat interface
            self.coach_chat.display_chat_interface(emotion_segments)


# Application entry point
def main():
    app = SpeechablyApp()
    app.run()

if __name__ == "__main__":
    main()