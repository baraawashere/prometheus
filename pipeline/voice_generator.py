import asyncio
import edge_tts
import os

VOICE = "en-US-AriaNeural"

async def generate_audio_async(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

def generate_audio(text: str, section_num: int) -> str:
    output_path = f"outputs/audio/section_{section_num}.mp3"
    asyncio.run(generate_audio_async(text, output_path))
    return output_path

def generate_all_audio(sections: list) -> list:
    audio_paths = []
    for section in sections:
        path = generate_audio(section["narration"], section["section"])
        audio_paths.append(path)
    return audio_paths