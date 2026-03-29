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

# 3. CELOTEN CSS STIL (Popravljeno centriranje znotraj okvirčka)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    /* Ozadje aplikacije */
    .stApp {{ 
        background-color: {BG_COLOR}; 
    }}

    /* Odstranitev privzetih Streamlit paddingov */
    .block-container {{
        max-width: 100% !important;
        padding: 0 !important;
    }}

    /* ZGORNJI DEL (Header) */
    .header-section {{
        background-color: #ffffff;
        padding: 40px 20px 30px 20px;
        text-align: center;
        width: 100%;
        border-bottom: 2px solid {BTN_COLOR};
        margin-bottom: 20px;
    }}

    /* SPODNJI DEL (Okvirček za gumbe) - DODANO CENTRIRANJE */
    .menu-container {{
        background-color: #ffffff;
        margin: 10px 15px;
        padding: 30px 20px;
        border-radius: 30px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.03);
        
        /* Centriranje vsebine znotraj okvirčka */
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    /* Globalni fonti */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, button {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
    }}

    /* GUMBI: Prisila na sredino in polno širino */
    div.stButton {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: none !important;
        width: 100% !important;
        max-width: 450px !important; 
        font-size: 26px !important;
        padding: 12px 20px !important;
        margin: 8px auto !important;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05) !important;
    }}

    /* KARTICA Z VPRAŠANJEM */
    .q-card {{
        background-color: {CARD_COLOR};
        padding: 35px;
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

    /* Skrijemo Streamlit elemente */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# 4. LOGIKA PODATKOV
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
        except: favs = []
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
    st.markdown(f"""
        <div class="header-section">
            <h1 style='font-size: 48px; margin: 0;'>ČAS ZA POGOVOR</h1>
            <p style='font-size: 22px; margin-top: 5px; opacity: 0.8;'>✨ Za povezanost na globlji ravni ✨</p>
        </div>
        """, unsafe_allow_html=True)
    
    # POMEMBNO: Gumbi morajo biti znotraj tega div-a
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: {TEXT_COLOR}; font-size: 36px; margin-bottom: 20px;'>IZBERI KATEGORIJO:</h2>", unsafe_allow_html=True)
    
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
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "count_selection":
    st.markdown(f'<div class="header-section"><h1 style="font-size: 42px;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 24px;">Koliko kartic želita vleči?</p>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "game":
    st.markdown(f'<div class="header-section"><h1 style="font-size: 38px;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.markdown(f"<p style='text-align: center; margin-top: 15px;'>Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}</p>", unsafe_allow_html=True)
        st.markdown(f'<div class="q-card"><p class="q-text">{current_q}</p></div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([1, 1, 0.7, 1.2])
        with col1:
            if st.button("<"):
                if st.session_state.index > 0:
                    st.session_state.index -= 1
                    st.rerun()
        with col2:
            if st.button("Meni"):
                st.session_state.page = "main"
                st.rerun()
        with col3:
            is_f = current_q in st.session_state.favorites
            if st.button("⭐" if is_f else "☆"):
                toggle_fav(current_q)
                st.rerun()
        with col4:
            if st.button("Naprej"):
                st.session_state.index += 1
                st.rerun()
    else:
        st.balloons()
        st.markdown("<div class='menu-container' style='text-align:center;'><h2>Prišla sta do konca! ❤️</h2></div>", unsafe_allow_html=True)
        if st.button("Nazaj na začetek"):
            st.session_state.page = "main"
            st.rerun()
