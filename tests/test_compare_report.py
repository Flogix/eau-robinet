"""Comparison report (page "Town against town" and its PDF): rule-based texts shared by the page and the PDF, valid
PDFs in English and French for 2 to 6 towns, towns without score, overseas towns, file names."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from utils import compare_report as CR
from utils.i18n import forced_lang
from utils.io import communes, load_table
from utils.town_report import is_valid_pdf

PARIS, VILLEJUIF, LYON, MARSEILLE, BORDEAUX, LILLE = "75056", "94076", "69123", "13055", "33063", "59350"
PEREYRES, MAMOUDZOU, ABYMES = "07173", "97611", "97101"     # no score; Mayotte; Guadeloupe


def selection(insees):
    c = communes().set_index("insee").reindex(insees).reset_index()
    return c[c["score"].notna()].reset_index(drop=True)


@pytest.mark.parametrize("lang", ["en", "fr"])
@pytest.mark.parametrize("towns", [[PARIS, VILLEJUIF], [PARIS, LYON, MARSEILLE, BORDEAUX, LILLE, VILLEJUIF],
                                   [PARIS, PEREYRES, ABYMES, MAMOUDZOU]])
def test_pdf_is_valid_in_both_languages(towns, lang):
    data = CR.build_pdf(towns, lang)
    assert is_valid_pdf(data) and 20_000 < len(data) < 400_000


def test_pdf_with_fewer_than_two_scored_towns_still_works():
    assert is_valid_pdf(CR.build_pdf([PARIS, PEREYRES], "en"))


def test_town_without_score_is_set_aside():
    d = CR.gather([PARIS, PEREYRES, LYON])
    assert list(d["sel"]["insee"]) == [PARIS, LYON] and list(d["unscored"]["insee"]) == [PEREYRES]


def test_texts_come_from_the_data():
    sel = selection([PARIS, VILLEJUIF, LILLE])
    best, worst = sel.loc[sel["score"].idxmax()], sel.loc[sel["score"].idxmin()]
    with forced_lang("en"):
        head = CR.headline_text(sel)
        assert best["nom"] in head and worst["nom"] in head and f"{best['score']:.1f}" in head
        assert f"{best['score'] - worst['score']:.1f}" in head
        nat = float(communes()["score"].median())
        pos = CR.position_text(sel, nat)
        assert f"{nat:.1f}" in pos and all(n in pos for n in sel["nom"])
    with forced_lang("fr"):
        assert f"{best['score']:.1f}".replace(".", ",") in CR.headline_text(sel)


def test_why_text_names_the_causes_in_lower_case():
    cat = load_table("params_catalog")
    with forced_lang("fr"):
        why = CR.why_text(selection([PARIS, MARSEILLE]), dict(zip(cat["code"], cat["label"])))
    assert "À Paris : plomb" in why and "Plomb" not in why


def test_file_names():
    assert CR.file_name(["Paris", "Villejuif"], "en") == "tap-water-comparison-paris-villejuif-en.pdf"
    assert CR.file_name(["Paris", "Lyon", "Marseille", "Lille"], "fr") == \
        "comparaison-eau-paris-lyon-marseille-et-1-autre-fr.pdf"
    assert CR.file_name(["Paris", "Lyon", "Marseille", "Lille", "Sète"], "en") == \
        "tap-water-comparison-paris-lyon-marseille-and-2-more-en.pdf"


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_page_shows_the_same_text_and_offers_both_pdfs(lang):
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=180)
    at.session_state["lang"] = lang
    at.run()
    at.switch_page("sections/comparer.py").run()
    assert not at.exception
    sel = selection(at.session_state["cmp_sel"])
    cat = load_table("params_catalog")
    with forced_lang(lang):
        why = CR.why_text(sel, dict(zip(cat["code"], cat["label"])))
    assert any(why in m.value for m in at.markdown)            # the page and the PDF say the same thing
    keys = {b.key for b in at.get("download_button")}
    assert {"cmp_pdf_en", "cmp_pdf_fr"} <= keys
