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

# 3. CSS STIL - KONČNA VERZIJA ZA CELOZASLONSKI HEADER
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    .stApp {{ background-color: {BG_COLOR}; }}
    
    /* Osrednji kontejner Streamlita */
    .block-container {{
        max-width: 800px !important; /* Omejimo širino vsebine na sredino */
        padding: 0 !important;
    }}

    /* MAGIČNI HEADER - Raztegnjen čez robove kljub omejeni širini spodaj */
    .header-section {{
        background-color: #ffffff;
        padding: 40px 0 30px 0;
        text-align: center;
        width: 100vw; /* Celotna širina zaslona */
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        border-bottom: 3px solid {BTN_COLOR};
        margin-bottom: 30px;
    }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
        text-align: center !important;
    }}

    /* CENTRIRANJE GUMBOV */
    [data-testid="stVerticalBlock"] > div {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }}

    /* STIL ZA GUMBE */
    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: none !important;
        width: 100% !important;
        max-width: 280px !important; 
        font-size: 22px !important;
        padding: 10px !important;
        margin: 5px auto !important;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05) !important;
        font-family: 'Patrick Hand', cursive !important;
    }}

    /* ANIMACIJA LETEČIH SRČKOV */
    @keyframes hearts-fly {{
        0% {{ 
            bottom: -50px;
            opacity: 1; 
        }}
        100% {{ 
            bottom: 110vh;
            opacity: 0; 
        }}
    }}

    .heart-particle {{
        position: fixed;
        left: 50%;
        color: #ff4b4b;
        font-size: 35px;
        user-select: none;
        pointer-events: none;
        z-index: 99999 !important;
        animation: hearts-fly 4s linear forwards;
    }}

    /* IZJEMA ZA IGRO: Stolpci vodoravno */
    .game-mode [data-testid="stHorizontalBlock"] {{
        flex-direction: row !important;
        align-items: stretch !important;
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
    }}

    .q-card {{
        background-color: {CARD_COLOR};
        padding: 30px;
        border-radius: 30px;
        border: 2px solid {BTN_COLOR};
        text-align: center;
        margin: 15px auto;
        min-height: 200px;
        max-width: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Funkcija za srčke
def trigger_custom_hearts():
    heart_html = ""
    for i in range(20):
        left = random.randint(0, 100)
        delay = random.uniform(0, 3)
        heart_html += f'<div class="heart-particle" style="left: {left}%; animation-delay: {delay}s;">❤️</div>'
    st.markdown(heart_html, unsafe_allow_html=True)

# --- LOGIKA PODATKOV ---
FAVORITES_FILE = "favorites.txt"
def load_data():
    try:
        df = pd.read_csv("cards.csv", encoding="utf-8")
        data = df.groupby("EDITION")["QUESTION"].apply(list).to_dict()
    except:
        data = {"Napaka": ["Manjka cards.csv!"]}
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
    st.markdown(f'<div class="header-section"><h1 style="font-size: 42px; margin: 0;">ČAS ZA POGOVOR</h1><p style="font-size: 18px; margin-top: 5px; opacity: 0.8;">✨ Za povezanost na globlji ravni ✨</p></div>', unsafe_allow_html=True)
    st.markdown(f"<h2 style='font-size: 32px; margin-bottom: 20px;'>IZBERI KATEGORIJO:</h2>", unsafe_allow_html=True)
    
    for cat in sorted(questions.keys()):
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
    st.markdown(f'<div class="header-section"><h1 style="font-size: 38px; margin: 0;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 22px; margin-top: 20px;">Koliko kartic?</p>', unsafe_allow_html=True)
    for opt in [5, 10, "Vse"]:
        if st.button(f"Igraj {opt}"):
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
    st.markdown(f'<div class="header-section"><h1 style="font-size: 34px; margin: 0;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.write(f"Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}")
        st.markdown(f'<div class="q-card"><p style="font-size: 26px; font-weight: bold;">{current_q}</p></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="game-mode">', unsafe_allow_html=True)
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
            if st.button("Naprej"):
                st.session_state.index += 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        trigger_custom_hearts()
        st.markdown("<h2 style='margin-top: 30px;'>Prišla sta do konca! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Domov"):
            st.session_state.page = "main"
            st.rerun()
