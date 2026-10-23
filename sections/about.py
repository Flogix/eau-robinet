# About page: project genesis, author information, open source links, data export, and tools.
"""About this project: author, open code and processed data, how to reproduce, sources and licences, tools."""
import streamlit as st

import config
from utils.i18n import t
from utils.io import build_processed_zip, get_processed_data_size_mb
from utils.viz import kicker, lede

kicker(t("about.kicker"))
st.title(t("about.title"))
lede(t("about.lede"))
st.markdown(t("about.why"))

kicker(t("about.open.kicker"))
st.header(t("about.open.title"))
st.markdown(t("about.open.text"))
st.markdown(t("about.reproduce"))
c1, c2, c3 = st.columns(3)
c1.link_button(t("about.repo"), config.REPO_URL, icon=":material/code:", width="stretch")
c2.link_button(t("about.linkedin"), config.AUTHOR_LINKEDIN, icon=":material/person:", width="stretch")
c3.link_button(t("about.sources.link"), f"{config.REPO_URL}/blob/main/docs/sources.md",
               icon=":material/menu_book:", width="stretch")

st.markdown("")
cd1, cd2 = st.columns([1, 1.6])
cd1.link_button(t("about.dataset"), config.DATASET_PAGE, icon=":material/database:", width="stretch", wrap=True)
cd2.download_button(
    t("about.download_processed", size=get_processed_data_size_mb()),
    data=build_processed_zip,
    file_name="eau-robinet-processed-data.zip",
    mime="application/zip",
    icon=":material/download:",
    width="stretch",
    wrap=True,
    key="about_download_zip",
)
st.caption(t("about.raw_data_note"))

kicker(t("about.sources.kicker"))
st.markdown(t("about.sources.text"))
kicker(t("about.tools.kicker"))
st.markdown(t("about.tools"))
st.info(t("about.disclaimer"))
