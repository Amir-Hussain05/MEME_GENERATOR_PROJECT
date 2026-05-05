from openai import OpenAI


def generate_caption(scenario: str, api_key: str):
    """
    Returns (top_text, bottom_text, category).
    api_key is passed directly — never stored in any file.
    """
    try:
        client = OpenAI(api_key=api_key)

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
        text = text.replace("```", "").strip()
        parts = [p.strip() for p in text.split("|")]

        if len(parts) >= 3:
            return parts[0], parts[1], parts[2].lower()
        else:
            raise ValueError(f"Unexpected format: {text!r}")

    except Exception as e:
        raise Exception(f"Caption generation failed: {e}")
