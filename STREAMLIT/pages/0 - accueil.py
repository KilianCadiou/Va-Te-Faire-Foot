import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import ast
from bs4 import BeautifulSoup
import pickle
import requests
import re
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from rapidfuzz import fuzz
from rapidfuzz import process
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns
import os

custom_css = """
    <style>
    /* Modifier l'arrière-plan de la page principale */
    .stApp {
        background-color: rgba(13, 52, 4, 0.6) !important;
    }

    /* Modifier l'arrière-plan du volet de navigation (sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #666866 !important; /* Couleur gris foncé */
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# st.markdown(
#     "<h1 style='text-align: center; color: white;'>Va te faire foot !</h1>",
#     unsafe_allow_html=True
# )


st.markdown(
    "<h3 style='text-align: center; color: white;'>Bienvenue sur notre service de recommandations de joueurs de football.</h3>",
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .page-break { page-break-before: always; }
    </style>
""", unsafe_allow_html=True)

# st.header("Va te faire foot !")
# st.html("<p>Bienvenue sur notre service de recommandations de joueurs de football.</p>")

# st.image("STREAMLIT/img/sticker-footballeur-pop-art-ambiance-sticker-col-SAND_A131.png", width=500)

st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/file-AfJoGfAn6WiPywEs5Y4Mb2.png" width="500">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .page-break { page-break-before: always; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""---""")
st.markdown(
    "<h3 style='text-align: center; color: white;'>Stack technique</h3>",
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .page-break { page-break-before: always; }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/pandas_white.png" height="50">
    </div>
    """,
    unsafe_allow_html=True
)
    
with col2:
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/github-removebg-preview.png" height="50">
    </div>
    """,
    unsafe_allow_html=True
)
    
with col3:
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/images.png" height="50">
    </div>
    """,
    unsafe_allow_html=True
)
    
with col4:
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/KilianCadiou/Bis/main/STREAMLIT/img/Python.png" height="50">
    </div>
    """,
    unsafe_allow_html=True
)

with col5:
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/streamlit-logo-secondary-colormark-lighttext.png" height="50">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""---""")
st.markdown(
    "<h3 style='text-align: center; color: white;'>Staff technique</h3>",
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .page-break { page-break-before: always; }
    </style>
""", unsafe_allow_html=True)



col3, col4 = st.columns(2)

with col3:
    st.markdown(
        "<h3 style='text-align: center; color: white;'>Matthieu</h3>",
        unsafe_allow_html=True
    )

    subcol1, subcol2 = st.columns(2)

    with subcol1:
        st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://www.linkedin.com/in/matthieu-martin-8063a417a/" target="_blank">
                <img src="STREAMLIT/img/4096186-removebg-preview%20(1).png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )
    
        # st.image("/Users/kilian/Documents/GitHub/Test_projet_3/STREAMLIT/img/Sans titre.png", width = 50)
    with subcol2:
            st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://github.com/MatthieuMARTIN3" target="_blank">
                <img src="https://raw.githubusercontent.com/KilianCadiou/Bis/main/STREAMLIT/img/Sans titre.png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )

    st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/Ctc6lbkXYAA8UoA-removebg-preview.png" height="400">
    </a>
    """,
    unsafe_allow_html=True
    )


    
with col4:
    st.markdown(
        "<h3 style='text-align: center; color: white;'>Loïc</h3>",
        unsafe_allow_html=True
    )

    subcol1, subcol2 = st.columns(2)

    with subcol1:
        st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://www.linkedin.com/in/loic-fotsing-637a221a8/" target="_blank">
                <img src="STREAMLIT/img/4096186-removebg-preview%20(1).png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )
    
        # st.image("/Users/kilian/Documents/GitHub/Test_projet_3/STREAMLIT/img/Sans titre.png", width = 50)
  
    with subcol2:
            st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://github.com/je-suis-lmfao" target="_blank">
                <img src="STREAMLIT/img//Sans titre.png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )
    
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/377.png" height="400">
    </a>
    """,
    unsafe_allow_html=True
    )

            
st.markdown("""---""")

col5, col6 = st.columns(2)

with col5:

    st.markdown(
        "<h3 style='text-align: center; color: white;'>Kilian</h3>",
        unsafe_allow_html=True
    )
    
    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://www.linkedin.com/in/kiliancadiou/" target="_blank">
                <img src="STREAMLIT/img/4096186-removebg-preview%20(1).png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )
    
        # st.image("/Users/kilian/Documents/GitHub/Test_projet_3/STREAMLIT/img/Sans titre.png", width = 50)
    with subcol2:
            st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://github.com/KilianCadiou" target="_blank">
                <img src="STREAMLIT/img/Sans titre.png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )
    
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="STREAMLIT/img/POSE_-16.png" height="400">
    </a>
    """,
    unsafe_allow_html=True
    )


with col6:
    st.markdown(
        "<h3 style='text-align: center; color: white;'>Malo</h3>",
        unsafe_allow_html=True
    )

    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://www.linkedin.com/in/malo-le-pors-5373a8273/" target="_blank">
                <img src="https://github.com/KilianCadiou/Va-Te-Faire-Foot/blob/172178691df91739c17e7a6e9af9464884f1dd82/STREAMLIT/img/20092808-removebg-preview.png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )
    
    with subcol2:
            st.markdown(
            """
            <div style="text-align: center;">
            <a href="https://github.com/MaloBang" target="_blank">
                <img src="STREAMLIT/img/Sans titre.png" width="60">
            </a>
            """,
            unsafe_allow_html=True
            )
    
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/KilianCadiou/Va-Te-Faire-Foot/blob/main/STREAMLIT/img/20092808-removebg-preview.png" height="400">
    </div>
    """,
    unsafe_allow_html=True
)
