import os
import base64
import requests
from openai import OpenAI


def generate_ai_image(prompt: str, api_key: str) -> str:
    """
    Generate an AI image for the given prompt.
    api_key is passed directly — never stored in any file.
    Tries dall-e-3 first, falls back to template on failure.
    """
    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/ai_image.png"

    client = OpenAI(api_key=api_key)

    # ── Try dall-e-3 (most reliable, returns URL) ────────────────────────────
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url, timeout=60).content
        with open(output_path, "wb") as f:
            f.write(img_data)
        return output_path

    except Exception as e:
        print(f"dall-e-3 failed: {e}")

    # ── Try gpt-image-1 (returns base64) ────────────────────────────────────
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        item = response.data[0]
        if hasattr(item, "b64_json") and item.b64_json:
            img_bytes = base64.b64decode(item.b64_json)
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            return output_path

    except Exception as e:
        print(f"gpt-image-1 also failed: {e}")

    # ── Final fallback: use a template ───────────────────────────────────────
    for path in ["templates/coding.png", "templates/student.png", "templates/office.png"]:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("No fallback template images found in templates/")
