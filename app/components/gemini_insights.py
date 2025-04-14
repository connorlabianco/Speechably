import streamlit as st
import json
from typing import List, Dict, Tuple, Any, Optional

class GeminiInsights:
    """
    Component for displaying Gemini AI analysis results.
    Handles caching, display, and regeneration of analysis.
    """
    
    def __init__(self, gemini_service):
        """
        Initialize the Gemini insights component.
        
        Args:
            gemini_service: The GeminiService instance for generating analysis
        """
        self.gemini_service = gemini_service
    
    def display_analysis(
        self, 
        emotion_segments: List[Tuple[str, str]], 
        transcription_data: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Display analysis results from Gemini.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            transcription_data: Optional list of transcription segment dictionaries
        """
        st.subheader("🧠 AI-Powered Speech Insights")
        
        # Check if we already have an analysis result in session state
        if "gemini_analysis" not in st.session_state:
            with st.spinner("🌌 Analyzing speech patterns with Gemini..."):
                # Use transcription data for enhanced analysis if available
                analysis_result = self.gemini_service.analyze_speech(
                    emotion_segments, 
                    transcription_data=transcription_data
                )
                # Cache the analysis in session state
                st.session_state.gemini_analysis = analysis_result
        else:
            analysis_result = st.session_state.gemini_analysis
        
        # Display analysis results
        self._display_analysis_summary(analysis_result)
        self._display_analysis_details(analysis_result)
        
        # Add option to regenerate analysis
        if st.button("🔄 Regenerate Analysis"):
            # Clear cached analysis
            if "gemini_analysis" in st.session_state:
                del st.session_state.gemini_analysis
            st.rerun()
        
        # Add a download button for the JSON data
        if transcription_data:
            self._add_download_button(transcription_data)
    
    def _display_analysis_summary(self, analysis_result: Dict[str, Any]):
        """
        Display the summary section of the analysis.
        
        Args:
            analysis_result: Dictionary containing the analysis data
        """
        st.markdown(f"""
        <div class="insight-card">
            <h4>Summary</h4>
            <p>{analysis_result["summary"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _display_analysis_details(self, analysis_result: Dict[str, Any]):
        """
        Display the detailed sections of the analysis.
        
        Args:
            analysis_result: Dictionary containing the analysis data
        """
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
            if isinstance(tip, dict):
                # Handle dictionary format tips
                area = tip.get("area", "General")
                tip_text = tip.get("tip", "")
                st.markdown(f"""
                <div class="insight-card" style="margin-bottom: 15px;">
                    <h4 style="margin: 0 0 5px 0; color: #ff6b6b;">{area}</h4>
                    <p style="margin: 0;">{tip_text}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Handle string format tips
                st.markdown(f"{i}. {tip}")
    
    def _add_download_button(self, transcription_data: List[Dict[str, Any]]):
        """
        Add a download button for the transcription data.
        
        Args:
            transcription_data: List of transcription segment dictionaries
        """
        json_str = json.dumps(transcription_data, indent=4)
        
        st.download_button(
            label="⬇️ Download Transcription Data (JSON)",
            data=json_str,
            file_name="snippet_transcripts.json",
            mime="application/json"
        )
    
    def get_key_insight(self, analysis_result: Optional[Dict[str, Any]] = None) -> str:
        """
        Extract a key insight from the analysis for display.
        
        Args:
            analysis_result: Optional dictionary containing the analysis data
            
        Returns:
            A string containing a key insight
        """
        # Use the provided analysis or get it from session state
        result = analysis_result or st.session_state.get("gemini_analysis", {})
        
        if not result or "summary" not in result:
            return "No analysis available yet."
        
        # Try to extract a key sentence from the summary
        summary = result["summary"]
        sentences = summary.split(". ")
        
        # Get the first substantive sentence that's not too long
        for sentence in sentences:
            if len(sentence) > 20 and len(sentence) < 120:
                return sentence + "."
        
        # Fallback to first improvement area if summary doesn't work
        if "improvement_areas" in result and result["improvement_areas"]:
            return result["improvement_areas"][0]
        
        # Final fallback
        return summary[:100] + "..." if len(summary) > 100 else summary
    
    def display_compact_insights(
        self,
        emotion_segments: List[Tuple[str, str]], 
        transcription_data: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Display a compact version of insights for dashboard view.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            transcription_data: Optional list of transcription segment dictionaries
        """
        # Get or generate analysis
        if "gemini_analysis" not in st.session_state:
            with st.spinner("Analyzing..."):
                analysis_result = self.gemini_service.analyze_speech(
                    emotion_segments, 
                    transcription_data=transcription_data
                )
                st.session_state.gemini_analysis = analysis_result
        else:
            analysis_result = st.session_state.gemini_analysis
        
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dominant_emotions = [e for _, e in emotion_segments]
            most_common = max(set(dominant_emotions), key=dominant_emotions.count)
            st.metric("Primary Emotion", most_common.capitalize())
        
        with col2:
            if transcription_data:
                wps_values = [segment["wps"] for segment in transcription_data]
                avg_wps = sum(wps_values) / len(wps_values) if wps_values else 0
                status = "📊"
                if avg_wps > 3.0:
                    status = "⚠️ Too Fast"
                elif avg_wps < 1.5:
                    status = "⚠️ Too Slow"
                else:
                    status = "✅ Good"
                st.metric("Avg. Speed", f"{avg_wps:.1f} WPS", status)
            else:
                st.metric("Emotion Shifts", len([i for i in range(1, len(emotion_segments)) 
                                              if emotion_segments[i][1] != emotion_segments[i-1][1]]))
        
        with col3:
            if "strengths" in analysis_result and analysis_result["strengths"]:
                strength_count = len(analysis_result["strengths"])
                st.metric("Strengths", strength_count)
            else:
                unique_emotions = len(set([e for _, e in emotion_segments]))
                st.metric("Emotion Range", unique_emotions)
        
        # Display key insight
        key_insight = self.get_key_insight(analysis_result)
        st.info(f"💡 **Key Insight:** {key_insight}")


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
    st.set_page_config(page_title="Gemini Insights Test", layout="wide")
    st.title("Gemini Insights Component Test")
    
    # Add custom styles for cards
    st.markdown("""
    <style>
    .insight-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #ff6b6b;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize components
    gemini_service = GeminiService()
    gemini_insights = GeminiInsights(gemini_service)
    
    # Sample emotion data
    sample_emotion_data = [
        ("00:00 - 00:15", "calm"),
        ("00:15 - 00:30", "happy"),
        ("00:30 - 00:45", "calm"),
        ("00:45 - 01:00", "surprised"),
        ("01:00 - 01:15", "angry")
    ]
    
    # Sample transcription data
    sample_transcription = [
        {
            "index": 0,
            "start": 0,
            "end": 15,
            "text": "This is a test of the emotion display component.",
            "wps": 2.2,
            "emotion": "calm"
        },
        {
            "index": 1,
            "start": 15,
            "end": 30,
            "text": "I'm feeling quite happy about how this is turning out!",
            "wps": 2.7,
            "emotion": "happy"
        },
        {
            "index": 2,
            "start": 30,
            "end": 45,
            "text": "Now I'll speak more calmly to demonstrate different emotions.",
            "wps": 1.8,
            "emotion": "calm"
        },
        {
            "index": 3,
            "start": 45,
            "end": 60,
            "text": "Wow! I can't believe how well this is working!",
            "wps": 3.2,
            "emotion": "surprised"
        },
        {
            "index": 4,
            "start": 60,
            "end": 75,
            "text": "This example is terrible! I hate it!",
            "wps": 2.5,
            "emotion": "angry"
        }
    ]
    
    # Test tabs
    tab1, tab2 = st.tabs(["Full Analysis", "Compact View"])
    
    with tab1:
        # Display the full insights
        gemini_insights.display_analysis(sample_emotion_data, sample_transcription)
    
    with tab2:
        # Display compact insights
        gemini_insights.display_compact_insights(sample_emotion_data, sample_transcription)