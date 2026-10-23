# Integration smoke tests: validates that every page and filter combination renders cleanly.
"""Smoke tests: every page runs without exception, in English and in French, with default and extreme filters."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(p.name for p in (ROOT / "sections").glob("*.py") if p.name != "__init__.py")


def run_app(lang: str = "en") -> AppTest:
    """Initialize and run Streamlit AppTest instance with chosen language."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120)
    at.session_state["lang"] = lang
    return at.run()


def test_app_entrypoint_runs():
    """Verify that main app entrypoint initializes without unhandled exceptions."""
    at = run_app()
    assert not at.exception


@pytest.mark.parametrize("lang", ["en", "fr"])
@pytest.mark.parametrize("page", PAGES)
def test_page_runs(page, lang):
    """Verify that each page renders without errors and contains no illegal em-dashes."""
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
    """Verify that all pages handle boundary filter combinations cleanly."""
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
    """Verify that homonymous towns are distinguished by department suffix."""
    from utils.town_search import town_matches
    labels = [lab for lab, _ in town_matches("Saint-Denis") if lab.startswith("Saint-Denis (")]
    assert len(labels) > 1   # homonyms shown with their department


def test_compare_defaults_to_five_cities():
    """Verify that town comparison page defaults to 5 example cities."""
    at = run_app()
    at.switch_page("sections/comparer.py").run()
    assert at.multiselect(key="cmp_sel").value == ["75056", "69123", "13055", "33063", "59350"]


def test_my_score_changes_and_resets():
    """Verify that interactive score sliders recompute scores and reset properly."""
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
    """Verify that commune detail page exposes PDF download buttons for EN and FR."""
    at = run_app()
    at.session_state["insee"] = insee            # what the town search box sets when a town is chosen
    at.switch_page("sections/ma_commune.py").run()
    assert not at.exception
    buttons = at.get("download_button")
    assert len(buttons) == 2


@pytest.mark.parametrize("lang, label", [("en", "What the map shows"), ("fr", "Ce que montre la carte")])
def test_map_variable_selection_is_in_the_sidebar(lang, label):
    """Verify that map variable selector appears inside sidebar container."""
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
    """Verify that LICENSE file exists and conforms to standard MIT terms."""
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert text.startswith("MIT License") and "2026 Florian Giraud" in text


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_footer_and_about_link_to_linkedin(lang):
    """Verify that footer and about page contain author LinkedIn profile link."""
    import config
    at = run_app(lang)
    at.switch_page("sections/about.py").run()
    footer = [m.value for m in at.markdown if m.value.startswith('<div class="ar-footer"')]
    assert footer and f'href="{config.AUTHOR_LINKEDIN}" target="_blank" rel="noopener noreferrer">Florian Giraud' in footer[0]
    assert any(b.proto.url == config.AUTHOR_LINKEDIN for b in at.get("link_button"))


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_about_page_has_both_dataset_buttons(lang):
    """Verify that About page has both data.gouv.fr link and processed ZIP download."""
    import config
    from utils.io import get_processed_data_size_mb
    at = run_app(lang)
    at.switch_page("sections/about.py").run()
    assert not at.exception
    # Check data.gouv.fr link button
    links = [b.proto.url for b in at.get("link_button")]
    assert config.DATASET_PAGE in links
    # Check processed data download button
    dl_buttons = at.get("download_button")
    assert len(dl_buttons) >= 1
    dl = dl_buttons[0]
    assert dl.key == "about_download_zip"
    expected_size = str(get_processed_data_size_mb())
    assert expected_size in dl.proto.label
    unit = "MB" if lang == "en" else "Mo"
    assert unit in dl.proto.label


# --- Filters: drawn only where they act, values kept across pages -------------------------------------------------
PAGE_FILES = {"": "intro", "reading": "comprendre", "town": "ma_commune", "compare": "comparer", "map": "overview",
              "monitor": "deep_dives", "my-score": "mon_score", "conclusions": "conclusions", "explore": "explore",
              "quality": "data_quality", "about": "about"}
FILTER_WIDGETS = {"years": "f_years", "region": "f_region_code", "ctype": "f_ctype"}
CHANGES = {"f_years": (2020, 2023), "f_region_code": "53", "f_ctype": "rural"}


def _signature(at: AppTest) -> str:
    """Extract element types and order signature for rendered page."""
    parts = ([m.value for m in at.markdown] + [c.value for c in at.caption] + [str(x.proto) for x in at.get("metric")]
             + [str(x.proto) for x in at.get("plotly_chart")])
    return "".join(parts)


@pytest.mark.parametrize("url", list(PAGE_FILES))
def test_filters_are_drawn_exactly_where_they_act(url):
    """Verify that filter controls are rendered only on pages where they operate."""
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
    """Verify that active filter states persist across navigation to filterless pages."""
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
    """Verify that regional filter defaults to all of France without blank state."""
    at = run_app()
    at.switch_page("sections/overview.py").run()
    box = at.selectbox(key="f_region_code")
    assert box.value == "all" and box.index == 0 and box.options[0] == "All of France"


@pytest.mark.parametrize("lang, program, coord, proposed", [
    ("en", "Data & AI, DAI group 2026", "<div>Coordinator: MATHEW Mano Joseph</div>",
     '<div>Project Proposed by <a href="mailto:mano.mathew@efrei.fr">mano.mathew@efrei.fr</a></div>'),
    ("fr", "Data & AI, groupe DAI 2026", "<div>Coordinateur : MATHEW Mano Joseph</div>",
     '<div>Projet proposé par <a href="mailto:mano.mathew@efrei.fr">mano.mathew@efrei.fr</a></div>')])
def test_sidebar_starts_with_the_author_block_then_the_menu(lang, program, coord, proposed):
    """Verify that custom sidebar header places author metadata above navigation."""
    import config
    at = run_app(lang)
    first = at.sidebar.markdown[0].value
    assert 'class="ar-side-head"' in first and "data:image/png;base64," in first and "Florian Giraud" in first
    assert program in first and coord in first and proposed in first and "<div>Data Analysis & Visualization</div>" in first
    assert '<a href="mailto:florian.giraud@efrei.net">florian.giraud@efrei.net</a>' in first
    assert 'class="ar-side-logo"' in first and "ar-side-plate" not in first      # no dark plate behind the logo
    assert f'href="{config.AUTHOR_LINKEDIN}" target="_blank"' in first
    assert f'href="{config.REPO_URL}" target="_blank"' in first
    links = [link.proto.page for link in at.sidebar.get("page_link")]
    assert len(links) == len(set(links)) == len(PAGE_FILES)          # every page in the menu, once


@pytest.mark.parametrize("lang, expected_lines", [
    ("en", [
        "Florian Giraud",
        "Data & AI, DAI group 2026",
        '<a href="mailto:florian.giraud@efrei.net">florian.giraud@efrei.net</a>',
        "LinkedIn", "GitHub",
        "Data Analysis & Visualization",
        "Coordinator: MATHEW Mano Joseph",
        'Project Proposed by <a href="mailto:mano.mathew@efrei.fr">mano.mathew@efrei.fr</a>',
    ]),
    ("fr", [
        "Florian Giraud",
        "Data & AI, groupe DAI 2026",
        '<a href="mailto:florian.giraud@efrei.net">florian.giraud@efrei.net</a>',
        "LinkedIn", "GitHub",
        "Data Analysis & Visualization",
        "Coordinateur : MATHEW Mano Joseph",
        'Projet proposé par <a href="mailto:mano.mathew@efrei.fr">mano.mathew@efrei.fr</a>',
    ]),
])
def test_sidebar_header_lines_order_and_links(lang, expected_lines):
    """Verify exact ordering of sidebar header metadata and mailto links."""
    at = run_app(lang)
    html = at.sidebar.markdown[0].value
    last_idx = -1
    for token in expected_lines:
        idx = html.find(token)
        assert idx != -1, f"Missing token {token!r} in {lang} sidebar"
        assert idx > last_idx, f"Token {token!r} appears out of order in {lang} sidebar"
        last_idx = idx


@pytest.mark.parametrize("name", ["efrei-logo-black.png"])
def test_efrei_logos_are_small_and_transparent(name):
    """Verify dimensions and file sizes of bundled school logo assets."""
    from PIL import Image
    path = ROOT / "assets" / name
    assert path.stat().st_size < 10_000
    im = Image.open(path).convert("RGBA")
    assert im.width == 400 and im.getpixel((0, 0))[3] == 0          # transparent background


def test_logo_follows_the_theme_in_css():
    """The logo is the shape of the PNG used as a mask, painted by light-dark(): black on the light theme, white on the
    dark one, switched by the browser as soon as Streamlit changes the theme (no rerun). Checked in Chrome by
    tests/test_performance.py style browser test below when Playwright is installed."""
    from utils import viz
    assert "background-color:light-dark(#000000, #FFFFFF)" in viz.CSS and "mask-size:contain" in viz.CSS
    at = run_app()
    head = at.sidebar.markdown[0].value
    assert 'role="img"' in head and f"mask-image:url({viz.LOGO_MASK})" in head


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_conclusions_come_second_and_link_to_the_evidence(lang):
    """Verify that conclusions page is second in menu and links to all evidence."""
    at = run_app(lang)
    menu = [link.proto.page for link in at.sidebar.get("page_link")]  # url paths, "" for the home page
    assert menu[:3] == ["", "conclusions", "reading"]
    at.switch_page("sections/conclusions.py").run()
    assert not at.exception
    in_page = [link.proto.page for link in at.main.get("page_link")]
    assert set(in_page[:6]) == {"reading", "town", "compare", "map", "monitor", "my-score"}
    assert in_page[6:] == ["map", "map", "monitor", "monitor"]                     # the evidence of H1 to H4
