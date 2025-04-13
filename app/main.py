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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Initialize session state for storing analysis results
if "emotion_segments" not in st.session_state:
    st.session_state.emotion_segments = None

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

# Initialize Gemini (uncomment and add your API key when ready)
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

def analyze_with_gemini(model, emotion_segments, video_context=None):
    """Use Gemini to analyze speech patterns and provide coaching feedback"""
    if model is None:
        return {
            "summary": "Gemini analysis not available. Please check your API key configuration.",
            "improvement_areas": [],
            "strengths": [],
            "coaching_tips": []
        }
    
    # Format emotion segments for Gemini
    emotion_timeline = "\n".join([f"{time_range}: {emotion}" for time_range, emotion in emotion_segments])
    
    # Create prompt for Gemini
    prompt = f"""
    You are a professional speech coach helping someone improve their communication skills.
    Analyze the following emotion timeline from a speech:
    
    {emotion_timeline}
    
    Based on this emotional pattern:
    1. Provide a brief summary of the speaker's emotional journey
    2. Identify 3 specific areas for improvement
    3. Point out 2-3 emotional strengths
    4. Give 3-5 practical coaching tips to help the speaker improve
    
    Format your response as JSON with fields: summary, improvement_areas (array), strengths (array), and coaching_tips (array).
    """
    
    try:
        # Get response from Gemini
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Extract JSON data from response
        import json
        import re
        
        # Look for JSON pattern in the response
        json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find any JSON-like structure
            json_str = response_text
            
        # Clean up the string if needed
        json_str = json_str.replace('```json', '').replace('```', '').strip()
        
        try:
            analysis_data = json.loads(json_str)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured response manually
            analysis_data = {
                "summary": "Unable to parse Gemini's response as JSON. Here's the raw analysis:",
                "improvement_areas": ["See summary for details"],
                "strengths": ["See summary for details"],
                "coaching_tips": ["See summary for details"]
            }
            analysis_data["raw_response"] = response_text
            
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

def display_emotion_insights(emotion_data):
    """Display visualizations and insights about emotion patterns"""
    # Convert emotion data to DataFrame for analysis
    emotion_df = pd.DataFrame(emotion_data, columns=["Time Range", "Emotion"])
    
    # Count occurrences of each emotion
    emotion_counts = emotion_df["Emotion"].value_counts()
    
    # Calculate diversity of emotions
    emotion_diversity = len(emotion_counts)
    
    # Create visualizations
    st.subheader("🚀 Emotion Distribution")
    
    # Display emotion counts as a horizontal bar chart
    st.bar_chart(emotion_counts)
    
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
            # Reset chat history when uploading a new file
            if "chat_history" in st.session_state:
                st.session_state.chat_history = [
                    {"role": "ai", "content": "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?"}
                ]
        
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
                
                # Show processing status
                with st.spinner("🛰️ Processing video and extracting audio segments..."):
                    # Extract full audio and split into segments
                    full_audio_path, segment_paths = segmenter.extract_and_split_audio(temp_video_path, output_dir)
                    
                    # Get total duration of the full audio
                    total_duration = get_audio_duration(full_audio_path, segmenter.config.ffmpeg_path)
                    
                    # Analyze the segments
                    results = analyzer.analyze_segments(output_dir)
                    
                    # Calculate and store timestamps for each segment
                    current_time = 0
                    emotion_segments = []
                    
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
                        
                        time_range = f"{start_time} - {end_time}"
                        emotion_segments.append((time_range, emotion))
                        
                        current_time += segment_duration
                    
                    # Store the results in session state
                    st.session_state.emotion_segments = emotion_segments
                    st.session_state.analysis_complete = True
                
                st.success("✅ Analysis complete! Here's your mission readout:")
            else:
                st.success("✅ Using cached analysis results!")
            
            # Get emotion segments from session state
            emotion_segments = st.session_state.emotion_segments
            
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
                
                # Display emotion analytics
                display_emotion_insights(emotion_segments)
                
                # Display AI analysis from Gemini
                st.markdown("### 🔍 Gemini Analysis")
                
                # Check if we already have an analysis result in session state
                if "gemini_analysis" not in st.session_state:
                    with st.spinner("🌌 Analyzing speech patterns with Gemini..."):
                        analysis_result = analyze_with_gemini(gemini_model, emotion_segments)
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