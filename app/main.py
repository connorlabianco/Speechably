import torch
import torchaudio
from transformers import Wav2Vec2FeatureExtractor, AutoModelForAudioClassification
from pathlib import Path

# Load model + feature extractor (not processor)
model_name = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = AutoModelForAudioClassification.from_pretrained(model_name)

# 🎧 Analyze a single audio file
def analyze_speech_local(audio_file_path):
    waveform, sample_rate = torchaudio.load(audio_file_path)
    waveform = waveform.squeeze()

    # Convert to model inputs
    inputs = feature_extractor(waveform, sampling_rate=sample_rate, return_tensors="pt")

    # Get logits
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()

    # Convert ID to label
    emotion_label = model.config.id2label[predicted_class_id]
    return emotion_label


# 📁 Path to your .wav files
output_folder = Path(r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\output_segments")

if not output_folder.exists():
    print(f"❌ Folder does not exist: {output_folder}")
    exit()

# 📄 Collect audio files
audio_files = [f for f in output_folder.glob("*.wav") if f.is_file()]

if not audio_files:
    print("⚠️ No audio files found in the output_segments folder.")
else:
    print(f"🔍 Found {len(audio_files)} audio segment(s).")
    for audio_file in sorted(audio_files):
        print(f"\n🎧 Analyzing segment: {audio_file.name}")
        feedback = analyze_speech_local(audio_file)
        print(f"🧠 Feedback for {audio_file.name}: {feedback}")
