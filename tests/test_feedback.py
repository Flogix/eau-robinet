"""Fixes after the user test of 20/10/2026: the home search shows a preview instead of leaving the page (2a), the towns
compared survive navigation (2d), the heatmap of missing values says so when a file has none (2g)."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def run_app(lang: str = "en") -> AppTest:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=180)
    at.session_state["lang"] = lang
    return at.run()


# --- 2a. Home: a preview, no automatic change of page ----------------------------------------------------------------
def test_home_search_never_switches_page():
    source = (ROOT / "sections" / "intro.py").read_text(encoding="utf-8")
    assert "switch_page" not in source


@pytest.mark.parametrize("lang, insee, expected, link", [
    ("en", "69123", "Lyon (69)", "See the full report"), ("fr", "69123", "Lyon (69)", "Voir le rapport complet"),
    ("en", "07173", "Péreyres (07)", "See the full report")])          # a town without score
def test_home_shows_a_preview_and_a_link_to_the_town_page(lang, insee, expected, link):
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
