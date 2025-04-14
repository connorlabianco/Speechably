import streamlit as st
from typing import List, Tuple, Any, Optional

class CoachChat:
    """
    Component for handling the AI coach chat interface.
    Manages chat history and interactions with the Gemini service.
    """
    
    def __init__(self, gemini_service):
        """
        Initialize the coach chat component.
        
        Args:
            gemini_service: The GeminiService instance for generating responses
        """
        self.gemini_service = gemini_service
    
    def initialize_chat(self):
        """Initialize chat history in session state"""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "ai", "content": "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?"}
            ]
    
    def display_chat_interface(self, emotion_segments: List[Tuple[str, str]]):
        """
        Display an interactive chat interface for coaching with Gemini.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
        """
        # Initialize chat history if needed
        self.initialize_chat()
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""<div class="user-message">{message["content"]}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="ai-message">{message["content"]}</div>""", unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input("Ask your AI coach a question", key="user_message")
        
        # Create columns for send and reset buttons
        col1, col2 = st.columns([1, 5])
        
        with col1:
            send_pressed = st.button("Send", key="send_message")
        
        with col2:
            reset_pressed = st.button("Reset Chat", key="reset_chat")
        
        if send_pressed:
            if user_input:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Format emotion segments for context
                emotion_context = "\n".join([f"{time_range}: {emotion}" for time_range, emotion in emotion_segments])
                
                # Show AI thinking animation
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("""<div class="ai-thinking">Thinking...</div>""", unsafe_allow_html=True)
                
                # Generate response
                ai_response = self.gemini_service.generate_chat_response(user_input, emotion_context)
                
                # Remove thinking animation
                thinking_placeholder.empty()
                
                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "ai", "content": ai_response})
                
                # Force a rerun to update the chat display
                st.rerun()
        
        # Handle reset button
        if reset_pressed:
            st.session_state.chat_history = [
                {"role": "ai", "content": "👋 I'm your AI speech coach. I've analyzed your speech patterns and emotions. What would you like to improve today?"}
            ]
            st.rerun()
    
    def get_coaching_tip(self, emotion_segments: List[Tuple[str, str]], area: str = "general") -> str:
        """
        Get a quick coaching tip based on emotion data.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            area: Area of focus for the tip
            
        Returns:
            A coaching tip string
        """
        # Count emotions
        emotions = [emotion for _, emotion in emotion_segments]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Get most common emotion
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral"
        
        # Create a prompt for a quick tip
        emotion_context = "\n".join([f"{time_range}: {emotion}" for time_range, emotion in emotion_segments])
        prompt = f"""
        As a speech coach, give ONE quick tip (1-2 sentences) for a speaker whose dominant emotion was {dominant_emotion}.
        Focus on {area} advice.
        Be specific, actionable, and encouraging.
        """
        
        # Generate response
        try:
            tip = self.gemini_service.generate_chat_response(prompt, emotion_context)
            return tip
        except Exception:
            # Fallback tips if Gemini fails
            fallback_tips = {
                "angry": "Try to breathe deeply before speaking to moderate your tone. Your passion is good, but balancing it will help your message land better.",
                "calm": "Your calm delivery is excellent; now try adding subtle variation in tone at key points to emphasize important ideas.",
                "sad": "Try lifting your voice slightly at the end of statements to avoid a downward pattern that can sound melancholy.",
                "surprised": "Channel your energy into deliberate emphasis rather than letting it spread across your whole delivery.",
                "happy": "Your enthusiasm comes through well; focus on slowing down slightly at key points so your audience can absorb your message.",
                "neutral": "Try adding more vocal variation to engage your audience. Identify 2-3 key points where you can add emphasis or change your pace."
            }
            return fallback_tips.get(dominant_emotion, "Focus on varying your tone and pace to engage your audience more effectively.")


# Example usage if run directly
if __name__ == "__main__":
    # This would be used for local testing
    import sys
    from pathlib import Path
    
    # Add project root to Python path
    project_root = Path(__file__).parent.parent.parent
    sys.path.append(str(project_root))
    
    from backend.gemini_service import GeminiService
    
    # Set up a simple Streamlit test page
    st.set_page_config(page_title="Coach Chat Test", layout="wide")
    st.title("Coach Chat Component Test")
    
    # Add custom styles for chat bubbles
    st.markdown("""
    <style>
    .user-message {
        background-color: rgba(100, 149, 237, 0.3);
        border-radius: 10px;
        padding: 8px 12px;
        margin: 5px 0;
        align-self: flex-end;
        max-width: 80%;
    }
    
    .ai-message {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 8px 12px;
        margin: 5px 0;
        align-self: flex-start;
        max-width: 80%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize components
    gemini_service = GeminiService()
    coach_chat = CoachChat(gemini_service)
    
    # Sample emotion data
    sample_emotion_data = [
        ("00:00 - 00:15", "calm"),
        ("00:15 - 00:30", "happy"),
        ("00:30 - 00:45", "calm"),
        ("00:45 - 01:00", "surprised"),
        ("01:00 - 01:15", "angry")
    ]
    
    # Display the chat interface
    coach_chat.display_chat_interface(sample_emotion_data)
    
    # Show a sample quick tip
    st.subheader("Sample Quick Tip")
    tip = coach_chat.get_coaching_tip(sample_emotion_data)
    st.info(tip)