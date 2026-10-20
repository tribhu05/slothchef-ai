import csv
from pathlib import Path
from typing import Dict, List, Optional
from app.models.schemas import IngredientItem

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "flavor_matrix.csv"

# Global cache of known ingredients
INGREDIENT_DATABASE: Dict[str, IngredientItem] = {}

def load_ingredients() -> Dict[str, IngredientItem]:
    global INGREDIENT_DATABASE
    if INGREDIENT_DATABASE:
        return INGREDIENT_DATABASE
    
    if not CSV_PATH.exists():
        return {}

    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["ingredient"].strip().lower()
            INGREDIENT_DATABASE[name] = IngredientItem(
                name=name,
                category=row.get("category", "pantry"),
                umami=float(row.get("umami", 2.0)),
                acidity=float(row.get("acidity", 1.0)),
                richness=float(row.get("richness", 2.0)),
                moisture=float(row.get("moisture", 3.0)),
                saltiness=float(row.get("saltiness", 1.0)),
            )
    return INGREDIENT_DATABASE

def get_ingredient_profile(name: str) -> IngredientItem:
    """Lookup ingredient or infer sensible default chemistry."""
    db = load_ingredients()
    norm_name = name.strip().lower()
    
    # Exact match
    if norm_name in db:
        return db[norm_name]
    
    # Partial substring match
    for k, item in db.items():
        if k in norm_name or norm_name in k:
            return item
            
    # Default fallback for unknown scavenger item
    return IngredientItem(
        name=name.strip(),
        category="misc",
        umami=3.0,
        acidity=2.0,
        richness=2.5,
        moisture=4.0,
        saltiness=2.0
    )

PRESET_DISASTERS = [
    {
        "id": "post-deploy-desperation",
        "title": "Post-Deploy Desperation",
        "emoji": "🍜",
        "description": "It is 2:30 AM, production is stable, your soul is drained, and you have instant ramen and condiments.",
        "ingredients": ["Ramen noodles", "Peanut butter", "Sriracha", "Soy sauce"],
        "vessel_preference": "One Skillet",
        "target_time": "3 mins",
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "college-stale-special",
        "title": "College Stale Special",
        "emoji": "🧀",
        "description": "Stale bottom-of-the-bag chips and canned beans rescued into restaurant-grade chilaquiles.",
        "ingredients": ["Corn tortilla chips", "Canned black beans", "Cheddar cheese", "Salsa (jarred)"],
        "vessel_preference": "One Skillet",
        "target_time": "4 mins",
        "image_url": "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "pantry-pauper-curry",
        "title": "9 PM Pantry Pauper",
        "emoji": "🥥",
        "description": "Canned goods from 2024 that refuse to die, transformed into a velvety luxury stew.",
        "ingredients": ["Canned chickpeas", "Curry powder", "Coconut milk (canned)", "Frozen peas"],
        "vessel_preference": "One Skillet",
        "target_time": "5 mins",
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "midnight-carbonara-cheat",
        "title": "Sloth Carbonara Cheat",
        "emoji": "🍳",
        "description": "Italian grandmothers may weep, but your belly is full in 4 minutes with zero pans to soak.",
        "ingredients": ["Ramen noodles", "Eggs", "Cheddar cheese", "Butter", "Black pepper"],
        "vessel_preference": "Single Pot",
        "target_time": "4 mins",
        "image_url": "https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "scavenger-tuna-rice",
        "title": "Campfire Tuna Mayo Bowl",
        "emoji": "🐟",
        "description": "Zero heat required. Mix directly in the bowl you eat from. Peak energy conservation.",
        "ingredients": ["Canned tuna", "Rice (cooked/leftover)", "Mayonnaise", "Soy sauce", "Green onion"],
        "vessel_preference": "Microwave Bowl",
        "target_time": "2 mins",
        "image_url": "https://images.unsplash.com/photo-1546069901-d8a1c97a5a8e?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "sloth-kimchi-rice",
        "title": "Sleepy Kimchi Sizzle",
        "emoji": "🥬",
        "description": "Cold rice + sour fermented cabbage + sizzled egg. The ultimate 1-skillet comfort.",
        "ingredients": ["Rice (cooked/leftover)", "Kimchi", "Eggs", "Butter", "Soy sauce"],
        "vessel_preference": "One Skillet",
        "target_time": "4 mins",
        "image_url": "https://images.unsplash.com/photo-1590301157890-4810ed352733?auto=format&fit=crop&w=800&q=80"
    }
]
