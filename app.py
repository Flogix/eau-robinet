"""Entry point: language, navigation (order = order of the story), header, sidebar filters, footer."""
import streamlit as st

from utils.filters import language_selector, sidebar
from utils.i18n import t
from utils.viz import footer, header, inject_css

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
