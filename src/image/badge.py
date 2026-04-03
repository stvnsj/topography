from PIL import Image, ImageDraw, ImageFont
import os
from typing import Optional



import re

def hyphenate_tag(s: str) -> str:
    """
    - Remove everything from the first '_' onward.
    - Insert a hyphen right before the first digit.
    Examples:
        "G001A_g" -> "G-001A"
        "G23_g"   -> "G-23"
    """
    base = s.split('_', 1)[0]          # strip from underscore forward
    m = re.search(r'\d', base)          # find first digit
    if not m:
        return base                     # no digits, return as-is
    i = m.start()
    if i > 0 and base[i-1] == '-':
        return base                     # already hyphenated
    return base[:i] + '-' + base[i:]







# ---------- Badge factory (fallback) ----------
def make_badge(text: str, pad_x: int = 8, pad_y: int = 4,
               font_size: int = 16, radius: int = 0) -> Image.Image:
    """
    Create a small label like: [ G-1 ]
    - White background (RGB), black 1px stroke, rounded corners
    - Centered black text
    """
    # Pick a common TrueType font; fall back to PIL's default.
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    # Text metrics
    l, t, r, b = font.getbbox(hyphenate_tag(text))  # may have negative l/t (bearings)
    text_w = r - l
    text_h = b - t

    w = text_w + 2 * pad_x
    h = text_h + 2 * pad_y

    # Solid white background (no transparency)
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    # Rounded white rectangle with black outline
    try:
        draw.rounded_rectangle(
            [(0.5, 0.5), (w - 0.5, h - 0.5)],
            #radius=radius,
            fill="white",
            outline="black",
            width=1,
        )
    except AttributeError:
        # If Pillow is too old for rounded_rectangle, fall back to a normal rectangle
        draw.rectangle(
            [(0.5, 0.5), (w - 0.5, h - 0.5)],
            fill="white",
            outline="black",
            width=1,
        )

    # Center text; compensate for left/top bearings
    tx = (w - text_w) // 2 - l
    ty = (h - text_h) // 2 - t
    draw.text((tx, ty),hyphenate_tag (text), fill="black", font=font)

    return img


def open_png_or_badge(path: str, badge_text: str) -> Image.Image:
    """
    Try to open 'path' (PNG preferred). If missing/unreadable, return a
    generated badge (RGB white background, black text).
    """
    #try:
    #    img = Image.open(path)
    #    # Preserve source mode; caller will decide how to composite.
    #    return img
    #except Exception:
    #    return make_badge(badge_text, radius=0)
    return make_badge(badge_text, radius=0)
