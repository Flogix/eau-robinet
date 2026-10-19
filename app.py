"""Entry point: page config, navigation (order = order of the story), global sidebar."""
import streamlit as st

st.set_page_config(page_title="Is my tap water good?", page_icon="💧", layout="wide")

pages = [
    st.Page("sections/intro.py", title="Is my tap water good?", icon="💧", default=True),
    st.Page("sections/comprendre.py", title="Understand your water", icon="🔬"),
    st.Page("sections/ma_commune.py", title="My town", icon="🏠"),
    st.Page("sections/comparer.py", title="Compare", icon="⚖️"),
    st.Page("sections/overview.py", title="France's water map", icon="🗺️"),
    st.Page("sections/deep_dives.py", title="Deep dives", icon="🔎"),
    st.Page("sections/data_quality.py", title="Data quality", icon="🧪"),
    st.Page("sections/conclusions.py", title="Conclusions", icon="✅"),
]

nav = st.navigation(pages)

with st.sidebar:
    st.caption(
        "Educational indicator, not a health opinion. "
        "The official opinion on your water is the one of your Regional Health Agency (ARS)."
    )

nav.run()
