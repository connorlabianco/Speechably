import streamlit as st
import base64
import os
from typing import Optional

class StyleManager:
    """
    Manages styling and UI configuration for the Streamlit application.
    """
    
    def __init__(self, background_image_path: Optional[str] = None):
        """
        Initialize the style manager.
        
        Args:
            background_image_path: Optional path to background image (not used anymore)
        """
        pass  # We don't need to store the background path anymore
    
    @staticmethod
    def configure_page():
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Speechably - Speech Emotion Analysis",
            page_icon=None,
            layout="wide"
        )
    
    def apply_custom_styling(self):
        """Apply custom CSS styling to the Streamlit app"""
        # Add custom CSS directly without image processing
        st.markdown(self._get_css_styles(), unsafe_allow_html=True)
    
    def _get_css_styles(self, img_base64: Optional[str] = None) -> str:
        """
        Generate CSS styles for the application.
        
        Args:
            img_base64: Not used anymore, kept for compatibility
            
        Returns:
            CSS styles as a string
        """
        return """
        <style>
        /* Main app styling */
        .stApp {
            background-color: #778ffc;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .main .block-container {
            background: rgba(13, 17, 23, 0.85);
            padding: 42px 77px 126px;
            border-radius: 15px;
            margin-top: -2rem;
            position: relative;
            z-index: 1;
        }

        /* Typography */
        h1, h2, h3, p, label {{
            color: white !important;
            text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
        }}

        /* UI elements */
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
            f"<h{level} style='color:white; background-color:rgba(255,255,255,0.1); "
            f"padding:10px; border-radius:5px; border-left:4px solid #ff6b6b;'>"
            f"{icon_html}{text}</h{level}>", 
            unsafe_allow_html=True
        )


# Example usage if run directly
if __name__ == "__main__":
    # This would be used for local testing
    import sys
    from pathlib import Path
    
    # Set background path for testing
    bg_path = os.path.join(os.path.dirname(__file__), "..", "background.png")
    if not os.path.exists(bg_path):
        print(f"Warning: Background image not found at {bg_path}")
        # Use a fallback color instead
        bg_path = None
    
    # Initialize style manager
    style_manager = StyleManager(bg_path) if bg_path else None
    
    # Configure page
    StyleManager.configure_page()
    
    # Apply custom styling if background is available
    if style_manager:
        style_manager.apply_custom_styling()
    
    # Test UI elements
    st.title("Style Manager Test")
    
    if style_manager:
        style_manager.add_fancy_header("This is a fancy header", "🚀", 2)
        style_manager.add_spacer(2)
        
        style_manager.add_custom_element("""
        <div class="insight-card">
            <h4>Test Insight</h4>
            <p>This is a test of the custom styling capabilities.</p>
        </div>
        """)
    else:
        st.write("Background image not found, custom styling not applied.")