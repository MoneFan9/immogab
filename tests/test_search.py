import pytest
from immogab.services import search_properties

def test_search_by_query_title():
    results = search_properties(query="Villa")
    assert len(results) >= 1
    assert all("Villa" in p.title for p in results)

def test_search_by_query_location():
    results = search_properties(query="Libreville")
    assert len(results) >= 1
    assert all("Libreville" in p.location for p in results)

def test_search_by_province():
    results = search_properties(province="Estuaire")
    assert len(results) >= 1
    assert all(p.province == "Estuaire" for p in results)

def test_search_by_property_type():
    results = search_properties(property_type="Maison")
    assert len(results) >= 1
    assert all(p.type == "Maison" for p in results)

def test_search_by_all_filters():
    results = search_properties(query="Villa", province="Estuaire", property_type="Maison")
    assert len(results) == 1
    assert results[0].title == "Villa Bord de Mer"

def test_search_no_results():
    results = search_properties(query="NonExistent")
    assert len(results) == 0

def test_search_by_province_no_match():
    results = search_properties(province="Ogooué-Lolo")
    assert len(results) == 0

def test_search_by_type_no_match():
    results = search_properties(property_type="Chambre")
    assert len(results) == 0
