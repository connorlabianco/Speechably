import streamlit as st
import tempfile
from pathlib import Path
import sys
import os
import base64
from moviepy.editor import VideoFileClip
import subprocess
import re
import google.generativeai as genai
import pandas as pd
import time
import json
import numpy as np
import torch
import whisper
from dotenv import load_dotenv
import plotly.express as px

# Load environment variables from .env file
load_dotenv()

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.speech_analysis import SpeechAnalyzer
from backend.segment_and_extract import AudioSegmenter, AudioSegmenterConfig

# Set FFmpeg path
FFMPEG_PATH = r"C:\Users\MCCLAB1200WL744\Downloads\ffmpeg-7.1.1-essentials_build (1)\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
os.environ['PATH'] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ['PATH']

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
    
    /* Styling for the tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: white;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: rgba(255, 255, 255, 0.25);
        border-bottom: 2px solid #ff6b6b;
    }}
    
    /* Chat container styling */
    .chat-container {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
    }}
    
    .user-message {{
        background-color: rgba(100, 149, 237, 0.3);
        border-radius: 10px;
        padding: 8px 12px;
        margin: 5px 0;
        align-self: flex-end;
        max-width: 80%;
    }}
    
    .ai-message {{
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 8px 12px;
        margin: 5px 0;
        align-self: flex-start;
        max-width: 80%;
    }}
    
    /* Insights card styling */
    .insight-card {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #ff6b6b;
    }}
    
    /* Transcript card styling */
    .transcript-card {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #6495ed;
    }}
    
    /* Ensure all text in insight cards is white */
    .insight-card h4, .insight-card p, .insight-card li {{
        color: white !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
    }}
    
    /* Progress meter styling */
    .progress-container {{
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        height: 25px;
        width: 100%;
        margin: 10px 0;
        position: relative;
    }}
    
    .progress-bar {{
        height: 100%;
        border-radius: 10px;
        text-align: center;
        line-height: 25px;
        color: white;
        font-weight: bold;
    }}
    
    /* Pulse animation for AI thinking */
    @keyframes pulse {{
        0% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.6; }}
    }}
    
    .ai-thinking {{
        animation: pulse 1.5s infinite;
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 10px;
        display: inline-block;
    }}

    /* Ensure all text in Gemini insights is white */
    .stTabs [data-baseweb="tab-panel"] p, 
    .stTabs [data-baseweb="tab-panel"] li, 
    .stTabs [data-baseweb="tab-panel"] span, 
    .stTabs [data-baseweb="tab-panel"] text, 
    .stTabs [data-baseweb="tab-panel"] .stMarkdown, 
    .stTabs [data-baseweb="tab-panel"] .st-emotion-cache-beoj2j, 
    .stTabs [data-baseweb="tab-panel"] .st-emotion-cache-9aoz2h, 
    .stTabs [data-baseweb="tab-panel"] .metric-value, 
    .stTabs [data-baseweb="tab-panel"] .metric-label {{
        color: white !important;
        fill: white !important;
    }}

    /* Set emotion distribution chart background color */
    .stTabs [data-baseweb="tab-panel"] [data-testid="stChart"] {{
        background-color: #343D46 !important;
        border-radius: 8px;
        padding: 10px;
    }}

    /* Ensure axis labels and tick marks are white */
    .stTabs [data-baseweb="tab-panel"] [data-testid="stChart"] g text {{
        fill: white !important;
    }}

    /* Make metric container text white */
    .stTabs [data-baseweb="tab-panel"] .st-emotion-cache-1xarl3l, 
    .stTabs [data-baseweb="tab-panel"] .st-emotion-cache-1wivap2 {{
        color: white !important;
    }}

    /* Make metric delta text white */
    .stTabs [data-baseweb="tab-panel"] .st-emotion-cache-5hmhkg {{
        color: white !important;
    }}

    /* Make chart legends white */
    .stTabs [data-baseweb="tab-panel"] [data-testid="stChart"] text {{
        fill: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Initialize the speech analyzer and audio segmenter
analyzer = SpeechAnalyzer()
segmenter = AudioSegmenter()  # Using default configuration

# Initialize Whisper model
@st.cache_resource
def load_whisper_model():
    try:
        return whisper.load_model("tiny")
    except Exception as e:
        st.error(f"Error loading Whisper model: {str(e)}")
        return None

whisper_model = load_whisper_model()

# Function to transcribe segments using Whisper
def transcribe_segments(segment_paths, segment_duration):
    """
    Transcribe audio segments using the Whisper model
    """
    if not whisper_model:
        st.error("Whisper model not loaded. Please check the error message above.")
        return []
        
    transcripts = []
    
    for i, segment_path in enumerate(segment_paths):
        if not os.path.exists(segment_path):
            st.error(f"Segment file not found: {segment_path}")
            continue
            
        try:
            # Get emotion from analyzer results if available
            emotion = st.session_state.emotion_segments[i][1] if hasattr(st.session_state, 'emotion_segments') else "unknown"
            
            # Calculate segment times
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration
            
            # Transcribe with Whisper
            result = whisper_model.transcribe(segment_path)
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
        except Exception as e:
            st.error(f"Error transcribing segment {i+1}: {str(e)}")
            continue
    
    return transcripts

# Function to format time for display
def format_time(seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    seconds_remainder = int(seconds % 60)
    return f"{minutes:02d}:{seconds_remainder:02d}"

# Function to generate Gemini prompt
def generate_gemini_prompt(transcription_data):
    """
    Generate a formatted prompt for Gemini based on speech analysis.
    """
    # Create the formatted timeline for reference
    timeline_blocks = []
    issues = []
    
    for segment in transcription_data:
        # Format times
        start_time = format_time(segment["start"])
        end_time = format_time(segment["end"])
        
        # Create formatted block
        block = (
            f"{start_time}-{end_time} | "
            f"WPS: {segment['wps']:.2f} | "
            f"Emotion: {segment['emotion']} | "
            f"Text: \"{segment['text']}\""
        )
        
        timeline_blocks.append(block)
        
        # Check for issues
        if segment["wps"] > 3.0:
            issues.append(f"- Segment at {start_time}-{end_time} is too fast ({segment['wps']:.2f} WPS)")
        elif segment["wps"] < 1.0:
            issues.append(f"- Segment at {start_time}-{end_time} is too slow ({segment['wps']:.2f} WPS)")
    
    # Calculate WPS statistics for overall feedback
    wps_values = [segment["wps"] for segment in transcription_data]
    avg_wps = sum(wps_values) / len(wps_values) if wps_values else 0
    wps_variation = max(wps_values) - min(wps_values) if wps_values else 0
    
    # Count emotion transitions
    emotion_transitions = 0
    for i in range(1, len(transcription_data)):
        if transcription_data[i]["emotion"] != transcription_data[i-1]["emotion"]:
            emotion_transitions += 1
    
    # Build the prompt
    prompt = f"""
You are a professional speech coach analyzing speech transcript data. The following is a timeline of speech segments with transcriptions, speaking rate (words per second), and detected emotions:

{chr(10).join(block for block in timeline_blocks)}

Based on this data, provide constructive feedback on:

1. Speaking Rate:
   - Average speaking rate: {avg_wps:.2f} WPS (optimal is 2.0-3.0 WPS)
   - Rate variation: {wps_variation:.2f} WPS (higher variation can indicate better engagement)
   - Specific segments to improve:
     {chr(10).join(f'     {issue}' for issue in issues) if issues else '     None identified'}

2. Emotional Expression:
   - Number of emotion transitions: {emotion_transitions}
   - Evaluate whether the emotions match the content of each segment
   - Suggest where emotional variety could improve engagement

3. Clarity and Enunciation:
   - Identify any unclear or nonsensical phrases that suggest poor enunciation
   - Suggest specific techniques to improve clarity

4. Overall Presentation:
   - Provide 3-5 specific action items to improve this speech
   - Suggest a practice exercise tailored to this speaker's needs

Format your response in JSON with the following structure:
{{
  "summary": "Your overall analysis and key observations",
  "improvement_areas": ["Area 1", "Area 2", "Area 3"],
  "strengths": ["Strength 1", "Strength 2"],
  "coaching_tips": ["Tip 1", "Tip 2", "Tip 3"]
}}
"""
    
    return prompt

# Initialize session state for storing analysis results
if "emotion_segments" not in st.session_state:
    st.session_state.emotion_segments = None

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if "transcription_data" not in st.session_state:
    st.session_state.transcription_data = None

# Initialize Gemini
def init_gemini():
    # Initialize Gemini API
    try:
        # Get API key from environment variable
        API_KEY = os.environ.get("GEMINI_API_KEY")
        if not API_KEY:
            st.error("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
            return None
            
        genai.configure(api_key=API_KEY)
        
        # Set up the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")
        return None

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

def analyze_with_gemini(model, emotion_segments, transcription_data=None, video_context=None):
    """Use Gemini to analyze speech patterns and provide coaching feedback"""
    if model is None:
        return {
            "summary": "Gemini analysis not available. Please check your API key configuration.",
            "improvement_areas": [],
            "strengths": [],
            "coaching_tips": []
        }
    
    # If we have transcription data, use that to generate a more detailed prompt
    if transcription_data:
        prompt = generate_gemini_prompt(transcription_data)
    else:
        # Fallback to simpler prompt with just emotion segments
        emotion_timeline = "\n".join([f"{time_range}: {emotion}" for time_range, emotion in emotion_segments])
        
        prompt = f"""
        You are a professional speech coach helping someone improve their communication skills.
        Analyze the following emotion timeline from a speech:
        
        {emotion_timeline}
        
        Based on this emotional pattern:
        1. Provide a brief summary of the speaker's emotional journey
        2. Identify 3 specific areas for improvement
        3. Point out 2-3 emotional strengths
        4. Give 3-5 practical coaching tips to help the speaker improve
        
        Format your response in JSON with the following structure:
        {{
          "summary": "Your overall analysis and key observations",
          "improvement_areas": ["Area 1", "Area 2", "Area 3"],
          "strengths": ["Strength 1", "Strength 2"],
          "coaching_tips": ["Tip 1", "Tip 2", "Tip 3"]
        }}
        """
    
    try:
        # Get response from Gemini
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Extract JSON data from response
        try:
            # First try direct JSON parsing
            analysis_data = json.loads(response_text)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON using regex
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find any JSON-like structure with curly braces
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    # Fallback to raw text
                    json_str = response_text
            
            # Clean up the string
            json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            try:
                analysis_data = json.loads(json_str)
            except json.JSONDecodeError:
                # If JSON parsing still fails, create a structured response manually
                analysis_data = {
                    "summary": response_text,
                    "improvement_areas": ["Please see summary for details"],
                    "strengths": ["Please see summary for details"],
                    "coaching_tips": ["Please see summary for details"]
                }
            
        return analysis_data
        
    except Exception as e:
        return {
            "summary": f"Error during Gemini analysis: {str(e)}",
            "improvement_areas": ["Unable to analyze with Gemini at this time"],
            "strengths": [],
            "coaching_tips": ["Try again later or check your API configuration"]
        }

def display_gemini_chat(model, emotion_segments):
    """Display an interactive chat interface for coaching with Gemini"""
    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "ai", "content": "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?"}
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""<div class="user-message">{message["content"]}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="ai-message">{message["content"]}</div>""", unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask your AI coach a question", key="user_message")
    
    if st.button("Send", key="send_message"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            if model:
                # Show AI thinking animation
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("""<div class="ai-thinking">Thinking...</div>""", unsafe_allow_html=True)
                
                # Format emotion segments for context
                emotion_context = "\n".join([f"{time_range}: {emotion}" for time_range, emotion in emotion_segments])
                
                # Create prompt for Gemini
                prompt = f"""
                You are a supportive and knowledgeable speech coach helping someone improve their communication.
                
                The user's speech had these emotional patterns:
                {emotion_context}
                
                The user is asking: "{user_input}"
                
                Provide helpful, specific coaching advice related to their question. Be encouraging but honest.
                Keep your response concise (3-5 sentences) unless detailed instructions are needed.
                """
                
                try:
                    # Get response from Gemini
                    response = model.generate_content(prompt)
                    ai_response = response.text.strip()
                    
                    # Remove thinking animation
                    thinking_placeholder.empty()
                    
                    # Add AI response to chat history
                    st.session_state.chat_history.append({"role": "ai", "content": ai_response})
                    
                    # Force a rerun to update the chat display
                    st.rerun()
                except Exception as e:
                    thinking_placeholder.empty()
                    st.session_state.chat_history.append({"role": "ai", "content": f"I'm having trouble generating a response right now. Error: {str(e)}"})
                    st.rerun()
            else:
                st.session_state.chat_history.append({"role": "ai", "content": "I'm not available right now. Please check the Gemini API configuration."})
                st.rerun()

def display_emotion_insights(emotion_data, transcription_data=None):
    """Display visualizations and insights about emotion patterns"""
    # Convert emotion data to DataFrame for analysis
    emotion_df = pd.DataFrame(emotion_data, columns=["Time Range", "Emotion"])
    
    # Create a new column with numeric start time for plotting
    emotion_df["Start Time"] = emotion_df["Time Range"].apply(lambda x: x.split(" - ")[0])
    emotion_df["End Time"] = emotion_df["Time Range"].apply(lambda x: x.split(" - ")[1])
    
    # Convert MM:SS format to seconds for plotting
    def time_to_seconds(time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds
    
    emotion_df["Start Seconds"] = emotion_df["Start Time"].apply(time_to_seconds)
    emotion_df["End Seconds"] = emotion_df["End Time"].apply(time_to_seconds)
    emotion_df["Mid Seconds"] = (emotion_df["Start Seconds"] + emotion_df["End Seconds"]) / 2
    
    # Count occurrences of each emotion
    emotion_counts = emotion_df["Emotion"].value_counts()
    
    # Calculate diversity of emotions
    emotion_diversity = len(emotion_counts)
    
    # Create visualizations
    st.subheader("🚀 Emotion Distribution")
    
    # Create emotion timeline chart
    # Create a plotly figure for emotion timeline
    fig = px.line(
        emotion_df, 
        x="Mid Seconds", 
        y="Emotion",
        markers=True,
        color_discrete_sequence=["#ff6b6b", "#6495ed", "#ffd700", "#7cfc00", "#9370db"],
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
    
    # Display the plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Display emotion diversity metrics
    st.markdown("### 🌟 Emotion Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Dominant Emotion", emotion_counts.index[0] if not emotion_counts.empty else "None")
        
        # Display emotion consistency as a percentage
        if len(emotion_df) > 0:
            main_emotion_percentage = (emotion_counts.iloc[0] / len(emotion_df)) * 100
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {main_emotion_percentage}%; background-color: rgba(255, 107, 107, 0.7);">
                    {main_emotion_percentage:.1f}%
                </div>
            </div>
            <p>Consistency of dominant emotion</p>
            """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Emotional Range", f"{emotion_diversity} emotions")
        
        # Display emotional versatility score
        versatility_score = min(emotion_diversity / 5 * 100, 100)  # Normalize to 100%
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {versatility_score}%; background-color: rgba(100, 149, 237, 0.7);">
                {versatility_score:.1f}%
            </div>
        </div>
        <p>Emotional versatility score</p>
        """, unsafe_allow_html=True)
    
    # Show emotion transitions
    st.markdown("### 🔄 Emotion Transitions")
    
    if len(emotion_df) > 1:
        # Create a list of transitions
        transitions = []
        for i in range(len(emotion_df) - 1):
            from_emotion = emotion_df.iloc[i]["Emotion"]
            to_emotion = emotion_df.iloc[i+1]["Emotion"]
            if from_emotion != to_emotion:
                transitions.append(f"{from_emotion} → {to_emotion}")
        
        if transitions:
            for transition in transitions:
                st.markdown(f"- {transition}")
        else:
            st.write("No emotion transitions detected.")
    else:
        st.write("Not enough data to analyze transitions.")
        
    # Display transcription data if available
    if transcription_data:
        st.markdown("### 📝 Speech Transcription")
        
        for segment in transcription_data:
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
                
            # Determine emotion color
            emotion_color = "#ffffff"  # Default white
            if segment["emotion"] == "angry":
                emotion_color = "#ff6b6b"
            elif segment["emotion"] == "calm":
                emotion_color = "#6495ed"
            elif segment["emotion"] == "sad":
                emotion_color = "#9370db"
            elif segment["emotion"] == "surprised":
                emotion_color = "#ffd700"
            elif segment["emotion"] == "happy":
                emotion_color = "#7cfc00"
            
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

def main():
    st.title("🪐 Speechably - Speech Emotion Analysis")
    st.write("Upload an MP4 video to analyze speech emotions across different segments. Boost your delivery and launch your confidence.")

    # Initialize Gemini model
    gemini_model = init_gemini()

    # File uploader
    uploaded_file = st.file_uploader("🚀 Choose an MP4 file to analyze", type=["mp4"])
    
    if uploaded_file is not None:
        # Reset analysis state if a new file is uploaded
        if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
            st.session_state.current_file = uploaded_file.name
            st.session_state.analysis_complete = False
            st.session_state.emotion_segments = None
            st.session_state.transcription_data = None
            # Reset chat history when uploading a new file
            if "chat_history" in st.session_state:
                st.session_state.chat_history = [
                    {"role": "ai", "content": "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?"}
                ]
            # Reset Gemini analysis when uploading a new file
            if "gemini_analysis" in st.session_state:
                del st.session_state.gemini_analysis
        
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the uploaded file temporarily
            temp_video_path = os.path.join(temp_dir, "uploaded_video.mp4")
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the video only if analysis is not complete
            if not st.session_state.analysis_complete:
                # Create output directory for segments
                output_dir = os.path.join(temp_dir, "output_segments")
                os.makedirs(output_dir, exist_ok=True)
                
                # Show processing status
                with st.spinner("🛰️ Processing video and extracting audio segments..."):
                    # Extract full audio and split into segments
                    full_audio_path, segment_paths = segmenter.extract_and_split_audio(temp_video_path, output_dir)
                    
                    # Get total duration of the full audio
                    total_duration = get_audio_duration(full_audio_path, segmenter.config.ffmpeg_path)
                    
                    # Analyze the segments for emotions
                    results = analyzer.analyze_segments(output_dir)
                    
                    # Calculate and store timestamps for each segment
                    current_time = 0
                    emotion_segments = []
                    segment_durations = []
                    
                    for i, (filename, emotion) in enumerate(results.items()):
                        # Get the segment duration from the audio file
                        segment_path = os.path.join(output_dir, f"segment_{i+1}.wav")
                        segment_duration = get_audio_duration(segment_path, segmenter.config.ffmpeg_path)
                        segment_durations.append(segment_duration)
                        
                        start_time = format_timestamp(current_time)
                        # For the last segment, use the total duration instead of current_time + segment_duration
                        if i == len(results) - 1:
                            end_time = format_timestamp(total_duration)
                        else:
                            end_time = format_timestamp(current_time + segment_duration)
                        
                        time_range = f"{start_time} - {end_time}"
                        emotion_segments.append((time_range, emotion))
                        
                        current_time += segment_duration
                    
                    # Store emotion segments in session state
                    st.session_state.emotion_segments = emotion_segments
                    
                    # Transcribe each segment using Whisper and analyze speech patterns
                    with st.spinner("📝 Transcribing audio with Whisper..."):
                        # Get paths to all segment files
                        segment_files = [os.path.join(output_dir, f"segment_{i+1}.wav") for i in range(len(results))]
                        
                        # Calculate average segment duration (for WPS)
                        average_segment_duration = total_duration / len(segment_files)
                        
                        # Transcribe segments
                        transcription_data = transcribe_segments(segment_files, average_segment_duration)
                        
                        # Store transcription data
                        st.session_state.transcription_data = transcription_data
                        
                        # Save transcription data to JSON file for reference
                        json_path = os.path.join(output_dir, "snippet_transcripts.json")
                        with open(json_path, "w") as f:
                            json.dump(transcription_data, f, indent=4)
                    
                    st.session_state.analysis_complete = True
                
                st.success("✅ Analysis complete! Here's your mission readout:")
            else:
                st.success("✅ Using cached analysis results!")
            
            # Get emotion segments and transcription data from session state
            emotion_segments = st.session_state.emotion_segments
            transcription_data = st.session_state.transcription_data
            
            # Create tabs for different analysis views
            tab1, tab2, tab3 = st.tabs(["📊 Basic Analysis", "🧠 Gemini Insights", "💬 AI Coach"])
            
            with tab1:
                # Create two columns for results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🚀 Emotion Analysis")
                    # Display the emotion segments
                    for time_range, emotion in emotion_segments:
                        st.write(f"**{time_range}**: {emotion}")
                
                with col2:
                    st.subheader("🛰️ Video Playback")
                    # Display the full video
                    st.video(temp_video_path)
            
            with tab2:
                st.subheader("🧠 AI-Powered Speech Insights")
                
                # Display emotion analytics with transcription data
                display_emotion_insights(emotion_segments, transcription_data)
                
                # Display AI analysis from Gemini
                st.markdown("### 🔍 Gemini Analysis")
                
                # Check if we already have an analysis result in session state
                if "gemini_analysis" not in st.session_state:
                    with st.spinner("🌌 Analyzing speech patterns with Gemini..."):
                        # Use transcription data for enhanced analysis if available
                        analysis_result = analyze_with_gemini(gemini_model, emotion_segments, 
                                                              transcription_data=transcription_data)
                        # Cache the analysis in session state
                        st.session_state.gemini_analysis = analysis_result
                else:
                    analysis_result = st.session_state.gemini_analysis
                
                # Display analysis results
                st.markdown(f"""
                <div class="insight-card">
                    <h4>Summary</h4>
                    <p>{analysis_result["summary"]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🌟 Strengths")
                    for strength in analysis_result["strengths"]:
                        st.markdown(f"- {strength}")
                
                with col2:
                    st.markdown("#### 🔧 Areas for Improvement")
                    for area in analysis_result["improvement_areas"]:
                        st.markdown(f"- {area}")
                
                st.markdown("#### 📝 Coaching Tips")
                for i, tip in enumerate(analysis_result["coaching_tips"], 1):
                    st.markdown(f"{i}. {tip}")
                    
                # Add option to regenerate analysis
                if st.button("🔄 Regenerate Analysis"):
                    # Clear cached analysis
                    if "gemini_analysis" in st.session_state:
                        del st.session_state.gemini_analysis
                    st.rerun()
                    
                # Add a download button for the JSON data
                if transcription_data:
                    json_str = json.dumps(transcription_data, indent=4)
                    
                    st.download_button(
                        label="⬇️ Download Transcription Data (JSON)",
                        data=json_str,
                        file_name="snippet_transcripts.json",
                        mime="application/json"
                    )
            
            with tab3:
                st.subheader("💬 Ask Your AI Speech Coach")
                st.write("Chat with your AI speech coach for personalized advice based on your speech analysis.")
                
                # Display interactive chat interface
                display_gemini_chat(gemini_model, emotion_segments)
                
                # Add a reset button for the chat
                if st.button("Reset Chat"):
                    st.session_state.chat_history = [
                        {"role": "ai", "content": "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?"}
                    ]
                    st.rerun()

if __name__ == "__main__":
    main()