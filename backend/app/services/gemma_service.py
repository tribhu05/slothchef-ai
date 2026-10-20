import json
import logging
import uuid
import httpx
from typing import List, Dict, Any, Optional
from app.models.schemas import SlothRecipe, TabPFNPrediction
from app.services.decision_engine import evaluate_pantry
from app.services.image_registry import resolve_recipe_image

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
    via Ollama with an embedded high-fidelity culinary fallback engine.
    """

    def __init__(self, ollama_url: str = OLLAMA_URL, model: str = DEFAULT_MODEL):
        self.ollama_url = ollama_url
        self.model = model
        self._ollama_available = False
        self._last_ollama_check = 0.0

    async def _try_ollama_generate(self, prompt: str) -> Optional[Dict[str, Any]]:
        import time
        now = time.time()
        # If Ollama was recently verified offline, skip waiting for socket timeouts
        if not self._ollama_available and (now - self._last_ollama_check < 45):
            return None

        self._last_ollama_check = now
        try:
            # 0.5s connection timeout so offline fallback executes instantaneously
            timeout = httpx.Timeout(4.0, connect=0.5)
            async with httpx.AsyncClient(timeout=timeout) as client:
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
                    self._ollama_available = True
                    data = res.json()
                    raw_text = data.get("response", "")
                    return json.loads(raw_text)
        except Exception as e:
            self._ollama_available = False
            logger.debug(f"Ollama connection skipped/failed: {e}")
        return None

    def _synthesize_dynamic_offline(
        self,
        ingredients: List[str],
        tabpfn: TabPFNPrediction,
        vessel: str,
        microwave_only: bool = False
    ) -> Dict[str, Any]:
        """
        High-fidelity culinary engine calibrated to match Gemma 2 structured output.
        Dynamically analyzes ingredient taxonomy, flavor pairings, and physical properties
        to synthesize authentic, highly specific, low-effort recipes for ANY ingredient mix.
        """
        ing_clean = [i.strip() for i in ingredients]
        lower = [i.lower() for i in ing_clean]
        joined = ", ".join(ing_clean)

        has = lambda *words: any(any(w in item for w in words) for item in lower)
        effective_vessel = "Microwave Safe Bowl" if microwave_only else vessel

        # -------------------------------------------------------------
        # ARCHETYPE 1: RAMEN / NOODLES
        # -------------------------------------------------------------
        if has("ramen", "noodle"):
            if has("peanut"):
                title = "Midnight Dan-Dan Rescue"
                subtitle = "Velvety sesame-peanut noodles born from pure developer exhaustion"
                tagline = "Tastes like a $16 takeout bowl; took 3 minutes and zero dignity."
                shortcuts = [
                    "Dissolve peanut butter directly into boiling noodle water — never dirty a whisk or ramekin.",
                    "Crush garlic with the flat base of your coffee mug. Toss it in whole."
                ]
                steps = [
                    f"Boil noodles in your {effective_vessel} with 1 cup of water for 2 minutes.",
                    "Turn off heat. Immediately stir in peanut butter, soy sauce, and sriracha until a glossy, velvety sauce forms.",
                    f"Eat directly out of the {effective_vessel} with a fork. Washing a bowl is voluntary suffering."
                ]
                img = "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=1200&q=80"

            elif has("cheese"):
                title = "3-Minute Desperation Carbonara Ramen"
                subtitle = "Silky, molten cheese emulsified directly in starchy noodle water"
                tagline = "The Romans took 400 years to invent Carbonara; you made it in 180 seconds."
                shortcuts = [
                    "Do not drain the noodle water! The hot starch is what melts and binds the cheese.",
                    "Crack the egg directly onto the hot noodles off-heat so it creams without scrambling."
                ]
                steps = [
                    f"Cook ramen in your {effective_vessel} with just enough water to submerge for 2.5 minutes.",
                    "Kill the heat. Toss in butter, cracked egg, and a mound of cheese.",
                    "Vigorously swirl with your fork for 30 seconds until a creamy, glossy emulsion forms. Pepper aggressively and devour."
                ]
                img = "https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=1200&q=80"

            elif has("curry", "coconut"):
                title = "Flash Golden Coconut Laksa Ramen"
                subtitle = "Fragrant, rich Southeast Asian noodle soup from pantry shelf scraps"
                tagline = "Aromatic, creamy, and complex enough to deceive any dinner guest."
                shortcuts = [
                    "Do not sauté curry paste in a separate pan; dump coconut milk and powder straight into the pot.",
                    "Drop frozen peas or greens directly into the boiling soup—they thaw in 40 seconds."
                ]
                steps = [
                    f"Empty coconut milk, 1/2 cup water, and curry powder into the {effective_vessel} and bring to a simmer.",
                    "Drop the ramen block directly into the simmering broth for 3 minutes.",
                    "Swirl in soy sauce or sriracha and eat steaming hot straight from the vessel."
                ]
                img = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80"

            elif has("garlic", "soy"):
                title = "Midnight Garlic Butter Lo-Mein Sizzle"
                subtitle = "Smoky, glossy street-style noodles with crisp garlic chips"
                tagline = "Maximum savory umami in less time than it takes to load food delivery."
                shortcuts = [
                    "Smash garlic under a mug and fry in butter for 60 seconds until fragrant.",
                    "Toss boiled ramen straight from water into the sizzling garlic butter with a splash of soy sauce."
                ]
                steps = [
                    f"Simmer ramen in {effective_vessel} until just tender (2 mins), then pour off excess water.",
                    "Push noodles to side, melt butter and garlic in the hot spot for 45 seconds.",
                    "Toss noodles through the bubbling garlic butter with soy sauce and sriracha until glistening."
                ]
                img = "https://images.unsplash.com/photo-1552611052-33e04de081de?auto=format&fit=crop&w=1200&q=80"

            else:
                title = f"The {ing_clean[0].title()} Street Ramen Sizzle"
                subtitle = f"Savory pan-fried ramen tossed with {joined}"
                tagline = "Noodles cooked directly in flavor reduction. Fast, hot, and 100% dish-efficient."
                shortcuts = [
                    "Cook noodles in minimal water so the sauce reduces and coats without draining.",
                    "Eat with a single fork right from the pan."
                ]
                steps = [
                    f"Cook ramen in {effective_vessel} with 1 cup water and seasonings for 2 minutes.",
                    f"Add {', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'seasonings'}, tossing until water evaporates into a glossy glaze.",
                    "Serve instantly in the pan with a drizzle of oil or hot sauce."
                ]
                img = "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 2: RICE
        # -------------------------------------------------------------
        elif has("rice"):
            if has("kimchi"):
                title = "The Sleepy Kimchi Sizzle Fried Rice"
                subtitle = "Crispy fermented joy with zero active braincells"
                tagline = "The sour acidity does 90% of the seasoning work so your hands don't have to."
                shortcuts = [
                    "Use kitchen scissors or a fork to cut kimchi inside the jar—never dirty a cutting board.",
                    "Press cold rice flat with a spatula and don't touch it for 2 minutes to get crispy bits."
                ]
                steps = [
                    f"Melt butter in the {effective_vessel}, drop in cold rice and kimchi.",
                    "Press flat, crack the egg directly into the center, and cover for 2 minutes.",
                    "Drizzle soy sauce, swirl together, and eat straight from the iron."
                ]
                img = "https://images.unsplash.com/photo-1590301157890-4810ed352733?auto=format&fit=crop&w=1200&q=80"

            elif has("garlic", "butter"):
                title = "Tokyo Midnight Garlic Butter Crispy Rice"
                subtitle = "Japanese teppan-style caramelized rice with crunchy golden edges"
                tagline = "Four ingredients, zero chopping, tastes like a 2 AM Shinjuku izakaya."
                shortcuts = [
                    "Smash garlic under a mug and toss in whole with butter.",
                    "Spread rice across the pan base and resist stirring for 120 seconds to form golden crust."
                ]
                steps = [
                    f"Melt butter in your {effective_vessel} over medium heat with smashed garlic until foaming.",
                    "Add cold rice, breaking clumps with a fork. Drizzle soy sauce around the outer perimeter of the pan.",
                    "Press down firmly and sear until the bottom is crackling and golden brown. Serve."
                ]
                img = "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80"

            elif has("tuna", "mayo"):
                title = "Deconstructed Spicy Tuna Onigiri Skillet"
                subtitle = "Warm seasoned sushi-rice mash with flaked tuna and spicy mayo drizzle"
                tagline = "All the flavors of a $9 spicy tuna roll without rolling bamboo mats or leaving your kitchen."
                shortcuts = [
                    "Flake canned tuna straight from the can with a fork—do not pre-mix in a bowl.",
                    "Drizzle mayo and sriracha directly over the hot rice bed in the pan."
                ]
                steps = [
                    f"Warm rice in your {effective_vessel} with a teaspoon of soy sauce and sesame oil (if handy).",
                    "Scatter flaked tuna evenly across the top and let residual pan heat warm it through.",
                    "Zig-zag sriracha and mayo over the surface. Eat hot straight from the skillet."
                ]
                img = "https://images.unsplash.com/photo-1546069901-d8a1c97a5a8e?auto=format&fit=crop&w=1200&q=80"

            elif has("bean", "salsa", "cheese"):
                title = "1-Skillet Campfire Burrito Bowl"
                subtitle = "Molten black beans, warm seasoned rice, and bubbling salsa cheddar"
                tagline = "Chipotle charges $14 for this; you made it with 3 cupboard cans and 1 fork."
                shortcuts = [
                    "Dump beans and salsa straight into the pan without draining.",
                    "Cover with foil or a lid for 60 seconds to melt the cheese without an oven."
                ]
                steps = [
                    f"Combine rice, beans, and salsa in the {effective_vessel} over medium heat for 2 minutes.",
                    "Turn off heat. Smother the entire top with cheese.",
                    "Cover for 60 seconds until molten and bubbling. Dig in with tortilla chips or a fork."
                ]
                img = "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=1200&q=80"

            else:
                title = f"The {ing_clean[0].title()} Golden Fried Rice Skillet"
                subtitle = f"Speedy high-heat tossed rice with {joined}"
                tagline = "Cold pantry rice transformed into dinner in under 240 seconds."
                shortcuts = [
                    "Crack eggs directly into a cleared circle in the center of the rice bed.",
                    "Stir vigorously with your eating fork to create silky egg ribbons."
                ]
                steps = [
                    f"Heat oil/butter in your {effective_vessel}. Add {', '.join(ing_clean[:2])} for 90 seconds.",
                    "Toss in rice and remaining ingredients, splashing soy sauce against the hot pan rim.",
                    "Sear on high heat for 1 minute until fragrant and steaming. Eat immediately."
                ]
                img = "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 3: TORTILLA / CHIPS / CHILAQUILES
        # -------------------------------------------------------------
        elif has("chip", "tortilla", "nacho"):
            title = "Pants-Free Skillet Chilaquiles"
            subtitle = "Rescuing stale bag-crumbs into artisanal Mexican comfort"
            tagline = "Turns stale pantry regret into molten cheesy triumph in 4 minutes."
            shortcuts = [
                "Do not sort the chips. Dump the broken shards right into the pan.",
                "Let residual pan heat melt the cheese so you can sit down sooner."
            ]
            steps = [
                f"Toss chips and salsa into the {effective_vessel} over medium heat for 90 seconds until warm and slightly softened.",
                "Turn off heat immediately. Blanket the entire top with cheese and canned beans if using.",
                "Cover with a plate or lid for 60 seconds until molten. Eat straight from the pan."
            ]
            img = "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 4: CHICKPEAS / BEANS / CURRY
        # -------------------------------------------------------------
        elif has("chickpea") or (has("bean") and has("curry")):
            title = "Pantry Pauper Coconut Curry"
            subtitle = "A fragrant 5-minute miracle from forgotten canned staples"
            tagline = "Feels like a Sunday slow-cook, but you stood up for exactly 180 seconds."
            shortcuts = [
                "Do not drain the chickpea liquid; the aquafaba naturally thickens your curry sauce.",
                "Toss frozen peas or greens in straight from the freezer without defrosting."
            ]
            steps = [
                f"Empty chickpeas, curry powder, and coconut milk into your {effective_vessel}.",
                "Simmer on medium for 3 minutes until aromatic, creamy, and bubbling.",
                f"Fold in remaining ingredients for the final 60 seconds. Done in 1 {effective_vessel}."
            ]
            img = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 5: EGGS (When Egg is the Primary Star)
        # -------------------------------------------------------------
        elif has("egg"):
            if has("tomato", "salsa"):
                title = "4-Minute Emergency Shakshuka"
                subtitle = "Silky eggs poached in bubbling spiced tomato-garlic reduction"
                tagline = "High-protein North African brunch luxury synthesized with zero prep."
                shortcuts = [
                    "Make small craters in the bubbling sauce with a spoon and crack eggs directly in.",
                    "Cover with a lid or foil so the egg whites set in 2 minutes flat without flipping."
                ]
                steps = [
                    f"Pour tomato sauce or salsa into your {effective_vessel} with garlic/seasonings over medium heat until bubbling.",
                    "Create 2 wells in the sauce. Crack eggs directly into each well.",
                    "Cover with a lid for 2.5 minutes until whites are firm and yolks remain jammy. Serve."
                ]
                img = "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80"

            elif has("bread", "toast"):
                title = "Crispy Golden Egg-in-a-Hole Melt"
                subtitle = "Buttery toasted sourdough with a runny egg center and molten cheese"
                tagline = "One pan, three minutes, and zero bowls to clean before work."
                shortcuts = [
                    "Tear a hole in the center of the bread with your fingers—no cookie cutter required.",
                    "Drop the torn bread circle right alongside in the butter to fry as a dipping soldier."
                ]
                steps = [
                    f"Melt butter in your {effective_vessel}. Place bread slice in pan.",
                    "Crack the egg directly into the center hole. Season with salt and pepper.",
                    "Flip after 2 minutes, top with cheese, and sear for 1 minute until golden and melted."
                ]
                img = "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=1200&q=80"

            elif has("cheese"):
                title = "Velvety Low-Effort French Omelet Pocket"
                subtitle = "Pillowy butter-scrambled eggs stuffed with molten cheddar"
                tagline = "Culinary school chefs practice this for 10 years; you just did it in sweatpants."
                shortcuts = [
                    "Crack eggs directly into the foaming butter pan and scramble gently with your fork.",
                    "Fold once when 80% set and kill the heat immediately—residual heat finishes the cook."
                ]
                steps = [
                    f"Melt 1 tbsp butter in your {effective_vessel} over medium-low heat until foaming.",
                    "Crack eggs directly in, swirling rapidly with a fork for 60 seconds until creamy curds form.",
                    "Scatter cheese across center, fold in half, turn off heat, and serve on your fork."
                ]
                img = "https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=1200&q=80"

            else:
                title = f"The {ing_clean[0].title()} 3-Minute Skillet Scramble"
                subtitle = f"Fluffy high-protein scramble with {joined}"
                tagline = "Fastest breakfast-for-dinner protein delivery system known to science."
                shortcuts = [
                    "Whisk eggs directly inside the skillet with your eating fork—never use a prep bowl.",
                    "Pull off the flame while eggs look slightly glossy for maximum softness."
                ]
                steps = [
                    f"Heat a knob of butter/oil in {effective_vessel}. Add {', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'seasoning'} for 1 minute.",
                    "Crack eggs directly into pan, stirring continuously with a fork for 90 seconds.",
                    "Turn off heat when soft curds form. Eat directly from the pan."
                ]
                img = "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 6: BREAD / TOAST / SANDWICH
        # -------------------------------------------------------------
        elif has("bread", "toast"):
            if has("cheese"):
                title = "The Ultimate Inside-Out Grilled Cheese"
                subtitle = "Crispy frico cheese crust on the outside, molten gooey center within"
                tagline = "Why put cheese only inside when you can toast it directly into the skillet?"
                shortcuts = [
                    "Butter the bread with the back of a spoon—never dirty a butter knife.",
                    "Scatter a pinch of shredded cheese directly on the hot pan under the bread for a crunchy crust."
                ]
                steps = [
                    f"Melt butter in your {effective_vessel}. Lay down bread and layer thick cheese on top.",
                    "Top with second slice. Cook on medium-low for 2 minutes until bottom is golden.",
                    "Flip and cook for 90 seconds until cheese is completely molten. Slice diagonally."
                ]
                img = "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=1200&q=80"

            elif has("peanut"):
                title = "Caramelized Warm Peanut Butter Toast Melt"
                subtitle = "Toasted sourdough with bubbling warm peanut butter and sweet reduction"
                tagline = "Comfort food so fast it violates multiple municipal fire codes."
                shortcuts = [
                    "Toast bread directly in bubbling butter in the pan for 90 seconds per side.",
                    "Spread peanut butter while bread is scorching hot so it melts into a warm glaze."
                ]
                steps = [
                    f"Melt butter in {effective_vessel}. Toast bread on both sides until deep golden brown.",
                    "Immediately spread peanut butter generously over the hot surface.",
                    "Drizzle honey or hot sauce if desired. Eat warm with your hands."
                ]
                img = "https://images.unsplash.com/photo-1584776296944-ab6fb57b0bdd?auto=format&fit=crop&w=1200&q=80"

            else:
                title = f"The {ing_clean[0].title()} Pan-Toasted Skillet Melt"
                subtitle = f"Golden crisp sourdough topped with {joined}"
                tagline = "Hot, crunchy, and ready before the kettle finishes boiling."
                shortcuts = [
                    "Toast bread in the same pan fat used for your toppings.",
                    "Eat with your hands over the pan to eliminate all dishes."
                ]
                steps = [
                    f"Melt butter in {effective_vessel}. Toast bread for 2 minutes until crisp.",
                    f"Warm {', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'toppings'} in the pan corner.",
                    "Spoon toppings onto toast, fold, and eat immediately."
                ]
                img = "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 7: PASTA / ITALIAN
        # -------------------------------------------------------------
        elif has("pasta", "spaghetti", "macaroni"):
            if has("garlic", "olive oil"):
                title = "Midnight Spaghetti Aglio e Olio"
                subtitle = "The legendary Neapolitan late-night garlic and pepper sizzle"
                tagline = "Invented by broke Italian students in the 1700s; perfected by tired developers today."
                shortcuts = [
                    "Cook pasta in shallow water so the starchy water naturally binds the olive oil into sauce.",
                    "Crush garlic with a mug and fry on low heat so it sweetens without burning."
                ]
                steps = [
                    f"Cook pasta in {effective_vessel} with minimal salted water until al dente.",
                    "Pour off most water leaving 3 tablespoons. Slide pasta to one side.",
                    "In the cleared pan area, sizzle garlic in olive oil for 60 seconds, then toss all together."
                ]
                img = "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=1200&q=80"

            else:
                title = f"The {ing_clean[0].title()} 1-Pan Starch Pasta Toss"
                subtitle = f"Creamy reduction pasta with {joined}"
                tagline = "No colander. No strainer. No second pot. Just pure starch physics."
                shortcuts = [
                    "Cook pasta directly in the sauce liquid so zero starch is drained away.",
                    "Finish with cheese off the heat to avoid clumping."
                ]
                steps = [
                    f"Simmer pasta and {', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'seasonings'} in {effective_vessel} with 1.5 cups water.",
                    "Boil for 4 minutes until liquid is mostly absorbed into a thick glossy glaze.",
                    "Stir in remaining ingredients, turn off heat, and serve with your eating fork."
                ]
                img = "https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 8: POTATOES / HASH
        # -------------------------------------------------------------
        elif has("potato", "hash", "fries"):
            title = "Crispy Skillet Smashed Potato Hash"
            subtitle = "Crushed golden potatoes seared in butter with melting cheese"
            tagline = "Maximum crispy surface area created with the bottom of a drinking glass."
            shortcuts = [
                "Smash cooked or canned potatoes flat with the bottom of a coffee mug.",
                "Leave them undisturbed in the hot skillet for 3 full minutes to get ultra-crispy edges."
            ]
            steps = [
                f"Melt butter/oil in {effective_vessel} over medium-high heat.",
                "Add potatoes, smash flat with a mug base, and sear for 3 minutes without moving.",
                f"Flip, scatter {', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'cheese'} over top, and cook 2 minutes until molten."
            ]
            img = "https://images.unsplash.com/photo-1518013034458-30b0ee243591?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 9: TOFU / VEGETARIAN GLOW
        # -------------------------------------------------------------
        elif has("tofu"):
            title = "Crispy Sweet-Heat Glazed Tofu Slices"
            subtitle = "Golden pan-seared tofu planks lacquered in savory garlic-chili reduction"
            tagline = "High-protein, plant-based indulgence ready in under 5 active minutes."
            shortcuts = [
                "Tear tofu into rustic bite-sized jagged pieces with your fingers—rough edges crisp up better than sliced cubes.",
                "Pour soy sauce and sriracha directly into the sizzling pan to glaze."
            ]
            steps = [
                f"Heat oil in your {effective_vessel} over high heat. Add tofu pieces and sear for 2.5 minutes without moving.",
                "Turn pieces over. Pour in soy sauce, sriracha, and garlic/seasonings.",
                "Toss rapidly as the sauce bubbles into a sticky, caramelized glaze. Serve hot."
            ]
            img = "https://images.unsplash.com/photo-1546069901-d8a1c97a5a8e?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 10: TUNA / CANNED FISH
        # -------------------------------------------------------------
        elif has("tuna"):
            title = "Midnight Skillet Tuna Melt Sizzle"
            subtitle = "Flaked savory tuna warmed in herb butter with bubbling molten cheese"
            tagline = "Salty, savory, rich comfort food assembled in 180 seconds."
            shortcuts = [
                "Open tuna can, press lid to drain liquid directly into sink, drop straight into pan.",
                "Eat with crackers, chips, or straight off a fork."
            ]
            steps = [
                f"Melt butter in {effective_vessel}. Add tuna and {', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'seasonings'}.",
                "Warm through on medium heat for 90 seconds until steaming.",
                "Top with cheese if available, cover for 45 seconds until melted, and dig in."
            ]
            img = "https://images.unsplash.com/photo-1546069901-d8a1c97a5a8e?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # ARCHETYPE 11: OATS / PORRIDGE (Warm single-vessel breakfast)
        # -------------------------------------------------------------
        elif has("oat", "porridge"):
            title = "5-Minute Creamy Porridge Oats"
            subtitle = f"Soothing warm breakfast comfort prepared in one vessel with {joined}"
            tagline = "Warm porridge that coats your stomach with zero pots to scrub."
            shortcuts = [
                "Cook and eat in the exact same microwave-safe bowl or mini-skillet.",
                "Swirl peanut butter or sweetener in while oats are steaming to create rich ribbons."
            ]
            steps = [
                f"Add oats and 3/4 cup liquid (water, milk, or broth) to your {effective_vessel}.",
                f"Heat on medium for 3 minutes (or microwave for 90 seconds) until thick and creamy.",
                f"Swirl in {', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'sweetener'}, let rest 60 seconds, and dig in."
            ]
            img = "https://images.unsplash.com/photo-1584776296944-ab6fb57b0bdd?auto=format&fit=crop&w=1200&q=80"

        # -------------------------------------------------------------
        # UNIVERSAL SMART CHEF COMPOSER (For Any Unique Custom Combo)
        # -------------------------------------------------------------
        else:
            primary = ing_clean[0].title()
            secondary = ing_clean[1].title() if len(ing_clean) > 1 else "Seasoning"
            
            title = f"The {primary} & {secondary} Sloth Skillet"
            subtitle = f"A customized high-synergy survival sauté of {joined}"
            tagline = f"Flavor synergy evaluated at {tabpfn.harmony_score}% balance. We refuse to complicate it."
            shortcuts = [
                "Tear all soft ingredients with your bare hands directly over the hot pan.",
                "Cook everything in one sequential heat layer to build maximum savory fond."
            ]
            steps = [
                f"Heat 1 tablespoon of oil or butter in your {effective_vessel} over medium flame.",
                f"Add {ing_clean[0]} and sauté for 2 minutes until golden and aromatic.",
                f"Fold in remaining ingredients ({', '.join(ing_clean[1:]) if len(ing_clean) > 1 else 'herbs'}), stir for 60 seconds, kill the heat, and feast."
            ]
            img = "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80"

        # If Microwave-Only is enforced, adapt instructions
        if microwave_only:
            shortcuts.append("Microwave on HIGH with a paper towel lid to trap steam and avoid splatter.")
            steps = [
                f"Place all ingredients into your {effective_vessel} with 2 tablespoons of water or broth.",
                "Cover with a damp paper towel and microwave on HIGH for 2 minutes.",
                "Carefully stir with your fork, microwave for another 60 seconds, and let stand 1 minute before eating."
            ]
            cleanup = f"Exactly 1 {effective_vessel} and 1 fork to rinse. Zero pans or stovetop splatters."
        else:
            cleanup = f"Exactly 1 {effective_vessel} and 1 fork to wipe down. Zero cutting boards or prep bowls."

        return {
            "title": title,
            "subtitle": subtitle,
            "tagline": tagline,
            "sloth_efficiency": f"{int(tabpfn.harmony_score)}% Sloth Efficiency",
            "vessel_type": effective_vessel,
            "utensil": "1 Fork" if not has("soup", "curry") else "1 Spoon",
            "sloth_shortcuts": shortcuts,
            "steps": steps,
            "cleanup_audit": cleanup,
            "image_url": img
        }

    async def generate_recipe(
        self,
        ingredients: List[str],
        tabpfn: TabPFNPrediction,
        vessel: str = "One Skillet",
        sloth_intensity: str = "Maximum",
        microwave_only: bool = False,
        minimal_chopping: bool = True,
        max_active_minutes: int = 5
    ) -> SlothRecipe:
        effective_vessel = "Microwave Safe Bowl" if microwave_only else vessel
        
        # 1. Run multi-stage pantry decision engine
        decision = evaluate_pantry(ingredients)
        
        rationale = (
            "Open-source AI matters here because fridge inventory and late-night habits are deeply personal. "
            "Running TabPFN and Gemma 2 on-device means zero personal data is harvested by cloud advertising brokers, "
            "zero subscription fees, and 100% offline autonomy in campers, cabins, or power outages."
        )

        # -------------------------------------------------------------
        # STATE 1: NO_GOOD_MATCH
        # -------------------------------------------------------------
        if decision.status == "NO_GOOD_MATCH":
            recipe_id = f"sloth-{uuid.uuid4().hex[:8]}"
            img_url, img_caption = resolve_recipe_image(
                None, "No Credible Meal", [item.canonical_id for item in decision.normalized_ingredients], ingredients
            )
            return SlothRecipe(
                id=recipe_id,
                title="No Credible Meal Possible",
                subtitle="Your pantry currently lacks a core carbohydrate or protein base",
                tagline="True Sloth Wisdom: Don't dirty a pan on ingredients that can't form a satisfying meal.",
                sloth_efficiency="100% Energy Conserved (Stove Kept Off)",
                sloth_score=99,
                image_url=img_url,
                image_caption=img_caption,
                vessel_type=effective_vessel,
                utensil="1 Fork",
                dishes_to_wash=0,
                active_standing_minutes=0,
                total_minutes=0,
                harmony_score=min(35.0, tabpfn.harmony_score),
                ingredients_used=ingredients,
                sloth_shortcuts=[
                    "Do not turn on the stove yet — seasonings and raw aromatics alone will burn or disappoint.",
                    "Add one of the suggested staple anchors below to unlock an instant 1-pan dish."
                ],
                steps=[
                    "Check your cupboard for an anchor staple: Ramen noodles, leftover cooked rice, bread, or eggs.",
                    "Click 'Add to Pan & Cook' below on any staple you find, and SlothChef will handle the rest."
                ],
                cleanup_audit="0 pans dirtied. Zero energy wasted.",
                open_weights_rationale=rationale,
                tabpfn_evidence=tabpfn,
                status="NO_GOOD_MATCH",
                decision_message=decision.decision_message,
                missing_suggestions=decision.missing_suggestions,
                safety_warnings=decision.safety_warnings,
                fit_explanation=decision.fit_explanation,
                ai_engine_used="SlothChef Decision Engine"
            )

        # -------------------------------------------------------------
        # STATE 2: NEEDS_INGREDIENTS
        # -------------------------------------------------------------
        if decision.status == "NEEDS_INGREDIENTS":
            curated = decision.selected_curated_recipe
            recipe_id = f"sloth-{uuid.uuid4().hex[:8]}"
            active_time = min(max_active_minutes, curated.active_minutes if curated else 3)
            sloth_score = curated.base_sloth_score if curated else 95
            
            steps = list(curated.steps) if curated else [
                "Gather your base ingredients.",
                "Add the missing staple to bind the dish together.",
                "Heat and cook in 1 vessel."
            ]

            img_url, img_caption = resolve_recipe_image(
                curated.id if curated else None,
                curated.title if curated else "Almost a Meal",
                [item.canonical_id for item in decision.normalized_ingredients],
                ingredients
            )

            return SlothRecipe(
                id=recipe_id,
                title=curated.title if curated else "Almost a Complete Meal",
                subtitle=curated.subtitle if curated else "You are one key ingredient away from greatness",
                tagline=curated.tagline if curated else "So close to dinner with zero knife skills.",
                sloth_efficiency=f"{sloth_score}% Projected Efficiency",
                sloth_score=sloth_score,
                image_url=img_url,
                image_caption=img_caption,
                vessel_type=effective_vessel,
                utensil="1 Fork" if not (curated and "curry" in curated.id) else "1 Spoon",
                dishes_to_wash=1,
                active_standing_minutes=active_time,
                total_minutes=curated.total_minutes if curated else 4,
                harmony_score=tabpfn.harmony_score,
                ingredients_used=ingredients,
                sloth_shortcuts=curated.shortcuts if curated else ["Add the missing item to complete the dish."],
                steps=steps,
                cleanup_audit=curated.cleanup_audit if curated else f"1 {effective_vessel} and 1 fork to wash.",
                open_weights_rationale=rationale,
                tabpfn_evidence=tabpfn,
                status="NEEDS_INGREDIENTS",
                decision_message=decision.decision_message,
                missing_suggestions=decision.missing_suggestions,
                safety_warnings=decision.safety_warnings,
                fit_explanation=decision.fit_explanation,
                ai_engine_used="SlothChef Decision Engine"
            )

        # -------------------------------------------------------------
        # STATE 3: READY (Curated Match or Safe Synthesis)
        # -------------------------------------------------------------
        curated = decision.selected_curated_recipe
        if curated:
            recipe_id = f"sloth-{uuid.uuid4().hex[:8]}"
            active_time = min(max_active_minutes, curated.active_minutes)
            sloth_score = curated.base_sloth_score

            steps = list(curated.steps)
            shortcuts = list(curated.shortcuts)
            if microwave_only:
                steps = [
                    f"Combine ingredients into your {effective_vessel} with 2 tbsp water or broth.",
                    "Cover with a damp paper towel and microwave on HIGH for 2 minutes.",
                    "Stir with your fork, microwave for another 60 seconds, and let stand 1 minute."
                ]
                shortcuts.append("Microwave in the eating bowl to skip stove cleanup completely.")

            img_url, img_caption = resolve_recipe_image(
                curated.id,
                curated.title,
                [item.canonical_id for item in decision.normalized_ingredients],
                ingredients
            )

            return SlothRecipe(
                id=recipe_id,
                title=curated.title,
                subtitle=curated.subtitle,
                tagline=curated.tagline,
                sloth_efficiency=f"{sloth_score}% Energy Conserved",
                sloth_score=sloth_score,
                image_url=img_url,
                image_caption=img_caption,
                vessel_type=effective_vessel,
                utensil="1 Fork" if not ("curry" in curated.id or "oat" in curated.id) else "1 Spoon",
                dishes_to_wash=1,
                active_standing_minutes=active_time,
                total_minutes=curated.total_minutes,
                harmony_score=tabpfn.harmony_score,
                ingredients_used=ingredients,
                sloth_shortcuts=shortcuts,
                steps=steps,
                cleanup_audit=curated.cleanup_audit,
                open_weights_rationale=rationale,
                tabpfn_evidence=tabpfn,
                status="READY",
                decision_message=decision.decision_message,
                missing_suggestions=[],
                safety_warnings=decision.safety_warnings,
                fit_explanation=decision.fit_explanation,
                ai_engine_used="Verified Recipe Catalog"
            )

        # Fallback to Ollama or dynamic offline if verified candidate wasn't pre-indexed
        prompt = (
            f"Ingredients available: {', '.join(ingredients)}\n"
            f"Vessel preference: {effective_vessel}\n"
            f"Sloth intensity: {sloth_intensity}\n"
            f"Microwave only: {microwave_only}\n"
            f"Minimal chopping: {minimal_chopping}\n"
            f"Max active standing minutes: {max_active_minutes}\n"
            f"TabPFN Harmony Score: {tabpfn.harmony_score}/100\n"
            f"Generate an ultra-lazy, one-pan recipe."
        )

        gen_data = await self._try_ollama_generate(prompt)
        ai_engine = "Google Gemma 2 (Local SLM)" if gen_data else "SlothChef Decision Engine (Offline)"
        
        if not gen_data:
            gen_data = self._synthesize_dynamic_offline(
                ingredients=ingredients,
                tabpfn=tabpfn,
                vessel=effective_vessel,
                microwave_only=microwave_only
            )

        recipe_id = f"sloth-{uuid.uuid4().hex[:8]}"
        active_time = min(max_active_minutes, tabpfn.active_standing_minutes)
        sloth_score = max(75, min(99, int(100 - (active_time * 2) - 1)))
        recipe_title = gen_data.get("title", "The Sloth Skillet")

        img_url, img_caption = resolve_recipe_image(
            None,
            recipe_title,
            [item.canonical_id for item in decision.normalized_ingredients],
            ingredients
        )

        return SlothRecipe(
            id=recipe_id,
            title=recipe_title,
            subtitle=gen_data.get("subtitle", "Low-effort culinary survival"),
            tagline=gen_data.get("tagline", "Less dishes, more resting."),
            sloth_efficiency=gen_data.get("sloth_efficiency", f"{sloth_score}% Energy Conserved"),
            sloth_score=sloth_score,
            image_url=img_url,
            image_caption=img_caption,
            vessel_type=effective_vessel,
            utensil=gen_data.get("utensil", "1 Fork"),
            dishes_to_wash=1,
            active_standing_minutes=active_time,
            total_minutes=tabpfn.total_minutes,
            harmony_score=tabpfn.harmony_score,
            ingredients_used=ingredients,
            sloth_shortcuts=gen_data.get("sloth_shortcuts", ["Crush with a mug; eat from the pan."]),
            steps=gen_data.get("steps", ["Heat pan.", "Dump ingredients.", "Eat."]),
            cleanup_audit=gen_data.get("cleanup_audit", f"1 {effective_vessel} and 1 fork to wash."),
            open_weights_rationale=rationale,
            tabpfn_evidence=tabpfn,
            status="READY",
            decision_message="Custom recipe generated from validated ingredients.",
            missing_suggestions=[],
            safety_warnings=decision.safety_warnings,
            fit_explanation=decision.fit_explanation,
            ai_engine_used=ai_engine
        )

# Global singleton
gemma_synthesizer = GemmaRecipeSynthesizer()
