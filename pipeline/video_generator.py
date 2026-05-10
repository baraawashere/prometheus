import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

def generate_video(image_paths: list, audio_paths: list, music_path: str = None) -> str:
    clips = []

    for image_path, audio_path in zip(image_paths, audio_paths):
        audio = AudioFileClip(audio_path)
        image = ImageClip(image_path).with_duration(audio.duration)
        image = image.with_audio(audio)
        clips.append(image)

    final = concatenate_videoclips(clips, method="compose")

    if music_path and os.path.exists(music_path):
        music = AudioFileClip(music_path).with_effects([])
        music = music.subclipped(0, final.duration)
        music = music.with_volume_scaled(0.15)
        
        final_audio = CompositeAudioClip([final.audio, music])
        final = final.with_audio(final_audio)

    output_path = "outputs/video/final_video.mp4"
    final.write_videofile(output_path, fps=24, logger=None)

    return output_path