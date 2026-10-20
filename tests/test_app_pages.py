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
    from utils.town_search import town_matches
    labels = [lab for lab, _ in town_matches("Saint-Denis") if lab.startswith("Saint-Denis (")]
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
    at.session_state["insee"] = insee            # what the town search box sets when a town is chosen
    at.switch_page("sections/ma_commune.py").run()
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


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_footer_and_about_link_to_linkedin(lang):
    import config
    at = run_app(lang)
    at.switch_page("sections/about.py").run()
    footer = [m.value for m in at.markdown if m.value.startswith('<div class="ar-footer"')]
    assert footer and f'href="{config.AUTHOR_LINKEDIN}" target="_blank" rel="noopener noreferrer">Florian Giraud' in footer[0]
    assert any(b.proto.url == config.AUTHOR_LINKEDIN for b in at.get("link_button"))


# --- Filters: drawn only where they act, values kept across pages -------------------------------------------------
PAGE_FILES = {"": "intro", "reading": "comprendre", "town": "ma_commune", "compare": "comparer", "map": "overview",
              "monitor": "deep_dives", "my-score": "mon_score", "conclusions": "conclusions", "explore": "explore",
              "quality": "data_quality", "about": "about"}
FILTER_WIDGETS = {"years": "f_years", "region": "f_region_code", "ctype": "f_ctype"}
CHANGES = {"f_years": (2020, 2023), "f_region_code": "53", "f_ctype": "rural"}


def _signature(at: AppTest) -> str:
    parts = ([m.value for m in at.markdown] + [c.value for c in at.caption] + [str(x.proto) for x in at.get("metric")]
             + [str(x.proto) for x in at.get("plotly_chart")])
    return "".join(parts)


@pytest.mark.parametrize("url", list(PAGE_FILES))
def test_filters_are_drawn_exactly_where_they_act(url):
    from utils.filters import PAGE_FILTERS
    page = f"sections/{PAGE_FILES[url]}.py"
    at = run_app()
    at.switch_page(page).run()
    drawn = {k for k, key in FILTER_WIDGETS.items()
             if any(w.key == key for w in list(at.sidebar.slider) + list(at.sidebar.selectbox))}
    assert drawn == PAGE_FILTERS[url], (url, drawn)
    has_title = any(m.value == "**Filters**" for m in at.sidebar.markdown)
    assert has_title == bool(drawn), url
    hint = [m.value for m in at.main.markdown if 'class="ar-filter-hint"' in m.value]   # line at the top of the page
    assert bool(hint) == bool(drawn), url
    if hint:
        for name, word in (("years", "period"), ("region", "region"), ("ctype", "kind of town")):
            assert (word in hint[0]) == (name in drawn), (url, hint[0])
    base, acting = _signature(at), set()
    for name, key in FILTER_WIDGETS.items():          # measured: does the page change when the filter changes?
        at2 = run_app()
        at2.session_state[key] = CHANGES[key]
        at2.switch_page(page).run()
        assert not at2.exception, at2.exception
        if _signature(at2) != base:
            acting.add(name)
    assert acting == PAGE_FILTERS[url], (url, acting)


def test_filter_values_survive_a_page_without_filters():
    at = run_app()
    at.switch_page("sections/overview.py").run()
    at.slider(key="f_years").set_value((2019, 2022))
    at.selectbox(key="f_region_code").set_value("53")
    at.run()
    at.switch_page("sections/ma_commune.py").run()            # no filter drawn here
    assert not at.sidebar.slider and not any(m.value == "**Filters**" for m in at.sidebar.markdown)
    at.switch_page("sections/conclusions.py").run()
    at.switch_page("sections/overview.py").run()
    assert at.slider(key="f_years").value == (2019, 2022)
    assert at.selectbox(key="f_region_code").value == "53"


def test_region_filter_shows_all_of_france_by_default():
    at = run_app()
    at.switch_page("sections/overview.py").run()
    box = at.selectbox(key="f_region_code")
    assert box.value == "all" and box.index == 0 and box.options[0] == "All of France"


@pytest.mark.parametrize("lang, program, coord", [
    ("en", "Data & AI, DAI group", "<div>coordinator: MATHEW Mano Joseph</div>"),
    ("fr", "Data & AI, groupe DAI", "<div>coordinateur : MATHEW Mano Joseph</div>")])
def test_sidebar_starts_with_the_author_block_then_the_menu(lang, program, coord):
    import config
    at = run_app(lang)
    first = at.sidebar.markdown[0].value
    assert 'class="ar-side-head"' in first and "data:image/png;base64," in first and "Florian Giraud" in first
    assert program in first and coord in first and "<div>Data Analysis & Visualization</div>" in first
    assert 'class="ar-side-logo"' in first and "ar-side-plate" not in first      # no dark plate behind the logo
    assert f'href="{config.AUTHOR_LINKEDIN}" target="_blank"' in first
    assert f'href="{config.REPO_URL}" target="_blank"' in first
    links = [link.proto.page for link in at.sidebar.get("page_link")]
    assert len(links) == len(set(links)) == len(PAGE_FILES)          # every page in the menu, once


@pytest.mark.parametrize("name", ["efrei-logo-white.png", "efrei-logo-black.png"])
def test_efrei_logos_are_small_and_transparent(name):
    from PIL import Image
    path = ROOT / "assets" / name
    assert path.stat().st_size < 10_000
    im = Image.open(path).convert("RGBA")
    assert im.width == 400 and im.getpixel((0, 0))[3] == 0          # transparent background


def test_logo_follows_the_theme():
    from utils import viz
    assert viz.LOGO_EFREI["light"] != viz.LOGO_EFREI["dark"]
    assert viz.theme_type() == "light"                               # outside a browser: light by default


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_conclusions_come_second_and_link_to_the_evidence(lang):
    at = run_app(lang)
    menu = [link.proto.page for link in at.sidebar.get("page_link")]  # url paths, "" for the home page
    assert menu[:3] == ["", "conclusions", "reading"]
    at.switch_page("sections/conclusions.py").run()
    assert not at.exception
    in_page = [link.proto.page for link in at.main.get("page_link")]
    assert set(in_page[:6]) == {"reading", "town", "compare", "map", "monitor", "my-score"}
    assert in_page[6:] == ["map", "map", "monitor", "monitor"]                     # the evidence of H1 to H4
