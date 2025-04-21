import streamlit as st
from typing import Optional

class StyleManager:
    """
    Modernized style manager for Speechably with a professional, clean aesthetic.
    """
    
    def __init__(self):
        """Initialize the style manager"""
        pass
    
    def apply_custom_styling(self):
        """Apply custom CSS styling to the Streamlit app"""
        st.markdown(self._get_css_styles(), unsafe_allow_html=True)
    
    def _get_css_styles(self) -> str:
        """
        Generate CSS styles for a clean, professional UI.
        Uses a light color scheme with clear typography and subtle accents.
            
        Returns:
            CSS styles as a string
        """
        return """
        <style>
        /* Base styles */
        :root {
            --primary: #4361ee;
            --primary-light: #eef2ff;
            --secondary: #3a0ca3;
            --accent: #f72585;
            --success: #06d6a0;
            --warning: #ffd166;
            --danger: #ef476f;
            --light-gray: #f8f9fa;
            --medium-gray: #e9ecef;
            --dark-gray: #343a40;
            --text: #212529;
            --text-light: #6c757d;
            --border-radius: 8px;
            --shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: var(--text) !important;
            font-weight: 600;
        }
        
        h1 {
            font-size: 1.8rem !important;
            letter-spacing: -0.02em;
        }
        
        h2 {
            font-size: 1.4rem !important;
            letter-spacing: -0.01em;
        }
        
        h3 {
            font-size: 1.2rem !important;
        }
        
        p, li, div, span {
            color: var(--text);
            font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
        }

        /* Main layout */
        .main .block-container {
            padding: 2rem 1.5rem !important;
            max-width: 1200px;
        }

        /* Custom components */
        .card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
            border: 1px solid var(--medium-gray);
        }
        
        .compact-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1rem;
            box-shadow: var(--shadow);
            margin-bottom: 0.75rem;
            border: 1px solid var(--medium-gray);
        }
        
        .metric-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1rem;
            text-align: center;
            box-shadow: var(--shadow);
            height: 100%;
            border: 1px solid var(--medium-gray);
        }
        
        .metric-card h4 {
            font-size: 0.875rem !important;
            color: var(--text-light) !important;
            margin-bottom: 0.5rem;
            font-weight: 400;
        }
        
        .metric-card .value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.25rem;
        }
        
        .metric-card .subtitle {
            font-size: 0.75rem;
            color: var(--text-light);
        }

        /* Feedback elements */
        .transcript-segment {
            padding: 1rem;
            border-radius: var(--border-radius);
            background: white;
            margin-bottom: 0.75rem;
            border-left: 3px solid var(--primary);
            transition: all 0.2s ease;
        }
        
        .transcript-segment:hover {
            box-shadow: var(--shadow);
        }
        
        .transcript-segment .timestamp {
            font-size: 0.75rem;
            color: var(--text-light);
            margin-bottom: 0.25rem;
        }
        
        .transcript-segment .metrics {
            display: flex;
            gap: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .transcript-segment .metrics .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        .transcript-segment .text {
            font-size: 1rem;
            line-height: 1.5;
        }
        
        /* Speed indicators */
        .speed-normal {
            background: var(--light-gray);
            color: var(--text) !important;
            font-weight: 500;
        }
        
        .speed-fast {
            background: rgba(239, 71, 111, 0.1);
            color: var(--danger);
            font-weight: bold;
        }
        
        .speed-slow {
            background: rgba(255, 209, 102, 0.1);
            color: #d68a00;
            font-style: italic;
        }
        
        /* Emotion badges */
        .emotion-badge {
            background: var(--primary-light);
            color: var(--primary);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 500;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: var(--border-radius) var(--border-radius) 0 0;
            color: var(--text-light);
            border: none;
            font-weight: 500;
            padding: 0 0.5rem;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: transparent;
            color: var(--primary) !important;
            border-bottom: 2px solid var(--primary);
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--primary) !important;
            color: white !important;
            font-weight: 500;
            padding: 0.5rem 1.25rem;
            border-radius: var(--border-radius);
            border: none;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--secondary) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .secondary-button button {
            background-color: white !important;
            color: var(--primary) !important;
            border: 1px solid var(--primary) !important;
        }
        
        .secondary-button button:hover {
            background-color: var(--primary-light) !important;
        }

        /* File uploader */
        .stFileUploader > div > label {
            background-color: var(--primary-light);
            color: var(--primary);
            border: 1px dashed var(--primary);
            border-radius: var(--border-radius);
            padding: 2.5rem 1rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .stFileUploader > div > label:hover {
            background-color: rgba(67, 97, 238, 0.1);
        }
        
        /* Progress bars */
        .progress-container {
            background-color: var(--medium-gray);
            border-radius: 4px;
            height: 8px;
            width: 100%;
            margin: 0.5rem 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 4px;
        }
        
        /* Charts */
        [data-testid="stChart"] {
            background-color: transparent !important;
            border-radius: var(--border-radius);
        }
        
        /* Toggles and expanders */
        .toggle-container {
            margin: 0.5rem 0;
        }
        
        .toggle-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            padding: 0.75rem;
            border-radius: var(--border-radius);
            background-color: var(--light-gray);
            transition: all 0.2s ease;
        }
        
        .toggle-header:hover {
            background-color: var(--medium-gray);
        }
        
        .toggle-content {
            padding: 0.75rem;
            border-radius: 0 0 var(--border-radius) var(--border-radius);
            border: 1px solid var(--medium-gray);
            border-top: none;
        }
        
        /* Chat components */
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .user-message {
            background-color: var(--primary-light);
            color: var(--text);
            padding: 0.75rem 1rem;
            border-radius: var(--border-radius);
            border-bottom-right-radius: 0;
            align-self: flex-end;
            max-width: 80%;
        }
        
        .ai-message {
            background-color: white;
            color: var(--text);
            padding: 0.75rem 1rem;
            border-radius: var(--border-radius);
            border-bottom-left-radius: 0;
            align-self: flex-start;
            max-width: 80%;
            box-shadow: var(--shadow);
        }
        
        /* Insights component */
        .insight-card {
            background-color: white;
            border-radius: var(--border-radius);
            padding: 1.25rem;
            margin-bottom: 1rem;
            border-left: 3px solid var(--primary);
            box-shadow: var(--shadow);
        }
        
        .insight-card h4 {
            margin: 0 0 0.5rem 0;
            color: var(--text) !important;
        }
        
        /* Mobile improvements */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem !important;
            }
            
            .transcript-segment {
                padding: 0.75rem;
            }
            
            .card, .compact-card, .metric-card {
                padding: 0.75rem;
            }
        }
        </style>
        """
    
    def add_metric_card(self, title: str, value: str, subtitle: Optional[str] = None):
        """
        Add a metric card to the UI.
        
        Args:
            title: Card title
            value: Main value to display
            subtitle: Optional subtitle or context
        """
        subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ''
        st.markdown(f"""
        <div class="metric-card">
            <h4>{title}</h4>
            <div class="value">{value}</div>
            {subtitle_html}
        </div>
        """, unsafe_allow_html=True)
    
    def render_transcript_segment(
        self, 
        text: str, 
        start_time: str, 
        end_time: str, 
        emotion: str, 
        wps: float,
        segment_id: str
    ):
        """
        Render a transcript segment with emotion and speed indicators.
        
        Args:
            text: Transcript text
            start_time: Start timestamp
            end_time: End timestamp
            emotion: Detected emotion
            wps: Words per second
            segment_id: Unique ID for the segment
        """
        # Determine speed class
        speed_class = "speed-normal"
        speed_text = f"{wps} WPS"
        if wps > 3.0:
            speed_class = "speed-fast"
            speed_text = f"{wps} WPS (too fast)"
        elif wps < 1.5:
            speed_class = "speed-slow"
            speed_text = f"{wps} WPS (too slow)"
        
        # Render the segment
        st.markdown(f"""
        <div class="transcript-segment" id="segment-{segment_id}">
            <div class="timestamp">{start_time} - {end_time}</div>
            <div class="metrics">
                <span class="emotion-badge">{emotion.capitalize()}</span>
                <span class="badge {speed_class}">{speed_text}</span>
            </div>
            <div class="text">{text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def create_expandable_section(self, title: str, content_function, expanded: bool = False):
        """
        Create an expandable section with a callback function for content.
        
        Args:
            title: Section title
            content_function: Function that generates section content
            expanded: Whether section is expanded by default
        """
        with st.expander(title, expanded=expanded):
            content_function()
    
    def create_toggle_section(self, title: str, content: str, default_open: bool = False):
        """
        Create a pure HTML toggle section using JavaScript.
        
        Args:
            title: Section title
            content: HTML content
            default_open: Whether section is open by default
        """
        section_id = "section_" + str(hash(title))
        display = "block" if default_open else "none"
        icon = "▼" if default_open else "▶"
        
        st.markdown(f"""
        <div class="toggle-container">
            <div class="toggle-header" onclick="toggleSection('{section_id}', this)">
                <span>{title}</span>
                <span id="icon_{section_id}">{icon}</span>
            </div>
            <div id="{section_id}" class="toggle-content" style="display: {display};">
                {content}
            </div>
        </div>
        <script>
        function toggleSection(id, element) {{
            var content = document.getElementById(id);
            var icon = document.getElementById('icon_' + id);
            if (content.style.display === 'none') {{
                content.style.display = 'block';
                icon.textContent = '▼';
            }} else {{
                content.style.display = 'none';
                icon.textContent = '▶';
            }}
        }}
        </script>
        """, unsafe_allow_html=True)

# Add helper for emotion colors
def get_emotion_color(emotion: str) -> str:
    """Get CSS color for an emotion."""
    emotion_colors = {
        "angry": "var(--danger)",
        "calm": "var(--primary)",
        "sad": "#6c757d",
        "surprised": "var(--warning)",
        "happy": "var(--success)",
        "neutral": "var(--text-light)"
    }
    return emotion_colors.get(emotion.lower(), "var(--primary)")