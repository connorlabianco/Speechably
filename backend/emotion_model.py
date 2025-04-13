import torch
import torchaudio
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
import numpy as np

class EmotionRecognizer:
    def __init__(self, model_path="models/emotion"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path).to(self.device)
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_path)
        
    def process_audio(self, audio_path):
        """Process audio file and predict emotions"""
        # Load and preprocess audio
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # Extract features
        inputs = self.feature_extractor(
            waveform.squeeze().numpy(),
            sampling_rate=sample_rate,
            return_tensors="pt",
            padding=True
        ).to(self.device)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
        return predictions.cpu().numpy() 