import streamlit as st
import tempfile
from pathlib import Path
import sys
import os
import base64
from moviepy.editor import VideoFileClip
import subprocess
import re

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.speech_analysis import SpeechAnalyzer
from backend.segment_and_extract import AudioSegmenter, AudioSegmenterConfig

# Set page config
st.set_page_config(
    page_title="Speechably - Speech Emotion Analysis",
    page_icon="🪐",
    layout="wide"
)

# Get the absolute path to the background image
background_path = os.path.join(os.path.dirname(__file__), "background.png")

# Convert image to base64 for inline display
with open(background_path, "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()

# Add custom CSS for layout
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .main .block-container {{
        background: rgba(13, 17, 23, 0.85);
        padding: 42px 77px 126px;
        border-radius: 15px;
        margin-top: -2rem;
        position: relative;
        z-index: 1;
    }}

    h1, h2, h3, p, label {{
        color: white !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
    }}

    .stButton>button, .stFileUploader>div, .stSpinner>div, .stSuccess {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px;
        color: #111 !important;
    }}

    /* Make spinner text black */
    .stSpinner>div p {{
        color: #111 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Initialize the speech analyzer and audio segmenter
analyzer = SpeechAnalyzer()
segmenter = AudioSegmenter()  # Using default configuration

def format_timestamp(seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_audio_duration(audio_path: str, ffmpeg_path: str) -> float:
    """Get the duration of an audio file using FFmpeg."""
    cmd = [
        ffmpeg_path,
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

def main():
    st.title("🪐 Speechably - Speech Emotion Analysis")
    st.write("Upload an MP4 video to analyze speech emotions across different segments. Boost your delivery and launch your confidence.")

    # File uploader
    uploaded_file = st.file_uploader("🚀 Choose an MP4 file to analyze", type=["mp4"])
    
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
            with st.spinner("🛰️ Processing video and extracting audio segments..."):
                # Extract full audio and split into segments
                full_audio_path, segment_paths = segmenter.extract_and_split_audio(temp_video_path, output_dir)
                
                # Get total duration of the full audio
                total_duration = get_audio_duration(full_audio_path, segmenter.config.ffmpeg_path)
                
                # Analyze the segments
                results = analyzer.analyze_segments(output_dir)
                
                # Display results
                st.success("✅ Analysis complete! Here's your mission readout:")
                
                # Create two columns for results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🚀 Emotion Analysis")
                    # Calculate and display timestamps for each segment
                    current_time = 0
                    for i, (filename, emotion) in enumerate(results.items()):
                        # Get the segment duration from the audio file
                        segment_path = os.path.join(output_dir, f"segment_{i+1}.wav")
                        segment_duration = get_audio_duration(segment_path, segmenter.config.ffmpeg_path)
                        
                        start_time = format_timestamp(current_time)
                        # For the last segment, use the total duration instead of current_time + segment_duration
                        if i == len(results) - 1:
                            end_time = format_timestamp(total_duration)
                        else:
                            end_time = format_timestamp(current_time + segment_duration)
                        
                        st.write(f"**{start_time} - {end_time}**: {emotion}")
                        current_time += segment_duration
                
                with col2:
                    st.subheader("🛰️ Video Playback")
                    # Display the full video
                    st.video(temp_video_path)

if __name__ == "__main__":
    main()
