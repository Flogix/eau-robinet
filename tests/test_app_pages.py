"""Smoke tests: every page runs without exception, in English and in French, with default and extreme filters."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(p.name for p in (ROOT / "sections").glob("*.py") if p.name != "__init__.py")


def run_app(lang: str = "en") -> AppTest:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120)
    at.session_state["lang"] = lang
    return at.run()


def test_app_entrypoint_runs():
    at = run_app()
    assert not at.exception


@pytest.mark.parametrize("lang", ["en", "fr"])
@pytest.mark.parametrize("page", PAGES)
def test_page_runs(page, lang):
    at = run_app(lang)
    at.switch_page(f"sections/{page}").run()
    assert not at.exception, at.exception
    text = " ".join(m.value for m in at.markdown) + " ".join(c.value for c in at.caption)
    assert chr(0x2014) not in text, f"em dash on {page} ({lang})"


# Edge cases of the sidebar filters: tiny overseas region, partial year alone, rare kinds of towns.
COMBOS = [
    ("06", "pfas", "med", (2026, 2026)),          # Mayotte
    ("94", "nitrates", "mountain", (2016, 2016)),  # Corse
    ("11", "comfort", "urban_dense", (2020, 2026)),  # Île-de-France
    ("03", "metals", "rural", (2025, 2025)),       # Guyane
]


@pytest.mark.parametrize("region, variable, ctype, years", COMBOS)
def test_pages_with_extreme_filters(region, variable, ctype, years):
    at = run_app()
    at.switch_page("sections/overview.py").run()   # the map page enables every filter
    at.selectbox(key="f_region_code").set_value(region)
    at.selectbox(key="f_variable").set_value(variable)
    at.selectbox(key="f_ctype").set_value(ctype)
    at.slider(key="f_years").set_value(years)
    at.run()
    assert not at.exception, at.exception
    for page in PAGES:
        at.switch_page(f"sections/{page}").run()
        assert not at.exception, (page, at.exception)


def test_town_search_tells_homonyms_apart():
    at = run_app()
    at.switch_page("sections/ma_commune.py").run()
    labels = [o for o in at.selectbox(key="town_pick").options if o.startswith("Saint-Denis (")]
    assert len(labels) > 1   # homonyms shown with their department


def test_compare_defaults_to_five_cities():
    at = run_app()
    at.switch_page("sections/comparer.py").run()
    assert at.multiselect(key="cmp_sel").value == ["75056", "69123", "13055", "33063", "59350"]
