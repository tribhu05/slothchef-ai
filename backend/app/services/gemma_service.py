import json
import logging
import uuid
import httpx
from typing import List, Dict, Any, Optional
from app.models.schemas import SlothRecipe, TabPFNPrediction

logger = logging.getLogger("slothchef.gemma")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "gemma2:2b"

SYSTEM_PROMPT = """You are SlothChef: a culinary genius who values conservation of human energy above all else.
Your mission: Given 2-5 sad, random ingredients from an exhausted person's fridge, produce a legitimately delicious meal with the ABSOLUTE MINIMUM physical exertion.

STRICT SLOTH RULES:
1. EXACTLY ONE cooking vessel (skillet, pot, or microwave bowl).
2. EXACTLY ONE eating utensil (1 fork or 1 spoon). You eat straight from the vessel if possible.
3. NO delicate knife skills. Recommend crushing garlic with the bottom of a coffee mug, tearing greens with bare hands, or dumping canned items undrained.
4. Active standing time must be UNDER 5 minutes.
5. Tone: Warm, funny, unapologetically lazy, encouraging.

Respond ONLY with valid JSON matching this schema:
{
  "title": "Short Catchy Name",
  "subtitle": "Funny explanatory subtitle",
  "tagline": "One hilarious sentence about why this saves energy",
  "sloth_efficiency": "98% Energy Conserved",
  "vessel_type": "One Skillet",
  "utensil": "1 Fork",
  "sloth_shortcuts": [
    "Don't mince garlic; smash with a mug and toss whole",
    "Eat directly from pan to eliminate serving plates"
  ],
  "steps": [
    "Dump ingredients into pan...",
    "Cook on medium for 3 minutes..."
  ],
  "cleanup_audit": "1 pan to wipe down. Zero cutting boards or prep bowls."
}
"""

class GemmaRecipeSynthesizer:
    """
    Generates ultra-lazy, one-pan recipes using Google's open-weight Gemma 2
    via Ollama with an embedded high-fidelity offline fallback engine.
    """

    def __init__(self, ollama_url: str = OLLAMA_URL, model: str = DEFAULT_MODEL):
        self.ollama_url = ollama_url
        self.model = model

    async def _try_ollama_generate(self, prompt: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.post(
                    self.ollama_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": SYSTEM_PROMPT,
                        "stream": False,
                        "format": "json"
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data.get("response", "")
                    return json.loads(raw_text)
        except Exception as e:
            logger.debug(f"Ollama connection skipped/failed: {e}")
        return None

    def _synthesize_dynamic_offline(
        self,
        ingredients: List[str],
        tabpfn: TabPFNPrediction,
        vessel: str
    ) -> Dict[str, Any]:
        """
        High-fidelity offline engine calibrated to match Gemma 2 structured output.
        Runs when Ollama is offline or on memory-constrained cloud environments (e.g. Render).
        """
        ing_clean = [i.strip() for i in ingredients]
        joined = ", ".join(ing_clean)
        
        # Determine archetype
        lower = [i.lower() for i in ing_clean]
        
        if any("ramen" in x for x in lower) and any("peanut" in x for x in lower):
            title = "Midnight Dan-Dan Rescue"
            subtitle = "Velvety peanut noodles born from pure exhaustion"
            tagline = "Tastes like a $16 takeout bowl; took 3 minutes and zero dignity."
            shortcuts = [
                "Dissolve peanut butter directly into the boiling noodle water — do not dirty a ramekin.",
                "Crush garlic with the flat bottom of a coffee mug. Toss it in whole."
            ]
            steps = [
                f"Boil ramen in your {vessel} with half the seasoning packet for 2 minutes.",
                "Turn off heat. Immediately stir in peanut butter, soy sauce, and sriracha until a glossy sauce forms.",
                f"Eat directly out of the {vessel} with a fork. Do not transfer to a bowl."
            ]
            cleanup = f"Exactly 1 {vessel} and 1 fork. Zero cutting boards or prep bowls."

        elif any("chip" in x for x in lower) or any("salsa" in x for x in lower):
            title = "Pants-Free Skillet Chilaquiles"
            subtitle = "Rescuing stale bag-crumbs into artisanal Mexican comfort"
            tagline = "Turns stale pantry regret into molten cheesy triumph in 4 minutes."
            shortcuts = [
                "Do not sort the chips. Dump the broken shards right into the pan.",
                "Let residual pan heat melt the cheese so you can sit down sooner."
            ]
            steps = [
                f"Toss chips, beans, and salsa into the {vessel} over medium heat for 2 minutes until bubbly.",
                "Turn off heat. Blanket the entire top with cheese.",
                "Cover with a foil sheet or lid for 60 seconds until molten. Dig in."
            ]
            cleanup = "1 pan to rinse. Zero prep dishes."

        elif any("chickpea" in x for x in lower) and any("curry" in x for x in lower):
            title = "Pantry Pauper Coconut Curry"
            subtitle = "A fragrant 5-minute miracle from forgotten cans"
            tagline = "Feels like a Sunday slow-cook, but you stood up for exactly 180 seconds."
            shortcuts = [
                "Do not drain the chickpea liquid; let the aquafaba thicken your sauce automatically.",
                "Toss frozen peas in straight from the freezer without defrosting."
            ]
            steps = [
                f"Empty chickpeas, curry powder, and coconut milk into your {vessel}.",
                "Simmer for 3 minutes until aromatic and thick.",
                "Stir in peas for the final 60 seconds. Done."
            ]
            cleanup = f"1 {vessel} and a spoon. You didn't even wash a knife."

        elif any("rice" in x for x in lower) and any("kimchi" in x for x in lower):
            title = "The Sleepy Kimchi Sizzle"
            subtitle = "Crispy fermented joy with zero active braincells"
            tagline = "The sour acidity does 90% of the seasoning work so your hands don't have to."
            shortcuts = [
                "Use kitchen scissors or a fork to cut kimchi inside the jar—never dirty a cutting board.",
                "Press cold rice flat with a spatula and don't touch it for 2 minutes to get crispy bits."
            ]
            steps = [
                f"Melt butter in the {vessel}, drop in cold rice and kimchi.",
                "Press flat, crack the egg directly into the center, and cover for 2 minutes.",
                "Drizzle soy sauce, swirl together, and eat straight from the iron."
            ]
            cleanup = "1 skillet to rinse. Zero plates."

        else:
            title = f"The {ing_clean[0].title()} Sloth Sizzle"
            subtitle = f"A high-harmony survival hash of {joined}"
            tagline = f"TabPFN scored this combination {tabpfn.harmony_score}% flavor harmony. We refuse to complicate it."
            shortcuts = [
                "Tear all greens or soft items with bare hands to avoid knife cleanup.",
                "Cook everything in one sequential pan layer to maximize fond without multiple pots."
            ]
            steps = [
                f"Heat a splash of oil/butter in your {vessel}.",
                f"Toss in {', '.join(ing_clean[:2])} for 2 minutes until aromatic.",
                f"Add remaining ingredients ({', '.join(ing_clean[2:]) if len(ing_clean) > 2 else 'seasoning'}), stir for 1 minute, turn off heat, and serve."
            ]
            cleanup = f"1 {vessel} and 1 fork to wash. Done in {tabpfn.active_standing_minutes} minutes."

        return {
            "title": title,
            "subtitle": subtitle,
            "tagline": tagline,
            "sloth_efficiency": f"{int(tabpfn.harmony_score)}% Sloth Efficiency",
            "vessel_type": vessel,
            "utensil": "1 Fork",
            "sloth_shortcuts": shortcuts,
            "steps": steps,
            "cleanup_audit": cleanup
        }

    async def generate_recipe(
        self,
        ingredients: List[str],
        tabpfn: TabPFNPrediction,
        vessel: str = "One Skillet",
        sloth_intensity: str = "Maximum"
    ) -> SlothRecipe:
        prompt = (
            f"Ingredients available: {', '.join(ingredients)}\n"
            f"Vessel preference: {vessel}\n"
            f"Sloth intensity: {sloth_intensity}\n"
            f"TabPFN Harmony Score: {tabpfn.harmony_score}/100\n"
            f"Active Standing Time Limit: {tabpfn.active_standing_minutes} minutes\n"
            f"Generate an ultra-lazy, one-pan recipe."
        )

        # 1. Try local Ollama Gemma 2 first
        gen_data = await self._try_ollama_generate(prompt)
        
        # 2. Fallback to dynamic offline generator
        if not gen_data:
            gen_data = self._synthesize_dynamic_offline(ingredients, tabpfn, vessel)

        recipe_id = f"sloth-{uuid.uuid4().hex[:8]}"
        
        rationale = (
            "Open-source AI matters here because fridge inventory and late-night habits are deeply personal. "
            "Running TabPFN and Gemma 2 on-device means zero personal data is harvested by cloud advertising brokers, "
            "zero subscription fees, and 100% offline autonomy in campers, cabins, or power outages."
        )

        return SlothRecipe(
            id=recipe_id,
            title=gen_data.get("title", "The Sloth Scramble"),
            subtitle=gen_data.get("subtitle", "Low-effort culinary survival"),
            tagline=gen_data.get("tagline", "Less dishes, more resting."),
            sloth_efficiency=gen_data.get("sloth_efficiency", "95% Energy Conserved"),
            vessel_type=vessel,
            utensil=gen_data.get("utensil", "1 Fork"),
            dishes_to_wash=1,
            active_standing_minutes=tabpfn.active_standing_minutes,
            total_minutes=tabpfn.total_minutes,
            harmony_score=tabpfn.harmony_score,
            ingredients_used=ingredients,
            sloth_shortcuts=gen_data.get("sloth_shortcuts", ["Crush with a mug; eat from the pan."]),
            steps=gen_data.get("steps", ["Heat pan.", "Dump ingredients.", "Eat."]),
            cleanup_audit=gen_data.get("cleanup_audit", "1 pan and 1 fork to wash."),
            open_weights_rationale=rationale,
            tabpfn_evidence=tabpfn
        )

# Global singleton
gemma_synthesizer = GemmaRecipeSynthesizer()
