import google.generativeai as genai
import json
import re
import os
from typing import Dict, List, Tuple, Any, Optional, Union

class GeminiService:
    """
    Service class for interacting with the Gemini API to generate feedback
    for speech analysis.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini service with optional API key.
        
        Args:
            api_key: The Gemini API key. If None, attempts to load from environment.
        """
        self.model = self.init_gemini(api_key)
    
    def init_gemini(self, api_key: Optional[str] = None) -> Any:
        """
        Initialize the Gemini API client.
        
        Args:
            api_key: The Gemini API key. If None, attempts to load from environment.
            
        Returns:
            The Gemini model or None if initialization fails.
        """
        try:
            # Get API key from parameter or environment variable
            API_KEY = api_key or os.environ.get("GEMINI_API_KEY")
            if not API_KEY:
                print("GEMINI_API_KEY not found in environment variables or parameters")
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
            print(f"Error initializing Gemini: {e}")
            return None
    
    def generate_speech_analysis_prompt(self, transcription_data: List[Dict[str, Any]]) -> str:
        """
        Generate a formatted prompt for Gemini based on speech analysis.
        
        Args:
            transcription_data: List of transcription segment dictionaries
            
        Returns:
            Formatted prompt string for Gemini
        """
        # Create the formatted timeline for reference
        timeline_blocks = []
        issues = []
        
        # Format time helper function
        def format_time(seconds: float) -> str:
            minutes = int(seconds // 60)
            seconds_remainder = int(seconds % 60)
            return f"{minutes:02d}:{seconds_remainder:02d}"
        
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
        
        # Calculate WPS statistics
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
   - Identify any unclear or nonsensical phrases that suggest poor enunciation. (If words are spoken too fast, or too quietly, or pronounced incorrectly, they may be unclear on the transcription. Please assume that the user's speech is written correctly, and that the transcription looking incorrect is due to the user speaking too fast, or too quietly, or pronounced incorrectly. This is mostly fixed by enunciating more clearly and slowing down.)
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
    
    def generate_simple_prompt(self, emotion_segments: List[Tuple[str, str]]) -> str:
        """
        Generate a simpler prompt when transcription data is not available.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            
        Returns:
            Formatted prompt string for Gemini
        """
        # Format emotion segments for context
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
        return prompt
    
    def analyze_speech(
        self, 
        emotion_segments: List[Tuple[str, str]], 
        transcription_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Use Gemini to analyze speech patterns and provide coaching feedback.
        
        Args:
            emotion_segments: List of (time_range, emotion) tuples
            transcription_data: Optional list of transcription segment dictionaries
            
        Returns:
            Dictionary containing analysis results
        """
        if self.model is None:
            return {
                "summary": "Gemini analysis not available. Please check your API key configuration.",
                "improvement_areas": [],
                "strengths": [],
                "coaching_tips": []
            }
        
        # Generate appropriate prompt based on available data
        if transcription_data:
            prompt = self.generate_speech_analysis_prompt(transcription_data)
        else:
            prompt = self.generate_simple_prompt(emotion_segments)
        
        try:
            # Get response from Gemini
            response = self.model.generate_content(prompt)
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
            
    def generate_chat_response(self, user_input: str, emotion_context: str) -> str:
        """
        Generate a chat response for the AI coach feature.
        
        Args:
            user_input: The user's question or message
            emotion_context: Formatted string describing the emotion context
            
        Returns:
            The AI coach's response text
        """
        if not self.model:
            return "I'm not available right now. Please check the Gemini API configuration."
            
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
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"I'm having trouble generating a response right now. Error: {str(e)}"