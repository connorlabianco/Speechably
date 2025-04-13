import subprocess
from moviepy.editor import VideoFileClip
from pathlib import Path
import os

def split_and_extract_audio(video_path: str, output_dir: str, min_duration=4, max_duration=7):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clip = VideoFileClip(video_path)
    total_duration = clip.duration

    # Calculate number of segments
    num_segments = int(total_duration // max_duration) + 1
    segment_duration = total_duration / num_segments

    # Adjust segment duration if it's below the minimum
    if segment_duration < min_duration:
        num_segments = int(total_duration // min_duration)
        segment_duration = total_duration / num_segments

    print(f"Splitting video into {num_segments} segments of ~{segment_duration:.2f}s each")

    ffmpeg_path = r'C:\Users\MCCLAB1200WL744\Downloads\ffmpeg-7.1.1-essentials_build (1)\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe'  # Hardcoded FFmpeg path

    for i in range(num_segments):
        start = i * segment_duration
        end = min((i + 1) * segment_duration, total_duration)

        # Use the hardcoded path to run the command for video segment
        cmd_video = [
            ffmpeg_path,
            '-i', str(video_path),
            '-ss', str(start),
            '-to', str(end),
            '-vcodec', 'libx264',
            '-acodec', 'aac',
            str(output_dir / f"segment_{i+1}.mp4")
        ]
        subprocess.run(cmd_video, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        # Use the hardcoded path to run the command for audio extraction
        cmd_audio = [
            ffmpeg_path,
            '-i', str(video_path),
            '-ss', str(start),
            '-to', str(end),
            '-vn',  # no video
            '-acodec', 'pcm_s16le',
            '-ar', '16000',  # audio sampling rate
            '-ac', '1',  # mono audio
            str(output_dir / f"segment_{i+1}.wav")
        ]
        subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        print(f"Saved segment {i+1}: {output_dir / f'segment_{i+1}.mp4'}, {output_dir / f'segment_{i+1}.wav'}")

    clip.close()

# Example usage
if __name__ == "__main__":
    video_file = r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\your_video.mp4"
    output_folder = r"C:\Users\MCCLAB1200WL744\Desktop\speechably\Speechably\backend\output_segments"
    split_and_extract_audio(video_file, output_folder)  # Call the correct function
