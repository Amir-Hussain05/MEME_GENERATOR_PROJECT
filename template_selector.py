import random
import os


# Map of category keywords → template images
TEMPLATES: dict[str, list[str]] = {
    "cricket":     ["templates/cricket.png"],
    "sport":       ["templates/cricket.png"],
    "study":       ["templates/student.png"],
    "education":   ["templates/student.png"],
    "exam":        ["templates/exam.png"],
    "coding":      ["templates/coding.png"],
    "programming": ["templates/coding.png"],
    "developer":   ["templates/coding.png"],
    "office":      ["templates/office.png"],
    "work":        ["templates/office.png"],
    "general": [
        "templates/coding.png",
        "templates/student.png",
        "templates/office.png",
    ],
}


def get_template(category: str | None) -> str:
    """
    Return the path of a template image for the given category.
    Falls back to 'general' if the category is unknown or missing.
    """
    key = (category or "general").lower().strip()

    # Partial match: e.g. "coding meme" → "coding"
    if key not in TEMPLATES:
        for known in TEMPLATES:
            if known in key:
                key = known
                break
        else:
            key = "general"

    choices = TEMPLATES[key]
    # Filter to paths that actually exist on disk
    valid = [p for p in choices if os.path.exists(p)]
    if not valid:
        valid = [p for p in TEMPLATES["general"] if os.path.exists(p)]
    if not valid:
        raise FileNotFoundError(
            "No template images found. Make sure the 'templates/' folder "
            "is present and contains PNG files."
        )

    return random.choice(valid)
