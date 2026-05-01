from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime


def _load_font(size: int = 28) -> ImageFont.FreeTypeFont:
    """
    Try several common font paths so the app works on Windows, macOS, Linux,
    and Streamlit Cloud.
    """
    candidates = [
        # Windows
        "arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Arial.ttf",
        # macOS
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        # Linux / Streamlit Cloud
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    # Ultimate fallback — PIL built-in (no TTF needed)
    return ImageFont.load_default()


def _wrap_text(text: str, font, max_width: int, draw: ImageDraw.Draw) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip() if current else word
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def create_meme(image_path: str, top_text: str, bottom_text: str) -> str:
    os.makedirs("outputs", exist_ok=True)

    img = Image.open(image_path).convert("RGB")
    img = img.resize((500, 500))
    draw = ImageDraw.Draw(img)

    font = _load_font(28)
    outline_font = font  # same font for outline

    def draw_text_with_outline(lines: list[str], y_start: int) -> None:
        y = y_start
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            x = (img.width - text_w) / 2
            # Black outline
            for dx in (-2, -1, 0, 1, 2):
                for dy in (-2, -1, 0, 1, 2):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), line, font=font, fill="black")
            # White text
            draw.text((x, y), line, font=font, fill="white")
            y += bbox[3] - bbox[1] + 6  # line-height

    top_lines = _wrap_text(top_text.upper(), font, img.width - 40, draw)
    bottom_lines = _wrap_text(bottom_text.upper(), font, img.width - 40, draw)

    draw_text_with_outline(top_lines, y_start=10)

    # Position bottom text above the bottom edge
    line_h = 34
    bottom_start = img.height - (len(bottom_lines) * line_h) - 10
    draw_text_with_outline(bottom_lines, y_start=bottom_start)

    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"outputs/meme_{timestamp}.png"
    img.save(filename)
    return filename
