"""Smoke test: every page of the app runs without exception."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(p.name for p in (ROOT / "sections").glob("*.py") if p.name != "__init__.py")


def test_app_entrypoint_runs():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception


@pytest.mark.parametrize("page", PAGES)
def test_page_runs(page):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    at.switch_page(f"sections/{page}").run()
    assert not at.exception, at.exception


# Edge cases of the sidebar filters: tiny overseas region, partial year alone, rare commune types.
COMBOS = [
    ("Mayotte", "pfas", "med", (2026, 2026)),
    ("Corse", "nitrates", "mountain", (2016, 2016)),
    ("Île-de-France", "comfort", "urban_dense", (2020, 2026)),
    ("Guyane", "metals", "rural", (2025, 2025)),
]


@pytest.mark.parametrize("region, variable, ctype, years", COMBOS)
def test_pages_with_extreme_filters(region, variable, ctype, years):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    at.selectbox(key="f_region").set_value(region)
    at.selectbox(key="f_variable").set_value(variable)
    at.selectbox(key="f_ctype").set_value(ctype)
    at.slider(key="f_years").set_value(years)
    at.run()
    assert not at.exception, at.exception
    for page in PAGES:
        at.switch_page(f"sections/{page}").run()
        assert not at.exception, (page, at.exception)


def test_town_page_with_homonyms_and_search():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    at.switch_page("sections/ma_commune.py").run()
    at.text_input(key="town_q").input("saint denis").run()
    assert not at.exception, at.exception
    labels = at.selectbox(key="town_pick").options
    assert len(labels) > 1 and all("(" in l for l in labels)   # homonyms shown with their department
