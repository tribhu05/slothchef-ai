import re
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class NormalizedIngredient(BaseModel):
    original_name: str
    canonical_id: str
    canonical_name: str
    category: str  # protein, starch, vegetable, fruit, fat, seasoning, liquid, dairy, legumes, condiments
    state: str = "fresh"  # raw, cooked, dry_grain, canned, frozen, condiment, cured
    is_substantial: bool = True  # True if it can provide calories/bulk; False if condiment/spice
    prep_requirement: str = "none"  # none, needs_liquid, needs_cooking, precooked
    flavor_role: str = "savory"  # savory, sweet, acid, umami, fatty, neutral

    @property
    def raw_name(self) -> str:
        return self.original_name

    @property
    def culinary_state(self) -> str:
        return self.state

# Taxonomy mapping: pattern -> metadata
CANONICAL_RULES = [
    # Starches & Grains
    (r"\b(instant\s+)?ramen(\s+noodles?)?\b", "ramen", "Ramen noodles", "starch", "dry_grain", True, "needs_liquid"),
    (r"\b(uncooked|raw|dry)(\s+white|\s+brown|\s+jasmine|\s+basmati)?\s+rice\b", "dry_rice", "Dry rice", "starch", "dry_grain", True, "needs_boiling"),
    (r"\b(cooked|leftover|day-old|steamed)\s+rice\b", "cooked_rice", "Cooked rice", "starch", "cooked", True, "none"),
    (r"\b(white|brown|jasmine|basmati)?\s*rice\b", "cooked_rice", "Rice", "starch", "cooked", True, "none"),
    (r"\b(corn\s+)?tortilla\s+chips?\b|doritos|tostitos|nachos", "tortilla_chips", "Tortilla chips", "starch", "cooked", True, "none"),
    (r"\b(flour\s+|corn\s+)?tortillas?\b", "tortillas", "Tortillas", "starch", "cooked", True, "none"),
    (r"\b(white\s+|wheat\s+|sourdough\s+)?bread\b|toast", "bread", "Bread", "starch", "cooked", True, "none"),
    (r"\b(dry\s+)?pasta\b|spaghetti|macaroni|penne|fusilli", "pasta", "Pasta", "starch", "dry_grain", True, "needs_boiling"),
    (r"\bpotatoes?\b|russet\s+potatoes?|baby\s+potatoes?", "potato", "Potatoes", "starch", "raw", True, "needs_cooking"),
    (r"\b(rolled\s+)?oats?\b|oatmeal", "oats", "Oats", "starch", "dry_grain", True, "needs_liquid"),

    # Proteins & Dairy
    (r"\beggs?\b", "eggs", "Eggs", "protein", "raw", True, "needs_cooking"),
    (r"\b(cheddar|mozzarella|parmesan|monterey\s+jack|swiss|jack|feta|gouda)?\s*cheese\b", "cheese", "Cheese", "dairy", "fresh", True, "none"),
    (r"\bpeanut\s+butter\b|skippy|jif", "peanut_butter", "Peanut butter", "protein", "canned", True, "none"),
    (r"\bcanned\s+tuna\b|tuna(\s+fish)?", "canned_tuna", "Canned tuna", "protein", "canned", True, "none"),
    (r"\b(firm\s+|silken\s+|extra\s+firm\s+)?tofu\b", "tofu", "Tofu", "protein", "fresh", True, "none"),
    (r"\bbacon(\s+strips?)?\b", "bacon", "Bacon", "protein", "cured", True, "needs_cooking"),
    (r"\b(raw\s+)?chicken(\s+breast|\s+thigh)?\b", "raw_chicken", "Raw chicken", "protein", "raw", True, "needs_safe_cooking"),
    (r"\b(ground\s+)?beef\b", "ground_beef", "Ground beef", "protein", "raw", True, "needs_safe_cooking"),

    # Legumes
    (r"\b(dry|uncooked)\s+(black|pinto|kidney)?\s*beans?\b", "dry_beans", "Dry beans", "legumes", "dry_grain", True, "long_boil_required"),
    (r"\b(canned\s+)?(black|pinto|kidney|cannellini|white)?\s*beans?\b", "canned_beans", "Canned beans", "legumes", "canned", True, "none"),
    (r"\b(dry|uncooked)\s+chickpeas?\b", "dry_chickpeas", "Dry chickpeas", "legumes", "dry_grain", True, "long_boil_required"),
    (r"\b(canned\s+)?chickpeas?\b|garbanzo\s+beans?", "canned_chickpeas", "Canned chickpeas", "legumes", "canned", True, "none"),

    # Liquids & Dairy (Crucial distinction: coconut milk vs dairy milk)
    (r"\bcoconut\s+milk\b|coconut\s+cream", "coconut_milk", "Coconut milk", "liquid", "canned", True, "none"),
    (r"\b(whole\s+|dairy\s+|cow\'?s?\s+|2%\s+|skim\s+)?milk\b", "dairy_milk", "Milk", "dairy", "fresh", True, "none"),
    (r"\bwater\b|tap\s+water", "water", "Water", "liquid", "fresh", False, "none"),
    (r"\b(chicken|vegetable|beef)\s+broth\b|stock", "broth", "Broth", "liquid", "canned", False, "none"),

    # Fats & Oils
    (r"\bbutter\b|ghee", "butter", "Butter", "fat", "fresh", True, "none"),
    (r"\b(olive|vegetable|canola|sesame|sunflower)\s+oil\b|cooking\s+oil", "cooking_oil", "Cooking oil", "fat", "fresh", False, "none"),
    (r"\bmayo(nnaise)?\b", "mayonnaise", "Mayonnaise", "fat", "condiment", False, "none"),

    # Sauces & Condiments
    (r"\bsoy\s+sauce\b|tamari|shoyu", "soy_sauce", "Soy sauce", "condiments", "condiment", False, "none"),
    (r"\bsriracha\b|hot\s+sauce|sambal|chili\s+crisp", "sriracha", "Sriracha", "condiments", "condiment", False, "none"),
    (r"\b(jarred\s+)?salsa\b|pico\s+de\s+gallo", "salsa", "Salsa", "condiments", "canned", True, "none"),
    (r"\bcurry\s+powder\b|curry\s+paste|garam\s+masala", "curry_powder", "Curry powder", "seasoning", "dry_grain", False, "none"),
    (r"\btomato\s+sauce\b|marinara|crushed\s+tomatoes|tomato\s+paste", "tomato_sauce", "Tomato sauce", "condiments", "canned", True, "none"),
    (r"\bmustard\b|dijon", "mustard", "Mustard", "condiments", "condiment", False, "none"),
    (r"\bketchup\b", "ketchup", "Ketchup", "condiments", "condiment", False, "none"),
    (r"\bhoney\b|maple\s+syrup", "sweetener", "Sweetener", "condiments", "condiment", False, "none"),
    (r"\bsalt\b|black\s+pepper|pepper", "seasoning", "Seasoning", "seasoning", "dry_grain", False, "none"),

    # Vegetables & Aromatics
    (r"\bgarlic(\s+cloves?)?\b", "garlic", "Garlic", "vegetable", "fresh", False, "none"),
    (r"\bonions?\b|shallots?", "onion", "Onion", "vegetable", "fresh", True, "none"),
    (r"\b(frozen\s+|green\s+)?peas?\b", "peas", "Frozen peas", "vegetable", "frozen", True, "none"),
    (r"\bkimchi\b", "kimchi", "Kimchi", "vegetable", "cured", True, "none"),
    (r"\bspinach\b|kale", "greens", "Spinach", "vegetable", "fresh", True, "none"),
    (r"\btomatoes?\b", "tomato", "Tomato", "vegetable", "fresh", True, "none"),
    (r"\bmushrooms?\b", "mushrooms", "Mushrooms", "vegetable", "fresh", True, "none"),
    (r"\bscallions?\b|green\s+onions?", "scallions", "Scallions", "vegetable", "fresh", False, "none"),
    (r"\bcorn\b", "corn", "Corn", "vegetable", "canned", True, "none"),
]

class IngredientNormalizer:
    """
    Standardizes user-entered raw strings into canonical ingredient entities,
    tracking preparation states, food-safety rules, and culinary roles.
    """

    @staticmethod
    def normalize(raw_name: str) -> NormalizedIngredient:
        cleaned = raw_name.strip()
        lower = cleaned.lower()

        # Check regex rules
        for pattern, canon_id, canon_name, cat, state, is_sub, prep in CANONICAL_RULES:
            if re.search(pattern, lower):
                return NormalizedIngredient(
                    original_name=cleaned,
                    canonical_id=canon_id,
                    canonical_name=canon_name,
                    category=cat,
                    state=state,
                    is_substantial=is_sub,
                    prep_requirement=prep
                )

        # Fallback for unknown ingredients
        # If ends in 's', guess base singular
        base_name = cleaned.title()
        canon_id = re.sub(r"[^a-z0-9]+", "_", lower).strip("_")
        
        return NormalizedIngredient(
            original_name=cleaned,
            canonical_id=canon_id or "unknown",
            canonical_name=base_name,
            category="vegetable" if any(w in lower for w in ["herb", "leaf", "pepper", "root"]) else "protein",
            state="fresh",
            is_substantial=True,
            prep_requirement="none"
        )

    @classmethod
    def normalize_list(cls, ingredients: List[str]) -> List[NormalizedIngredient]:
        seen_ids = set()
        normalized = []
        for ing in ingredients:
            item = cls.normalize(ing)
            # Avoid duplicate canonical entries (e.g. user entered 'garlic' and 'garlic cloves')
            if item.canonical_id not in seen_ids:
                seen_ids.add(item.canonical_id)
                normalized.append(item)
        return normalized

ingredient_normalizer = IngredientNormalizer()

def normalize_ingredient(raw_name: str) -> NormalizedIngredient:
    return IngredientNormalizer.normalize(raw_name)

def normalize_pantry(ingredients: List[str]) -> List[NormalizedIngredient]:
    return IngredientNormalizer.normalize_list(ingredients)
