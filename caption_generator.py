import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    _key = os.getenv("OPENAI_API_KEY", "")
    client = OpenAI(api_key=_key) if _key else None
    API_WORKING = client is not None
except Exception:
    client = None
    API_WORKING = False


def generate_caption(scenario: str):
    """
    Returns (top_text, bottom_text, category).
    Falls back to defaults if the API call fails.
    """
    try:
        if not API_WORKING:
            raise Exception("OpenAI API key not configured")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create short, funny meme captions. "
                        "Always respond STRICTLY in this format and nothing else:\n"
                        "line1 | line2 | category\n\n"
                        "Valid categories: coding, study, office, cricket, general\n"
                        "Keep each line under 60 characters."
                    )
                },
                {
                    "role": "user",
                    "content": f"Scenario: {scenario}"
                }
            ],
            temperature=0.9,
            max_tokens=100
        )

        text = response.choices[0].message.content.strip()
        # Strip markdown fences if model wraps output
        text = text.replace("```", "").strip()
        parts = [p.strip() for p in text.split("|")]

        if len(parts) >= 3:
            top = parts[0]
            bottom = parts[1]
            category = parts[2].lower()
        else:
            raise ValueError(f"Unexpected AI format: {text!r}")

    except Exception as e:
        print(f"CAPTION ERROR: {e}")
        top = "WHEN YOU TRY HARD"
        bottom = "BUT NOTHING WORKS"
        category = "general"

    return top, bottom, category
