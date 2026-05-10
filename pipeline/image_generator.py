import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_API_KEY"),
)

def generate_image(section_title: str, narration: str, section_num: int) -> str:
    prompt = f"Cinematic documentary style illustration: {section_title}. {narration[:100]}. Highly detailed, professional, 4K quality."

    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell",
    )

    output_path = f"outputs/images/section_{section_num}.png"
    image.save(output_path)

    return output_path

def generate_all_images(sections: list) -> list:
    image_paths = []
    for section in sections:
        path = generate_image(
            section["title"],
            section["narration"],
            section["section"]
        )
        image_paths.append(path)
    return image_paths