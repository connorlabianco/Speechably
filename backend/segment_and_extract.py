import subprocess
from moviepy.editor import VideoFileClip
from pathlib import Path
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoSegmenterConfig:
    min_duration: float = 4
    max_duration: float = 7
    ffmpeg_path: Optional[str] = None
    audio_sample_rate: int = 16000
    audio_channels: int = 1

class VideoSegmenter:
    def __init__(self, config: Optional[VideoSegmenterConfig] = None):
        self.config = config or VideoSegmenterConfig()
        if not self.config.ffmpeg_path:
            # Default FFmpeg path - you might want to make this configurable or detect it
            self.config.ffmpeg_path = r'C:\Users\MCCLAB1200WL744\Downloads\ffmpeg-7.1.1-essentials_build (1)\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe'

    def split_and_extract_audio(self, video_path: str, output_dir: str) -> list[tuple[str, str]]:
        """
        Split video into segments and extract audio for each segment.
        
        Args:
            video_path: Path to the input video file
            output_dir: Directory to save the segments
            
        Returns:
            List of tuples containing (video_segment_path, audio_segment_path)
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        clip = VideoFileClip(video_path)
        total_duration = clip.duration

        # Calculate number of segments
        num_segments = int(total_duration // self.config.max_duration) + 1
        segment_duration = total_duration / num_segments

        # Adjust segment duration if it's below the minimum
        if segment_duration < self.config.min_duration:
            num_segments = int(total_duration // self.config.min_duration)
            segment_duration = total_duration / num_segments

        print(f"Splitting video into {num_segments} segments of ~{segment_duration:.2f}s each")
        
        segments = []
        for i in range(num_segments):
            start = i * segment_duration
            end = min((i + 1) * segment_duration, total_duration)
            
            video_segment_path = str(output_dir / f"segment_{i+1}.mp4")
            audio_segment_path = str(output_dir / f"segment_{i+1}.wav")
            
            self._extract_video_segment(video_path, start, end, video_segment_path)
            self._extract_audio_segment(video_path, start, end, audio_segment_path)
            
            segments.append((video_segment_path, audio_segment_path))
            print(f"Saved segment {i+1}: {video_segment_path}, {audio_segment_path}")

        clip.close()
        return segments

    def _extract_video_segment(self, video_path: str, start: float, end: float, output_path: str):
        cmd = [
            self.config.ffmpeg_path,
            '-i', str(video_path),
            '-ss', str(start),
            '-to', str(end),
            '-vcodec', 'libx264',
            '-acodec', 'aac',
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def _extract_audio_segment(self, video_path: str, start: float, end: float, output_path: str):
        cmd = [
            self.config.ffmpeg_path,
            '-i', str(video_path),
            '-ss', str(start),
            '-to', str(end),
            '-vn',  # no video
            '-acodec', 'pcm_s16le',
            '-ar', str(self.config.audio_sample_rate),
            '-ac', str(self.config.audio_channels),
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Example usage
if __name__ == "__main__":
    config = VideoSegmenterConfig(
        min_duration=4,
        max_duration=7,
        audio_sample_rate=16000,
        audio_channels=1
    )
    segmenter = VideoSegmenter(config)
    
    video_file = r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\your_video.mp4"
    output_folder = r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\output_segments"
    segments = segmenter.split_and_extract_audio(video_file, output_folder)
