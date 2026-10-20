from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class IngredientItem(BaseModel):
    name: str
    category: str = Field(..., description="starch, protein, allium, fat, sauce, veggie, spice")
    umami: float = Field(0.0, ge=0.0, le=10.0)
    acidity: float = Field(0.0, ge=0.0, le=10.0)
    moisture: float = Field(0.0, ge=0.0, le=10.0)
    richness: float = Field(0.0, ge=0.0, le=10.0)
    saltiness: float = Field(0.0, ge=0.0, le=10.0)

class TabPFNPrediction(BaseModel):
    harmony_score: float = Field(..., description="Overall pairing harmony from 0 to 100")
    confidence: float = Field(..., description="Model predictive confidence 0.0 to 1.0")
    effort_class: str = Field(..., description="Ultra-Sloth (<4 min), Low-Effort (5-7 min), Overachiever")
    dish_count: int = Field(1, description="Strict maximum number of vessels to wash")
    active_standing_minutes: int = Field(..., description="Minutes of actual physical standing")
    total_minutes: int = Field(..., description="Total cook time")
    flavor_balance: Dict[str, float] = Field(default_factory=dict)
    pairing_synergies: List[str] = Field(default_factory=list)
    model_version: str = "TabPFN-3.5 Prior Labs Foundation Model"

class RecipeRequest(BaseModel):
    ingredients: List[str] = Field(..., min_length=1, description="List of raw ingredients in the fridge/pantry")
    vessel_preference: Optional[str] = Field("One Skillet", description="Preferred cooking vessel: One Skillet, Microwave Bowl, Single Pot")
    sloth_intensity: Optional[str] = Field("Maximum", description="Sloth mode: Maximum (refuse to chop), Balanced, Cozy")
    max_active_minutes: Optional[int] = Field(5, ge=1, le=15, description="Maximum active standing minutes")
    max_cookware_count: Optional[int] = Field(1, ge=1, le=2, description="Maximum cookware count")
    max_utensil_count: Optional[int] = Field(1, ge=1, le=2, description="Maximum utensil count")
    microwave_only: Optional[bool] = Field(False, description="Enforce microwave-only cooking")
    minimal_chopping: Optional[bool] = Field(True, description="Strict zero/minimal knife prep")

class MissingIngredientSuggestion(BaseModel):
    ingredient_name: str
    canonical_id: str
    reason: str
    unlocks_recipe_title: str
    substitutes: List[str] = Field(default_factory=list)

class SlothRecipe(BaseModel):
    id: str
    title: str
    subtitle: str
    tagline: str
    sloth_efficiency: str
    sloth_score: int = 96
    image_url: Optional[str] = None
    vessel_type: str
    utensil: str = "1 Fork"
    dishes_to_wash: int = 1
    active_standing_minutes: int
    total_minutes: int
    harmony_score: float
    ingredients_used: List[str]
    sloth_shortcuts: List[str]
    steps: List[str]
    cleanup_audit: str
    open_weights_rationale: str
    tabpfn_evidence: TabPFNPrediction
    status: str = Field("READY", description="READY, NEEDS_INGREDIENTS, or NO_GOOD_MATCH")
    decision_message: Optional[str] = None
    missing_suggestions: List[MissingIngredientSuggestion] = Field(default_factory=list)
    safety_warnings: List[str] = Field(default_factory=list)
    fit_explanation: Optional[str] = None
    image_caption: Optional[str] = "Verified 1-Pan Presentation"
    ai_engine_used: Optional[str] = "SlothChef Decision Engine"

