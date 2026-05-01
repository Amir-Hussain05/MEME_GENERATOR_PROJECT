import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    _key = os.getenv("OPENAI_API_KEY", "")
    client = OpenAI(api_key=_key) if _key else None
except Exception:
    client = None


def generate_ai_image(prompt: str) -> str:
    """
    Generate an AI image for the given prompt.
    Tries gpt-image-1 first, falls back to dall-e-3, then to a local template.
    Returns the file path of the saved image.
    """
    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/ai_image.png"

    if client is None:
        print("IMAGE ERROR: OpenAI client not initialised — using fallback")
        return _fallback()

    # ── Try gpt-image-1 (returns base64) ────────────────────────────────────
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        item = response.data[0]

        # gpt-image-1 returns b64_json, not a URL
        if hasattr(item, "b64_json") and item.b64_json:
            img_bytes = base64.b64decode(item.b64_json)
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            return output_path

        # Fallback: if somehow a URL is present
        if hasattr(item, "url") and item.url:
            img_data = requests.get(item.url, timeout=30).content
            with open(output_path, "wb") as f:
                f.write(img_data)
            return output_path

        raise ValueError("No image data in gpt-image-1 response")

    except Exception as e:
        print(f"gpt-image-1 failed: {e}")

    # ── Fallback: dall-e-3 (returns URL) ────────────────────────────────────
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url, timeout=30).content
        with open(output_path, "wb") as f:
            f.write(img_data)
        return output_path

    except Exception as e:
        print(f"dall-e-3 also failed: {e}")
        return _fallback()


def _fallback() -> str:
    """Return a safe local template image."""
    for path in [
        "templates/coding.png",
        "templates/student.png",
        "templates/office.png",
    ]:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("No fallback template images found in templates/")
