"""Downloadable town report: a valid PDF in English and in French, accents embedded, numbers from the data only."""
import re
import zlib

import pandas as pd
import pytest

from utils import town_report as R
from utils.i18n import forced_lang, lang, t
from utils.io import commune_network_links, communes, network_history, read_processed


@pytest.fixture(scope="module")
def tables():
    return {"communes": communes(), "udi_scores": read_processed("udi_scores"), "links": commune_network_links(),
            "dim_udi": read_processed("dim_udi"), "udi_param_window": read_processed("udi_param_window"),
            "udi_family_window": read_processed("udi_family_window"),
            "udi_param_p95": read_processed("udi_param_p95"), "params_catalog": read_processed("params_catalog")}


def with_history(tables, insee):
    nets = tuple(tables["links"].loc[tables["links"]["insee"] == insee, "cdreseau"])
    return {**tables, "history": network_history(nets)}


def small_town(tables):
    d = tables["communes"]
    d = d[d["score"].notna() & (d["population"] < 300) & d["is_current"]]
    return d.sort_values("insee").iloc[0]["insee"]


def overseas_town(tables):
    d = tables["communes"]
    return d[d["score"].notna() & d["dep"].astype(str).str.startswith("97")].sort_values("insee").iloc[0]["insee"]


def pdf_text(data: bytes) -> str:
    """Rough text of the PDF content streams (enough to find the town name and the score)."""
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        try:
            out.append(zlib.decompress(m.group(1)).decode("latin-1"))
        except zlib.error:
            pass
    return "\n".join(out)


@pytest.mark.parametrize("language", ["en", "fr"])
@pytest.mark.parametrize("which", ["paris", "small", "overseas"])
def test_pdf_is_valid_in_both_languages(tables, language, which):
    insee = {"paris": "75056", "small": small_town(tables), "overseas": overseas_town(tables)}[which]
    data = R.build_pdf(insee, with_history(tables, insee), language)
    assert R.is_valid_pdf(data)
    assert 10_000 < len(data) < 2_000_000
    assert b"/FontFile2" in data            # TrueType fonts embedded: accents and µ, ≤, × are drawn


def test_pdf_metadata_and_fonts(tables):
    data = R.build_pdf("75056", with_history(tables, "75056"), "fr")
    assert b"IBMPlexSans" in data and b"Fraunces" in data   # identity of the app


def test_language_is_forced_then_restored():
    assert lang() == "en"
    with forced_lang("fr"):
        assert t("grade") == "Note"
    assert t("grade") == "Grade"


def test_paris_is_not_compared_with_its_own_department(tables):
    c = tables["communes"].set_index("insee").loc["75056"].copy()
    nets = tables["links"].loc[tables["links"]["insee"] == "75056", "cdreseau"]
    u = tables["udi_scores"].set_index("cdreseau").reindex(nets).dropna(subset=["score"])
    txt = R.explanation(c, u, tables["communes"], {})
    assert "department" not in txt and "national middle" in txt
    assert "mainly lead" in txt and "mainly Lead" not in txt
    assert not R.show_dep_median(c, tables["communes"])
    assert R.show_dep_median(tables["communes"].set_index("insee").loc["69123"], tables["communes"])
    with forced_lang("fr"):
        txt = R.explanation(c, u, tables["communes"], {})
        assert "département" not in txt and "en cause : plomb" in txt


def test_lower_name_keeps_acronyms():
    assert R.lower_name("Plomb") == "plomb"
    assert R.lower_name("Total des pesticides") == "total des pesticides"
    assert R.lower_name("Lead") == "lead" and R.lower_name("Chlorothalonil R471811") == "chlorothalonil R471811"
    for keep in ("PFAS (somme de 20)", "ESA-métolachlore", "E. coli", "pH", "NOA-métolachlore"):
        assert R.lower_name(keep) == keep


def test_explanation_uses_the_published_numbers(tables):
    c = tables["communes"].set_index("insee").loc["69123"].copy()   # Lyon: department with many towns
    nets = tables["links"].loc[tables["links"]["insee"] == "69123", "cdreseau"]
    u = tables["udi_scores"].set_index("cdreseau").reindex(nets).dropna(subset=["score"])
    txt = R.explanation(c, u, tables["communes"], {})
    loss = 100 - float(c["score"])
    assert f"{loss:.1f}" in txt
    nat, dep = R.medians(c, tables["communes"])
    assert f"{nat:.1f}" in txt and f"{dep:.1f}" in txt
    assert nat == pytest.approx(tables["communes"]["score"].median())
    with forced_lang("fr"):
        assert f"{loss:.1f}".replace(".", ",") in R.explanation(c, u, tables["communes"], {})


def test_explanation_of_a_perfect_town(tables):
    d = tables["communes"]
    c = d[(d["score"] >= 99.95)].iloc[0].copy()
    txt = R.explanation(c, pd.DataFrame(columns=["n_bact", "n_bact_nc"]), d, {})
    assert "maximum" in txt


def test_history_codes_put_key_parameters_first():
    h = pd.DataFrame({"code": ["TH", "ZZZ", "NO3", "ZZZ"], "n": [5, 50, 3, 50]})
    assert R.history_codes(h)[:2] == ["NO3", "TH"]
    assert R.history_codes(pd.DataFrame()) == []
    # the substance that costs the most points comes first; a single pesticide is followed through the total
    u = pd.DataFrame({"worst_chem_code": ["QMRC"], "worst_chem_penalty": [80.0]})
    h2 = pd.DataFrame({"code": ["NO3", "PESTOT"], "n": [9, 3]})
    assert R.history_codes(h2, u, {"QMRC"})[0] == "PESTOT"
    assert R.history_codes(h2, u, set())[0] == "NO3"            # not a pesticide: usual order
    u = pd.DataFrame({"worst_chem_code": ["PB"], "worst_chem_penalty": [20.0]})
    assert R.history_codes(pd.DataFrame({"code": ["NO3", "PB"], "n": [9, 1]}), u)[0] == "PB"


def test_markdown_is_cleaned_for_the_pdf():
    assert R._clean("a **b** *c* [d](http://x)") == "a **b** __c__ d (http://x)"
    assert "<" not in R._clean("x<br>y <b>z</b>")


def test_file_names():
    assert R.file_name("Saint-Étienne", "en") == "tap-water-report-saint-etienne-en.pdf"
    assert R.file_name("Saint-Étienne", "fr") == "rapport-eau-saint-etienne-fr.pdf"


def test_texts_have_no_em_dash():
    from utils.texts.myscore import T as T1
    from utils.texts.pdf import T as T2
    for entry in list(T1.values()) + list(T2.values()):
        for s in entry.values():
            assert chr(0x2014) not in s
