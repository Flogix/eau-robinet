# Regression and UX feedback tests: verifies search previews, state persistence, and missing data cues.
"""Fixes after the user test of 20/10/2026: the home search shows a preview instead of leaving the page (2a), the towns
compared survive navigation (2d), the heatmap of missing values says so when a file has none (2g)."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def run_app(lang: str = "en") -> AppTest:
    """Helper executing AppTest against app entrypoint in given language."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=180)
    at.session_state["lang"] = lang
    return at.run()


# --- 2a. Home: a preview, no automatic change of page ----------------------------------------------------------------
def test_home_search_never_switches_page():
    """Verify that home search box displays preview without navigating away."""
    source = (ROOT / "sections" / "intro.py").read_text(encoding="utf-8")
    assert "switch_page" not in source


@pytest.mark.parametrize("lang, insee, expected, link", [
    ("en", "69123", "Lyon (69)", "See the full report"), ("fr", "69123", "Lyon (69)", "Voir le rapport complet"),
    ("en", "07173", "Péreyres (07)", "See the full report")])          # a town without score
def test_home_shows_a_preview_and_a_link_to_the_town_page(lang, insee, expected, link):
    """Verify that home preview displays town grade, score, and link to town report."""
    from utils.io import communes
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=180)
    at.session_state["lang"] = lang
    at.session_state["home_insee"] = insee         # what choosing the town in the search box stores
    at.session_state["insee"] = insee
    at.run()
    assert not at.exception
    text = " ".join(m.value for m in at.main.markdown)
    assert expected in text and any(m.value.startswith('<div class="ar-kicker">') for m in at.main.markdown)
    c = communes().set_index("insee").loc[insee]
    if c["score"] == c["score"]:                    # scored town: score and grade in the preview
        score = f"{c['score']:.1f}" if lang == "en" else f"{c['score']:.1f}".replace(".", ",")
        assert f"{score}/100" in text and f'">{c["grade"]}</span>' in text
    links = [(x.proto.page, x.proto.label) for x in at.main.get("page_link")]
    assert ("town", link) in links
    assert at.session_state["insee"] == insee        # the town page will open on this town


# --- 2d. Town against town: the towns compared survive navigation ---------------------------------------------------
def test_towns_compared_survive_a_visit_to_other_pages():
    """Verify that selected towns in comparison view survive navigating across pages."""
    at = run_app()
    at.switch_page("sections/comparer.py").run()
    at.multiselect(key="cmp_sel").set_value(["69123", "13055"]).run()     # two of the options shown
    assert not at.exception
    for page in ("ma_commune", "overview", "conclusions"):          # pages without this widget
        at.switch_page(f"sections/{page}.py").run()
    at.switch_page("sections/comparer.py").run()
    assert at.multiselect(key="cmp_sel").value == ["69123", "13055"]
    assert at.query_params["towns"] in ("69123,13055", ["69123,13055"])


def test_towns_compared_can_come_from_the_link():
    """Verify that towns parameter in URL query string pre-populates comparison view."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=180)
    at.query_params["towns"] = "13055,59350,zzzzz"                  # an unknown code is ignored
    at.run()
    at.switch_page("sections/comparer.py").run()
    assert at.multiselect(key="cmp_sel").value == ["13055", "59350"]


# --- 2g. Behind the numbers: a file without missing values says so -------------------------------------------------
@pytest.mark.parametrize("lang, headline, caption", [
    ("en", "In the COM_UDI files, 0% of the cells are empty", "0% of empty cells in every column"),
    ("fr", "Dans les fichiers COM_UDI, 0 % de cases vides", "0 % de cases vides dans toutes les colonnes")])
def test_heatmap_of_a_complete_file_says_zero_percent(lang, headline, caption):
    """Verify that completeness heatmap announces zero percent missing for complete files."""
    import json
    at = run_app(lang)
    at.switch_page("sections/data_quality.py").run()
    at.button_group(key="dq_table").set_value("COM_UDI").run()
    assert not at.exception
    text = " ".join(m.value for m in at.main.markdown)
    captions = " ".join(c.value for c in at.main.caption)
    expected = headline.replace(" ", " ") if lang == "fr" else headline
    assert headline in text or expected in text
    assert caption in captions or caption.replace(" ", " ") in captions
    heat = json.loads(at.get("plotly_chart")[0].proto.spec)["data"][0]
    assert heat["type"] == "heatmap" and heat["texttemplate"] == "%{z:.0f}%"      # 0% written in each cell
    zero = heat["colorscale"][0][1]
    assert not zero.startswith("rgba") or float(zero.rstrip(")").split(",")[-1]) >= 0.1   # the zero colour is visible


def test_heatmap_of_a_file_with_gaps_names_the_emptiest_column():
    """Verify that completeness heatmap names the column with the highest missing share."""
    at = run_app()
    at.switch_page("sections/data_quality.py").run()
    at.button_group(key="dq_table").set_value("PLV").run()
    text = " ".join(m.value for m in at.main.markdown)
    assert "In the PLV files," in text and "columns are complete every year; the emptiest is" in text


# --- 3. The same count everywhere --------------------------------------------------------------------------------
def test_parameter_counts_explained():
    """All codes of the file (data dictionary: 1,276 in 2016, 1,405 in 2025) minus the codes with a text result give
    exactly the numeric parameters of the tables of figures (1,260 and 1,391)."""
    from utils.io import read_processed
    v = read_processed("explore_volume").set_index("annee")
    assert v.loc[2016, "n_params"] == 1276 and v.loc[2025, "n_params"] == 1405
    py = read_processed("param_year").groupby("annee")["code"].nunique()
    assert ((v["n_params"] - v["n_params_text"]) == py).all()
    ch = read_processed("explore_param_changes")
    new, gone = ch.loc[ch["change"] == "new", "n"].sum(), ch.loc[ch["change"] == "gone", "n"].sum()
    assert new - gone == 1405 - 1276


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_pages_use_the_same_counts(lang):
    """Verify that all pages reference identical sample and row counts for data consistency."""
    import re
    def page_text(page):
        """Helper concatenating all markdown and caption text blocks on a page."""
        at = run_app(lang)
        at.switch_page(f"sections/{page}.py").run()
        assert not at.exception
        return re.sub(r"<[^>]+>", " ", " ".join(m.value for m in at.main.markdown))
    sep = "," if lang == "en" else " "
    home, monitor, quality = page_text("intro"), page_text("deep_dives"), page_text("data_quality")
    assert "133 " in home and ("133 million results" in quality or "133 millions de résultats" in quality)
    assert f"1{sep}276" in monitor and f"1{sep}405" in monitor and f"1{sep}260" not in monitor
    assert "25,000" not in home and "25 000" not in home
    overview, mine = page_text("overview"), page_text("mon_score")
    assert f"34{sep}816" in overview and f"34{sep}826" not in mine
