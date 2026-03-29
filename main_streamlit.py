import streamlit as st
import pandas as pd
import random
import os

# 1. KONFIGURACIJA STRANI
st.set_page_config(page_title="Najina Pot", page_icon="❤️", layout="wide")

# 2. DEFINICIJA BARV
BG_COLOR = "#f5f2ee"
CARD_COLOR = "#fff2f5"
BTN_COLOR = "#f2bfc9"
TEXT_COLOR = "#993366"

# 3. POSODOBLJEN CSS STIL (Zamenjaj svoj trenutni stil s temle)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    .block-container {{
        max-width: 100% !important;
        padding: 10px 15px !important;
    }}

    .stApp {{ 
        background-color: {BG_COLOR}; 
    }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, button {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
    }}

    /* Sredinska poravnava vseh gumbov */
    div.stButton {{
        text-align: center;
        width: 100%;
    }}

    /* Stil za glavne gumbe (Kategorije) */
    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: 2px solid {BTN_COLOR} !important;
        
        /* Centriranje */
        margin-left: auto !important;
        margin-right: auto !important;
        
        /* Širina: na telefonu 100%, na računalniku max 450px */
        width: 100% !important;
        max-width: 450px !important; 
        
        display: block !important;
        font-size: 24px !important;
        padding: 12px 20px !important;
        margin-bottom: 12px !important;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.1) !important; /* Rahla senca za "klikljivost" */
    }}

    /* Stil za navigacijske gumbe v vrstici (Igra) */
    [data-testid="column"] div.stButton > button {{
        max-width: 100% !important;
        font-size: 18px !important;
        padding: 10px 5px !important;
        margin-bottom: 5px !important;
    }}

    .q-card {{
        background-color: {CARD_COLOR};
        padding: 25px;
        border-radius: 25px;
        border: 2px solid {BTN_COLOR};
        text-align: center;
        margin: 15px auto;
        min-height: 200px;
        max-width: 500px; /* Da kartica na računalniku ni preširoka */
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .q-text {{ 
        font-size: 28px !important; 
        font-weight: bold;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# 4. NADALJEVANJE LOGIKE (FAVORITES_FILE = ...)
