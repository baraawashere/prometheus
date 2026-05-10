import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

def generate_video(image_paths: list, audio_paths: list) -> str:
    clips = []

    for image_path, audio_path in zip(image_paths, audio_paths):
        audio = AudioFileClip(audio_path)
        image = ImageClip(image_path).with_duration(audio.duration)
        image = image.with_audio(audio)
        clips.append(image)

    final = concatenate_videoclips(clips, method="compose")

    output_path = "outputs/video/final_video.mp4"
    final.write_videofile(output_path, fps=24, logger=None)

    return output_path