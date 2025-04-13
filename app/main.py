import streamlit as st
import tempfile
from pathlib import Path
import sys
import os
import base64

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.speech_analysis import SpeechAnalyzer
from backend.segment_and_extract import VideoSegmenter, VideoSegmenterConfig

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

# Initialize the speech analyzer and video segmenter
analyzer = SpeechAnalyzer()
segmenter = VideoSegmenter()  # Using default configuration

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
                # Split video and extract audio using the VideoSegmenter
                segments = segmenter.split_and_extract_audio(temp_video_path, output_dir)
                
                # Analyze the segments
                results = analyzer.analyze_segments(output_dir)
                
                # Display results
                st.success("✅ Analysis complete! Here's your mission readout:")
                
                # Create two columns for results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🚀 Emotion Analysis")
                    for filename, emotion in results.items():
                        st.write(f"**{filename}**: {emotion}")
                
                with col2:
                    st.subheader("🛰️ Segment Playback")
                    # Display video segments
                    for video_path, _ in segments:  # Using the returned segments list
                        st.video(video_path)

if __name__ == "__main__":
    main()
