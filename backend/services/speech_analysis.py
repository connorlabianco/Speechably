import torch
import torchaudio
from transformers import Wav2Vec2FeatureExtractor, AutoModelForAudioClassification
from pathlib import Path
import os

class SpeechAnalyzer:
    """
    Service for analyzing speech emotions using a pre-trained model.
    """
    
    def __init__(self, model_name="r-f/wav2vec-english-speech-emotion-recognition"):
        """
        Initialize the speech analyzer with a pre-trained model.
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self._load_model()
    
    def _load_model(self):
        """Load the feature extractor and model"""
        try:
            self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(self.model_name)
            self.model = AutoModelForAudioClassification.from_pretrained(self.model_name)
            print(f"Successfully loaded model: {self.model_name}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.feature_extractor = None
            self.model = None

    def analyze_speech(self, audio_file_path):
        """
        Analyze a single audio file and return the emotion label.
        
        Args:
            audio_file_path: Path to the audio file to analyze
            
        Returns:
            The predicted emotion label
        """
        if not self.model or not self.feature_extractor:
            print("Model not loaded. Cannot analyze speech.")
            return "neutral"
            
        try:
            waveform, sample_rate = torchaudio.load(audio_file_path)
            waveform = waveform.squeeze()

            # Convert to model inputs
            inputs = self.feature_extractor(waveform, sampling_rate=sample_rate, return_tensors="pt")

            # Get logits
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                predicted_class_id = torch.argmax(logits, dim=-1).item()

            # Convert ID to label
            emotion_label = self.model.config.id2label[predicted_class_id]
            return emotion_label
            
        except Exception as e:
            print(f"Error analyzing speech: {str(e)}")
            return "neutral"

    def analyze_segments(self, output_folder):
        """
        Analyze all audio segments in the specified folder.
        
        Args:
            output_folder: Path to the folder containing audio segments
            
        Returns:
            Dictionary mapping segment filenames to their emotion labels
        """
        output_path = Path(output_folder)
        if not output_path.exists():
            raise FileNotFoundError(f"Folder does not exist: {output_folder}")

        # Collect audio files (only segment files, not full_audio)
        audio_files = [f for f in output_path.glob("segment_*.wav") if f.is_file()]
        
        if not audio_files:
            print("No audio files found in the output folder.")
            return {}

        results = {}
        print(f"Found {len(audio_files)} audio segment(s).")
        for audio_file in sorted(audio_files):
            print(f"Analyzing segment: {audio_file.name}")
            emotion = self.analyze_speech(audio_file)
            results[audio_file.name] = emotion
            print(f"Detected emotion for {audio_file.name}: {emotion}")
            
        return results