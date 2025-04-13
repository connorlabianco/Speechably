import streamlit as st
import tempfile
from pathlib import Path
import sys
import os

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.speech_analysis import SpeechAnalyzer
from backend.segment_and_extract import split_and_extract_audio

# Set page config
st.set_page_config(
    page_title="Speechably - Speech Emotion Analysis",
    page_icon="🎤",
    layout="wide"
)

# Initialize the speech analyzer
analyzer = SpeechAnalyzer()

def main():
    st.title("🎤 Speechably - Speech Emotion Analysis")
    st.write("Upload an MP4 video to analyze speech emotions in different segments")

    # File uploader
    uploaded_file = st.file_uploader("Choose an MP4 file", type=["mp4"])
    
    if uploaded_file is not None:
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the uploaded file temporarily
            temp_video_path = os.path.join(temp_dir, "uploaded_video.mp4")
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Create output directory for segments
            output_dir = os.path.join(temp_dir, "output_segments")
            
            # Show processing status
            with st.spinner("Processing video and extracting audio segments..."):
                # Split video and extract audio
                split_and_extract_audio(temp_video_path, output_dir)
                
                # Analyze the segments
                results = analyzer.analyze_segments(output_dir)
                
                # Display results
                st.success("Analysis complete!")
                
                # Create two columns for results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Emotion Analysis Results")
                    for filename, emotion in results.items():
                        st.write(f"**{filename}**: {emotion}")
                
                with col2:
                    st.subheader("🎥 Video Segments")
                    # Display video segments
                    for i in range(1, len(results) + 1):
                        video_path = os.path.join(output_dir, f"segment_{i}.mp4")
                        st.video(video_path)

if __name__ == "__main__":
    main()