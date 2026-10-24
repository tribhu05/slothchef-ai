import os
import sys
import math
import random
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

# Output video settings
WIDTH, HEIGHT = 1920, 1080
W, H = WIDTH, HEIGHT
FPS = 30
TOTAL_SECONDS = 170.0
TOTAL_FRAMES = int(FPS * TOTAL_SECONDS)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_AUDIO = os.path.join(SCRIPT_DIR, "assets", "audio", "master_audio.wav")
OUTPUT_VIDEO = os.path.join(SCRIPT_DIR, "slothchef_animated_explainer.mp4")

# High-performance FFmpeg binary
FFMPEG_BIN = r"C:\Python314\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
if not os.path.exists(FFMPEG_BIN):
    import shutil
    FFMPEG_BIN = shutil.which("ffmpeg")

print(f"Using FFmpeg: {FFMPEG_BIN}")

# Color Palette: Hand-Drawn MS Paint Educational Style
BG_PAPER = (252, 250, 246)       # Creamy textured paper
INK_BLACK = (24, 24, 24)         # Heavy doodle pen outline
INK_MUTED = (130, 130, 130)      # Sketch gray
COLOR_YELLOW = (254, 222, 85)    # Marker Yellow
COLOR_CORAL = (248, 113, 113)    # Marker Red/Coral
COLOR_GREEN = (52, 211, 153)     # Marker Emerald Green
COLOR_BLUE = (96, 165, 250)      # Marker Sky Blue
COLOR_PURPLE = (192, 132, 252)   # Marker Purple
COLOR_ORANGE = (251, 146, 60)    # Marker Orange
COLOR_BROWN = (180, 130, 85)     # Sloth fur
COLOR_LIGHT_BROWN = (245, 225, 200)

# Fonts
try:
    FONT_HERO = ImageFont.truetype("C:/Windows/Fonts/comicbd.ttf", 76)
    FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/comicbd.ttf", 52)
    FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/comicbd.ttf", 36)
    FONT_BODY = ImageFont.truetype("C:/Windows/Fonts/comic.ttf", 28)
    FONT_BADGE = ImageFont.truetype("C:/Windows/Fonts/comicbd.ttf", 26)
    FONT_SUBTITLE_BAR = ImageFont.truetype("C:/Windows/Fonts/comicbd.ttf", 30)
except Exception:
    FONT_HERO = ImageFont.load_default()
    FONT_TITLE = ImageFont.load_default()
    FONT_SUBTITLE = ImageFont.load_default()
    FONT_BODY = ImageFont.load_default()
    FONT_BADGE = ImageFont.load_default()
    FONT_SUBTITLE_BAR = ImageFont.load_default()

# ----------------- DOODLE DRAWING PRIMITIVES -----------------

def draw_wobbly_line(draw, p1, p2, color=INK_BLACK, width=6, jitter=2):
    x1, y1 = p1
    x2, y2 = p2
    dist = math.hypot(x2 - x1, y2 - y1)
    steps = max(int(dist / 30), 2)
    pts = [(x1, y1)]
    for i in range(1, steps):
        t = i / steps
        rx = x1 + (x2 - x1) * t + random.uniform(-jitter, jitter)
        ry = y1 + (y2 - y1) * t + random.uniform(-jitter, jitter)
        pts.append((rx, ry))
    pts.append((x2, y2))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)

def draw_doodle_box(draw, bbox, fill=None, outline=INK_BLACK, width=6, radius=18):
    x1, y1, x2, y2 = bbox
    if fill:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)
    draw_wobbly_line(draw, (x1, y1), (x2, y1), outline, width)
    draw_wobbly_line(draw, (x2, y1), (x2, y2), outline, width)
    draw_wobbly_line(draw, (x2, y2), (x1, y2), outline, width)
    draw_wobbly_line(draw, (x1, y2), (x1, y1), outline, width)

def draw_doodle_pill(draw, bbox, text, font, fill=COLOR_YELLOW, text_color=INK_BLACK, outline=INK_BLACK, width=5):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle(bbox, radius=(y2 - y1)//2, fill=fill, outline=outline, width=width)
    bbox_t = font.getbbox(text)
    tw = bbox_t[2] - bbox_t[0]
    th = bbox_t[3] - bbox_t[1]
    tx = x1 + (x2 - x1 - tw) // 2
    ty = y1 + (y2 - y1 - th) // 2 - 4
    draw.text((tx, ty), text, font=font, fill=text_color)

def draw_sloth(draw, cx, cy, hat=True, wink=False, wave=False, t=0.0):
    # Head circle
    draw.ellipse([cx - 85, cy - 75, cx + 85, cy + 75], fill=COLOR_BROWN, outline=INK_BLACK, width=6)
    # Lighter face mask
    draw.ellipse([cx - 65, cy - 45, cx + 65, cy + 55], fill=COLOR_LIGHT_BROWN, outline=INK_BLACK, width=4)
    # Dark brown eye patches
    draw.ellipse([cx - 60, cy - 20, cx - 18, cy + 20], fill=(139, 85, 40))
    draw.ellipse([cx + 18, cy - 20, cx + 60, cy + 20], fill=(139, 85, 40))
    
    # Eyes
    if wink:
        draw.line([(cx - 50, cy - 2), (cx - 28, cy - 2)], fill=INK_BLACK, width=6)
        draw.ellipse([cx + 30, cy - 10, cx + 46, cy + 6], fill=INK_BLACK)
    else:
        draw.arc([cx - 52, cy - 15, cx - 26, cy + 8], 0, 180, fill=INK_BLACK, width=5)
        draw.arc([cx + 26, cy - 15, cx + 52, cy + 8], 0, 180, fill=INK_BLACK, width=5)
        
    # Black nose & smile
    draw.ellipse([cx - 14, cy + 6, cx + 14, cy + 24], fill=INK_BLACK)
    draw.arc([cx - 22, cy + 18, cx + 22, cy + 44], 0, 180, fill=INK_BLACK, width=5)
    
    # Body
    draw.ellipse([cx - 75, cy + 65, cx + 75, cy + 195], fill=COLOR_BROWN, outline=INK_BLACK, width=6)
    
    # Arms
    if wave:
        arm_wave = int(math.sin(t * 8) * 15)
        draw.line([(cx - 65, cy + 90), (cx - 130, cy + 30 + arm_wave)], fill=INK_BLACK, width=12)
        draw.line([(cx + 65, cy + 90), (cx + 115, cy + 130)], fill=INK_BLACK, width=12)
    else:
        draw.line([(cx - 65, cy + 90), (cx - 105, cy + 140)], fill=INK_BLACK, width=12)
        draw.line([(cx + 65, cy + 90), (cx + 105, cy + 140)], fill=INK_BLACK, width=12)
        
    # Chef Hat
    if hat:
        draw_doodle_box(draw, [cx - 60, cy - 95, cx + 60, cy - 72], fill=(255, 255, 255), outline=INK_BLACK, width=5, radius=6)
        draw.ellipse([cx - 70, cy - 165, cx - 12, cy - 85], fill=(255, 255, 255), outline=INK_BLACK, width=5)
        draw.ellipse([cx - 28, cy - 185, cx + 28, cy - 85], fill=(255, 255, 255), outline=INK_BLACK, width=5)
        draw.ellipse([cx + 12, cy - 165, cx + 70, cy - 85], fill=(255, 255, 255), outline=INK_BLACK, width=5)

def draw_stick_figure(draw, cx, cy, state="tired", t=0.0):
    # Head
    draw.ellipse([cx - 40, cy - 110, cx + 40, cy - 30], fill=(255, 255, 255), outline=INK_BLACK, width=6)
    if state == "tired":
        draw.arc([cx - 28, cy - 82, cx - 10, cy - 64], 0, 360, fill=INK_BLACK, width=4)
        draw.arc([cx + 10, cy - 82, cx + 28, cy - 64], 0, 360, fill=INK_BLACK, width=4)
        draw.line([(cx - 18, cy - 48), (cx + 18, cy - 48)], fill=INK_BLACK, width=4)
        draw.line([(cx, cy - 30), (cx - 20, cy + 90)], fill=INK_BLACK, width=6)
        draw.line([(cx - 10, cy + 15), (cx - 50, cy + 75)], fill=INK_BLACK, width=5)
        draw.line([(cx - 10, cy + 15), (cx + 40, cy + 75)], fill=INK_BLACK, width=5)
    elif state == "happy":
        draw.arc([cx - 26, cy - 80, cx - 8, cy - 62], 180, 360, fill=INK_BLACK, width=4)
        draw.arc([cx + 8, cy - 80, cx + 26, cy - 62], 180, 360, fill=INK_BLACK, width=4)
        draw.arc([cx - 20, cy - 60, cx + 20, cy - 38], 0, 180, fill=INK_BLACK, width=5)
        draw.line([(cx, cy - 30), (cx, cy + 90)], fill=INK_BLACK, width=6)
        # Victory arms
        draw.line([(cx, cy + 10), (cx - 55, cy - 35)], fill=INK_BLACK, width=6)
        draw.line([(cx, cy + 10), (cx + 55, cy - 35)], fill=INK_BLACK, width=6)

def draw_skillet(draw, cx, cy, scale=1.0):
    # Skillet circle
    r = int(90 * scale)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(45, 45, 45), outline=INK_BLACK, width=6)
    draw.ellipse([cx - r + 15, cy - r + 15, cx + r - 15, cy + r - 15], fill=(70, 70, 70))
    # Handle
    handle_len = int(140 * scale)
    draw_wobbly_line(draw, (cx + r - 10, cy), (cx + r + handle_len, cy + 30), color=INK_BLACK, width=12)

def draw_noodle_bowl(draw, cx, cy, t=0.0):
    # Bowl body
    draw.pieslice([cx - 130, cy - 80, cx + 130, cy + 100], 0, 180, fill=COLOR_CORAL, outline=INK_BLACK, width=6)
    draw.ellipse([cx - 130, cy - 95, cx + 130, cy - 60], fill=(245, 215, 120), outline=INK_BLACK, width=6)
    # Wavy noodles inside
    for ox in [-70, -30, 10, 50]:
        draw.arc([cx + ox - 20, cy - 85, cx + ox + 20, cy - 65], 0, 180, fill=INK_BLACK, width=4)
    # Steam
    s_off = math.sin(t * 6) * 12
    draw.arc([cx - 40 + s_off, cy - 160, cx - 10 + s_off, cy - 90], 270, 90, fill=INK_MUTED, width=4)
    draw.arc([cx + 10 - s_off, cy - 170, cx + 40 - s_off, cy - 90], 270, 90, fill=INK_MUTED, width=4)

# ----------------- TIMELINE SCENE RENDERER -----------------

def render_frame_for_time(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_PAPER)
    draw = ImageDraw.Draw(img)
    
    # Paper border & margins
    draw_wobbly_line(draw, (50, 40), (WIDTH - 50, 40), color=(225, 220, 210), width=3)
    draw_wobbly_line(draw, (50, HEIGHT - 110), (WIDTH - 50, HEIGHT - 110), color=(225, 220, 210), width=3)
    
    # Subtitle pill background & caption
    caption = ""
    
    # ---------------- SCENE 1: THE MIDNIGHT CRISIS (0 - 18s) ----------------
    if t < 18.0:
        if t < 2.5:
            caption = "Production is broken."
            # Server smoking
            draw_doodle_box(draw, [W//2 - 240, 220, W//2 + 240, 680], fill=(255, 255, 255), outline=INK_BLACK, width=7)
            draw_doodle_pill(draw, [W//2 - 190, 260, W//2 + 190, 330], "STATUS: 500 CRASH", FONT_TITLE, fill=COLOR_CORAL, text_color=(255,255,255))
            # Smoke puffs
            for i, (sx, sy, r) in enumerate([(-100, -80, 45), (0, -110, 55), (90, -80, 50)]):
                draw.ellipse([W//2 + sx - r, 220 + sy - r, W//2 + sx + r, 220 + sy + r], fill=(200, 200, 200), outline=INK_BLACK, width=4)
            draw.text((W//2 - 180, 400), "FATAL: Connection Refused\nPods CrashLoopBackOff\nCluster CPU: 99.8%", font=FONT_BODY, fill=INK_BLACK)
            draw_doodle_pill(draw, [W//2 - 280, 740, W//2 + 280, 830], "PRODUCTION IS BROKEN", FONT_HERO, fill=COLOR_CORAL, text_color=(255, 255, 255))
            
        elif t < 5.0:
            caption = "Dinner shouldn't be."
            draw_noodle_bowl(draw, W//2, 460, t)
            draw_doodle_pill(draw, [W//2 - 240, 180, W//2 + 240, 270], "DINNER SHOULDN'T BE", FONT_HERO, fill=COLOR_GREEN, text_color=(255, 255, 255))
            draw_doodle_pill(draw, [W//2 - 180, 700, W//2 + 180, 770], "WARM • SIMPLE • EDIBLE", FONT_SUBTITLE, fill=COLOR_YELLOW)
            
        elif t < 8.5:
            caption = "You've spent eight hours debugging,"
            draw_stick_figure(draw, W//2 - 150, 480, state="tired", t=t)
            # Desk & laptop
            draw_wobbly_line(draw, (W//2 - 350, 570), (W//2 + 100, 570), width=6)
            draw_doodle_box(draw, [W//2 - 230, 490, W//2 - 110, 570], fill=(230, 230, 230))
            # Clock
            draw.ellipse([W//2 + 180, 260, W//2 + 420, 500], fill=(255, 255, 255), outline=INK_BLACK, width=7)
            draw.text((W//2 + 240, 350), "8h", font=FONT_HERO, fill=COLOR_CORAL)
            draw_doodle_pill(draw, [W//2 - 320, 720, W//2 + 320, 810], "8 HOURS OF CODE DECAY", FONT_TITLE, fill=COLOR_YELLOW)
            
        elif t < 11.5:
            caption = "your brain is running on fumes,"
            draw.ellipse([W//2 - 220, 240, W//2 + 220, 540], fill=(255, 235, 235), outline=INK_BLACK, width=7)
            draw.text((W//2 - 110, 340), "BRAIN", font=FONT_HERO, fill=INK_BLACK)
            # Fuel Gauge
            draw_doodle_box(draw, [W//2 - 260, 600, W//2 + 260, 720], fill=(255, 255, 255), outline=INK_BLACK, width=6)
            draw.text((W//2 - 220, 630), "E", font=FONT_HERO, fill=COLOR_CORAL)
            draw.text((W//2 + 180, 630), "F", font=FONT_HERO, fill=INK_MUTED)
            draw.line([(W//2, 690), (W//2 - 170, 630)], fill=COLOR_CORAL, width=8)
            draw_doodle_pill(draw, [W//2 - 200, 770, W//2 + 200, 840], "ENERGY: 0%", FONT_SUBTITLE, fill=COLOR_CORAL, text_color=(255, 255, 255))
            
        elif t < 14.8:
            caption = "and your fridge has four ingredients that don't look like a meal."
            # Fridge door open
            draw_doodle_box(draw, [W//2 - 360, 180, W//2 + 360, 740], fill=(255, 255, 255), outline=INK_BLACK, width=7)
            draw.line([(W//2 - 360, 420), (W//2 + 360, 420)], fill=INK_BLACK, width=5)
            draw.line([(W//2 - 360, 580), (W//2 + 360, 580)], fill=INK_BLACK, width=5)
            # 4 tiny items
            draw_doodle_pill(draw, [W//2 - 280, 470, W//2 - 150, 540], "Ramen", FONT_BADGE, fill=COLOR_YELLOW)
            draw_doodle_pill(draw, [W//2 - 120, 470, W//2 + 10, 540], "PB", FONT_BADGE, fill=COLOR_ORANGE)
            draw_doodle_pill(draw, [W//2 + 40, 470, W//2 + 140, 540], "Soy", FONT_BADGE, fill=COLOR_PURPLE, text_color=(255,255,255))
            draw_doodle_pill(draw, [W//2 + 170, 470, W//2 + 290, 540], "Heat", FONT_BADGE, fill=COLOR_CORAL, text_color=(255,255,255))
            draw.text((W//2 - 160, 260), "4 SAD ITEMS", font=FONT_TITLE, fill=COLOR_CORAL)
            
        else:
            caption = "The last thing you need... is a recipe that demands another hour of work."
            draw_doodle_box(draw, [W//2 - 320, 180, W//2 + 320, 700], fill=(255, 255, 255), outline=INK_BLACK, width=8)
            draw.text((W//2 - 260, 230), "FANCY RECIPE SCAM", font=FONT_TITLE, fill=COLOR_CORAL)
            draw.text((W//2 - 260, 330), "• Step 1: Caramelize shallots (45m)\n• Step 2: Use 6 prep bowls\n• Step 3: Clean 3 pots\n• Step 4: Cry in the sink", font=FONT_BODY, fill=INK_BLACK)
            draw_wobbly_line(draw, (W//2 - 300, 200), (W//2 + 300, 680), color=COLOR_CORAL, width=14)
            draw_wobbly_line(draw, (W//2 + 300, 200), (W//2 - 300, 680), color=COLOR_CORAL, width=14)
            draw_doodle_pill(draw, [W//2 - 220, 740, W//2 + 220, 830], "REJECTED!", FONT_HERO, fill=COLOR_CORAL, text_color=(255, 255, 255))

    # ---------------- SCENE 2: MEET SLOTHCHEF & CONTRACT (18 - 38s) ----------------
    elif t < 38.0:
        if t < 23.5:
            caption = "Meet SlothChef: an extreme low-effort cooking companion..."
            draw_sloth(draw, W//2, 420, hat=True, wink=(int(t*2)%2 == 0), wave=True, t=t)
            draw_doodle_pill(draw, [W//2 - 240, 160, W//2 + 240, 250], "SLOTHCHEF AI", FONT_HERO, fill=COLOR_YELLOW)
            draw_doodle_pill(draw, [W//2 - 340, 690, W//2 + 340, 760], "THE LOW-EFFORT SURVIVAL ENGINE", FONT_SUBTITLE, fill=(255, 255, 255))
            
        elif t < 28.5:
            caption = "...built for people who want dinner, not a second project."
            draw_stick_figure(draw, W//2 - 280, 480, state="happy", t=t)
            draw_doodle_box(draw, [W//2 - 120, 240, W//2 + 420, 660], fill=(255, 255, 255), outline=INK_BLACK, width=6)
            draw.text((W//2 - 80, 280), "CORPORATE COOKING GANTT", font=FONT_SUBTITLE, fill=INK_MUTED)
            draw.text((W//2 - 80, 360), "Sprint 1: Mise en place\nSprint 2: Whisk hollandaise\nSprint 3: Soak 5 pans", font=FONT_BODY, fill=INK_BLACK)
            draw_wobbly_line(draw, (W//2 - 100, 260), (W//2 + 400, 640), color=COLOR_CORAL, width=12)
            draw_wobbly_line(draw, (W//2 + 400, 260), (W//2 - 100, 640), color=COLOR_CORAL, width=12)
            draw_doodle_pill(draw, [W//2 - 260, 720, W//2 + 260, 800], "NO SECOND PROJECTS", FONT_TITLE, fill=COLOR_GREEN, text_color=(255, 255, 255))
            
        elif t < 33.5:
            caption = "Give it what you've got. Let it help you figure out what you can make."
            draw_doodle_box(draw, [200, 240, W - 200, 660], fill=(255, 255, 255), outline=INK_BLACK, width=7)
            draw.text((250, 290), "INPUT: 4 RANDOM FRIDGE ITEMS", font=FONT_TITLE, fill=INK_BLACK)
            draw.text((250, 380), "➔ Automatic Chemistry Extraction\n➔ Strict Single-Vessel Mapping\n➔ Instant Recipe Synthesis", font=FONT_SUBTITLE, fill=COLOR_PURPLE)
            draw_sloth(draw, W - 360, 450, hat=True, wink=False)
            draw_doodle_pill(draw, [250, 540, 650, 620], "ZERO SHOPPING RUNS", FONT_TITLE, fill=COLOR_YELLOW)
            
        else:
            caption = "The Sloth Contract: strictly one vessel, zero cutting boards, under 5 minutes."
            cards = [
                ("1 VESSEL CAP", "1 skillet, pot, or bowl", COLOR_YELLOW),
                ("0 CUTTING BOARDS", "Crush with mug, tear greens", COLOR_CORAL),
                ("< 5 MIN STANDING", "Save energy, eat quickly", COLOR_GREEN)
            ]
            cw = 480
            for i, (head, sub, col) in enumerate(cards):
                cx = 120 + i * (cw + 50)
                draw_doodle_box(draw, [cx, 240, cx + cw, 680], fill=(255, 255, 255), outline=INK_BLACK, width=6)
                draw_doodle_pill(draw, [cx + 25, 280, cx + cw - 25, 360], head, FONT_SUBTITLE, fill=col, text_color=INK_BLACK if col==COLOR_YELLOW else (255,255,255))
                draw.text((cx + 40, 420), sub, font=FONT_BODY, fill=INK_BLACK)
            draw_doodle_pill(draw, [W//2 - 280, 740, W//2 + 280, 820], "STRICT SLOTH CONTRACT", FONT_HERO, fill=INK_BLACK, text_color=(255, 255, 255))

    # ---------------- SCENE 3: REAL PRODUCT DEMO (38 - 83.5s) ----------------
    elif t < 83.5:
        if t < 48.0:
            caption = "Let's test the post-deploy pantry: instant ramen, peanut butter, soy, sriracha."
            items = [
                ("🍜 RAMEN", COLOR_YELLOW),
                ("🥜 PEANUT BUTTER", COLOR_ORANGE),
                ("🍶 SOY SAUCE", COLOR_PURPLE),
                ("🌶️ SRIRACHA", COLOR_CORAL)
            ]
            iw = 380
            for i, (name, col) in enumerate(items):
                ix = 140 + i * (iw + 45)
                draw_doodle_box(draw, [ix, 280, ix + iw, 620], fill=(255, 255, 255), outline=INK_BLACK, width=6)
                draw_doodle_pill(draw, [ix + 20, 340, ix + iw - 20, 440], name, FONT_TITLE, fill=col, text_color=INK_BLACK if col in [COLOR_YELLOW, COLOR_ORANGE] else (255,255,255))
                draw.text((ix + 60, 510), "In Pantry: OK", font=FONT_BODY, fill=COLOR_GREEN)
            draw_doodle_pill(draw, [W//2 - 320, 700, W//2 + 320, 790], "1-CLICK PRESET DISASTER", FONT_HERO, fill=COLOR_GREEN, text_color=(255, 255, 255))
            
        elif t < 58.0:
            caption = "SlothChef turns those ingredients into a practical starting point..."
            # Funnel diagram
            draw.polygon([(W//2 - 300, 200), (W//2 + 300, 200), (W//2 + 100, 450), (W//2 - 100, 450)], fill=(255, 255, 255), outline=INK_BLACK)
            draw.text((W//2 - 180, 250), "4 RAW INGREDIENTS", font=FONT_TITLE, fill=INK_BLACK)
            draw.text((W//2 - 90, 340), "TabPFN Matrix", font=FONT_SUBTITLE, fill=COLOR_PURPLE)
            # Arrow down
            draw.polygon([(W//2, 530), (W//2 - 40, 460), (W//2 + 40, 460)], fill=COLOR_GREEN)
            draw_doodle_pill(draw, [W//2 - 320, 560, W//2 + 320, 680], "MIDNIGHT DAN-DAN RESCUE", FONT_TITLE, fill=COLOR_YELLOW)
            draw_doodle_pill(draw, [W//2 - 200, 720, W//2 + 200, 790], "HARMONY: 94%", FONT_TITLE, fill=COLOR_GREEN, text_color=(255, 255, 255))
            
        elif t < 68.0:
            caption = "It synthesizes the Midnight Dan-Dan Rescue: 1 skillet, 1 fork, 3 mins active cooking."
            draw_skillet(draw, W//2 - 320, 440, scale=1.3)
            # Fork
            draw.line([(W//2 + 50, 320), (W//2 + 50, 560)], fill=INK_BLACK, width=10)
            draw.line([(W//2 + 30, 320), (W//2 + 70, 320)], fill=INK_BLACK, width=6)
            draw.line([(W//2 + 30, 300), (W//2 + 30, 340)], fill=INK_BLACK, width=6)
            draw.line([(W//2 + 70, 300), (W//2 + 70, 340)], fill=INK_BLACK, width=6)
            # Stopwatch
            draw_doodle_box(draw, [W//2 + 160, 320, W//2 + 440, 560], fill=(255, 255, 255), outline=INK_BLACK, width=6)
            draw.text((W//2 + 200, 400), "03:00", font=FONT_HERO, fill=COLOR_GREEN)
            draw.text((W//2 + 210, 490), "STAND TIME", font=FONT_BADGE, fill=INK_MUTED)
            draw_doodle_pill(draw, [W//2 - 300, 710, W//2 + 300, 800], "1 SKILLET • 1 FORK • 3 MINS", FONT_TITLE, fill=COLOR_YELLOW)
            
        elif t < 76.5:
            caption = "Radical shortcuts: crush garlic flat with a coffee mug, tear greens bare-handed."
            # Left: Coffee mug crushing
            draw_doodle_box(draw, [200, 220, 850, 680], fill=(255, 255, 255), outline=INK_BLACK, width=6)
            draw_doodle_pill(draw, [250, 260, 800, 330], "MUG CRUSH METHOD", FONT_TITLE, fill=COLOR_CORAL, text_color=(255, 255, 255))
            draw.text((280, 420), "Smash garlic with bottom of mug.\nZero knives. Zero cutting boards.\nToss directly in pan.", font=FONT_BODY, fill=INK_BLACK)
            # Right: Tear greens
            draw_doodle_box(draw, [1000, 220, 1650, 680], fill=(255, 255, 255), outline=INK_BLACK, width=6)
            draw_doodle_pill(draw, [1050, 260, 1600, 330], "BARE HAND TEAR", FONT_TITLE, fill=COLOR_GREEN, text_color=(255, 255, 255))
            draw.text((1080, 420), "Rip scallions with bare fingers.\nNo dicing. No prep plates.\nEat directly from skillet.", font=FONT_BODY, fill=INK_BLACK)
            draw_doodle_pill(draw, [W//2 - 250, 730, W//2 + 250, 810], "RADICAL SLOTH SHORTCUTS", FONT_TITLE, fill=COLOR_YELLOW)
            
        else:
            caption = "Cook-Along mode reads steps aloud with an audible timer -- no dirty screen touches."
            # Smartphone with chime
            draw_doodle_box(draw, [W//2 - 180, 200, W//2 + 180, 640], fill=(255, 255, 255), outline=INK_BLACK, width=7)
            draw.text((W//2 - 120, 260), "STEP 1: SIZZLE", font=FONT_TITLE, fill=COLOR_PURPLE)
            draw.text((W//2 - 140, 360), "Toss PB, soy, sriracha\ninto pan. Stir 1 min.", font=FONT_BODY, fill=INK_BLACK)
            # Chime bell
            draw.ellipse([W//2 + 260, 280, W//2 + 440, 460], fill=COLOR_YELLOW, outline=INK_BLACK, width=6)
            draw.text((W//2 + 300, 340), "DING!", font=FONT_TITLE, fill=COLOR_CORAL)
            draw_doodle_pill(draw, [W//2 - 320, 700, W//2 + 320, 790], "HANDS-FREE COOK-ALONG", FONT_HERO, fill=COLOR_BLUE, text_color=(255, 255, 255))

    # ---------------- SCENE 4: DUAL-AI ARCHITECTURE (83.5 - 118.5s) ----------------
    elif t < 118.5:
        if t < 94.0:
            caption = "A request moves from React frontend into FastAPI backend, through decoupled dual-AI."
            boxes = [
                ("REACT 19", "SPA Interface", COLOR_BLUE),
                ("FASTAPI", "Python Engine", COLOR_GREEN),
                ("TabPFN-3.5", "Prior Labs Foundation", COLOR_PURPLE),
                ("GEMMA 2", "Local Open SLM", COLOR_CORAL)
            ]
            bw = 360
            for i, (top, bot, col) in enumerate(boxes):
                bx = 120 + i * (bw + 55)
                draw_doodle_box(draw, [bx, 280, bx + bw, 620], fill=(255, 255, 255), outline=INK_BLACK, width=6)
                draw_doodle_pill(draw, [bx + 20, 330, bx + bw - 20, 420], top, FONT_TITLE, fill=col, text_color=(255, 255, 255) if col != COLOR_YELLOW else INK_BLACK)
                draw.text((bx + 40, 490), bot, font=FONT_SUBTITLE, fill=INK_BLACK)
            draw_doodle_pill(draw, [W//2 - 300, 710, W//2 + 300, 800], "DECOUPLED DUAL-AI PIPELINE", FONT_HERO, fill=COLOR_YELLOW)
            
        elif t < 107.0:
            caption = "TabPFN evaluates continuous chemical vectors: umami, salt, acidity, lipids..."
            sliders = [
                ("UMAMI", 88, COLOR_PURPLE),
                ("SALT", 92, COLOR_BLUE),
                ("ACIDITY", 74, COLOR_YELLOW),
                ("LIPIDS", 85, COLOR_ORANGE)
            ]
            sw = 360
            for i, (name, val, col) in enumerate(sliders):
                sx = 140 + i * (sw + 65)
                draw_doodle_box(draw, [sx, 220, sx + sw, 660], fill=(255, 255, 255), outline=INK_BLACK, width=6)
                draw.text((sx + 50, 260), name, font=FONT_TITLE, fill=INK_BLACK)
                # Meter track
                draw_doodle_box(draw, [sx + 130, 330, sx + 210, 560], fill=(240, 240, 240))
                # Fill level
                fill_h = int(210 * (val / 100.0))
                draw.rectangle([sx + 134, 556 - fill_h, sx + 206, 556], fill=col)
                draw.text((sx + 110, 580), f"{val}%", font=FONT_TITLE, fill=col)
            draw_doodle_pill(draw, [W//2 - 360, 720, W//2 + 360, 810], "PRIOR LABS TabPFN-3.5 IN-CONTEXT", FONT_TITLE, fill=COLOR_PURPLE, text_color=(255, 255, 255))
            
        else:
            caption = "Google Gemma 2 translates exact physical bounds into zero-friction instructions."
            draw_doodle_box(draw, [200, 220, 850, 660], fill=(255, 255, 255), outline=INK_BLACK, width=6)
            draw_doodle_pill(draw, [250, 260, 800, 340], "TABULAR BAYESIAN (<45ms)", FONT_SUBTITLE, fill=COLOR_PURPLE, text_color=(255, 255, 255))
            draw.text((280, 420), "• Continuous In-Context Matrix\n• Synergy: 94% Harmony\n• Standing Bound: <= 5m\n• Zero Hallucinated Ratios", font=FONT_BODY, fill=INK_BLACK)
            
            draw_doodle_box(draw, [950, 220, 1600, 660], fill=(255, 255, 255), outline=INK_BLACK, width=6)
            draw_doodle_pill(draw, [1000, 260, 1550, 340], "GOOGLE GEMMA 2 (LOCAL SLM)", FONT_SUBTITLE, fill=COLOR_CORAL, text_color=(255, 255, 255))
            draw.text((1030, 420), "• Radical Laziness Heuristics\n• Sequential 1-Pan Workflow\n• 1 Fork Cleanup Audit\n• Empathetic Sloth Tone", font=FONT_BODY, fill=INK_BLACK)
            draw_doodle_pill(draw, [W//2 - 340, 720, W//2 + 340, 810], "MATHEMATICS MEETS CULINARY EMPATHY", FONT_TITLE, fill=COLOR_YELLOW)

    # ---------------- SCENE 5: OPEN INNOVATION & DEPLOYMENT (118.5 - 143.5s) ----------------
    elif t < 143.5:
        if t < 130.0:
            caption = "SlothChef is deployed live on Render via multi-stage Docker with health monitoring."
            draw_doodle_box(draw, [150, 220, W - 150, 660], fill=(255, 255, 255), outline=INK_BLACK, width=7)
            draw_doodle_pill(draw, [200, 260, 850, 350], "HOSTED ON RENDER", FONT_TITLE, fill=COLOR_GREEN, text_color=(255, 255, 255))
            draw.text((250, 410), "• Endpoint: slothchef-ai.onrender.com\n• Multi-stage Dockerfile (React Vite + FastAPI Uvicorn)\n• 1-Click Blueprint: render.yaml\n• Live Telemetry: /api/health -> 200 OK", font=FONT_SUBTITLE, fill=INK_BLACK)
            # EKG Pulse
            draw.line([(950, 470), (1100, 470), (1140, 380), (1180, 560), (1220, 440), (1260, 470), (1450, 470)], fill=COLOR_GREEN, width=8)
            draw_doodle_pill(draw, [W//2 - 260, 710, W//2 + 260, 800], "PRODUCTION VERIFIED", FONT_HERO, fill=COLOR_YELLOW)
            
        else:
            caption = "Open innovation keeps private fridge telemetry on your device with zero token anxiety."
            pillars = [
                ("🔒 PRIVATE TELEMETRY", "Midnight fridge habits stay on your device.", COLOR_PURPLE),
                ("⚡ 100% OFFLINE", "Runs off-grid in campervans and power cuts.", COLOR_GREEN),
                ("💰 ZERO TOKEN ANXIETY", "Zero API bills, zero monthly subscriptions.", COLOR_YELLOW)
            ]
            pw = 480
            for i, (p_title, p_desc, col) in enumerate(pillars):
                px = 120 + i * (pw + 50)
                draw_doodle_box(draw, [px, 240, px + pw, 680], fill=(255, 255, 255), outline=INK_BLACK, width=6)
                draw_doodle_pill(draw, [px + 20, 280, px + pw - 20, 360], p_title, FONT_SUBTITLE, fill=col, text_color=INK_BLACK if col==COLOR_YELLOW else (255,255,255))
                draw.text((px + 35, 420), p_desc, font=FONT_BODY, fill=INK_BLACK)
            draw_doodle_pill(draw, [W//2 - 320, 730, W//2 + 320, 820], "WHY OPEN INNOVATION MATTERS", FONT_HERO, fill=COLOR_BLUE, text_color=(255, 255, 255))

    # ---------------- SCENE 6: THE PAYOFF (143.5 - 162.2s) ----------------
    elif t < 162.2:
        caption = "The result: rich Dan-Dan noodles. 38 mins reclaimed, 6 fewer dishes, edible victory."
        draw_noodle_bowl(draw, W//2 - 340, 450, t=t)
        # Stats on right
        draw_doodle_box(draw, [W//2 + 50, 200, W - 150, 680], fill=(255, 255, 255), outline=INK_BLACK, width=6)
        draw_doodle_pill(draw, [W//2 + 100, 240, W - 200, 330], "+38 MINS RECLAIMED", FONT_TITLE, fill=COLOR_GREEN, text_color=(255, 255, 255))
        draw_doodle_pill(draw, [W//2 + 100, 360, W - 200, 450], "6 FEWER DISHES", FONT_TITLE, fill=COLOR_YELLOW)
        draw_doodle_pill(draw, [W//2 + 100, 480, W - 200, 570], "1 SKILLET • 1 FORK", FONT_TITLE, fill=COLOR_CORAL, text_color=(255, 255, 255))
        draw.text((W//2 + 110, 600), "Conservation of energy is virtue.", font=FONT_BODY, fill=INK_MUTED)
        draw_doodle_pill(draw, [W//2 - 320, 730, W//2 + 320, 820], "THE EDIBLE VICTORY", FONT_HERO, fill=COLOR_CORAL, text_color=(255, 255, 255))

    # ---------------- SCENE 7: CLOSING CALL TO ACTION (162.2 - 170.0s) ----------------
    else:
        caption = "Production is broken. Dinner shouldn't be. Try SlothChef on Render or GitHub."
        draw_sloth(draw, W//2, 380, hat=True, wink=True, wave=True, t=t)
        draw_doodle_pill(draw, [W//2 - 280, 130, W//2 + 280, 220], "SLOTHCHEF AI", FONT_HERO, fill=COLOR_YELLOW)
        draw_doodle_pill(draw, [W//2 - 420, 580, W//2 + 420, 660], "TRY LIVE: slothchef-ai.onrender.com", FONT_TITLE, fill=COLOR_GREEN, text_color=(255, 255, 255))
        draw_doodle_pill(draw, [W//2 - 420, 680, W//2 + 420, 760], "GITHUB: github.com/tribhu05/slothchef-ai", FONT_TITLE, fill=COLOR_BLUE, text_color=(255, 255, 255))
        draw.text((W//2 - 280, 800), "DEV HACKTOBERFEST 2026: SLOW AND STEADY", font=FONT_BADGE, fill=INK_MUTED)

    # ---------------- BOTTOM SUBTITLE PILL ----------------
    if caption:
        draw_doodle_pill(draw, [100, HEIGHT - 100, WIDTH - 100, HEIGHT - 30], caption, FONT_SUBTITLE_BAR, fill=(245, 242, 235), text_color=INK_BLACK, outline=INK_BLACK, width=4)

    return np.array(img)[:, :, ::-1] # Convert RGB to BGR for OpenCV / FFmpeg

# ----------------- MAIN RENDERING PIPELINE -----------------

def render_animation_video():
    print(f"============================================================")
    print(f"Rendering SlothChef Hand-Drawn Animated Explainer Video")
    print(f"Total Duration: {TOTAL_SECONDS}s | FPS: {FPS} | Total Frames: {TOTAL_FRAMES}")
    print(f"Style: Hand-drawn MS Paint educational YouTube doodle style")
    print(f"Output: {OUTPUT_VIDEO}")
    print(f"============================================================")

    ffmpeg_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "bgr24",
        "-r", str(FPS),
        "-i", "-",                       # Frame input from stdin pipe
        "-i", MASTER_AUDIO,              # Synchronized master audio
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    report_interval = int(FPS * 10) # Print progress every 10 seconds of video
    for frame_idx in range(TOTAL_FRAMES):
        current_time = frame_idx / float(FPS)
        frame_bgr = render_frame_for_time(current_time)
        pipe.stdin.write(frame_bgr.tobytes())

        if frame_idx % report_interval == 0:
            pct = (frame_idx / TOTAL_FRAMES) * 100
            print(f"Rendering: {current_time:.1f}s / {TOTAL_SECONDS:.1f}s ({pct:.1f}% complete)...")

    pipe.stdin.close()
    pipe.wait()

    if pipe.returncode != 0:
        err = pipe.stderr.read().decode('utf-8', errors='ignore')
        print(f"FFmpeg Error: {err}")
        raise RuntimeError("Animation rendering failed")

    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"\n============================================================")
    print(f"SUCCESS: Animated Explainer Video Generated!")
    print(f"File: {OUTPUT_VIDEO} ({size_mb:.2f} MB)")
    print(f"Duration: {TOTAL_SECONDS} seconds (1080p, 30fps)")
    print(f"============================================================")

if __name__ == '__main__':
    render_animation_video()
