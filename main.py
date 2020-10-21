import page1
import page2
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE
st.beta_set_page_config(layout="wide")

PAGES = {
    "Macro City View": page1,
    "Individual City View": page2
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("View", list(PAGES.keys()))
page = PAGES[selection]
page.app()
