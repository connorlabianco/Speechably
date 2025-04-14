"""
Backend package for speech analysis functionality.
Contains core services for audio processing, transcription, and analysis.
"""

from backend.speech_analysis import SpeechAnalyzer
from backend.segment_and_extract import AudioSegmenter, AudioSegmenterConfig
from backend.transcription_service import TranscriptionService
from backend.gemini_service import GeminiService
from backend.data_processor import DataProcessor
from backend.visualization_helper import VisualizationHelper

__all__ = [
    'SpeechAnalyzer',
    'AudioSegmenter',
    'AudioSegmenterConfig',
    'TranscriptionService',
    'GeminiService',
    'DataProcessor',
    'VisualizationHelper'
]