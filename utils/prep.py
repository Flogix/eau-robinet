# Data transformation rules, DuckDB SQL parsing macros, and parameter classification logic.
"""Cleaning rules shared by the pipeline and the tests.

Parsing is written as DuckDB SQL macros (the RESULT table has 133 million rows, so it is never
loaded into pandas). `register_macros(con)` installs them on a connection; the unit tests run the
same macros on small synthetic tables.

Parameter families (Python, applied to the ~1,800-row parameter catalogue):
  micro  , microbiology with a quality limit (E. coli, enterococci)
  chem   , health-related chemistry with a quality limit (nitrates, pesticides, PFAS, metals, ...)
  comfort, indicators / comfort with a quality reference (turbidity, coliform bacteria, iron, ...)
            + pesticide metabolites classified "non-relevant" (0.9 µg/L indicative value)
  info   , no threshold, information only (hardness, calcium, temperature, ...)
"""
from __future__ import annotations

import config

# --- SQL macros -------------------------------------------------------------------------
MACROS = r"""
-- French or English decimal text -> DOUBLE ("0,5", "0.5", " 1 ", ",71", "11,")
CREATE OR REPLACE MACRO num_fr(s) AS try_cast(replace(replace(trim(s), ' ', ''), ',', '.') AS DOUBLE);

-- Status of a raw result (rqana); qualitative parameters are kept apart
CREATE OR REPLACE MACRO rq_status(rq, qualit) AS CASE
    WHEN qualit = 'O' THEN 'qualitative'
    WHEN rq IS NULL OR trim(rq) = '' THEN 'missing'
    WHEN upper(trim(rq)) IN ('N.M.', 'N.M') THEN 'not_measured'
    WHEN upper(trim(rq)) LIKE 'ILLIS%' THEN 'unreadable'
    WHEN upper(trim(rq)) IN ('<SEUIL', 'N.D.', 'TRACES') THEN 'not_quantified'
    WHEN upper(trim(rq)) = 'INCOMPT.' THEN 'uncountable'
    WHEN upper(trim(rq)) = 'PRESENCE' THEN 'present'
    WHEN trim(rq) LIKE '<%' AND num_fr(ltrim(trim(rq), '<')) IS NOT NULL THEN 'not_quantified'
    WHEN trim(rq) LIKE '>%' AND num_fr(ltrim(trim(rq), '>')) IS NOT NULL THEN 'above'
    WHEN num_fr(rq) IS NOT NULL THEN 'quantified'
    ELSE 'other' END;

-- Numeric value used for exceedances: the producer's translation (valtraduite), 0 when not quantified
CREATE OR REPLACE MACRO rq_value(rq, qualit, vt) AS CASE rq_status(rq, qualit)
    WHEN 'quantified' THEN coalesce(try_cast(vt AS DOUBLE), num_fr(rq))
    WHEN 'above' THEN coalesce(try_cast(vt AS DOUBLE), num_fr(ltrim(trim(rq), '>')))
    WHEN 'not_quantified' THEN 0.0
    WHEN 'present' THEN 1.0
    ELSE NULL END;

-- Limit of quantification when the result is "<x"
CREATE OR REPLACE MACRO rq_lq(rq, qualit) AS CASE
    WHEN rq_status(rq, qualit) = 'not_quantified' AND trim(rq) LIKE '<%' THEN num_fr(ltrim(trim(rq), '<'))
    END;

-- Thresholds written like "<=0,1 µg/L" or ">=6,5 et <=9 unité pH"
CREATE OR REPLACE MACRO thr_max(s) AS num_fr(nullif(regexp_extract(s, '<=\s*(-?[0-9]*[.,]?[0-9]+)', 1), ''));
CREATE OR REPLACE MACRO thr_min(s) AS num_fr(nullif(regexp_extract(s, '>=\s*(-?[0-9]*[.,]?[0-9]+)', 1), ''));
CREATE OR REPLACE MACRO thr_unit(s) AS nullif(trim(regexp_extract(s, '<=\s*-?[0-9]*[.,]?[0-9]+\s+(.*)$', 1)), '');

-- Equivalent unit spellings: "mg(Mg)/L" == "mg/L", "µg(Se)/L" == "µg/L"
CREATE OR REPLACE MACRO unit_norm(u) AS regexp_replace(trim(u), '^(mg|µg|ng)\([A-Za-z0-9]+\)/L$', '\1/L');

-- Which threshold applies to a result row: the limit written on the row; else, for a metabolite classified
-- non-relevant by Anses, the 0.9 µg/L indicative value; else the quality reference written on the row.
CREATE OR REPLACE MACRO thr_kind(lim_max, non_relevant, ref_min, ref_max) AS CASE
    WHEN lim_max IS NOT NULL THEN 'limit'
    WHEN non_relevant THEN 'indicative'
    WHEN ref_max IS NOT NULL OR ref_min IS NOT NULL THEN 'reference' END;

-- Exceedance: above the maximum, below the minimum of an interval (pH...), or "uncountable" bacteria
CREATE OR REPLACE MACRO is_exceed(status, value, kind, tmax, tmin) AS
    coalesce((status = 'uncountable' AND kind IS NOT NULL)
             OR (value IS NOT NULL AND tmax IS NOT NULL AND value > tmax)
             OR (status = 'quantified' AND tmin IS NOT NULL AND value < tmin), false);

-- Detected = quantified above zero (a "<LQ" result is not a detection)
CREATE OR REPLACE MACRO is_detected(status, value) AS
    coalesce((status IN ('quantified', 'above') AND value > 0) OR status IN ('present', 'uncountable'), false);
"""

# Units that are not concentrations: thresholds expressed with them are ignored.
EXCLUDED_THRESHOLD_UNITS = ("NG/(KG POIDS CORPOREL/J)",)


def register_macros(con) -> None:
    """Install the parsing macros on a DuckDB connection."""
    con.execute(MACROS)


# --- Parameter families ------------------------------------------------------------------
MICRO_UNITS = {"n/(100mL)", "NPP/100mL", "n/(250mL)"}

NITRATE_CODES = {"NO3", "NO2", "NO3_NO2"}
PFAS_SUM_CODES = {"SPFAS"}
METAL_CODES = {"AS", "CD", "CRT", "CR6", "SB", "SE", "SECL", "HG", "PB", "PBD", "NI", "CU", "CUD", "URAN"}
DBP_CODES = {"THM4", "CLF", "BRF", "DCLMBR", "DBRMCL", "BRATE", "CLITEMG", "CLITE_T", "CLATE", "CLATE_T", "AHA_S1"}
PESTICIDE_TOTAL_CODES = {"PESTOT", "ATRZMET", "TBZMETA"}
# Limit of 0.1 µg/L but not pesticides (materials, hydrocarbons, PFAS sum)
NOT_PESTICIDE_01 = {"ACRYL", "EPICL", "BKFLUO", "BGPERY", "BBFLUO", "HPAT4", "SPFAS"}

# Explicit project choices (decisions in docs/AVANCEMENT.md, phase 2)
FAMILY_OVERRIDES = {
    "TURBNFU": ("comfort", "turbidity"),       # has a limit at the plant outlet, but is an operating indicator
    "TEAU": ("info", "temperature"),
    "TEMP_PH": ("info", "temperature"),
    "TH": ("info", "hardness"),
    "TAC": ("info", "hardness"),
    "TA": ("info", "hardness"),
    "CA": ("info", "minerals"),
    "MG": ("info", "minerals"),
}


def classify_parameter(code: str, unit: str | None, has_limit: bool, has_ref: bool,
                       limit_max: float | None, limit_unit: str | None) -> tuple[str, str]:
    """Return (family, subfamily) for one parameter of the catalogue."""
    if code in config.NON_RELEVANT_METABOLITES:
        return "comfort", "pesticide_metabolite_non_relevant"
    if code in FAMILY_OVERRIDES:
        return FAMILY_OVERRIDES[code]
    unit = unit or ""
    if has_limit:
        if unit in MICRO_UNITS or (limit_unit or "") in MICRO_UNITS:
            return "micro", "bacteria"
        if code in NITRATE_CODES:
            return "chem", "nitrates"
        if code in PFAS_SUM_CODES:
            return "chem", "pfas"
        if code in METAL_CODES:
            return "chem", "metals"
        if code in DBP_CODES:
            return "chem", "disinfection_byproducts"
        if code.startswith("MC") and limit_max == 1.0:  # microcystins (cyanobacteria toxins), limit 1 µg/L
            return "chem", "cyanotoxins"
        if code in PESTICIDE_TOTAL_CODES:
            return "chem", "pesticides"
        if (limit_unit in ("µg/L", "ng/L") and limit_max is not None and limit_max <= 0.1
                and code not in NOT_PESTICIDE_01 and code != "BAPYR"):
            return "chem", "pesticides"
        return "chem", "other_chemicals"
    if has_ref:
        if unit in MICRO_UNITS or unit == "n/mL":
            return "comfort", "bacteria_indicators"
        if unit in ("Bq/L", "mSv/a"):
            return "comfort", "radioactivity"
        return "comfort", "indicators"
    return "info", "no_threshold"
