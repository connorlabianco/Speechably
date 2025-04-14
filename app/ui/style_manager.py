import streamlit as st
from typing import Optional

class StyleManager:
    """
    Manages styling and UI configuration for the Streamlit application.
    Uses calming colors and simple layout to reduce anxiety.
    """
    
    def __init__(self, background_image_path: Optional[str] = None):
        """
        Initialize the style manager.
        Background image parameter kept for backward compatibility but not used.
        
        Args:
            background_image_path: Not used
        """
        pass
    
    @staticmethod
    def configure_page():
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Speechably - Speech Emotion Analysis",
            page_icon="🎙️",
            layout="wide"
        )
    
    def apply_custom_styling(self):
        """Apply custom CSS styling to the Streamlit app"""
        st.markdown(self._get_css_styles(), unsafe_allow_html=True)
    
    def _get_css_styles(self) -> str:
        """
        Generate CSS styles for the application.
        Uses a calming color palette with soft blues and greens.
            
        Returns:
            CSS styles as a string
        """
        return """
        <style>
        /* Main app styling with calming colors */
        .stApp {
            background-color: #f0f4f8;
        }

        .main .block-container {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            margin: 1rem auto;
        }

        /* Typography with softer colors */
        h1 {
            color: #3a7ca5 !important;
            font-weight: 600;
            border-bottom: 1px solid #e6eef7;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        
        h2, h3 {
            color: #2c6e8e !important;
            font-weight: 500;
        }
        
        p, label {
            color: #2c3e50 !important;
        }

        /* UI elements with softer styling */
        .stButton>button {
            background-color: #7ec8e3 !important;
            color: #05445e !important;
            border-radius: 6px;
            border: none;
            padding: 0.3rem 1rem;
            font-weight: 500;
        }
        
        .stButton>button:hover {
            background-color: #6db5d9 !important;
        }

        .stFileUploader>div {
            background-color: #fff !important;
            border: 1px dashed #7ec8e3;
            border-radius: 6px;
        }

        .stSpinner>div {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 6px;
        }
        
        .stSuccess {
            background-color: #d4edda !important;
            color: #155724 !important;
            border-radius: 6px;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: 1px solid #e6eef7;
            padding-bottom: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #f8fafc;
            border-radius: 6px 6px 0 0;
            padding: 8px 16px;
            color: #5c7080;
            border: 1px solid #e6eef7;
            border-bottom: none;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
            color: #3a7ca5 !important;
            border-bottom: 2px solid #3a7ca5;
        }

        /* Chat styling */
        .chat-container {
            background-color: #f8fafc;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #e6eef7;
        }
        
        .user-message {
            background-color: #e6eef7;
            border-radius: 8px;
            padding: 10px 15px;
            margin: 8px 0;
            align-self: flex-end;
            max-width: 80%;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
        
        .ai-message {
            background-color: #f0f7f4;
            border-radius: 8px;
            padding: 10px 15px;
            margin: 8px 0;
            align-self: flex-start;
            max-width: 80%;
            border-left: 3px solid #7ec8e3;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
        
        /* Card styling */
        .insight-card {
            background-color: #f8fafc;
            border-radius: 8px;
            padding: 15px;
            margin: 12px 0;
            border-left: 3px solid #3a7ca5;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .transcript-card {
            background-color: #f8fafc;
            border-radius: 8px;
            padding: 15px;
            margin: 12px 0;
            border-left: 3px solid #75b9be;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        /* Progress meter */
        .progress-container {
            background-color: #e9ecef;
            border-radius: 6px;
            height: 20px;
            width: 100%;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 6px;
            text-align: center;
            line-height: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        /* Pulse animation */
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
        
        .ai-thinking {
            animation: pulse 1.5s infinite;
            background-color: #f0f7f4;
            border-radius: 8px;
            padding: 8px 12px;
            display: inline-block;
            border-left: 3px solid #7ec8e3;
        }

        /* Chart styling */
        [data-testid="stChart"] {
            background-color: #ffffff !important;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #e6eef7;
        }
        </style>
        """
    
    @staticmethod
    def add_custom_element(html_content: str):
        """
        Add a custom HTML element to the UI.
        
        Args:
            html_content: HTML content to render
        """
        st.markdown(html_content, unsafe_allow_html=True)
    
    @staticmethod
    def add_spacer(height: int = 1):
        """
        Add vertical space to the UI.
        
        Args:
            height: Height of the spacer in ems
        """
        st.markdown(f"<div style='margin-top: {height}em;'></div>", unsafe_allow_html=True)
    
    @staticmethod
    def add_fancy_header(text: str, icon: Optional[str] = None, level: int = 2):
        """
        Add a fancy styled header to the UI.
        
        Args:
            text: Header text
            icon: Optional emoji icon
            level: Header level (1-6)
        """
        icon_html = f"{icon} " if icon else ""
        st.markdown(
            f"<h{level} style='color:#2c6e8e; background-color:#f0f7f4; "
            f"padding:10px; border-radius:6px; border-left:3px solid #3a7ca5;'>"
            f"{icon_html}{text}</h{level}>", 
            unsafe_allow_html=True
        )


# Example usage if run directly
if __name__ == "__main__":
    # This would be used for local testing
    
    # Initialize style manager
    style_manager = StyleManager()
    
    # Configure page
    StyleManager.configure_page()
    
    # Apply custom styling
    style_manager.apply_custom_styling()
    
    # Test UI elements
    st.title("Speechably Style Test")
    
    style_manager.add_fancy_header("Speech Analysis Results", "🎙️", 2)
    style_manager.add_spacer(1)
    
    st.write("This is a test of the new calming style for Speechably.")
    
    # Test tabs
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🧠 Insights", "💬 Coach"])
    
    with tab1:
        st.write("This is the analysis tab")
        st.metric("Speaking Rate", "2.4 WPS", "Good")
    
    with tab2:
        style_manager.add_custom_element("""
        <div class="insight-card">
            <h4>Key Insight</h4>
            <p>Your speech shows good emotional variation and clear articulation.</p>
        </div>
        """)
    
    with tab3:
        st.write("Chat with your coach:")
        style_manager.add_custom_element("""
        <div class="ai-message">
            How can I help you improve your speech today?
        </div>
        """)
        style_manager.add_custom_element("""
        <div class="user-message">
            How can I reduce filler words?
        </div>
        """)
        style_manager.add_custom_element("""
        <div class="ai-thinking">
            Thinking...
        </div>
        """)