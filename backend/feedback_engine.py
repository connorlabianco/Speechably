import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

class FeedbackEngine:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_feedback(self, emotion_data, posture_data):
        """Generate personalized feedback based on emotion and posture analysis"""
        prompt = f"""
        Based on the following analysis, provide constructive feedback for public speaking improvement:
        
        Emotion Analysis: {json.dumps(emotion_data, indent=2)}
        Posture Analysis: {json.dumps(posture_data, indent=2)}
        
        Please provide:
        1. Overall assessment
        2. Specific areas for improvement
        3. Practical tips for enhancement
        """
        
        response = self.model.generate_content(prompt)
        return response.text
        
    def format_feedback(self, raw_feedback):
        """Format the feedback into a structured response"""
        # Add your formatting logic here
        return {
            'feedback': raw_feedback,
            'timestamp': 'current_time',
            'version': '1.0'
        } 