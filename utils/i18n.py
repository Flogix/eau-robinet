# Internationalization engine: translation lookups and locale-aware number/date formatting.
"""Translation: every text of the app goes through t(key). English is the official version, French is a choice.

The strings live in utils/texts/ (one module per page + common), merged in TEXTS below. A missing French string
falls back to English, a missing key raises (caught by the tests). Numbers are formatted per language:
1,234.5 and 98.0% in English, 1 234,5 and 98,0 % in French.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar

import streamlit as st

from utils.texts import TEXTS

LANGS = {"en": "EN", "fr": "FR"}
NBSP = " "   # narrow no-break space: French thousands separator and space before %


_FORCED: ContextVar[str | None] = ContextVar("forced_lang", default=None)


@contextmanager
def forced_lang(code: str):
    """Write in `code` whatever the language of the interface (the PDF report exists in both languages).
    A context variable, so that other sessions served by other threads are not affected."""
    token = _FORCED.set(code)
    try:
        yield
    finally:
        _FORCED.reset(token)


def lang() -> str:
    """Return current language code ('en' or 'fr') from context or session state."""
    forced = _FORCED.get()
    if forced:
        return forced
    try:
        return st.session_state.get("lang", "en")
    except Exception:   # outside a Streamlit run (scripts, tests)
        return "en"


def t(key: str, **kw) -> str:
    """Translate key into current language with format interpolation."""
    entry = TEXTS[key]
    s = entry.get(lang()) or entry["en"]
    return s.format(**kw) if kw else s


def num(x, digits: int = 0) -> str:
    """Number with thousands separators, in the current language."""
    if x is None:
        return "?"
    s = f"{float(x):,.{digits}f}"
    if lang() == "fr":
        s = s.replace(",", "§").replace(".", ",").replace("§", NBSP)
    return s


def pct(x, digits: int = 1) -> str:
    """Share (0–1) as a percentage, in the current language."""
    if x is None:
        return "?"
    v = num(100 * float(x), digits)
    return f"{v}{NBSP}%" if lang() == "fr" else f"{v}%"


def pp(x, digits: int = 2) -> str:
    """Signed difference in percentage points."""
    v = num(abs(x), digits)
    sign = "+" if x >= 0 else "−"
    return f"{sign}{v}{NBSP}pt" if lang() == "fr" else f"{sign}{v} pt"


def date_fr_en(d) -> str:
    """dd/mm/yyyy in French, 12 Mar 2025 style in English."""
    import pandas as pd
    d = pd.Timestamp(d)
    if lang() == "fr":
        return d.strftime("%d/%m/%Y")
    return f"{d.day} {d.strftime('%b %Y')}"


MONTHS = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          "fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]}


def months() -> list[str]:
    """Return localized list of abbreviated month names."""
    return MONTHS[lang()]


def tn(key: str, count, **kw) -> str:
    """Like t(), but uses the singular variant `key.one` when count == 1 (French and English agreement)."""
    one = f"{key}.one"
    return t(one if int(count) == 1 and one in TEXTS else key, **kw)
