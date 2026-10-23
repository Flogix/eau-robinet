# Main Streamlit application entry point configuring page layout, global navigation, and sidebar controls.
# Routes user requests across storytelling sections and handles dynamic module reloading for live deployment.
"""Entry point: language, navigation (order = order of the story), header, sidebar filters, footer."""
import sys
from pathlib import Path

import streamlit as st


def _forget_stale_project_modules() -> None:
    """Evict cached project modules from sys.modules when their files change on disk, preventing stale imports."""
    project = _project_modules()
    for mod in project.values():
        stamp = getattr(mod, "_au_robinet_mtime", None)
        if stamp is not None and _mtime(mod) != stamp:
            for name in project:
                sys.modules.pop(name, None)
            st.cache_data.clear()
            st.cache_resource.clear()
            return


def _project_modules() -> dict:
    """Find loaded sys.modules belonging to config or utils within the project root."""
    root = Path(__file__).resolve().parent
    return {n: m for n, m in list(sys.modules.items())
            if (n == "config" or n == "utils" or n.startswith("utils.")) and getattr(m, "__file__", None)
            and Path(m.__file__).resolve().is_relative_to(root)}


def _mtime(mod) -> float | None:
    """Get file modification timestamp for a module, returning None on filesystem error."""
    try:
        return Path(mod.__file__).stat().st_mtime
    except OSError:
        return None


def _stamp_project_modules() -> None:
    """Record the initial modification timestamp of each loaded project module to detect subsequent file edits."""
    for mod in _project_modules().values():
        if getattr(mod, "_au_robinet_mtime", None) is None:
            mod._au_robinet_mtime = _mtime(mod)


_forget_stale_project_modules()

from utils.filters import filter_hint, init_language, language_selector, sidebar  # noqa: E402
from utils.i18n import t  # noqa: E402
from utils.viz import footer, header, inject_css, sidebar_menu  # noqa: E402

_stamp_project_modules()

st.set_page_config(page_title="Au robinet", page_icon=":material/water_drop:", layout="wide")
inject_css()
init_language()

PAGES = {   # url path -> (file, title key, material icon)
    "": ("sections/intro.py", "nav.home", ":material/water_drop:"),
    "reading": ("sections/comprendre.py", "nav.reading", ":material/science:"),
    "town": ("sections/ma_commune.py", "nav.town", ":material/home_pin:"),
    "compare": ("sections/comparer.py", "nav.compare", ":material/compare_arrows:"),
    "map": ("sections/overview.py", "nav.map", ":material/map:"),
    "monitor": ("sections/deep_dives.py", "nav.monitor", ":material/search_insights:"),
    "explore": ("sections/explore.py", "nav.explore", ":material/table_view:"),
    "quality": ("sections/data_quality.py", "nav.quality", ":material/fact_check:"),
    "my-score": ("sections/mon_score.py", "nav.myscore", ":material/tune:"),
    "conclusions": ("sections/conclusions.py", "nav.conclusions", ":material/flag:"),
    "about": ("sections/about.py", "nav.about", ":material/info:"),
}


def page(path: str) -> st.Page:
    """Build a localized st.Page instance from the PAGES registry with translated title and icon."""
    file, title, icon = PAGES[path]
    return st.Page(file, title=t(title), icon=icon, url_path=path or None, default=(path == ""))


SECTIONS = {   # the menu, drawn by sidebar_menu() under the author block (Streamlit's own menu is hidden)
    t("nav.section.story"): [page(p) for p in ("", "conclusions", "reading", "town", "compare", "map", "monitor",
                                                     "my-score")],   # the findings first, then the evidence
    t("nav.section.more"): [page(p) for p in ("explore", "quality", "about")],
}
nav = st.navigation(SECTIONS, position="hidden")
sidebar_menu(SECTIONS)
language_selector()
sidebar(nav.url_path)
header()
filter_hint(nav.url_path)
nav.run()
footer()
_stamp_project_modules()   # modules imported by the page are dated too
