import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "assets", "cards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1920x1080 dimensions
W, H = 1920, 1080

# SlothChef Color Palette
BG_DARK = (24, 24, 24)          # #181818 Deep Charcoal
SURFACE = (32, 32, 32)          # #202020 Card surface
SURFACE_LIGHT = (42, 42, 42)    # #2A2A2A
TEXT_LIGHT = (245, 242, 235)    # #F5F2EB Cream White
TEXT_MUTED = (165, 163, 157)    # #A5A39D Gray
ACCENT_GOLD = (244, 215, 121)   # #F4D779 Butter Gold
ACCENT_GREEN = (16, 185, 129)   # Emerald 500
ACCENT_RED = (239, 68, 68)      # Red 500
ACCENT_BLUE = (59, 130, 246)    # Blue 500
ACCENT_PURPLE = (139, 92, 246)  # Purple 500
BORDER_COLOR = (55, 55, 55)

# Fonts
try:
    FONT_HERO = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 68)
    FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 46)
    FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 30)
    FONT_BODY = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24)
    FONT_BADGE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    FONT_MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22)
    FONT_MONO_LG = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 32)
except Exception:
    FONT_HERO = ImageFont.load_default()
    FONT_TITLE = ImageFont.load_default()
    FONT_SUBTITLE = ImageFont.load_default()
    FONT_BODY = ImageFont.load_default()
    FONT_BADGE = ImageFont.load_default()
    FONT_MONO = ImageFont.load_default()
    FONT_MONO_LG = ImageFont.load_default()

def draw_pill(draw, box, text, font, fill=SURFACE_LIGHT, text_color=TEXT_LIGHT, border=BORDER_COLOR):
    draw.rounded_rectangle(box, radius=12, fill=fill, outline=border, width=2)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = box[0] + (box[2] - box[0] - tw) // 2
    y = box[1] + (box[3] - box[1] - th) // 2 - 2
    draw.text((x, y), text, font=font, fill=text_color)

# Card 1: Midnight Crisis Hook
def create_card_scene1():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Background terminal simulation box
    term_box = (140, 100, W - 140, H - 220)
    draw.rounded_rectangle(term_box, radius=20, fill=(18, 18, 18), outline=(45, 45, 45), width=2)
    
    # Terminal header dots
    draw.ellipse((170, 125, 186, 141), fill=(239, 68, 68))
    draw.ellipse((196, 125, 212, 141), fill=(245, 158, 11))
    draw.ellipse((222, 125, 238, 141), fill=(16, 185, 129))
    draw.text((260, 122), "bash -- dev-cluster-prod -- 02:47 AM", font=FONT_MONO, fill=TEXT_MUTED)
    
    # Terminal code / error simulation
    code_lines = [
        "$ kubectl get pods -n production",
        "NAME                              READY   STATUS             RESTARTS   AGE",
        "api-gateway-7b9d8c-4x9pl          0/1     CrashLoopBackOff   14         8h12m",
        "ERR_DATABASE_CONNECTION_POOL_EXHAUSTION: [Errno 111] Connection refused",
        "FATAL: Production deploy stalled. Developer energy: 2%",
        "---",
        "$ cat /dev/fridge",
        "Inventory: 1x instant ramen, 2x tbsp peanut butter, sriracha drizzle, soy sauce splash",
        "ERROR: Zero cooking energy detected. Recipe search requires 45 mins prep + 6 pans."
    ]
    y_code = 180
    for idx, cl in enumerate(code_lines):
        color = TEXT_MUTED
        if "CrashLoopBackOff" in cl or "FATAL" in cl:
            color = ACCENT_RED
        elif "Inventory" in cl or "/dev/fridge" in cl:
            color = ACCENT_GOLD
        elif "$" in cl:
            color = ACCENT_GREEN
        draw.text((180, y_code), cl, font=FONT_MONO, fill=color)
        y_code += 36
        
    # Big Hero Foreground Hook
    hook_box = (100, 600, W - 100, 980)
    draw.rounded_rectangle(hook_box, radius=24, fill=(28, 28, 28), outline=ACCENT_GOLD, width=3)
    
    draw.text((150, 640), "PRODUCTION IS BROKEN. DINNER SHOULDN'T BE.", font=FONT_HERO, fill=ACCENT_GOLD)
    draw.text((150, 735), "You've spent hours debugging. Your fridge has four ingredients that don't look like a meal.", font=FONT_SUBTITLE, fill=TEXT_LIGHT)
    
    # Pill badges
    draw_pill(draw, (150, 840, 480, 910), "8 HOURS DEBUGGING", FONT_BADGE, fill=(45, 20, 20), text_color=ACCENT_RED, border=ACCENT_RED)
    draw_pill(draw, (510, 840, 820, 910), "4 SAD INGREDIENTS", FONT_BADGE, fill=(45, 40, 20), text_color=ACCENT_GOLD, border=ACCENT_GOLD)
    draw_pill(draw, (850, 840, 1140, 910), "0 COOKING ENERGY", FONT_BADGE, fill=(35, 35, 35), text_color=TEXT_MUTED, border=BORDER_COLOR)
    draw_pill(draw, (1170, 840, 1750, 910), "SOLUTION: RADICAL SLOTH HEURISTICS", FONT_BADGE, fill=(20, 45, 30), text_color=ACCENT_GREEN, border=ACCENT_GREEN)
    
    path = os.path.join(OUTPUT_DIR, "card_scene1_hook.png")
    img.save(path)
    print("Saved", path)

# Card 2: Meet SlothChef & The Sloth Contract
def create_card_scene2():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Header Banner
    draw_pill(draw, (140, 70, 520, 120), "DEV HACKTOBERFEST 2026", FONT_BADGE, fill=(40, 30, 10), text_color=ACCENT_GOLD, border=ACCENT_GOLD)
    draw.text((140, 150), "SlothChef AI: Extreme Low-Effort Cooking", font=FONT_HERO, fill=TEXT_LIGHT)
    draw.text((140, 240), "LESS PREP. LESS FRICTION. MORE DINNER.", font=FONT_TITLE, fill=ACCENT_GOLD)
    draw.text((140, 305), "Treating kitchen physical exertion as an asymptotic complexity bound.", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    
    # 4 Strict Sloth Contract Bounds Cards
    bounds = [
        {
            "icon": "1 VESSEL",
            "title": "Strict 1-Vessel Cap",
            "desc": "Exactly 1 skillet, pot, or microwave bowl. Multiple prep dishes violate the Sloth Contract.",
            "color": ACCENT_GOLD
        },
        {
            "icon": "O(< 5m)",
            "title": "Active Standing Bound",
            "desc": "Max 5 minutes on your feet. Long stirs or multi-stage browning are mathematically pruned.",
            "color": ACCENT_GREEN
        },
        {
            "icon": "1 UTENSIL",
            "title": "1 Eating Utensil",
            "desc": "Eat directly from the cooking vessel with 1 fork. Washing bowls is banned by policy.",
            "color": ACCENT_BLUE
        },
        {
            "icon": "0 BOARDS",
            "title": "Zero Cutting Boards",
            "desc": "Crush garlic flat with the bottom of a coffee mug. Tear greens with your bare hands.",
            "color": ACCENT_PURPLE
        }
    ]
    
    card_w = 385
    card_h = 440
    start_x = 140
    y_pos = 420
    
    for i, b in enumerate(bounds):
        x = start_x + i * (card_w + 35)
        # Card Background
        draw.rounded_rectangle((x, y_pos, x + card_w, y_pos + card_h), radius=20, fill=SURFACE, outline=BORDER_COLOR, width=2)
        # Top Accent Badge
        draw_pill(draw, (x + 30, y_pos + 35, x + card_w - 30, y_pos + 95), b["icon"], FONT_MONO_LG, fill=(24, 24, 24), text_color=b["color"], border=b["color"])
        # Title
        draw.text((x + 30, y_pos + 125), b["title"], font=FONT_TITLE, fill=TEXT_LIGHT)
        # Description
        # Word wrap desc
        words = b["desc"].split()
        lines = []
        cur = ""
        for w in words:
            test = cur + " " + w if cur else w
            if len(test) > 24:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
            
        desc_y = y_pos + 205
        for l in lines:
            draw.text((x + 30, desc_y), l, font=FONT_BODY, fill=TEXT_MUTED)
            desc_y += 34
            
    # Bottom footnote
    draw.text((140, 960), "Official Principle: 'Conservation of energy is the supreme evolutionary virtue.'", font=FONT_SUBTITLE, fill=ACCENT_GOLD)
    
    path = os.path.join(OUTPUT_DIR, "card_scene2_sloth_contract.png")
    img.save(path)
    print("Saved", path)

# Card 4: Architecture Diagram
def create_card_scene4():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    draw_pill(draw, (140, 60, 480, 110), "DUAL-ENGINE AI ARCHITECTURE", FONT_BADGE, fill=(30, 20, 45), text_color=ACCENT_PURPLE, border=ACCENT_PURPLE)
    draw.text((140, 135), "Decoupled Culinary Intelligence Pipeline", font=FONT_HERO, fill=TEXT_LIGHT)
    draw.text((140, 220), "Why LLMs alone fail: LLMs hallucinate flavor chemistry and cannot compute physical bounds.", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    
    # 4 Architecture stages horizontally
    stages = [
        {
            "tag": "1. INGESTION",
            "title": "Raw Kitchen Scavenge",
            "sub": "React 19 Frontend",
            "items": ["• 3-5 Scavenged Fridge Items", "• Vessel Cap: Exactly 1 Pan", "• Fatigue Level Constraint", "• Autocomplete Pantry Chips"],
            "color": ACCENT_BLUE,
            "badge": "ZERO-CONFIG"
        },
        {
            "tag": "2. FOUNDATION MODEL",
            "title": "Prior Labs TabPFN-3.5",
            "sub": "In-Context Bayesian Engine",
            "items": ["• Chemical Feature Vectors", "• Umami (88%), Lipids (85%)", "• Salt (92%), Acidity (74%)", "• Single Forward Pass <45ms"],
            "color": ACCENT_GOLD,
            "badge": "CONTINUOUS ACCURACY"
        },
        {
            "tag": "3. LANGUAGE MODEL",
            "title": "Google Gemma 2",
            "sub": "Open-Weight Local SLM",
            "items": ["• Radical Laziness Heuristics", "• Sloth Voice & Tone Engine", "• Sequential 1-Pan Steps", "• Cleanup Dish Audit (0 Extra)"],
            "color": ACCENT_GREEN,
            "badge": "OPEN WEIGHTS"
        },
        {
            "tag": "4. INTERFACE",
            "title": "SlothChef App UX",
            "sub": "FastAPI + Vite Static",
            "items": ["• 1-Click Recipe Cards", "• Cook-Along Voice Mode", "• Web Audio Microwave Chime", "• TabPFN Flavor Telemetry"],
            "color": ACCENT_PURPLE,
            "badge": "100% OFFLINE"
        }
    ]
    
    col_w = 380
    col_h = 490
    y_start = 300
    
    for i, s in enumerate(stages):
        x = 140 + i * (col_w + 38)
        # Stage Box
        draw.rounded_rectangle((x, y_start, x + col_w, y_start + col_h), radius=18, fill=SURFACE, outline=BORDER_COLOR, width=2)
        # Header Badge
        draw_pill(draw, (x + 24, y_start + 24, x + col_w - 24, y_start + 70), s["tag"], FONT_BADGE, fill=(24, 24, 24), text_color=s["color"], border=s["color"])
        # Title
        draw.text((x + 24, y_start + 90), s["title"], font=FONT_TITLE, fill=TEXT_LIGHT)
        draw.text((x + 24, y_start + 145), s["sub"], font=FONT_SUBTITLE, fill=s["color"])
        draw.line((x + 24, y_start + 195, x + col_w - 24, y_start + 195), fill=BORDER_COLOR, width=1)
        
        # Items
        item_y = y_start + 215
        for it in s["items"]:
            draw.text((x + 24, item_y), it, font=FONT_BODY, fill=TEXT_MUTED)
            item_y += 42
            
        # Bottom pill
        draw_pill(draw, (x + 24, y_start + col_h - 60, x + col_w - 24, y_start + col_h - 20), s["badge"], FONT_BADGE, fill=(28, 28, 28), text_color=TEXT_LIGHT, border=BORDER_COLOR)
        
        # Draw connector arrow between stages
        if i < len(stages) - 1:
            arrow_x = x + col_w + 8
            arrow_y = y_start + col_h // 2
            draw.text((arrow_x, arrow_y - 20), "➔", font=FONT_TITLE, fill=ACCENT_GOLD)
            
    # Bottom Summary
    draw.rounded_rectangle((140, 850, W - 140, 990), radius=16, fill=(28, 28, 28), outline=BORDER_COLOR, width=2)
    draw.text((180, 885), "KEY TAKEAWAY: TabPFN-3.5 guarantees mathematical food chemistry before Gemma 2 writes a single word.", font=FONT_SUBTITLE, fill=ACCENT_GOLD)
    draw.text((180, 935), "Zero hallucinated ingredient ratios. Zero unrealistic multi-pan prep workflows.", font=FONT_BODY, fill=TEXT_LIGHT)
    
    path = os.path.join(OUTPUT_DIR, "card_scene4_architecture.png")
    img.save(path)
    print("Saved", path)

# Card 5: Open Innovation & Render Deployment
def create_card_scene5():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    draw_pill(draw, (140, 60, 480, 110), "PRODUCTION & OPEN INNOVATION", FONT_BADGE, fill=(20, 35, 30), text_color=ACCENT_GREEN, border=ACCENT_GREEN)
    draw.text((140, 135), "Deployed Live on Render • Why Open Innovation Matters", font=FONT_HERO, fill=TEXT_LIGHT)
    draw.text((140, 220), "Live Endpoint: https://slothchef-ai.onrender.com | Built for DEV Hacktoberfest 2026", font=FONT_SUBTITLE, fill=ACCENT_GOLD)
    
    # 3 Pillars of Open Innovation
    pillars = [
        {
            "tag": "PILLAR 1",
            "title": "Private Fridge Telemetry",
            "desc": "What and when you eat reveals intimate health, financial, and lifestyle patterns. Cloud AI providers profile your habits for targeted ads. Running open models locally keeps your midnight pantry strictly between you and your machine.",
            "badge": "100% PRIVATE DATA",
            "color": ACCENT_GREEN
        },
        {
            "tag": "PILLAR 2",
            "title": "True Offline Resilience",
            "desc": "Hunger strikes during internet outages, off-grid campervan trips, and remote travel. SlothChef's open-weight SLM and embedded TabPFN heuristic matrix execute completely offline with zero network dependency.",
            "badge": "OFF-GRID SURVIVAL",
            "color": ACCENT_BLUE
        },
        {
            "tag": "PILLAR 3",
            "title": "Zero Token Anxiety",
            "desc": "Commercial API meters create hesitation and cost overhead for simple daily tasks. Open-source models allow SlothChef to run 24/7 as an ambient kitchen assistant without monthly subscriptions or token billing surprises.",
            "badge": "NO RECURRING COSTS",
            "color": ACCENT_GOLD
        }
    ]
    
    col_w = 510
    col_h = 420
    y_start = 290
    
    for i, p in enumerate(pillars):
        x = 140 + i * (col_w + 45)
        draw.rounded_rectangle((x, y_start, x + col_w, y_start + col_h), radius=20, fill=SURFACE, outline=BORDER_COLOR, width=2)
        draw_pill(draw, (x + 30, y_start + 30, x + 200, y_start + 75), p["tag"], FONT_BADGE, fill=(24, 24, 24), text_color=p["color"], border=p["color"])
        draw.text((x + 30, y_start + 95), p["title"], font=FONT_TITLE, fill=TEXT_LIGHT)
        
        # Word wrap description
        words = p["desc"].split()
        lines = []
        cur = ""
        for w in words:
            test = cur + " " + w if cur else w
            if len(test) > 34:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
            
        dy = y_start + 160
        for l in lines:
            draw.text((x + 30, dy), l, font=FONT_BODY, fill=TEXT_MUTED)
            dy += 32
            
        draw_pill(draw, (x + 30, y_start + col_h - 60, x + col_w - 30, y_start + col_h - 20), p["badge"], FONT_BADGE, fill=(28, 28, 28), text_color=p["color"], border=p["color"])
        
    # Render Hosting Proof Banner
    draw.rounded_rectangle((140, 755, W - 140, 990), radius=18, fill=(20, 24, 22), outline=ACCENT_GREEN, width=2)
    draw.text((180, 785), "RENDER CLOUD DEPLOYMENT VERIFICATION", font=FONT_TITLE, fill=ACCENT_GREEN)
    draw.text((180, 845), "• Multi-stage Docker packaging (React 19 Vite compiler + Uvicorn Python runtime)", font=FONT_BODY, fill=TEXT_LIGHT)
    draw.text((180, 885), "• 1-Click Infrastructure Blueprint: render.yaml with automatic environment routing", font=FONT_BODY, fill=TEXT_LIGHT)
    draw.text((180, 925), "• Automated Health Check: /api/health monitoring uptime, dish bounds, and model status", font=FONT_BODY, fill=TEXT_LIGHT)
    
    path = os.path.join(OUTPUT_DIR, "card_scene5_deployment.png")
    img.save(path)
    print("Saved", path)

# Card 6: The Payoff (Food Reveal + Metric Badges)
def create_card_scene6():
    img = Image.new("RGB", (W, H), BG_DARK)
    
    # Load and composite dish image on the right half
    dish_path = os.path.join(SCRIPT_DIR, "assets", "footage", "dan_dan_noodles.jpg")
    if os.path.exists(dish_path):
        dish_img = Image.open(dish_path).convert("RGB")
        # Resize/crop to fill right half (width 960, height 1080)
        dish_img = dish_img.resize((1040, 1080), Image.Resampling.LANCZOS)
        img.paste(dish_img, (880, 0))
        
        # Add subtle dark gradient overlay on the seam
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for gx in range(800, 1050):
            alpha = int(255 * (1.0 - (gx - 800) / 250.0))
            ov_draw.line([(gx, 0), (gx, H)], fill=(24, 24, 24, alpha))
        img.paste(overlay, (0, 0), overlay)
        
    draw = ImageDraw.Draw(img)
    
    # Left Content
    draw_pill(draw, (120, 70, 480, 120), "THE PAYOFF • EDIBLE VICTORY", FONT_BADGE, fill=(40, 30, 10), text_color=ACCENT_GOLD, border=ACCENT_GOLD)
    draw.text((120, 150), "Midnight Dan-Dan Rescue", font=FONT_HERO, fill=ACCENT_GOLD)
    draw.text((120, 240), "Delicious. Velvety. Zero Regrets.", font=FONT_TITLE, fill=TEXT_LIGHT)
    draw.text((120, 305), "Pantry: Instant ramen, peanut butter, sriracha, soy sauce.", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    
    # Metric cards
    metrics = [
        {"val": "+38 MIN", "label": "Life Reclaimed vs Standard Cooking", "color": ACCENT_GREEN},
        {"val": "6 FEWER", "label": "Dirty Dishes & Prep Bowls Eliminated", "color": ACCENT_GOLD},
        {"val": "1 SKILLET", "label": "Cooked & Eaten Straight from Pan", "color": ACCENT_BLUE},
        {"val": "94% SCORE", "label": "TabPFN Mathematical Flavor Harmony", "color": ACCENT_PURPLE}
    ]
    
    my = 380
    for m in metrics:
        draw.rounded_rectangle((120, my, 820, my + 105), radius=16, fill=SURFACE, outline=BORDER_COLOR, width=2)
        draw.text((150, my + 18), m["val"], font=FONT_HERO, fill=m["color"])
        draw.text((400, my + 38), m["label"], font=FONT_BODY, fill=TEXT_LIGHT)
        my += 125
        
    draw.text((120, 930), "\"Conservation of energy is the supreme evolutionary virtue.\"", font=FONT_SUBTITLE, fill=ACCENT_GOLD)
    draw.text((120, 975), "SlothChef AI • DEV Hacktoberfest 2026 Week 3", font=FONT_BODY, fill=TEXT_MUTED)
    
    path = os.path.join(OUTPUT_DIR, "card_scene6_payoff.png")
    img.save(path)
    print("Saved", path)

# Card 7: Closing End Card
def create_card_scene7():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Center Brand Frame
    center_box = (200, 120, W - 200, H - 120)
    draw.rounded_rectangle(center_box, radius=28, fill=SURFACE, outline=ACCENT_GOLD, width=3)
    
    # Top Hackathon Tag
    draw_pill(draw, (W//2 - 240, 170, W//2 + 240, 225), "DEV HACKTOBERFEST 2026: WEEK 3", FONT_BADGE, fill=(40, 30, 10), text_color=ACCENT_GOLD, border=ACCENT_GOLD)
    
    # Big Title
    title = "SlothChef AI"
    bbox = FONT_HERO.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 260), title, font=FONT_HERO, fill=TEXT_LIGHT)
    
    # Tagline
    tagline = "Production is broken. Dinner shouldn't be."
    bbox = FONT_TITLE.getbbox(tagline)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 355), tagline, font=FONT_TITLE, fill=ACCENT_GOLD)
    
    # Subtag
    sub = "The Extreme Low-Effort, One-Pan Survival Engine powered by TabPFN-3.5 and Gemma 2."
    bbox = FONT_SUBTITLE.getbbox(sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 430), sub, font=FONT_SUBTITLE, fill=TEXT_MUTED)
    
    # Call to actions
    draw.rounded_rectangle((320, 520, W - 320, 640), radius=18, fill=(20, 35, 25), outline=ACCENT_GREEN, width=2)
    draw.text((360, 545), "TRY THE LIVE APP:", font=FONT_TITLE, fill=ACCENT_GREEN)
    draw.text((360, 595), "https://slothchef-ai.onrender.com", font=FONT_MONO_LG, fill=TEXT_LIGHT)
    
    draw.rounded_rectangle((320, 670, W - 320, 790), radius=18, fill=(24, 28, 40), outline=ACCENT_BLUE, width=2)
    draw.text((360, 695), "FORK ON GITHUB:", font=FONT_TITLE, fill=ACCENT_BLUE)
    draw.text((360, 745), "https://github.com/tribhu05/slothchef-ai", font=FONT_MONO_LG, fill=TEXT_LIGHT)
    
    # Footer badges
    draw_pill(draw, (320, 840, 680, 895), "100% OPEN SOURCE (MIT)", FONT_BADGE, fill=(28, 28, 28), text_color=TEXT_LIGHT, border=BORDER_COLOR)
    draw_pill(draw, (710, 840, 1140, 895), "PRIOR LABS TABPFN-3.5", FONT_BADGE, fill=(28, 28, 28), text_color=ACCENT_PURPLE, border=BORDER_COLOR)
    draw_pill(draw, (1170, 840, 1600, 895), "GOOGLE GEMMA 2 (LOCAL SLM)", FONT_BADGE, fill=(28, 28, 28), text_color=ACCENT_GREEN, border=BORDER_COLOR)
    
    path = os.path.join(OUTPUT_DIR, "card_scene7_endcard.png")
    img.save(path)
    print("Saved", path)

# Thumbnail (1920x1080 & 1280x720)
def create_thumbnail():
    img = Image.new("RGB", (W, H), BG_DARK)
    
    # Right half food image
    dish_path = os.path.join(SCRIPT_DIR, "assets", "footage", "dan_dan_noodles.jpg")
    if os.path.exists(dish_path):
        dish_img = Image.open(dish_path).convert("RGB")
        dish_img = dish_img.resize((1060, 1080), Image.Resampling.LANCZOS)
        img.paste(dish_img, (860, 0))
        
        # Soft darkening gradient
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for gx in range(700, 1050):
            alpha = int(255 * (1.0 - (gx - 700) / 350.0))
            ov_draw.line([(gx, 0), (gx, H)], fill=(20, 20, 20, alpha))
        img.paste(overlay, (0, 0), overlay)
        
    draw = ImageDraw.Draw(img)
    
    # Big punchy YouTube hook
    draw_pill(draw, (100, 80, 520, 140), "DEV HACKTOBERFEST 2026", FONT_BADGE, fill=(45, 30, 10), text_color=ACCENT_GOLD, border=ACCENT_GOLD)
    
    draw.text((100, 180), "PRODUCTION", font=FONT_HERO, fill=TEXT_LIGHT)
    draw.text((100, 260), "IS BROKEN.", font=FONT_HERO, fill=ACCENT_RED)
    
    draw.text((100, 380), "DINNER", font=FONT_HERO, fill=TEXT_LIGHT)
    draw.text((100, 460), "SHOULDN'T BE.", font=FONT_HERO, fill=ACCENT_GOLD)
    
    # Sloth badge
    draw.rounded_rectangle((100, 600, 780, 780), radius=22, fill=(28, 28, 28), outline=BORDER_COLOR, width=3)
    draw.text((140, 630), "SlothChef AI", font=FONT_HERO, fill=ACCENT_GOLD)
    draw.text((140, 715), "The Extreme Low-Effort 1-Pan Survival Engine", font=FONT_BODY, fill=TEXT_LIGHT)
    
    # Pill badges
    draw_pill(draw, (100, 840, 390, 920), "PRIOR LABS TABPFN", FONT_BADGE, fill=(35, 20, 45), text_color=ACCENT_PURPLE, border=ACCENT_PURPLE)
    draw_pill(draw, (420, 840, 740, 920), "GOOGLE GEMMA 2", FONT_BADGE, fill=(20, 40, 25), text_color=ACCENT_GREEN, border=ACCENT_GREEN)
    draw_pill(draw, (100, 940, 540, 1010), "LIVE ON RENDER: slothchef-ai.onrender.com", FONT_BADGE, fill=(20, 20, 20), text_color=TEXT_LIGHT, border=BORDER_COLOR)
    
    # Big round badge over image
    draw.ellipse((1480, 80, 1820, 420), fill=(244, 215, 121), outline=(255, 255, 255), width=6)
    draw.text((1540, 180), "3 MIN", font=FONT_HERO, fill=(24, 24, 24))
    draw.text((1550, 265), "1 PAN", font=FONT_TITLE, fill=(24, 24, 24))
    draw.text((1535, 330), "0 DISHES", font=FONT_BADGE, fill=(100, 80, 20))
    
    thumb_path = os.path.join(OUTPUT_DIR, "thumbnail.png")
    img.save(thumb_path)
    img.save(os.path.join(SCRIPT_DIR, "thumbnail.png"))
    print("Saved thumbnail:", thumb_path)

if __name__ == '__main__':
    create_card_scene1()
    create_card_scene2()
    create_card_scene4()
    create_card_scene5()
    create_card_scene6()
    create_card_scene7()
    create_thumbnail()
    print("All graphic cards and thumbnail generated successfully!")
