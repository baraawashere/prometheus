import asyncio
import edge_tts
import os

VOICE = "en-US-AriaNeural"

async def generate_audio_async(text: str, output_path: str, voice: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_audio(text: str, section_num: int, voice: str = "en-US-AriaNeural") -> str:
    output_path = f"outputs/audio/section_{section_num}.mp3"
    asyncio.run(generate_audio_async(text, output_path, voice))
    return output_path

def generate_all_audio(sections: list, voice: str = "en-US-AriaNeural") -> list:
    audio_paths = []
    for section in sections:
        path = generate_audio(section["narration"], section["section"], voice)
        audio_paths.append(path)
    return audio_paths