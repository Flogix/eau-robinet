"""Town search shared by the pages: one list that filters as you type, without 35,000 options in the browser.

Why not st.selectbox: Streamlit's selectbox filters and draws its options in the browser, without virtualisation. With
the 34,812 French towns, emptying the field (or closing the list after a choice) makes the browser draw tens of
thousands of options: the page froze 4 to 25 seconds (measured with scripts/perf_audit.py, before and after are in
docs/AVANCEMENT.md). Here the search runs on the server (accents ignored, homonyms told apart by their department) and
the browser only ever receives the 5 examples or the 20 best matches.

The search box lives in a fragment: each keystroke reruns only the box, not the page. Choosing a town updates the
session state, empties the box and reruns the whole page in a single round trip; the box then shows the current town as
its placeholder, so that choosing again a town seen before always works.
"""
from __future__ import annotations

import streamlit as st

from utils.i18n import t
from utils.io import EXAMPLE_TOWNS, search_communes, town_options

MAX_MATCHES = 20


def town_matches(term: str) -> list[tuple[str, str]]:
    """(label, INSEE code) of the towns matching `term`; the five examples when the field is empty."""
    _, labels = town_options()
    if not str(term or "").strip():
        return [(labels[i], i) for i in EXAMPLE_TOWNS if i in labels]
    hits = search_communes(term, limit=MAX_MATCHES)
    return list(zip(hits["label"], hits["insee"]))


def _style() -> dict:
    """Colours of the app inside the component's frame (it does not inherit the page CSS)."""
    return {"searchbox": {"optionEmpty": "hidden"}, "clear": {"clearable": "never"},
            "wrapper": {"fontFamily": "IBM Plex Sans, Helvetica, Arial, sans-serif"}}


def town_search(label: str, key: str, on_pick, current: str | None = None, help: str | None = None,
                placeholder: str | None = None, disabled: bool = False) -> None:
    """Draw the search box. `on_pick(insee)` is called once when a town is chosen; then the page reruns."""
    _box(label, key, on_pick, current, help, placeholder, disabled)


@st.fragment
def _box(label: str, key: str, on_pick, current: str | None, help: str | None, placeholder: str | None,
         disabled: bool) -> None:
    from streamlit_searchbox import _set_defaults, st_searchbox

    if disabled:
        st.text_input(label, value="", placeholder=placeholder or "", disabled=True, help=help, key=f"{key}_off")
        return
    _, labels = town_options()

    def picked(insee):
        if insee:
            on_pick(insee)
            # empty the box (as clear_on_submit would) and rerun the whole page at once: a single round trip
            _set_defaults(key, None, "", town_matches(""))
            st.rerun()

    if placeholder is None:
        placeholder = t("search.placeholder.current", town=labels[current]) if current in labels else \
            t("search.placeholder")
    st_searchbox(town_matches, label=label, placeholder=placeholder, key=key, help=help,
                 default_options=town_matches(""), submit_function=picked,
                 rerun_scope="fragment", debounce=150, style_overrides=_style())
