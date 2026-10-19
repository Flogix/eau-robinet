"""Parsing macros and parameter families, tested on synthetic values taken from formats seen in the data."""
import duckdb
import pytest

from utils.prep import classify_parameter, register_macros


@pytest.fixture(scope="module")
def con():
    c = duckdb.connect()
    register_macros(c)
    return c


def one(con, sql, *params):
    return con.execute(f"SELECT {sql}", list(params)).fetchone()[0]


@pytest.mark.parametrize("text, expected", [
    ("0,5", 0.5), ("0.5", 0.5), (" 12 ", 12.0), (",71", 0.71), ("11,", 11.0), ("-0,94573", -0.94573), ("abc", None),
])
def test_num_fr(con, text, expected):
    assert one(con, "num_fr(?)", text) == pytest.approx(expected) if expected is not None else one(con, "num_fr(?)", text) is None


@pytest.mark.parametrize("rq, qualit, vt, status, value, lq", [
    ("<0,005", "N", "0.000000", "not_quantified", 0.0, 0.005),
    ("< 0,1", "N", "0.000000", "not_quantified", 0.0, 0.1),
    ("<0.020", "N", "0.000000", "not_quantified", 0.0, 0.02),
    ("11,00", "N", "11.000000", "quantified", 11.0, None),
    ("560", "N", "560.000000", "quantified", 560.0, None),
    (">300", "N", "300.000000", "above", 300.0, None),
    ("N.M.", "N", None, "not_measured", None, None),
    (None, "N", None, "missing", None, None),
    ("ILLISIBL", "N", None, "unreadable", None, None),
    ("N.D.", "N", "0.000000", "not_quantified", 0.0, None),
    ("TRACES", "N", "0.000000", "not_quantified", 0.0, None),
    ("<SEUIL", "N", "0.000000", "not_quantified", 0.0, None),
    ("INCOMPT.", "N", "1.110000", "uncountable", None, None),
    ("PRESENCE", "N", "1.000000", "present", 1.0, None),
    ("Aspect normal", "O", "0.000000", "qualitative", None, None),
    ("?", "N", None, "other", None, None),
])
def test_result_parsing(con, rq, qualit, vt, status, value, lq):
    assert one(con, "rq_status(?, ?)", rq, qualit) == status
    got = one(con, "rq_value(?, ?, ?)", rq, qualit, vt)
    assert got == pytest.approx(value) if value is not None else got is None
    got_lq = one(con, "rq_lq(?, ?)", rq, qualit)
    assert got_lq == pytest.approx(lq) if lq is not None else got_lq is None


@pytest.mark.parametrize("text, tmin, tmax, unit", [
    ("<=0,1 µg/L", None, 0.1, "µg/L"),
    ("<=0.5 µg/L", None, 0.5, "µg/L"),
    ("<=50 mg/L", None, 50.0, "mg/L"),
    ("<=0 n/(100mL)", None, 0.0, "n/(100mL)"),
    (">=6,5 et <=9 unité pH", 6.5, 9.0, "unité pH"),
    (">=200 et <=1100 µS/cm", 200.0, 1100.0, "µS/cm"),
    ("<=20 µg(Se)/L", None, 20.0, "µg(Se)/L"),
    (None, None, None, None),
])
def test_threshold_parsing(con, text, tmin, tmax, unit):
    got_min, got_max, got_unit = con.execute("SELECT thr_min(?), thr_max(?), thr_unit(?)", [text] * 3).fetchone()
    assert (got_min is None) if tmin is None else got_min == pytest.approx(tmin)
    assert (got_max is None) if tmax is None else got_max == pytest.approx(tmax)
    assert got_unit == unit


@pytest.mark.parametrize("unit, expected", [
    ("mg(Mg)/L", "mg/L"), ("µg(Se)/L", "µg/L"), ("mg(Cl2)/L", "mg/L"), ("n/(100mL)", "n/(100mL)"), ("µg/L", "µg/L"),
])
def test_unit_norm(con, unit, expected):
    assert one(con, "unit_norm(?)", unit) == expected


@pytest.mark.parametrize("args, expected", [
    (("ECOLI", "n/(100mL)", True, False, 0.0, "n/(100mL)"), ("micro", "bacteria")),
    (("NO3", "mg/L", True, False, 50.0, "mg/L"), ("chem", "nitrates")),
    (("ATRZ", "µg/L", True, False, 0.1, "µg/L"), ("chem", "pesticides")),
    (("MCPA", "µg/L", True, False, 0.1, "µg/L"), ("chem", "pesticides")),
    (("EPICL", "µg/L", True, False, 0.1, "µg/L"), ("chem", "other_chemicals")),
    (("SPFAS", "µg/L", True, False, 0.1, "µg/L"), ("chem", "pfas")),
    (("PB", "µg/L", True, False, 10.0, "µg/L"), ("chem", "metals")),
    (("MCLR", "µg/L", True, False, 1.0, "µg/L"), ("chem", "cyanotoxins")),
    (("MTCESA", "µg/L", False, False, None, None), ("comfort", "pesticide_metabolite_non_relevant")),
    (("ESAMTC", "µg/L", True, False, 0.1, "µg/L"), ("comfort", "pesticide_metabolite_non_relevant")),
    (("CTF", "n/(100mL)", False, True, None, None), ("comfort", "bacteria_indicators")),
    (("FET", "µg/L", False, True, None, None), ("comfort", "indicators")),
    (("TURBNFU", "NFU", True, True, 1.0, "NFU"), ("comfort", "turbidity")),
    (("TH", "°f", False, False, None, None), ("info", "hardness")),
    (("CL2LIB", "mg(Cl2)/L", False, False, None, None), ("info", "no_threshold")),
])
def test_classify_parameter(args, expected):
    assert classify_parameter(*args) == expected


@pytest.mark.parametrize("lim_max, nonrel, ref_min, ref_max, expected", [
    (0.1, False, None, None, "limit"),
    (0.1, True, None, None, "limit"),          # a row that still carries a limit keeps it
    (None, True, None, None, "indicative"),    # non-relevant metabolite without limit -> 0.9 µg/L
    (None, False, 6.5, 9.0, "reference"),
    (None, False, None, None, None),
])
def test_thr_kind(con, lim_max, nonrel, ref_min, ref_max, expected):
    assert one(con, "thr_kind(?::DOUBLE, ?::BOOLEAN, ?::DOUBLE, ?::DOUBLE)", lim_max, nonrel, ref_min, ref_max) == expected


@pytest.mark.parametrize("status, value, kind, tmax, tmin, expected", [
    ("quantified", 38.0, "limit", 50.0, None, False),     # nitrates 38 mg/L under 50
    ("quantified", 50.0, "limit", 50.0, None, False),     # "<=50": equal is conform
    ("quantified", 51.0, "limit", 50.0, None, True),
    ("quantified", 3.0, "limit", 0.0, None, True),        # E. coli 3/100 mL, limit 0
    ("not_quantified", 0.0, "limit", 0.0, None, False),   # "<1" bacteria
    ("uncountable", None, "limit", 0.0, None, True),      # INCOMPT.
    ("quantified", 1.2, "indicative", 0.9, None, True),   # non-relevant metabolite above 0.9 µg/L
    ("quantified", 0.5, "indicative", 0.9, None, False),
    ("quantified", 6.2, "reference", 9.0, 6.5, True),     # pH below the interval
    ("not_quantified", 0.0, "reference", 1100.0, 200.0, False),  # "<LQ" is not "below the minimum"
    ("not_measured", None, "limit", 0.1, None, False),
])
def test_is_exceed(con, status, value, kind, tmax, tmin, expected):
    assert one(con, "is_exceed(?, ?::DOUBLE, ?, ?::DOUBLE, ?::DOUBLE)", status, value, kind, tmax, tmin) is expected


@pytest.mark.parametrize("status, value, expected", [
    ("quantified", 0.02, True), ("quantified", 0.0, False), ("not_quantified", 0.0, False),
    ("present", 1.0, True), ("not_measured", None, False),
])
def test_is_detected(con, status, value, expected):
    assert one(con, "is_detected(?, ?::DOUBLE)", status, value) is expected
