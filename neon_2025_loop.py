from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random

# -------------------------
# VIDEO SETTINGS
# -------------------------
WIDTH, HEIGHT = 1080, 1920   # 9:16 TikTok
FPS = 30
BG_COLOR = (0, 0, 0)
FONT_SIZE = 300
FONT_PATH = "arial.ttf"  # replace if needed
NEON_COLOR = (0, 246, 255)  # neon cyan

# -------------------------
# NEON TEXT GENERATOR
# -------------------------
def neon_text(text):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    w, h = draw.textsize(text, font=font)
    position = ((WIDTH - w) // 2, (HEIGHT - h) // 2)

    # Glow layers
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    for i in range(10):
        glow_draw.text(position, text, font=font, fill=NEON_COLOR + (20,))
        glow = glow.filter(ImageFilter.GaussianBlur(radius=8))

    draw.text(position, text, font=font, fill=NEON_COLOR + (255,))
    img = Image.alpha_composite(glow, img)

    return np.array(img)

# -------------------------
# GLITCH EFFECT
# -------------------------
def glitch_frame(frame):
    img = frame.copy()
    h, w, _ = img.shape

    for _ in range(6):
        y = random.randint(0, h - 30)
        slice_h = random.randint(5, 25)
        shift = random.randint(-40, 40)
        img[y:y+slice_h] = np.roll(img[y:y+slice_h], shift, axis=1)

    return img

# -------------------------
# CREATE CLIPS
# -------------------------
clips = []

# Countdown: 2025 → 2021
for year in ["2025", "2024", "2023", "2022", "2021"]:
    frame = neon_text(year)
    clip = ImageClip(frame).set_duration(0.7)
    clips.append(clip)

# Glitch rewind section
glitch_base = ImageClip(neon_text("2025")).set_duration(0.8)
glitch = glitch_base.fl(lambda gf, t: glitch_frame(gf(t)))
clips.append(glitch)

# Final 2025 (loop anchor)
final_clip = ImageClip(neon_text("2025")).set_duration(1.2)
clips.append(final_clip)

# -------------------------
# EXPORT
# -------------------------
video = concatenate_videoclips(clips, method="compose")
video.write_videofile(
    "neon_2025_loop.mp4",
    fps=FPS,
    codec="libx264",
    audio=False
)
