import pytest
from immogab.services import search_properties

def test_search_properties_filter_province():
    results = search_properties(province="ESTUAIRE")
    assert len(results) == 3
    for prop in results:
        assert prop.province == "ESTUAIRE"

def test_search_properties_filter_type():
    results = search_properties(property_type="MAISON")
    assert len(results) == 1
    assert results[0].type == "MAISON"

def test_search_properties_filter_none():
    results = search_properties(query="NonExistent")
    assert len(results) == 0

def test_search_properties_all_filters():
    results = search_properties(province="ESTUAIRE", property_type="APPARTEMENT")
    assert len(results) == 1
    assert results[0].type == "APPARTEMENT"
    assert results[0].province == "ESTUAIRE"
