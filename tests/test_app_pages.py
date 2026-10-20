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
    at.selectbox(key="f_ctype").set_value(ctype)
    at.slider(key="f_years").set_value(years)
    at.run()
    at.selectbox(key="map_view").set_value(variable)
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


def test_my_score_changes_and_resets():
    at = run_app()
    at.switch_page("sections/mon_score.py").run()
    assert not at.exception
    official = {m.label: m.value for m in at.metric}
    assert official["Official score"] == official["Your score"]
    at.select_slider(key="my_sev_pesticides").set_value(3.0)
    at.slider(key="my_thr_NO3").set_value(20.0)
    at.slider(key="my_w_comfort").set_value(0.0)
    at.run()
    assert not at.exception
    changed = {m.label: m.value for m in at.metric}
    assert changed["Your score"] != changed["Official score"]
    assert changed["Towns changing grade"] != "0%"
    at.button[0].click().run()                    # back to the official settings
    assert at.session_state["my_thr_NO3"] == 50.0 and at.session_state["my_sev_pesticides"] == 1.0
    assert {m.label: m.value for m in at.metric} == official


@pytest.mark.parametrize("insee", ["75056", "97411", "01001"])   # Paris, Saint-Denis (Réunion), a small town
def test_town_page_offers_the_pdf_in_both_languages(insee):
    at = run_app()
    at.switch_page("sections/ma_commune.py").run()
    at.selectbox(key="town_pick").set_value(insee).run()
    assert not at.exception
    buttons = at.get("download_button")
    assert len(buttons) == 2


@pytest.mark.parametrize("lang, label", [("en", "What the map shows"), ("fr", "Ce que montre la carte")])
def test_map_variable_selection_is_in_the_sidebar(lang, label):
    at = run_app(lang)
    at.switch_page("sections/overview.py").run()
    assert not at.exception
    sidebar_keys = [s.key for s in at.sidebar.selectbox]
    assert "map_view" in sidebar_keys
    assert at.selectbox(key="map_view").label == label
    at.selectbox(key="map_view").set_value("nitrates").run()
    assert not at.exception
    at.switch_page("sections/intro.py").run()     # other pages: no map selector in the sidebar
    assert "map_view" not in [s.key for s in at.sidebar.selectbox]


def test_license_file():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert text.startswith("MIT License") and "2026 Florian Giraud" in text
