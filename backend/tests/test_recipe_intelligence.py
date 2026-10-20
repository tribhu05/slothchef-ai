import pytest
from app.services.tabpfn_service import tabpfn_predictor
from app.services.gemma_service import gemma_synthesizer
from app.services.decision_engine import evaluate_pantry
from app.services.ingredient_normalizer import normalize_pantry, normalize_ingredient

def test_normalization_aliases_and_states():
    # Test normalization of various aliases and spellings
    ramen_item = normalize_ingredient("Instant Ramen Noodles")
    assert ramen_item.canonical_id == "ramen"
    assert ramen_item.category == "starch"
    assert ramen_item.state == "dry_grain"

    dry_rice = normalize_ingredient("uncooked white rice")
    assert dry_rice.canonical_id == "dry_rice"
    assert dry_rice.prep_requirement == "needs_boiling"

    cooked_rice = normalize_ingredient("leftover day-old rice")
    assert cooked_rice.canonical_id == "cooked_rice"
    assert cooked_rice.state == "cooked"

    # Distinguish coconut milk vs regular milk
    coconut = normalize_ingredient("canned coconut milk")
    assert coconut.canonical_id == "coconut_milk"
    assert coconut.category == "liquid"

    dairy = normalize_ingredient("whole cow's milk")
    assert dairy.canonical_id == "dairy_milk"
    assert dairy.category == "dairy"

@pytest.mark.asyncio
async def test_ready_ramen_dandan():
    pantry = ["Ramen", "Peanut butter", "Soy sauce", "Sriracha"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Dan-Dan" in recipe.title or "Peanut" in recipe.title
    assert "peanut_butter" in recipe.fit_explanation or "Dan-Dan" in recipe.fit_explanation or "lipid" in recipe.fit_explanation

@pytest.mark.asyncio
async def test_ready_chickpea_curry():
    pantry = ["Canned chickpeas", "Coconut milk", "Curry powder", "Frozen peas"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Curry" in recipe.title
    assert "chickpea" in recipe.title.lower()

@pytest.mark.asyncio
async def test_ready_potatoes_cheese_eggs():
    pantry = ["Potatoes", "Cheddar cheese", "Eggs", "Butter"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Potato" in recipe.title
    assert recipe.dishes_to_wash == 1

@pytest.mark.asyncio
async def test_ready_egg_fried_rice():
    pantry = ["Cooked rice", "Eggs", "Soy sauce", "Butter"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Fried Rice" in recipe.title

@pytest.mark.asyncio
async def test_ready_egg_in_a_hole():
    pantry = ["Sourdough bread", "Eggs", "Butter"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Egg-in-a-Hole" in recipe.title

@pytest.mark.asyncio
async def test_ready_grilled_cheese():
    pantry = ["Bread", "Cheese", "Butter"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Grilled Cheese" in recipe.title

@pytest.mark.asyncio
async def test_ready_pasta_aglio_olio():
    pantry = ["Pasta", "Garlic", "Cooking oil"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Aglio e Olio" in recipe.title

@pytest.mark.asyncio
async def test_ready_oat_bowl():
    pantry = ["Rolled oats", "Coconut milk", "Peanut butter"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Oat" in recipe.title

@pytest.mark.asyncio
async def test_ready_chilaquiles():
    pantry = ["Tortilla chips", "Salsa", "Cheddar cheese"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Chilaquiles" in recipe.title

@pytest.mark.asyncio
async def test_ready_bean_cheese_quesadilla():
    pantry = ["Tortillas", "Canned black beans", "Cheese"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Bean" in recipe.title or "Quesadilla" in recipe.title or "Fold" in recipe.title

@pytest.mark.asyncio
async def test_ready_kimchi_fried_rice():
    pantry = ["Cooked rice", "Kimchi", "Eggs"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Kimchi" in recipe.title

@pytest.mark.asyncio
async def test_ready_tuna_mayo_rice():
    pantry = ["Cooked rice", "Canned tuna", "Mayonnaise", "Sriracha"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Tuna" in recipe.title

@pytest.mark.asyncio
async def test_ready_glazed_tofu():
    pantry = ["Firm tofu", "Soy sauce", "Sriracha"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "READY"
    assert "Tofu" in recipe.title

@pytest.mark.asyncio
async def test_condiments_only_returns_no_good_match():
    # Only condiments, sauces, and spices
    pantry = ["Soy sauce", "Sriracha", "Ketchup", "Salt"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "NO_GOOD_MATCH"
    assert len(recipe.missing_suggestions) >= 1
    # Check that it suggests staples like Ramen, Cooked Rice, or Eggs
    suggested_names = [s.ingredient_name.lower() for s in recipe.missing_suggestions]
    assert any("ramen" in s or "rice" in s or "egg" in s for s in suggested_names)

@pytest.mark.asyncio
async def test_needs_ingredients_ramen_missing_pb():
    pantry = ["Ramen", "Soy sauce", "Sriracha"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "NEEDS_INGREDIENTS"
    assert len(recipe.missing_suggestions) >= 1
    # Check that peanut butter is recommended with culinary explanation
    pb_sug = next((s for s in recipe.missing_suggestions if "peanut" in s.canonical_id), None)
    assert pb_sug is not None
    assert "Dan-Dan" in pb_sug.unlocks_recipe_title
    assert len(pb_sug.reason) > 10

@pytest.mark.asyncio
async def test_needs_ingredients_chickpea_missing_curry():
    pantry = ["Canned chickpeas", "Coconut milk"]
    pred = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, pred)
    assert recipe.status == "NEEDS_INGREDIENTS"
    curry_sug = next((s for s in recipe.missing_suggestions if "curry" in s.canonical_id), None)
    assert curry_sug is not None
    assert "Curry" in curry_sug.unlocks_recipe_title

@pytest.mark.asyncio
async def test_raw_dry_rice_safety_warning():
    pantry = ["Uncooked white rice", "Eggs", "Soy sauce"]
    decision = evaluate_pantry(pantry)
    assert any("raw dry grain" in w or "needs" in w or "15-20" in w for w in decision.safety_warnings)

@pytest.mark.asyncio
async def test_dry_beans_safety_warning():
    pantry = ["Dry black beans", "Tortillas", "Cheese"]
    decision = evaluate_pantry(pantry)
    assert any("phytohaemagglutinin" in w or "soaking" in w for w in decision.safety_warnings)

@pytest.mark.asyncio
async def test_differentiation_across_inputs():
    """Ensure different ingredient combos produce distinctly different recipes."""
    p1 = ["Ramen", "Peanut butter", "Soy sauce"]
    p2 = ["Canned chickpeas", "Coconut milk", "Curry powder"]
    p3 = ["Potatoes", "Cheese", "Eggs"]

    r1 = await gemma_synthesizer.generate_recipe(p1, tabpfn_predictor.predict(p1))
    r2 = await gemma_synthesizer.generate_recipe(p2, tabpfn_predictor.predict(p2))
    r3 = await gemma_synthesizer.generate_recipe(p3, tabpfn_predictor.predict(p3))

    assert r1.title != r2.title
    assert r2.title != r3.title
    assert r1.title != r3.title
    assert r1.steps != r2.steps
    assert r2.steps != r3.steps

@pytest.mark.asyncio
async def test_image_registry_and_caption_trustworthiness():
    """Verify that oat recipes never display salad photos, and images have truthful captions."""
    from app.services.image_registry import resolve_recipe_image
    
    # 1. Direct registry lookup
    img, caption = resolve_recipe_image(
        recipe_id="creamy-oat-bowl",
        title="5-Minute Creamy Porridge Oats",
        canonical_ids=["oats", "milk"]
    )
    assert "photo-1584776296944" in img
    assert "photo-1540420773420" not in img
    assert "Oats" in caption or "Porridge" in caption or "Oatmeal" in caption

    # 2. End-to-end recipe generation for Oats + Milk
    pantry = ["Rolled oats", "Whole milk"]
    tabpfn = tabpfn_predictor.predict(pantry)
    recipe = await gemma_synthesizer.generate_recipe(pantry, tabpfn)
    
    assert "Oat" in recipe.title or "Porridge" in recipe.title
    assert "photo-1584776296944" in recipe.image_url
    assert "photo-1540420773420" not in recipe.image_url  # No raw garden salad photo!
    assert recipe.image_caption is not None
    assert recipe.ai_engine_used is not None
    assert len(recipe.ingredients_used) >= 2

