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

    /* 1. PRISILA GLAVNEGA KONTEJNERJA NA SREDINO */
    [data-testid="stVerticalBlock"] > div {{
        display: flex;
        flex-direction: column;
        align-items: center !important;
        justify-content: center !important;
        width: 100%;
    }}

    /* 2. PRILAGODITEV ŠIRINE VSEBINE */
    .block-container {{
        max-width: 100% !important;
        padding: 10px 15px !important;
    }}

    .stApp {{ 
        background-color: {BG_COLOR}; 
    }}

    /* 3. PISAVA IN BARVE */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, button {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
        text-align: center;
    }}

    /* 4. STIL ZA GUMBE (Kategorije) */
    div.stButton {{
        width: 100%;
        display: flex;
        justify-content: center;
    }}

    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: 2px solid {BTN_COLOR} !important;
        
        /* Centriranje in širina */
        margin: 10px auto !important;
        width: 100% !important;
        max-width: 450px !important; 
        
        display: block !important;
        font-size: 26px !important;
        padding: 12px 20px !important;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.1) !important;
    }}

    /* 5. IZJEMA ZA NAVIGACIJO V IGRI (da gumbi ostanejo v vrsti) */
    [data-testid="column"] [data-testid="stVerticalBlock"] > div {{
        flex-direction: row !important;
        align-items: stretch !important;
        justify-content: space-between !important;
    }}
    
    [data-testid="column"] div.stButton > button {{
        max-width: 100% !important;
        font-size: 18px !important;
        padding: 10px 5px !important;
    }}

    /* 6. KARTICA Z VPRAŠANJEM */
    .q-card {{
        background-color: {CARD_COLOR};
        padding: 30px;
        border-radius: 30px;
        border: 2px solid {BTN_COLOR};
        text-align: center;
        margin: 20px auto;
        min-height: 250px;
        max-width: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .q-text {{ 
        font-size: 32px !important; 
        font-weight: bold;
    }}

    /* Skrijemo nepotrebne Streamlit elemente */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)


FAVORITES_FILE = "favorites.txt"

def load_data():
    try:
        df = pd.read_csv("cards.csv", encoding="utf-8")
        data = df.groupby("EDITION")["QUESTION"].apply(list).to_dict()
    except:
        data = {"Info": ["Manjka cards.csv!"]}
    
    favs = []
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                favs = [line.strip() for line in f.readlines() if line.strip()]
        except:
            favs = []
    return data, favs

questions, favorites = load_data()

if 'page' not in st.session_state: st.session_state.page = "main"
if 'index' not in st.session_state: st.session_state.index = 0
if 'deck' not in st.session_state: st.session_state.deck = []
if 'category' not in st.session_state: st.session_state.category = ""
if 'favorites' not in st.session_state: st.session_state.favorites = favorites

def save_favorites():
    try:
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            for fav in st.session_state.favorites:
                f.write(fav + "\n")
    except: pass

def toggle_fav(q):
    if q in st.session_state.favorites:
        st.session_state.favorites.remove(q)
    else:
        st.session_state.favorites.append(q)
    save_favorites()

# --- STRANI ---
if st.session_state.page == "main":
    st.markdown("<h1 style='text-align: center; font-size: 45px;'>ČAS ZA POGOVOR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 22px;'>✨ Za povezanost na globlji ravni ✨</p>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(f"<h2 style='text-align: center; color: {TEXT_COLOR}; font-size: 38px;'>IZBERI KATEGORIJO:</h2>", unsafe_allow_html=True)
    
    categories = sorted([c for c in questions.keys()])
    for cat in categories:
        if st.button(cat.upper()):
            st.session_state.category = cat
            st.session_state.page = "count_selection"
            st.rerun()
            
    if st.session_state.favorites:
        st.write("---")
        if st.button("⭐ PRILJUBLJENE"):
            st.session_state.category = "PRILJUBLJENE"
            st.session_state.deck = st.session_state.favorites.copy()
            random.shuffle(st.session_state.deck)
            st.session_state.index = 0
            st.session_state.page = "game"
            st.rerun()

elif st.session_state.page == "count_selection":
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.category}</h1>", unsafe_allow_html=True)
    for opt in [5, 10, "Vse"]:
        if st.button(f"Igraj {opt} kartic"):
            q_list = questions[st.session_state.category]
            n = len(q_list) if opt == "Vse" else opt
            st.session_state.deck = random.sample(q_list, min(n, len(q_list)))
            st.session_state.index = 0
            st.session_state.page = "game"
            st.rerun()
    if st.button("< Nazaj"):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "game":
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.markdown(f"<p style='text-align: center;'><b>{st.session_state.category}</b> ({st.session_state.index + 1}/{len(st.session_state.deck)})</p>", unsafe_allow_html=True)
        st.markdown(f'<div class="q-card"><p class="q-text">{current_q}</p></div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns([1, 1, 0.7, 1.2])
        with c1: 
            if st.button("<"):
                if st.session_state.index > 0:
                    st.session_state.index -= 1
                    st.rerun()
        with c2:
            if st.button("Meni"):
                st.session_state.page = "main"
                st.rerun()
        with c3:
            is_f = current_q in st.session_state.favorites
            if st.button("⭐" if is_f else "☆"):
                toggle_fav(current_q)
                st.rerun()
        with c4:
            if st.button("Naprej >"):
                st.session_state.index += 1
                st.rerun()
    else:
        st.balloons()
        st.markdown("<h2 style='text-align: center;'>Prišla sta do konca! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Nazaj na začetek"):
            st.session_state.page = "main"
            st.rerun()
