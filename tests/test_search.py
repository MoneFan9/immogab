import pytest
from immogab.services import search_properties

def test_search_by_query():
    results = search_properties(query="Villa")
    assert len(results) == 1
    assert results[0].title == "Villa Bord de Mer"

def test_search_by_province_match():
    results = search_properties(province="Estuaire")
    assert len(results) == 3
    for r in results:
        assert r.province == "Estuaire"

def test_search_by_province_no_match():
    results = search_properties(province="Woleu-Ntem")
    assert len(results) == 0

def test_search_by_type_match():
    results = search_properties(property_type="Appartement")
    assert len(results) == 1
    assert results[0].type == "Appartement"

def test_search_by_type_no_match():
    results = search_properties(property_type="Chambre")
    assert len(results) == 0

def test_search_combined_filters():
    results = search_properties(province="Ogooué-Maritime", property_type="Espace Événementiel")
    assert len(results) == 1
    assert results[0].location == "Port-Gentil"

def test_search_no_results():
    results = search_properties(query="Palais", province="Nyanga")
    assert len(results) == 0

def test_search_empty():
    results = search_properties()
    assert len(results) == 4
