"""Page "Explore the data": precomputed tables (consistent with the data dictionary and the other pages, no new raw
row in the repository) and the page itself (both languages, every control, fast reruns)."""
import json
import math
import re
import time
from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

import config
from utils.io import read_processed

ROOT = Path(__file__).resolve().parents[1]
RERUN_S = 1.5        # one rerun of the page after an interaction (measured 0.1 to 0.3 s on the dev laptop)
TABLES = ["explore_volume", "explore_fanout", "explore_links", "explore_samples_hist", "explore_lq",
          "explore_top_params", "explore_values", "explore_dept", "explore_spearman"]


@pytest.mark.parametrize("name", TABLES)
def test_explore_tables_exist_and_are_small(name):
    path = config.PROCESSED / f"{name}.parquet"
    assert path.exists() and path.stat().st_size < 200_000, name
    assert len(read_processed(name)) > 0


def test_volume_matches_the_data_dictionary():
    v = read_processed("explore_volume")
    assert list(v["annee"]) == config.YEARS
    assert v["samples"].sum() == 2_991_181 and v["result_rows"].sum() == 133_474_398   # data_dictionary.md section 3
    assert v["plv_rows"].sum() == 4_262_629


def test_spearman_matrix_is_consistent_with_the_other_pages():
    sp = read_processed("explore_spearman")
    m = sp.pivot(index="x", columns="y", values="rho")
    assert (abs(m.values.diagonal() - 1) < 1e-12).all() and (abs(m - m.T) < 1e-12).all().all()
    assert round(m.loc["bact_rate", "chem_rate"], 2) == 0.05          # H2, as on the map and in the conclusions
    # the map's sentence on small networks: median score of departments with >= 5 scored towns, 2016-2025
    assert round(m.loc["score_median", "small_share"], 2) == -0.14
    d = read_processed("explore_dept")
    assert len(d) == 96 and not d["dep"].str.startswith("97").any()
    paris = d.set_index("dep").loc["75"]
    assert pd.isna(paris["score_median"]) and 15_000 < paris["density"] < 25_000       # one town: no median


def test_examples_add_no_raw_row_to_the_repository():
    """The raw example rows are exactly those already printed in docs/data_dictionary.md (seed 42)."""
    ex = json.loads((config.PROCESSED / "explore_examples.json").read_text(encoding="utf-8"))
    md = (ROOT / "docs" / "data_dictionary.md").read_text(encoding="utf-8")
    for kind in ("PLV", "RESULT", "COM_UDI"):
        assert len(ex[kind]["rows"]) == 10
        for row in ex[kind]["rows"]:
            assert row[1] in md, (kind, row[1])
    assert set(ex["udi_year"]["columns"]) == set(read_processed("udi_year").columns)


def test_value_bins_add_up():
    v = read_processed("explore_values")
    for code, g in v.groupby("code"):
        assert g["n_networks"].sum() == g["n_total"].iloc[0], code
        assert g["p05"].iloc[0] <= g["p50"].iloc[0] <= g["p95"].iloc[0]


# --- the page ----------------------------------------------------------------------------------------------------
def run_page(lang: str) -> AppTest:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=180)
    at.session_state["lang"] = lang
    at.run()
    at.switch_page("sections/explore.py").run()
    assert not at.exception, at.exception
    return at


def timed(at: AppTest) -> float:
    t0 = time.perf_counter()
    at.run()
    assert not at.exception, at.exception
    return time.perf_counter() - t0


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_every_control_of_the_page_is_fast(lang):
    at = run_page(lang)
    times = []
    for table in ("RESULT", "COM_UDI", "udi_year", "PLV"):
        at.button_group(key="ex_rows").set_value(table)
        times.append(timed(at))
    for code in ("TH", "PB", "AS", "PESTOT", "SPFAS", "CL", "SO4", "NO3"):
        at.button_group(key="ex_val").set_value(code)
        times.append(timed(at))
    for x, y in (("density", "bact_rate"), ("population", "score_median"), ("hardness", "nitrates"),
                 ("chem_rate", "chem_rate")):
        at.selectbox(key="ex_x").set_value(x)
        at.selectbox(key="ex_y").set_value(y)
        times.append(timed(at))
    from utils.i18n import forced_lang, t
    with forced_lang(lang):
        assert any(t("ex.sc.same") in i.value for i in at.info)      # same indicator twice: a message, no chart
    assert max(times) < RERUN_S, times


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_page_texts_are_computed_and_clean(lang):
    at = run_page(lang)
    text = " ".join(m.value for m in at.markdown if not m.value.startswith("<style")) + " ".join(
        c.value for c in at.caption)
    assert chr(0x2014) not in text
    assert re.search(r"ρ = 0[.,]05", text) and re.search(r"ρ = −0[.,]14", text)
    assert "{" not in text                                                       # no placeholder left unfilled
    crit = 1.96 / math.sqrt(96 - 1)
    assert f"{crit:.2f}".replace(".", "," if lang == "fr" else ".") in text
