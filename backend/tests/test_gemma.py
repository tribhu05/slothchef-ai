import pytest
from app.services.tabpfn_service import tabpfn_predictor
from app.services.gemma_service import gemma_synthesizer

@pytest.mark.asyncio
async def test_gemma_recipe_synthesis():
    ingredients = ["Ramen noodles", "Peanut butter", "Soy sauce", "Sriracha"]
    tabpfn_pred = tabpfn_predictor.predict(ingredients)
    
    recipe = await gemma_synthesizer.generate_recipe(
        ingredients=ingredients,
        tabpfn=tabpfn_pred,
        vessel="One Skillet",
        sloth_intensity="Maximum"
    )
    
    assert recipe.dishes_to_wash == 1
    assert "Fork" in recipe.utensil or "Spoon" in recipe.utensil
    assert recipe.active_standing_minutes <= 5
    assert len(recipe.steps) >= 2
    assert len(recipe.sloth_shortcuts) >= 1
    assert "open-source" in recipe.open_weights_rationale.lower()
    assert recipe.tabpfn_evidence.harmony_score == tabpfn_pred.harmony_score

@pytest.mark.asyncio
async def test_gemma_chilaquiles_synthesis():
    ingredients = ["Corn tortilla chips", "Canned black beans", "Cheddar cheese", "Salsa (jarred)"]
    tabpfn_pred = tabpfn_predictor.predict(ingredients)
    
    recipe = await gemma_synthesizer.generate_recipe(
        ingredients=ingredients,
        tabpfn=tabpfn_pred,
        vessel="One Skillet"
    )
    
    assert "chilaquiles" in recipe.title.lower() or "skillet" in recipe.title.lower()
    assert recipe.dishes_to_wash == 1
