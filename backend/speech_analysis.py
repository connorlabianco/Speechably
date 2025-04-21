import torch
import torchaudio
from transformers import Wav2Vec2FeatureExtractor, AutoModelForAudioClassification
from pathlib import Path

class SpeechAnalyzer:
    def __init__(self):
        # Load model + feature extractor
        self.model_name = "r-f/wav2vec-english-speech-emotion-recognition"
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(self.model_name)
        self.model = AutoModelForAudioClassification.from_pretrained(self.model_name)

    def analyze_speech(self, audio_file_path):
        """
        Analyze a single audio file and return the emotion label.
        
        Args:
            audio_file_path (str): Path to the audio file to analyze
            
        Returns:
            str: The predicted emotion label
        """
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

    def analyze_segments(self, output_folder):
        """
        Analyze all audio segments in the specified folder.
        
        Args:
            output_folder (str): Path to the folder containing audio segments
            
        Returns:
            dict: Dictionary mapping segment filenames to their emotion labels
        """
        output_path = Path(output_folder)
        if not output_path.exists():
            raise FileNotFoundError(f"Folder does not exist: {output_folder}")

        # Collect audio files
        audio_files = [f for f in output_path.glob("*.wav") if f.is_file()]
        
        if not audio_files:
            print("⚠️ No audio files found in the output_segments folder.")
            return {}

        results = {}
        print(f"🔍 Found {len(audio_files)} audio segment(s).")
        for audio_file in sorted(audio_files):
            print(f"\n🎧 Analyzing segment: {audio_file.name}")
            emotion = self.analyze_speech(audio_file)
            results[audio_file.name] = emotion
            print(f"🧠 Feedback for {audio_file.name}: {emotion}")
            
        return results 
    
if __name__ == "__main__":
    analyzer = SpeechAnalyzer()
    results = analyzer.analyze_segments(r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\output_segments")
    print(results)
