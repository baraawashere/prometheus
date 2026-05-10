import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_script(topic: str, num_sections: int = 4, length_instruction: str = "Each section should be 2-3 sentences long.", tone: str = "Documentary") -> list[dict]:
    prompt = f"""You are a documentary script writer. Write a {tone.lower()} style educational script about: {topic}

Split the script into exactly {num_sections} sections.
{length_instruction}
CRITICAL RULES:
- Each narration MUST meet the word count range. Count every word.
- Write full, detailed, informative sentences. Add facts, context, and explanation.
- Do NOT summarize. Do NOT write short sentences. Expand every idea fully.
- Do NOT repeat yourself or use filler.
- Before finalizing each narration, count the words yourself and confirm it is within the target range. If it is too short, add more detail until it reaches the minimum.

Respond ONLY in this JSON format, no extra text, no markdown:
[
  {{"section": 1, "title": "Introduction", "narration": "...full narration here..."}},
  {{"section": 2, "title": "...", "narration": "...full narration here..."}},
  {{"section": 3, "title": "...", "narration": "...full narration here..."}},
  {{"section": 4, "title": "Conclusion", "narration": "...full narration here..."}}
]"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    sections = json.loads(raw)
    return sections