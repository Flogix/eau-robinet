"""Entry point: language, navigation (order = order of the story), header, sidebar filters, footer."""
import sys
from pathlib import Path

import streamlit as st


def _forget_stale_project_modules() -> None:
    """After a code update (git push to Streamlit Cloud, or an edit in local development), the server keeps the old
    project modules in memory, and a page importing a new function fails with ImportError. Forget the project
    modules whose source file changed since they were loaded, so that the imports below load the new code."""
    root = Path(__file__).resolve().parent
    project = [n for n in sys.modules if n == "config" or n == "utils" or n.startswith("utils.")]
    for name in project:
        mod = sys.modules[name]
        src, pyc = getattr(mod, "__file__", None), getattr(mod, "__cached__", None)
        if not src or not pyc or not Path(src).resolve().is_relative_to(root):
            continue
        try:   # the compiled file is written when the module is imported: a newer source means stale code
            stale = Path(src).stat().st_mtime > Path(pyc).stat().st_mtime + 1
        except OSError:
            continue
        if stale:
            for other in project:
                sys.modules.pop(other, None)
            st.cache_data.clear()
            st.cache_resource.clear()
            break


_forget_stale_project_modules()

from utils.filters import language_selector, sidebar  # noqa: E402
from utils.i18n import t  # noqa: E402
from utils.viz import footer, header, inject_css  # noqa: E402

st.set_page_config(page_title="Au robinet", page_icon=":material/water_drop:", layout="wide")
inject_css()
language_selector()

PAGES = {   # url path -> (file, title key, material icon)
    "": ("sections/intro.py", "nav.home", ":material/water_drop:"),
    "reading": ("sections/comprendre.py", "nav.reading", ":material/science:"),
    "town": ("sections/ma_commune.py", "nav.town", ":material/home_pin:"),
    "compare": ("sections/comparer.py", "nav.compare", ":material/compare_arrows:"),
    "map": ("sections/overview.py", "nav.map", ":material/map:"),
    "monitor": ("sections/deep_dives.py", "nav.monitor", ":material/search_insights:"),
    "quality": ("sections/data_quality.py", "nav.quality", ":material/fact_check:"),
    "conclusions": ("sections/conclusions.py", "nav.conclusions", ":material/flag:"),
    "about": ("sections/about.py", "nav.about", ":material/info:"),
}


def page(path: str) -> st.Page:
    file, title, icon = PAGES[path]
    return st.Page(file, title=t(title), icon=icon, url_path=path or None, default=(path == ""))


nav = st.navigation({
    t("nav.section.story"): [page(p) for p in ("", "reading", "town", "compare", "map", "monitor", "conclusions")],
    t("nav.section.more"): [page(p) for p in ("quality", "about")],
})
sidebar(nav.url_path)
header()
nav.run()
footer()
