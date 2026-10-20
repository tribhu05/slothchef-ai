from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class CuratedRecipe(BaseModel):
    id: str
    title: str
    subtitle: str
    tagline: str
    required_ids: List[str] = Field(..., description="Canonical ingredient IDs that MUST be present")
    optional_ids: List[str] = Field(default_factory=list, description="Canonical ingredient IDs that enhance the dish")
    vessel_type: str = "One Skillet"
    supports_microwave: bool = True
    active_minutes: int = 3
    total_minutes: int = 4
    base_sloth_score: int = 96
    steps: List[str]
    shortcuts: List[str]
    cleanup_audit: str
    image_url: str
    culinary_rationale: str
    missing_ingredient_hints: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

VERIFIED_RECIPES: List[CuratedRecipe] = [
    # 1. Ramen + Peanut Butter + Condiments
    CuratedRecipe(
        id="ramen-dandan",
        title="Midnight Dan-Dan Rescue",
        subtitle="Velvety sesame-peanut noodles born from pure exhaustion",
        tagline="Tastes like a $16 takeout bowl; took 3 minutes and zero dignity.",
        required_ids=["ramen", "peanut_butter"],
        optional_ids=["soy_sauce", "sriracha", "garlic", "scallions"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=97,
        shortcuts=[
            "Dissolve peanut butter directly into boiling noodle water — never dirty a prep bowl.",
            "Crush garlic with the flat bottom of a coffee mug. Toss it in whole."
        ],
        steps=[
            "Boil ramen in your vessel with 1 cup of water for 2 minutes until tender.",
            "Turn off heat. Immediately stir in peanut butter, soy sauce, and sriracha until a glossy sauce forms.",
            "Eat directly out of the vessel with a fork. Do not transfer to a serving plate."
        ],
        cleanup_audit="Exactly 1 vessel and 1 fork. Zero cutting boards or prep bowls.",
        image_url="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Hot ramen cooking starch emulsifies with the dense lipids in peanut butter and sodium in soy sauce to create a rich Dan-Dan style glaze.",
        missing_ingredient_hints={
            "peanut_butter": {
                "why": "Peanut butter provides the rich lipid emulsion that transforms plain boiled ramen into a velvety, takeout-grade noodle sauce.",
                "substitutions": ["Sesame paste (tahini)", "Cheddar cheese", "Butter"]
            }
        }
    ),

    # 2. Ramen + Cheese + Egg (Sloth Carbonara)
    CuratedRecipe(
        id="ramen-carbonara",
        title="3-Minute Desperation Carbonara Ramen",
        subtitle="Silky, molten cheese emulsified in starchy noodle water",
        tagline="The Romans took 400 years to invent Carbonara; you made it in 180 seconds.",
        required_ids=["ramen", "cheese", "eggs"],
        optional_ids=["butter", "bacon", "seasoning"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=95,
        shortcuts=[
            "Do not drain the water! Hot noodle starch is what melts and binds the cheese.",
            "Crack the egg onto hot noodles off-heat so it creams without scrambling."
        ],
        steps=[
            "Boil ramen in your vessel with just enough water to submerge for 2 minutes.",
            "Turn off heat. Toss in butter, cracked egg, and a mound of cheese.",
            "Vigorously swirl with your fork for 30 seconds until a creamy, glossy emulsion forms."
        ],
        cleanup_audit="1 pan to wipe down. Zero colanders or whisks to wash.",
        image_url="https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Noodle starch water + egg yolk proteins + molten cheese form an instantaneous carbonara emulsion off residual heat.",
        missing_ingredient_hints={
            "eggs": {
                "why": "Egg yolk proteins provide the classic custard binder that thickens the cheese into a sauce.",
                "substitutions": ["Extra butter", "Splash of cream"]
            },
            "cheese": {
                "why": "Cheese delivers the savory, salty fat core required for Carbonara.",
                "substitutions": ["Peanut butter (switch to Dan-Dan)", "Butter + soy sauce"]
            }
        }
    ),

    # 3. Tortilla Chips + Salsa + Cheese (Chilaquiles)
    CuratedRecipe(
        id="chilaquiles-skillet",
        title="Pants-Free Skillet Chilaquiles",
        subtitle="Rescuing stale bag-crumbs into artisanal Mexican comfort",
        tagline="Turns stale pantry regret into molten cheesy triumph in 4 minutes.",
        required_ids=["tortilla_chips", "salsa", "cheese"],
        optional_ids=["canned_beans", "eggs", "sour_cream"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=96,
        shortcuts=[
            "Do not sort the chips. Dump the broken shards right into the pan.",
            "Let residual pan heat melt the cheese so you can sit down sooner."
        ],
        steps=[
            "Toss chips, beans, and salsa into the vessel over medium heat for 90 seconds until warm.",
            "Turn off heat. Blanket the entire top with cheese.",
            "Cover with a lid or foil for 60 seconds until molten. Dig in."
        ],
        cleanup_audit="1 pan to rinse. Zero prep dishes.",
        image_url="https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Acidic, spiced tomato salsa gently softens crisp corn masa chips while molten cheese blankets and binds the texture.",
        missing_ingredient_hints={
            "cheese": {
                "why": "Cheese is essential to bind the salsa and chips together into a cohesive bake rather than soggy chips.",
                "substitutions": ["Refried beans", "Cracked eggs"]
            },
            "salsa": {
                "why": "Salsa provides the moisture and acid that softens the tortilla chips into traditional chilaquiles.",
                "substitutions": ["Canned crushed tomatoes + hot sauce", "Enchilada sauce"]
            }
        }
    ),

    # 4. Chickpeas + Coconut Milk + Curry Powder (Pantry Curry)
    CuratedRecipe(
        id="chickpea-coconut-curry",
        title="Pantry Pauper Chickpea Coconut Curry",
        subtitle="A fragrant 5-minute miracle from forgotten cans",
        tagline="Feels like a Sunday slow-cook, but you stood up for exactly 180 seconds.",
        required_ids=["canned_chickpeas", "coconut_milk", "curry_powder"],
        optional_ids=["peas", "greens", "garlic", "cooked_rice"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=3,
        total_minutes=5,
        base_sloth_score=94,
        shortcuts=[
            "Do not drain the chickpea liquid; the natural aquafaba starches thicken your sauce.",
            "Toss frozen peas in straight from the freezer without defrosting."
        ],
        steps=[
            "Empty chickpeas, curry powder, and coconut milk into your vessel.",
            "Simmer on medium heat for 3 minutes until aromatic, thick, and bubbling.",
            "Fold in frozen peas or greens for the final 60 seconds. Eat with a spoon."
        ],
        cleanup_audit="1 vessel and 1 spoon. You didn't even wash a knife.",
        image_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Coconut milk fats bloom fat-soluble curcumin in curry powder, while chickpea proteins create a hearty stew base.",
        missing_ingredient_hints={
            "coconut_milk": {
                "why": "Coconut milk provides the rich, non-dairy lipid base that carries the curry spices without curdling.",
                "substitutions": ["Tomato sauce + butter", "Yogurt (stirred in off heat)"]
            },
            "curry_powder": {
                "why": "Curry powder delivers all aromatic spices (turmeric, cumin, coriander) in one scoop without measuring.",
                "substitutions": ["Garam masala", "Cumin + chili powder"]
            }
        }
    ),

    # 5. Potatoes + Cheese + Eggs (Cheesy Potato Egg Skillet)
    CuratedRecipe(
        id="cheesy-potato-egg-skillet",
        title="Cheesy Smashed Potato & Egg Skillet",
        subtitle="Crispy seared potato chunks with runny eggs and bubbling cheddar",
        tagline="A diner-grade breakfast hash made in one pan with zero knife skills.",
        required_ids=["potato", "cheese", "eggs"],
        optional_ids=["butter", "bacon", "onion", "garlic"],
        vessel_type="One Skillet",
        supports_microwave=False,
        active_minutes=4,
        total_minutes=5,
        base_sloth_score=95,
        shortcuts=[
            "Smash cooked or canned potatoes with the bottom of a mug to maximize crispy surface area.",
            "Crack eggs directly into craters made between the potato chunks."
        ],
        steps=[
            "Melt butter/oil in your skillet over medium-high heat. Add potatoes and smash flat with a mug.",
            "Sear undisturbed for 2.5 minutes until golden brown. Flip potato pieces.",
            "Crack eggs into pan crevices, blanket with cheese, cover for 90 seconds until eggs set and cheese is molten."
        ],
        cleanup_audit="1 skillet and 1 fork to wash. Done in under 5 minutes.",
        image_url="https://images.unsplash.com/photo-1518013034458-30b0ee243591?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Starch-dense potatoes crisp up in fat, creating an ideal savory bed for rich egg yolks and melted dairy.",
        missing_ingredient_hints={
            "eggs": {
                "why": "Eggs turn loose potatoes and cheese into a cohesive, high-protein skillet meal.",
                "substitutions": ["Canned black beans", "Breakfast sausage / bacon"]
            },
            "cheese": {
                "why": "Cheese binds the crispy potato hash together and adds necessary salt and fat.",
                "substitutions": ["Butter + hot sauce", "Sour cream"]
            }
        }
    ),

    # 6. Cooked Rice + Kimchi + Eggs (Sleepy Kimchi Sizzle)
    CuratedRecipe(
        id="kimchi-fried-rice",
        title="The Sleepy Kimchi Sizzle Fried Rice",
        subtitle="Crispy fermented joy with zero active braincells",
        tagline="The sour acidity does 90% of the seasoning work so your hands don't have to.",
        required_ids=["cooked_rice", "kimchi", "eggs"],
        optional_ids=["butter", "soy_sauce", "scallions"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=97,
        shortcuts=[
            "Cut kimchi directly inside the jar using kitchen scissors—never dirty a cutting board.",
            "Press cold rice flat with a spatula and don't touch for 2 minutes to get crispy bits."
        ],
        steps=[
            "Melt butter in your skillet, add cold rice and kimchi.",
            "Press flat, crack the egg directly into the center, and cover for 2 minutes.",
            "Drizzle soy sauce, swirl together, and eat straight from the iron."
        ],
        cleanup_audit="1 skillet to rinse. Zero plates.",
        image_url="https://images.unsplash.com/photo-1590301157890-4810ed352733?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Lactic acid in fermented kimchi balances the rich egg yolk and savory browned rice starches.",
        missing_ingredient_hints={
            "cooked_rice": {
                "why": "Pre-cooked, day-old rice provides the dry starch base that absorbs kimchi juice without turning to mush.",
                "substitutions": ["Ramen noodles (Kimchi Ramen)", "Tortilla chips"]
            },
            "eggs": {
                "why": "Rich egg yolk balances the sharp, spicy acidity of fermented kimchi.",
                "substitutions": ["Tofu cubes", "Cheese slice"]
            }
        }
    ),

    # 7. Cooked Rice + Garlic + Butter + Soy Sauce
    CuratedRecipe(
        id="garlic-butter-rice",
        title="Tokyo Midnight Garlic Butter Crispy Rice",
        subtitle="Caramelized teppan-style rice with crunchy golden edges",
        tagline="Four ingredients, zero chopping, tastes like a 2 AM Shinjuku izakaya.",
        required_ids=["cooked_rice", "garlic", "butter", "soy_sauce"],
        optional_ids=["eggs", "scallions", "peas"],
        vessel_type="One Skillet",
        supports_microwave=False,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=98,
        shortcuts=[
            "Smash garlic under a mug and toss in whole with butter.",
            "Spread rice across pan base and resist stirring for 120 seconds to form golden crust."
        ],
        steps=[
            "Melt butter in your skillet over medium heat with smashed garlic until foaming.",
            "Add cold rice, breaking clumps with a fork. Drizzle soy sauce around the outer pan perimeter.",
            "Press down firmly and sear until the bottom is crackling and golden brown. Serve."
        ],
        cleanup_audit="1 skillet to rinse. Zero prep dishes.",
        image_url="https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Butter and allicin-rich garlic sizzle against the pan rim, allowing soy sauce sugars to caramelize against rice starch.",
        missing_ingredient_hints={
            "butter": {
                "why": "Butter fat carries the garlic flavor and enables the rice to develop a crispy, non-stick crust.",
                "substitutions": ["Sesame oil", "Olive oil"]
            }
        }
    ),

    # 8. Cooked Rice + Eggs + Soy Sauce (Egg Fried Rice)
    CuratedRecipe(
        id="egg-fried-rice",
        title="3-Minute Golden Scramble Fried Rice",
        subtitle="Fluffy scrambled egg ribbons folded through hot seasoned rice",
        tagline="Faster than waiting for food delivery, and 100% dish-efficient.",
        required_ids=["cooked_rice", "eggs", "soy_sauce"],
        optional_ids=["butter", "cooking_oil", "peas", "scallions"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=96,
        shortcuts=[
            "Push rice to one side and scramble the eggs directly in the cleared half of the skillet.",
            "Splash soy sauce against the bare hot metal to vaporize and impart wok hei aroma."
        ],
        steps=[
            "Heat oil or butter in skillet over medium-high heat. Add cooked rice and toss for 1 minute.",
            "Push rice to the side. Crack eggs into the hot spot and scramble with your fork for 45 seconds.",
            "Fold eggs into rice, splash soy sauce around the rim, toss vigorously, and serve."
        ],
        cleanup_audit="1 skillet and 1 eating fork. Done.",
        image_url="https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Eggs provide quick moisture, protein, and emulsification that coats each grain of rice with savory umami.",
        missing_ingredient_hints={
            "cooked_rice": {
                "why": "Fried rice requires pre-cooked rice. Raw dry rice cannot be fried directly without boiling first.",
                "substitutions": ["Ramen noodles", "Bread cubes"]
            }
        }
    ),

    # 9. Eggs + Tomato Sauce + Garlic (Emergency Shakshuka)
    CuratedRecipe(
        id="emergency-shakshuka",
        title="4-Minute Emergency Shakshuka",
        subtitle="Silky eggs poached in bubbling spiced tomato reduction",
        tagline="High-protein North African brunch luxury synthesized with zero prep.",
        required_ids=["eggs", "tomato_sauce"],
        optional_ids=["garlic", "cheese", "bread", "cooking_oil"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=2,
        total_minutes=4,
        base_sloth_score=96,
        shortcuts=[
            "Make craters in the bubbling sauce with a spoon and crack eggs directly in.",
            "Cover with a lid or foil so egg whites set in 2 minutes flat without flipping."
        ],
        steps=[
            "Pour tomato sauce into skillet with garlic and seasonings over medium heat until bubbling.",
            "Create 2 wells in the sauce. Crack eggs directly into each well.",
            "Cover with a lid for 2.5 minutes until whites are firm and yolks remain jammy. Serve."
        ],
        cleanup_audit="1 pan to wipe down. Zero prep bowls.",
        image_url="https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Acidic, seasoned tomato sauce poaches eggs gently without needing water or poaching vinegar.",
        missing_ingredient_hints={
            "eggs": {
                "why": "Eggs provide the protein core of Shakshuka.",
                "substitutions": ["Canned chickpeas", "Tofu slices"]
            },
            "tomato_sauce": {
                "why": "Tomato sauce provides the bubbling poaching liquid that cooks the eggs gently.",
                "substitutions": ["Jarred salsa", "Crushed canned tomatoes"]
            }
        }
    ),

    # 10. Bread + Eggs + Butter (Egg in a Hole)
    CuratedRecipe(
        id="egg-in-a-hole",
        title="Crispy Golden Egg-in-a-Hole Melt",
        subtitle="Buttery toasted sourdough with a runny egg center and molten cheese",
        tagline="One pan, three minutes, and zero bowls to clean before work.",
        required_ids=["bread", "eggs", "butter"],
        optional_ids=["cheese", "bacon", "seasoning"],
        vessel_type="One Skillet",
        supports_microwave=False,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=98,
        shortcuts=[
            "Tear a hole in the bread center with your bare fingers—no cookie cutter required.",
            "Drop the torn bread center right alongside in the pan as a crispy dipping soldier."
        ],
        steps=[
            "Melt butter in your skillet. Lay down bread slice.",
            "Crack the egg directly into the center hole. Season with salt and pepper.",
            "Flip after 2 minutes, top with cheese, and sear for 1 minute until golden and melted."
        ],
        cleanup_audit="1 skillet and 1 spatula. Done.",
        image_url="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="The bread boundary contains the egg white while the bottom fries into a crispy buttered crust.",
        missing_ingredient_hints={
            "eggs": {
                "why": "The egg fills the center hole and provides protein and moisture.",
                "substitutions": ["Cheese slice (switch to Grilled Cheese)"]
            }
        }
    ),

    # 11. Bread + Cheese + Butter (Inside-Out Grilled Cheese)
    CuratedRecipe(
        id="grilled-cheese",
        title="The Ultimate Inside-Out Grilled Cheese",
        subtitle="Crispy frico cheese crust on the outside, molten gooey center within",
        tagline="Why put cheese only inside when you can toast it directly into the skillet?",
        required_ids=["bread", "cheese", "butter"],
        optional_ids=["garlic", "tomato_sauce", "bacon"],
        vessel_type="One Skillet",
        supports_microwave=False,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=97,
        shortcuts=[
            "Butter the bread with the back of a spoon—never dirty a butter knife.",
            "Scatter a pinch of shredded cheese directly on the hot pan under the bread for a crunchy crust."
        ],
        steps=[
            "Melt butter in skillet. Lay down bread and layer thick cheese on top.",
            "Top with second slice. Cook on medium-low for 2 minutes until bottom is golden.",
            "Flip and cook for 90 seconds until cheese is completely molten. Slice and eat."
        ],
        cleanup_audit="1 skillet to wipe down. Zero prep bowls.",
        image_url="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Thermal conduction melts the dairy core while browning exterior milk solids into crispy frico.",
        missing_ingredient_hints={
            "cheese": {
                "why": "Cheese is the primary filling and binding agent.",
                "substitutions": ["Peanut butter", "Cooked eggs"]
            }
        }
    ),

    # 12. Pasta + Garlic + Olive Oil (Spaghetti Aglio e Olio)
    CuratedRecipe(
        id="pasta-aglio-olio",
        title="Midnight Spaghetti Aglio e Olio",
        subtitle="The legendary Neapolitan late-night garlic and pepper sizzle",
        tagline="Invented by broke Italian students in the 1700s; perfected by tired developers today.",
        required_ids=["pasta", "garlic", "cooking_oil"],
        optional_ids=["cheese", "seasoning", "canned_tuna"],
        vessel_type="One Skillet",
        supports_microwave=False,
        active_minutes=4,
        total_minutes=6,
        base_sloth_score=94,
        shortcuts=[
            "Cook pasta in shallow water so the starchy water naturally binds the olive oil into sauce.",
            "Crush garlic with a mug and fry on low heat so it sweetens without burning."
        ],
        steps=[
            "Cook pasta in skillet with minimal salted water until al dente.",
            "Pour off most water leaving 3 tablespoons. Slide pasta to one side.",
            "In cleared pan area, sizzle garlic in olive oil for 60 seconds, then toss all together."
        ],
        cleanup_audit="1 skillet and 1 fork. Done.",
        image_url="https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Pasta cooking water starch acts as a natural emulsifier, binding rich olive oil and garlic allicin into a glossy sauce.",
        missing_ingredient_hints={
            "pasta": {
                "why": "Pasta provides the starch base for Aglio e Olio.",
                "substitutions": ["Ramen noodles"]
            }
        }
    ),

    # 13. Oats + Milk / Coconut Milk (Creamy Warm Oats)
    CuratedRecipe(
        id="creamy-oat-bowl",
        title="5-Minute Creamy Porridge Oats",
        subtitle="Warm, creamy breakfast comfort synthesized in a single bowl",
        tagline="Warm porridge that coats your stomach with zero pots to scrub.",
        required_ids=["oats"],
        optional_ids=["coconut_milk", "dairy_milk", "peanut_butter", "sweetener"],
        vessel_type="Microwave Safe Bowl",
        supports_microwave=True,
        active_minutes=1,
        total_minutes=3,
        base_sloth_score=99,
        shortcuts=[
            "Cook and eat in the exact same microwave-safe bowl.",
            "Swirl peanut butter in while oats are steaming to create rich ribbons."
        ],
        steps=[
            "Add oats and 3/4 cup liquid (water, milk, or coconut milk) to your bowl.",
            "Microwave on HIGH for 90 seconds. Stir with your spoon.",
            "Swirl in peanut butter or sweetener. Let cool 1 minute and enjoy."
        ],
        cleanup_audit="1 bowl and 1 spoon to rinse. Zero pans.",
        image_url="https://images.unsplash.com/photo-1584776296944-ab6fb57b0bdd?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Beta-glucan soluble fibers in oats absorb liquid rapidly under microwave heat to form a soothing porridge.",
        missing_ingredient_hints={
            "peanut_butter": {
                "why": "Peanut butter provides healthy fats and protein to keep you full for hours.",
                "substitutions": ["Milk", "Honey"]
            }
        }
    ),

    # 14. Canned Beans + Tortillas + Cheese (Burrito / Quesadilla)
    CuratedRecipe(
        id="bean-cheese-quesadilla",
        title="Crispy Skillet Bean & Cheese Fold",
        subtitle="Toasted tortilla stuffed with molten cheddar and seasoned black beans",
        tagline="Restaurant-grade quesadilla crunch with zero chopping and 1 pan to wipe.",
        required_ids=["tortillas", "cheese", "canned_beans"],
        optional_ids=["salsa", "sriracha", "butter"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=3,
        total_minutes=4,
        base_sloth_score=96,
        shortcuts=[
            "Mash beans lightly with your fork directly on the tortilla—never pre-mash in a bowl.",
            "Fold in half to make flipping easy with no spatula required."
        ],
        steps=[
            "Warm tortilla in skillet. Spread beans on one half, top with cheese and salsa.",
            "Fold in half. Sear for 2 minutes on medium heat until golden and crispy.",
            "Flip once for 60 seconds until cheese is completely molten. Eat with hands."
        ],
        cleanup_audit="1 pan to wipe down. Zero plates if eaten on a napkin.",
        image_url="https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Beans provide protein and earthiness while cheese melts to form an adhesive matrix inside the toasted tortilla.",
        missing_ingredient_hints={
            "cheese": {
                "why": "Cheese binds the beans inside the tortilla so they don't spill out when flipping.",
                "substitutions": ["Refried beans + salsa"]
            }
        }
    ),

    # 15. Canned Tuna + Mayo + Rice (Spicy Tuna Rice Bowl)
    CuratedRecipe(
        id="tuna-mayo-rice",
        title="Deconstructed Spicy Tuna Rice Skillet",
        subtitle="Warm seasoned rice with savory flaked tuna and spicy mayo drizzle",
        tagline="All the flavors of a $9 spicy tuna roll without rolling bamboo mats.",
        required_ids=["cooked_rice", "canned_tuna", "mayonnaise"],
        optional_ids=["sriracha", "soy_sauce", "scallions", "garlic"],
        vessel_type="One Skillet",
        supports_microwave=True,
        active_minutes=2,
        total_minutes=3,
        base_sloth_score=97,
        shortcuts=[
            "Flake tuna directly into the pan from the can using your eating fork.",
            "Zig-zag sriracha and mayo directly over the warm rice bed."
        ],
        steps=[
            "Warm cooked rice in skillet with a teaspoon of soy sauce for 1 minute.",
            "Scatter flaked tuna evenly across the top and let residual pan heat warm it.",
            "Drizzle mayonnaise and sriracha generously over the surface. Eat hot."
        ],
        cleanup_audit="1 pan and 1 fork. Done.",
        image_url="https://images.unsplash.com/photo-1546069901-d8a1c97a5a8e?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="Emulsified mayonnaise binds savory lean tuna flakes while warm rice starch absorbs the umami soy seasoning.",
        missing_ingredient_hints={
            "canned_tuna": {
                "why": "Tuna delivers lean protein and savory depth to the rice bowl.",
                "substitutions": ["Canned salmon", "Scrambled eggs"]
            },
            "mayonnaise": {
                "why": "Mayonnaise provides the necessary moisture and fat that keeps tuna from tasting dry.",
                "substitutions": ["Butter", "Sour cream"]
            }
        }
    ),

    # 16. Tofu + Soy Sauce + Sriracha (Sweet-Heat Glazed Tofu)
    CuratedRecipe(
        id="glazed-tofu-skillet",
        title="Crispy Sweet-Heat Glazed Tofu Planks",
        subtitle="Golden pan-seared tofu planks lacquered in savory garlic-chili reduction",
        tagline="High-protein, plant-based indulgence ready in under 5 active minutes.",
        required_ids=["tofu", "soy_sauce"],
        optional_ids=["sriracha", "garlic", "sweetener", "cooking_oil"],
        vessel_type="One Skillet",
        supports_microwave=False,
        active_minutes=3,
        total_minutes=5,
        base_sloth_score=95,
        shortcuts=[
            "Tear tofu into rustic jagged pieces with bare fingers—jagged edges crisp up better than sliced cubes.",
            "Pour soy sauce and sriracha directly into the sizzling pan to glaze."
        ],
        steps=[
            "Heat oil in skillet over high heat. Add tofu pieces and sear for 2.5 minutes without moving.",
            "Turn pieces over. Pour in soy sauce, sriracha, and garlic/seasonings.",
            "Toss rapidly as the sauce bubbles into a sticky, caramelized glaze. Serve hot."
        ],
        cleanup_audit="1 skillet and 1 fork. Zero cutting boards.",
        image_url="https://images.unsplash.com/photo-1546069901-d8a1c97a5a8e?auto=format&fit=crop&w=1200&q=80",
        culinary_rationale="High heat caramelizes the soy amino acids against the porous, absorbent soy proteins of the tofu.",
        missing_ingredient_hints={
            "soy_sauce": {
                "why": "Soy sauce is the primary savory glutamate source that flavors plain tofu.",
                "substitutions": ["Curry powder + coconut milk", "Teriyaki sauce"]
            }
        }
    )
]

def find_candidate_recipes(available_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Ranks curated recipes against user's canonical ingredients.
    Returns ranked candidates with overlap, missing required items, and score.
    """
    avail_set = set(available_ids)
    results = []

    for recipe in VERIFIED_RECIPES:
        req_set = set(recipe.required_ids)
        opt_set = set(recipe.optional_ids)

        matched_req = req_set.intersection(avail_set)
        missing_req = req_set.difference(avail_set)
        matched_opt = opt_set.intersection(avail_set)

        # How many user ingredients were used in this recipe
        used_count = len(matched_req) + len(matched_opt)
        coverage = used_count / max(len(avail_set), 1)

        # Scoring
        score = (len(matched_req) * 35) + (len(matched_opt) * 12) - (len(missing_req) * 30) + (coverage * 20)

        results.append({
            "recipe": recipe,
            "matched_req": list(matched_req),
            "missing_req": list(missing_req),
            "matched_opt": list(matched_opt),
            "coverage": coverage,
            "score": score
        })

    # Sort descending by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
