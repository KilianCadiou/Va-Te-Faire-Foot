import streamlit as st
import base64
from st_pages import get_nav_from_toml
import time

nav = get_nav_from_toml("STREAMLIT/.streamlit/pages.toml")

st.logo("https://raw.githubusercontent.com/KilianCadiou/Va-Te-Faire-Foot/main/STREAMLIT/img/Bandeau.png", size = 'large')

pg = st.navigation(nav)

pg.run()

custom_css = """
    <style>
    /* Modifier l'arrière-plan de la page principale avec un dégradé */
    .stApp {
        background: linear-gradient(to bottom, rgba(13, 52, 4, 0.8), rgba(0, 0, 0, 0.8)) !important;
    }

    /* Modifier l'arrière-plan du volet de navigation (sidebar) avec un dégradé */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #FFFFFF, #333333) !important;
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
