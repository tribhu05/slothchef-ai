import os
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.models.schemas import RecipeRequest, SlothRecipe, TabPFNPrediction
from app.services.tabpfn_service import tabpfn_predictor
from app.services.gemma_service import gemma_synthesizer
from app.services.pantry_catalog import PRESET_DISASTERS, load_ingredients

app = FastAPI(
    title="SlothChef API 🍳🦥",
    description="The Extreme Low-Effort, One-Pan Survival Engine powered by TabPFN-3.5 and Gemma 2.",
    version="1.0.0"
)

# Enable CORS for local dev & frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "app": "SlothChef",
        "version": "1.0.0",
        "challenge": "DEV Hacktoberfest 2026: Week 3 (Slow and Steady)",
        "ai_engines": {
            "tabular_foundation_model": "TabPFN-3.5 (Prior Labs)",
            "recipe_synthesizer": "Google Gemma 2 (Local Open-Weight SLM)"
        },
        "sloth_rules": {
            "dish_cap": 1,
            "max_standing_minutes": 5,
            "active_pantries": len(PRESET_DISASTERS)
        }
    }

@app.get("/api/pantry/presets")
async def get_presets() -> List[Dict[str, Any]]:
    """Return 1-click test scenarios for judges and exhausted users."""
    return PRESET_DISASTERS

@app.get("/api/pantry/catalog")
async def get_catalog() -> List[str]:
    """Return common scavenged fridge items for autocomplete chips."""
    db = load_ingredients()
    return sorted([k.title() for k in db.keys()])

@app.post("/api/predict/harmony", response_model=TabPFNPrediction)
async def predict_harmony(req: RecipeRequest) -> TabPFNPrediction:
    """Evaluate ingredient synergy using TabPFN tabular in-context foundation model."""
    if not req.ingredients:
        raise HTTPException(status_code=400, detail="At least 1 ingredient must be specified.")
    return tabpfn_predictor.predict(req.ingredients, req.vessel_preference or "One Skillet")

@app.post("/api/recipe/generate", response_model=SlothRecipe)
async def generate_recipe(req: RecipeRequest) -> SlothRecipe:
    """Run full dual-AI pipeline: TabPFN flavor prediction + Gemma 2 sloth synthesis."""
    if not req.ingredients:
        raise HTTPException(status_code=400, detail="At least 1 ingredient must be specified.")
    
    # 1. Run TabPFN Stage
    tabpfn_res = tabpfn_predictor.predict(req.ingredients, req.vessel_preference or "One Skillet")
    
    # 2. Run Gemma 2 Stage
    recipe = await gemma_synthesizer.generate_recipe(
        ingredients=req.ingredients,
        tabpfn=tabpfn_res,
        vessel=req.vessel_preference or "One Skillet",
        sloth_intensity=req.sloth_intensity or "Maximum"
    )
    return recipe

# Static SPA mounting for production / Render
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")
