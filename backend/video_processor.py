import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import os

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = VideoFileClip(video_path)
        
    def extract_frames(self, output_dir):
        """Extract frames from video at regular intervals"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Extract frames every second
        for i, frame in enumerate(self.video.iter_frames(fps=1)):
            frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
            cv2.imwrite(frame_path, frame)
            
    def extract_audio(self, output_path):
        """Extract audio from video"""
        audio = self.video.audio
        if audio is not None:
            audio.write_audiofile(output_path)
            
    def close(self):
        """Close video resources"""
        self.video.close() 