import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "TabPFN-3.5" in data["ai_engines"]["tabular_foundation_model"]
    assert "Gemma 2" in data["ai_engines"]["recipe_synthesizer"]

@pytest.mark.asyncio
async def test_pantry_presets():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/pantry/presets")
    assert response.status_code == 200
    presets = response.json()
    assert len(presets) >= 4
    assert any("Dan-Dan" in p["title"] or "Desperation" in p["title"] for p in presets)

@pytest.mark.asyncio
async def test_predict_harmony_api():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/predict/harmony", json={
            "ingredients": ["Eggs", "Kimchi", "Rice (cooked/leftover)", "Butter"],
            "vessel_preference": "One Skillet"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["harmony_score"] >= 80.0
    assert data["dish_count"] == 1

@pytest.mark.asyncio
async def test_generate_recipe_api():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/recipe/generate", json={
            "ingredients": ["Canned chickpeas", "Curry powder", "Coconut milk (canned)", "Frozen peas"],
            "vessel_preference": "One Skillet",
            "sloth_intensity": "Maximum"
        })
    assert response.status_code == 200
    recipe = response.json()
    assert recipe["dishes_to_wash"] == 1
    assert recipe["active_standing_minutes"] <= 5
    assert len(recipe["steps"]) >= 2
    assert "tabpfn_evidence" in recipe

@pytest.mark.asyncio
async def test_spa_root_serving():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert "SlothChef" in response.text


