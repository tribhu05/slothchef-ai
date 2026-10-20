from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.schemas import MissingIngredientSuggestion
from app.services.ingredient_normalizer import normalize_pantry, NormalizedIngredient, normalize_ingredient
from app.services.recipe_catalog import find_candidate_recipes, CuratedRecipe, VERIFIED_RECIPES

class DecisionResult(BaseModel):
    status: str = Field(..., description="READY, NEEDS_INGREDIENTS, or NO_GOOD_MATCH")
    decision_message: str
    selected_curated_recipe: Optional[CuratedRecipe] = None
    matched_req_ids: List[str] = Field(default_factory=list)
    matched_opt_ids: List[str] = Field(default_factory=list)
    missing_suggestions: List[MissingIngredientSuggestion] = Field(default_factory=list)
    safety_warnings: List[str] = Field(default_factory=list)
    fit_explanation: Optional[str] = None
    normalized_ingredients: List[NormalizedIngredient] = Field(default_factory=list)

def evaluate_pantry(raw_ingredients: List[str]) -> DecisionResult:
    """
    Evaluates the user's pantry through multi-stage intelligence:
    1. Normalization & State Tracking
    2. Feasibility, Food Safety & Substance Evaluation
    3. Curated Recipe Retrieval & Transparent Ranking
    4. Classification into READY, NEEDS_INGREDIENTS, or NO_GOOD_MATCH
    """
    if not raw_ingredients:
        return DecisionResult(
            status="NO_GOOD_MATCH",
            decision_message="No ingredients provided. Enter at least one pantry staple to begin.",
            safety_warnings=["Pantry is empty."]
        )

    # Stage A: Normalize
    norm_items = normalize_pantry(raw_ingredients)
    canonical_ids = [item.canonical_id for item in norm_items]
    canonical_set = set(canonical_ids)
    
    substantial_items = [item for item in norm_items if item.is_substantial]
    safety_warnings: List[str] = []

    # Food Safety & Cooking Constraint Inspections
    for item in norm_items:
        if item.prep_requirement == "needs_boiling" and item.culinary_state == "dry_grain":
            safety_warnings.append(
                f"⚠️ '{item.raw_name}' is raw dry grain: it cannot be stir-fried in a quick 3-minute skillet without 15-20 mins boiling liquid. Use day-old cooked rice for instant frying."
            )
        if item.prep_requirement in ("needs_soaking_and_boiling", "long_boil_required"):
            safety_warnings.append(
                f"⚠️ '{item.raw_name}' contains phytohaemagglutinin toxin: requires overnight soaking and vigorous boiling. We strongly recommend canned pre-cooked beans for fast cooking."
            )

    # Check 1: Condiments / Seasonings only (no calorie / protein / starch anchor)
    if len(substantial_items) == 0:
        # User only entered condiments or spices (e.g. Soy Sauce + Sriracha)
        suggestions = [
            MissingIngredientSuggestion(
                ingredient_name="Ramen Noodles",
                canonical_id="ramen",
                reason="Provides the starchy noodle base to absorb and bind your sauces into a luscious glaze.",
                unlocks_recipe_title="Midnight Dan-Dan Rescue",
                substitutes=["Rice Noodles", "Spaghetti", "Udon"]
            ),
            MissingIngredientSuggestion(
                ingredient_name="Cooked Rice",
                canonical_id="cooked_rice",
                reason="Provides a neutral warm grain bed that crisps up when sizzled with savory sauces.",
                unlocks_recipe_title="3-Minute Golden Scramble Fried Rice",
                substitutes=["Leftover quinoa", "Crushed tortilla chips"]
            ),
            MissingIngredientSuggestion(
                ingredient_name="Eggs",
                canonical_id="eggs",
                reason="Adds essential protein and quick emulsifying fats that transform sharp sauces into a rich meal.",
                unlocks_recipe_title="Tokyo Midnight Egg Sizzle",
                substitutes=["Tofu", "Canned chickpeas"]
            )
        ]
        return DecisionResult(
            status="NO_GOOD_MATCH",
            decision_message="Your pantry currently contains only condiments, seasonings, or spices. A meal requires a core staple (like Ramen, Rice, Bread, Pasta, or Eggs) to carry these flavors.",
            missing_suggestions=suggestions,
            safety_warnings=safety_warnings,
            fit_explanation="Seasonings cannot provide metabolic satiety or dish structure without a substantial carbohydrate or protein base.",
            normalized_ingredients=norm_items
        )

    # Stage B: Match against curated catalog
    candidate_matches = find_candidate_recipes(canonical_ids)

    if not candidate_matches:
        return DecisionResult(
            status="NO_GOOD_MATCH",
            decision_message="No culinary precedent found for this ingredient set. Add an everyday staple to anchor your pan.",
            safety_warnings=safety_warnings,
            normalized_ingredients=norm_items
        )

    best_match = candidate_matches[0]
    best_recipe: CuratedRecipe = best_match["recipe"]
    missing_req = best_match["missing_req"]
    matched_req = best_match["matched_req"]
    matched_opt = best_match["matched_opt"]

    # Case 1: READY (All required ingredients for the top dish are present!)
    if len(missing_req) == 0:
        return DecisionResult(
            status="READY",
            decision_message=f"You have everything required to cook {best_recipe.title}!",
            selected_curated_recipe=best_recipe,
            matched_req_ids=matched_req,
            matched_opt_ids=matched_opt,
            safety_warnings=safety_warnings,
            fit_explanation=best_recipe.culinary_rationale,
            normalized_ingredients=norm_items
        )

    # Case 2: NEEDS_INGREDIENTS (User has 1 or 2 missing essential items for a high-compatibility dish)
    if len(missing_req) <= 2 and (len(matched_req) >= 1 or len(substantial_items) >= 1):
        suggestions: List[MissingIngredientSuggestion] = []
        for m_id in missing_req:
            hint = best_recipe.missing_ingredient_hints.get(m_id, {})
            human_name = m_id.replace("_", " ").title()
            reason = hint.get("why", f"{human_name} is the essential flavor, binding, or moisture core needed to complete {best_recipe.title}.")
            substitutes = hint.get("substitutions", [])
            suggestions.append(
                MissingIngredientSuggestion(
                    ingredient_name=human_name,
                    canonical_id=m_id,
                    reason=reason,
                    unlocks_recipe_title=best_recipe.title,
                    substitutes=substitutes
                )
            )

        return DecisionResult(
            status="NEEDS_INGREDIENTS",
            decision_message=f"You're {len(missing_req)} ingredient away from a proper meal: {best_recipe.title}.",
            selected_curated_recipe=best_recipe,
            matched_req_ids=matched_req,
            matched_opt_ids=matched_opt,
            missing_suggestions=suggestions,
            safety_warnings=safety_warnings,
            fit_explanation=f"Your ingredients ({', '.join(raw_ingredients)}) form the base, but adding {suggestions[0].ingredient_name} provides the necessary emulsification, moisture, or binding.",
            normalized_ingredients=norm_items
        )

    # Case 3: NO_GOOD_MATCH
    general_suggestions = [
        MissingIngredientSuggestion(
            ingredient_name="Eggs",
            canonical_id="eggs",
            reason="High protein and natural emulsifier that binds disparate ingredients into a cohesive skillet hash.",
            unlocks_recipe_title="Cheesy Smashed Egg Skillet",
            substitutes=["Cheese", "Canned beans"]
        ),
        MissingIngredientSuggestion(
            ingredient_name="Ramen Noodles",
            canonical_id="ramen",
            reason="Instant starch base that cooks in 2 minutes and pairs with almost any pantry sauce.",
            unlocks_recipe_title="Midnight Dan-Dan Rescue",
            substitutes=["Bread", "Rice"]
        )
    ]

    return DecisionResult(
        status="NO_GOOD_MATCH",
        decision_message="No credible, harmonious one-pan dish could be verified for this combination without compromising food quality.",
        missing_suggestions=general_suggestions,
        safety_warnings=safety_warnings,
        fit_explanation="These ingredients lack a unifying culinary bridge (moisture, binding fat, or starch matrix) required for one-pan cooking.",
        normalized_ingredients=norm_items
    )
