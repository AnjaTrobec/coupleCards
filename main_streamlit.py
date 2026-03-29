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

# 3. LOČENI CSS STILI
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    .stApp {{ background-color: {BG_COLOR}; }}
    .block-container {{ max-width: 100% !important; padding: 0 !important; }}

    /* HEADER */
    .header-section {{
        background-color: #ffffff;
        padding: 40px 20px 30px 20px;
        text-align: center;
        border-bottom: 3px solid {BTN_COLOR};
        margin-bottom: 30px;
    }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
        text-align: center;
    }}

    /* --- STIL 1: GLAVNI MENI (Navpično centriranje) --- */
    .main-menu-container [data-testid="stVerticalBlock"] > div {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        width: 100% !important;
    }}

    /* --- STIL 2: IGRA (Vodoravna vrsta brez prisilnega centriranja) --- */
    .game-controls [data-testid="column"] [data-testid="stVerticalBlock"] > div {{
        display: block !important; /* Povrne privzeto Streamlit obnašanje */
    }}

    /* SPLOŠNI STIL ZA GUMBE */
    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: none !important;
        font-family: 'Patrick Hand', cursive !important;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05) !important;
    }}

    /* Gumbi v meniju (večji) */
    .main-menu-container div.stButton > button {{
        width: 100% !important;
        max-width: 400px !important;
        font-size: 26px !important;
        padding: 12px !important;
        margin: 10px auto !important;
    }}

    /* Gumbi v igri (manjši in v vrsti) */
    .game-controls div.stButton > button {{
        font-size: 18px !important;
        padding: 10px 2px !important;
        width: 100% !important;
        margin: 0 !important;
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
        data = {{"Info": ["Manjka cards.csv!"]}}
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
    st.markdown(f'<div class="header-section"><h1 style="font-size: 42px;">ČAS ZA POGOVOR</h1><p>✨ Za povezanost na globlji ravni ✨</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-menu-container">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "count_selection":
    st.markdown(f'<div class="header-section"><h1 style="font-size: 38px;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-menu-container">', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 22px;">Število kartic:</p>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "game":
    st.markdown(f'<div class="header-section"><h1 style="font-size: 34px;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.write(f"Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}")
        st.markdown(f'<div class="q-card"><p style="font-size: 28px; font-weight: bold;">{current_q}</p></div>', unsafe_allow_html=True)
        
        # NAVIGACIJA V VRSTI
        st.markdown('<div class="game-controls">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1.2, 0.8, 1.5])
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
            if st.button("Naprej >"):
                st.session_state.index += 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.balloons()
        st.markdown("<h2 style='margin-top: 50px;'>Konec! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Nazaj"):
            st.session_state.page = "main"
            st.rerun()
