"""About this project: author, open code and processed data, how to reproduce, sources and licences, tools."""
import streamlit as st

import config
from utils.i18n import t
from utils.viz import kicker, lede

kicker(t("about.kicker"))
st.title(t("about.title"))
lede(t("about.lede"))
st.markdown(t("about.why"))

kicker(t("about.open.kicker"))
st.header(t("about.open.title"))
st.markdown(t("about.open.text"))
st.markdown(t("about.reproduce"))
c1, c2, c3, c4 = st.columns(4)
c1.link_button(t("about.repo"), config.REPO_URL, icon=":material/code:", width="stretch")
c2.link_button(t("about.linkedin"), config.AUTHOR_LINKEDIN, icon=":material/person:", width="stretch")
c3.link_button(t("about.sources.link"), f"{config.REPO_URL}/blob/main/docs/sources.md",
               icon=":material/menu_book:", width="stretch")
c4.link_button(t("about.dataset"), config.DATASET_PAGE, icon=":material/database:", width="stretch")

kicker(t("about.sources.kicker"))
st.markdown(t("about.sources.text"))
kicker(t("about.tools.kicker"))
st.markdown(t("about.tools"))
st.info(t("about.disclaimer"))
