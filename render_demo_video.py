import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Video Configuration
WIDTH, HEIGHT = 1920, 1080
FPS = 24
OUTPUT_FILE = "slothchef_demo.mp4"

# Color Palette
BG_COLOR = (24, 24, 24)           # #181818 Deep Charcoal
CARD_BG = (32, 32, 32)           # #202020 Surface
TEXT_PRIMARY = (245, 242, 235)   # #F5F2EB Cream White
TEXT_MUTED = (165, 163, 157)     # #A5A39D Gray
ACCENT_GOLD = (244, 215, 121)    # #F4D779 Butter Gold
ACCENT_GREEN = (16, 185, 129)    # Emerald 500
BORDER_COLOR = (50, 50, 50)

# Fonts
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 52)
FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 32)
FONT_BODY = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 26)
FONT_MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 24)
FONT_BADGE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
FONT_HERO = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 74)

SCENES = [
    {
        "title": "THE MIDNIGHT CRISIS",
        "tag": "Scene 1: The Problem",
        "headline": "9:30 PM. 8 Hours Debugging. 4 Sad Ingredients.",
        "quote": "\"Cooking should take less effort than deciding what to eat.\"",
        "bullet1": "• Fridge Inventory: 1 Ramen packet, 2 tbsp Peanut Butter, Sriracha, Soy Sauce",
        "bullet2": "• The Online Recipe Scam: 45 min caramelizing shallots, 6 dirty prep bowls, 3 pans",
        "bullet3": "• Result: Sore feet, exhaustion, and a sink overflowing with regret",
        "badge": "CHALLENGE: CHANNEL YOUR INNER SLOTH",
        "duration_sec": 8
    },
    {
        "title": "THE SLOTH PHILOSOPHY",
        "tag": "Scene 2: Asymptotic Bounds",
        "headline": "Treating Kitchen Exertion as an Algorithmic Complexity Problem",
        "quote": "\"Conservation of energy is the supreme evolutionary virtue.\"",
        "bullet1": "• Active Standing Time Bound: O(< 5 minutes on your feet)",
        "bullet2": "• Cookware Space Bound: Exactly 1 vessel (skillet, pot, or microwave bowl)",
        "bullet3": "• Utensil & Prep Bound: 1 fork (eat from pan) & zero cutting boards",
        "badge": "STRICT SLOTH CONTRACT ENFORCED",
        "duration_sec": 8
    },
    {
        "title": "THE KITCHEN WORKBENCH",
        "tag": "Scene 3: Live Application Demo",
        "headline": "Post-Deploy Desperation ➔ Midnight Dan-Dan Rescue",
        "quote": "\"Crush garlic flat with a coffee mug. Life is too short to dice.\"",
        "bullet1": "• 1-Click Desperation Menu: Tap preset to instantly load and synthesize",
        "bullet2": "• Ingredients in this Pan: Explicitly tags core staples vs optional garnishes",
        "bullet3": "• Cook-Along Mode: Hands-free voice readouts & Web Audio microwave chime ding",
        "badge": "VERIFIED 1-PAN HIGH-RES PRESENTATION",
        "duration_sec": 9
    },
    {
        "title": "PRIOR LABS TABPFN-3.5",
        "tag": "Scene 4: Tabular Foundation Model",
        "headline": "Chemical Flavor Vectors & In-Context Bayesian Inference",
        "quote": "\"Single forward pass (< 45ms) over continuous sensory feature matrices.\"",
        "bullet1": "• Feature Extraction: Umami (88%), Richness (85%), Acidity (74%), Salt (92%)",
        "bullet2": "• Mathematical Synergy: Sriracha acetic acid cuts heavy peanut butter lipids",
        "bullet3": "• Active Fatigue Prediction: Accurately models physical human energy tax",
        "badge": "BEST USE OF TABPFN ($200 CATEGORY)",
        "duration_sec": 9
    },
    {
        "title": "DEPLOYED ON RENDER",
        "tag": "Scene 5: Production & Privacy",
        "headline": "slothchef-ai.onrender.com (Live Full-Stack Web Service)",
        "quote": "\"Private fridge telemetry. 100% offline-resilient. Zero token anxiety.\"",
        "bullet1": "• Architecture: Multi-stage Dockerfile compiling React 19 SPA & FastAPI backend",
        "bullet2": "• Infrastructure as Code: 1-Click Blueprint (render.yaml) & /api/health monitoring",
        "bullet3": "• Why Open Innovation: Midnight pantry habits stay strictly on your machine",
        "badge": "BEST USE OF RENDER ($200 CATEGORY)",
        "duration_sec": 9
    },
    {
        "title": "SLOTHCHEF: REWARDING LAZINESS",
        "tag": "Scene 6: Final Words & Try It Live",
        "headline": "Built for DEV Hacktoberfest 2026: Week 3 (Slow and Steady)",
        "quote": "\"Life is too short to wash colanders. Let AI do the dishes.\"",
        "bullet1": "• Live Hosted Demo: https://slothchef-ai.onrender.com",
        "bullet2": "• GitHub Repository: https://github.com/tribhu05/slothchef-ai",
        "bullet3": "• Benchmark: Reclaims 38 minutes of human life & eliminates 6 dirty dishes per meal",
        "badge": "OCTOBER 2026 • INTERNATIONAL SLOTH DAY",
        "duration_sec": 9
    }
]

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def render_frame(scene, scene_progress, total_progress, scene_idx, total_scenes):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top Brand Navigation Bar
    draw_rounded_rect(draw, (80, 50, WIDTH - 80, 130), 20, CARD_BG, BORDER_COLOR)
    draw.text((110, 68), "🍳🦥 SlothChef Studio", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.text((WIDTH - 550, 75), f"DEV Hacktoberfest 2026 | Week 3", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # Main Center Card
    card_box = (80, 160, WIDTH - 80, HEIGHT - 110)
    draw_rounded_rect(draw, card_box, 30, CARD_BG, BORDER_COLOR, width=2)

    # Scene Tag & Badge
    draw_rounded_rect(draw, (120, 200, 480, 250), 12, (45, 45, 45), ACCENT_GOLD)
    draw.text((140, 212), scene["tag"].upper(), font=FONT_BADGE, fill=ACCENT_GOLD)

    draw_rounded_rect(draw, (WIDTH - 520, 200, WIDTH - 120, 250), 12, (20, 45, 30), ACCENT_GREEN)
    draw.text((WIDTH - 500, 212), scene["badge"], font=FONT_BADGE, fill=ACCENT_GREEN)

    # Hero Title & Headline
    draw.text((120, 280), scene["title"], font=FONT_HERO, fill=ACCENT_GOLD)
    draw.text((120, 380), scene["headline"], font=FONT_SUBTITLE, fill=TEXT_PRIMARY)

    # Quote Box
    draw_rounded_rect(draw, (120, 440, WIDTH - 120, 510), 16, (20, 20, 20), (60, 60, 60))
    draw.text((150, 458), scene["quote"], font=FONT_SUBTITLE, fill=ACCENT_GOLD)

    # Content Bullets
    y_pos = 550
    bullets = [scene["bullet1"], scene["bullet2"], scene["bullet3"]]
    for b in bullets:
        draw_rounded_rect(draw, (120, y_pos, WIDTH - 120, y_pos + 70), 16, (26, 26, 26), BORDER_COLOR)
        draw.text((150, y_pos + 18), b, font=FONT_BODY, fill=TEXT_PRIMARY)
        y_pos += 90

    # Telemetry Footnote
    draw.text((120, 840), "Prior Labs TabPFN-3.5 • Google Gemma 2 • Render Cloud • Strict 1-Pan Guarantee", font=FONT_MONO, fill=TEXT_MUTED)

    # Global Progress Bar at Bottom
    draw.rectangle((0, HEIGHT - 16, WIDTH, HEIGHT), fill=(30, 30, 30))
    bar_width = int(WIDTH * total_progress)
    draw.rectangle((0, HEIGHT - 16, bar_width, HEIGHT), fill=ACCENT_GOLD)

    # Scene Progress Bar (subtle)
    scene_bar_width = int((WIDTH - 240) * scene_progress)
    draw.rectangle((120, 885, 120 + scene_bar_width, 890), fill=ACCENT_GREEN)

    # Convert PIL Image to OpenCV BGR format
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def generate_video():
    total_duration = sum(s["duration_sec"] for s in SCENES)
    total_frames = total_duration * FPS
    print(f"[Generating Video] SlothChef Demo Video: {WIDTH}x{HEIGHT} @ {FPS}fps ({total_duration}s, {total_frames} frames)...")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))

    current_frame = 0
    for s_idx, scene in enumerate(SCENES):
        scene_frames = scene["duration_sec"] * FPS
        print(f"  Rendering [{s_idx + 1}/{len(SCENES)}] {scene['title']} ({scene['duration_sec']}s)...")
        
        for f in range(scene_frames):
            s_prog = f / float(scene_frames)
            t_prog = current_frame / float(total_frames)
            
            frame_img = render_frame(scene, s_prog, t_prog, s_idx, len(SCENES))
            out.write(frame_img)
            current_frame += 1

    out.release()
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"[Success] Video generated successfully: {OUTPUT_FILE} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    generate_video()
