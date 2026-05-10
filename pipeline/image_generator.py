import os
import requests
from PIL import Image
from io import BytesIO
import time

def generate_image(section_title: str, narration: str, section_num: int, image_style: str = "Cinematic documentary") -> str:
    prompt = f"{image_style} style illustration: {section_title}. {narration[:100]}. Highly detailed, professional, 4K quality."

    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=180)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                output_path = f"outputs/images/section_{section_num}.png"
                image.save(output_path)
                return output_path
        except requests.exceptions.Timeout:
            if attempt < 2:
                time.sleep(10)
                continue
            raise Exception("Image generation timed out after 3 attempts")

    raise Exception("Image generation failed after 3 attempts")


def generate_all_images(sections: list, image_style: str = "Cinematic documentary") -> list:
    image_paths = []
    for section in sections:
        path = generate_image(
            section["title"],
            section["narration"],
            section["section"],
            image_style
        )
        image_paths.append(path)
    return image_paths