import subprocess
from pathlib import Path
import os
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class AudioSegmenterConfig:
    min_duration: float = 4
    max_duration: float = 7
    ffmpeg_path: Optional[str] = None
    audio_sample_rate: int = 16000
    audio_channels: int = 1

class AudioSegmenter:
    def __init__(self, config: Optional[AudioSegmenterConfig] = None):
        self.config = config or AudioSegmenterConfig()
        if not self.config.ffmpeg_path:
            # Default FFmpeg path - you might want to make this configurable or detect it
            self.config.ffmpeg_path = r'C:\Users\MCCLAB1200WL744\Downloads\ffmpeg-7.1.1-essentials_build (1)\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe'

    def _get_audio_duration(self, audio_path: str) -> float:
        """Get the duration of an audio file using FFmpeg."""
        cmd = [
            self.config.ffmpeg_path,
            '-i', audio_path,
            '-f', 'null',
            '-'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Extract duration using regex
        duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2}', result.stderr)
        if duration_match:
            hours, minutes, seconds = map(int, duration_match.groups())
            return hours * 3600 + minutes * 60 + seconds
        return 0.0

    def extract_and_split_audio(self, video_path: str, output_dir: str) -> tuple[str, list[str]]:
        """
        Extract audio from video and split it into segments.
        
        Args:
            video_path: Path to the input video file
            output_dir: Directory to save the audio segments
            
        Returns:
            Tuple containing (full_audio_path, list_of_segment_paths)
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # First extract the full audio
        full_audio_path = str(output_dir / "full_audio.wav")
        self._extract_full_audio(video_path, full_audio_path)

        # Get duration of the audio file
        duration = self._get_audio_duration(full_audio_path)

        # Calculate number of segments
        num_segments = int(duration // self.config.max_duration) + 1
        segment_duration = duration / num_segments

        # Adjust segment duration if it's below the minimum
        if segment_duration < self.config.min_duration:
            num_segments = int(duration // self.config.min_duration)
            segment_duration = duration / num_segments

        print(f"Splitting audio into {num_segments} segments of ~{segment_duration:.2f}s each")
        
        segment_paths = []
        for i in range(num_segments):
            start = i * segment_duration
            end = min((i + 1) * segment_duration, duration)
            
            audio_segment_path = str(output_dir / f"segment_{i+1}.wav")
            self._extract_audio_segment(full_audio_path, start, end, audio_segment_path)
            
            segment_paths.append(audio_segment_path)
            print(f"Saved segment {i+1}: {audio_segment_path}")

        return full_audio_path, segment_paths

    def _extract_full_audio(self, video_path: str, output_path: str):
        cmd = [
            self.config.ffmpeg_path,
            '-i', str(video_path),
            '-vn',  # no video
            '-acodec', 'pcm_s16le',
            '-ar', str(self.config.audio_sample_rate),
            '-ac', str(self.config.audio_channels),
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def _extract_audio_segment(self, audio_path: str, start: float, end: float, output_path: str):
        cmd = [
            self.config.ffmpeg_path,
            '-i', str(audio_path),
            '-ss', str(start),
            '-to', str(end),
            '-acodec', 'pcm_s16le',
            '-ar', str(self.config.audio_sample_rate),
            '-ac', str(self.config.audio_channels),
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Example usage
if __name__ == "__main__":
    config = AudioSegmenterConfig(
        min_duration=4,
        max_duration=7,
        audio_sample_rate=16000,
        audio_channels=1
    )
    segmenter = AudioSegmenter(config)
    
    video_file = r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\your_video.mp4"
    output_folder = r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\output_segments"
    full_audio, segments = segmenter.extract_and_split_audio(video_file, output_folder)
