import pytest
from app.services.tabpfn_service import tabpfn_predictor
from app.services.pantry_catalog import get_ingredient_profile

def test_ingredient_profile_lookup():
    item = get_ingredient_profile("ramen noodles")
    assert item.name == "ramen noodles"
    assert item.umami > 0
    assert "starch" in item.category

def test_unknown_ingredient_fallback():
    item = get_ingredient_profile("mysterious leftover tuber")
    assert item.umami > 0
    assert item.category == "misc"

def test_tabpfn_classic_ramen_pb_synergy():
    pred = tabpfn_predictor.predict(["Ramen noodles", "Peanut butter", "Sriracha", "Soy sauce"])
    assert pred.harmony_score >= 85.0
    assert pred.dish_count == 1
    assert pred.active_standing_minutes <= 4
    assert "TabPFN" in pred.model_version
    assert len(pred.pairing_synergies) > 0

def test_tabpfn_single_ingredient():
    pred = tabpfn_predictor.predict(["bread slices"])
    assert 40.0 <= pred.harmony_score <= 75.0
    assert pred.dish_count == 1

def test_tabpfn_flavor_balance_keys():
    pred = tabpfn_predictor.predict(["Kimchi", "Eggs", "Rice (cooked/leftover)"])
    assert "Umami" in pred.flavor_balance
    assert "Acidity" in pred.flavor_balance
    assert "Richness" in pred.flavor_balance
    assert "Saltiness" in pred.flavor_balance
