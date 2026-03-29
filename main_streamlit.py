import streamlit as st
import pandas as pd
import random
import os

# 1. KONFIGURACIJA STRANI (Vrnemo 'wide' za celozaslonski header)
st.set_page_config(page_title="Najina Pot", page_icon="❤️", layout="wide")

# 2. DEFINICIJA BARV
BG_COLOR = "#f5f2ee"      
CARD_COLOR = "#fff2f5"    
BTN_COLOR = "#f2bfc9"     
TEXT_COLOR = "#993366"    

# 3. ZMAGOVALNI CSS STIL (S fokusom na celozaslonski header in omejitev širine vsebin)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    .stApp {{ background-color: {BG_COLOR}; }}
    
    /*Header naj bo čez celo širino */
    .block-container {{
        max-width: 100% !important;
        padding: 0 !important;
    }}

    /* HEADER - Bel, raztegnjen čez celo širino, s tvojo črto */
    .header-section {{
        background-color: #ffffff;
        padding: 40px 20px 30px 20px;
        text-align: center;
        width: 100%;
        border-bottom: 3px solid {BTN_COLOR};
        margin-bottom: 20px; /* Malo manjši razmik, da ne bo preveč 'zraka' */
    }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
        text-align: center !important;
    }}

    /* KLJUČ ZA CENTRIRANJE KATEGORIJ NA IPHONU IN OMEJITEV ŠIRINE VSEBIN */
    /* Z data-testid='stMain' ciljamo na vsebino pod headerjem */
    [data-testid="stMain"] [data-testid="stVerticalBlock"] > div {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        max-width: 600px !important; /* Omejitev širine vsebin pod headerjem */
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    /* STIL ZA GUMBE */
    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: none !important;
        width: 100% !important;
        max-width: 280px !important; /* Omejitev širine za telefon */
        font-size: 22px !important;
        padding: 10px !important;
        margin: 5px auto !important; /* To centrirani gumb */
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05) !important;
        font-family: 'Patrick Hand', cursive !important;
    }}

    /* IZJEMA ZA IGRO: Stolpci vodoravno */
    .game-mode [data-testid="stHorizontalBlock"] {{
        flex-direction: row !important;
        align-items: stretch !important;
        width: 100% !important;
        max-width: 600px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    /* KARTICA */
    .q-card {{
        background-color: {CARD_COLOR};
        padding: 30px;
        border-radius: 30px;
        border: 2px solid {BTN_COLOR};
        text-align: center;
        margin: 20px auto;
        min-height: 200px;
        max-width: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* --- ANIMACIJA LETEČIH SRČKOV --- */
    @keyframes hearts-fly {{
        0% {{ transform: translateY(100vh) scale(0); opacity: 1; }}
        100% {{ transform: translateY(-100vh) scale(1.5); opacity: 0; }}
    }}

    .heart-particle {{
        position: fixed;
        bottom: 0;
        color: #ff4b4b;
        font-size: 30px;
        user-select: none;
        pointer-events: none;
        z-index: 9999;
        animation: hearts-fly 4s linear forwards;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Funkcija za srčke (HTML/CSS)
def trigger_custom_hearts():
    heart_html = ""
    for i in range(20): # Število srčkov
        left = random.randint(0, 100)
        delay = random.uniform(0, 3)
        heart_html += f'<div class="heart-particle" style="left: {left}%; animation-delay: {delay}s;">❤️</div>'
    st.markdown(heart_html, unsafe_allow_html=True)

# 4. LOGIKA PODATKOV
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

# STRAN 1: GLAVNI MENI
if st.session_state.page == "main":
    # Beli header raztegnjen čez celo širino
    st.markdown(f'<div class="header-section"><h1 style="font-size: 42px; margin: 0;">ČAS ZA POGOVOR</h1><p style="font-size: 18px; margin-top: 5px; opacity: 0.8;">✨ Za povezanost na globlji ravni ✨</p></div>', unsafe_allow_html=True)
    
    # Zdaj naslov 'IZBERI KATEGORIJO' ne bo več porezan
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

# STRAN 2: IZBIRA ŠTEVILA KARTIC
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

# STRAN 3: IGRA
elif st.session_state.page == "game":
    st.markdown(f'<div class="header-section"><h1 style="font-size: 34px; margin: 0;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.write(f"Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}")
        st.markdown(f'<div class="q-card"><p style="font-size: 26px; font-weight: bold;">{current_q}</p></div>', unsafe_allow_html=True)
        
        # Gumbi v igri (vodoravno, omejena širina)
        st.markdown('</div><div class="game-controls"><div class="game-mode">', unsafe_allow_html=True)
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
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        # SPROŽIVA SRČKE NAMESTO SNEŽINK
        trigger_custom_hearts()
        st.markdown("<h2 style='margin-top: 30px;'>Prišla sta do konca! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Domov"):
            st.session_state.page = "main"
            st.rerun()
