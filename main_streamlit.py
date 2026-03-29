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

# 3. CSS STIL
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    .stApp {{ background-color: {BG_COLOR}; }}
    
    .header-section {{
        background-color: #ffffff;
        padding: 40px 20px 30px 20px;
        text-align: center;
        border-bottom: 3px solid {BTN_COLOR};
        margin-bottom: 20px;
    }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, button {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
    }}

    /* STIL ZA GUMBE */
    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: none !important;
        width: 100% !important;
        font-size: 22px !important;
        padding: 10px !important;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05) !important;
    }}

    /* PRISILNO CENTRIRANJE ZA MOBILNE NAPRAVE */
    [data-testid="column"] {{
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 10% !important;
    }}

    /* Poseben kontejner, ki bo vse prisilil na sredino */
    .force-center {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        text-align: center;
    }}

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
    st.markdown(f'<div class="header-section"><h1 style="font-size: 42px;">ČAS ZA POGOVOR</h1><p>✨ Za povezanost ✨</p></div>', unsafe_allow_html=True)
    
    # Tukaj vse zapreva v centriran div
    st.markdown('<div class="force-center">', unsafe_allow_html=True)
    st.markdown(f"<h2 style='font-size: 32px; margin-bottom: 20px;'>KATEGORIJA:</h2>", unsafe_allow_html=True)
    
    for cat in sorted(questions.keys()):
        # Uporabiva ožje stolpce, da omejiva širino gumba na sredini
        _, m, _ = st.columns([1, 2, 1])
        with m:
            if st.button(cat.upper()):
                st.session_state.category = cat
                st.session_state.page = "count_selection"
                st.rerun()
            
    if st.session_state.favorites:
        st.markdown('<br>', unsafe_allow_html=True)
        _, m, _ = st.columns([1, 2, 1])
        with m:
            if st.button("⭐ PRILJUBLJENE"):
                st.session_state.category = "PRILJUBLJENE"
                st.session_state.deck = st.session_state.favorites.copy()
                random.shuffle(st.session_state.deck)
                st.session_state.index = 0
                st.session_state.page = "game"
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "count_selection":
    st.markdown(f'<div class="header-section"><h1>{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="force-center">', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 24px;">Koliko kartic?</p>', unsafe_allow_html=True)
    for opt in [5, 10, "Vse"]:
        _, m, _ = st.columns([1, 2, 1])
        with m:
            if st.button(f"Igraj {opt}"):
                q_list = questions[st.session_state.category]
                n = len(q_list) if opt == "Vse" else opt
                st.session_state.deck = random.sample(q_list, min(n, len(q_list)))
                st.session_state.index = 0
                st.session_state.page = "game"
                st.rerun()
    
    _, m, _ = st.columns([1, 2, 1])
    with m:
        if st.button("< Nazaj"):
            st.session_state.page = "main"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "game":
    st.markdown(f'<div class="header-section"><h1>{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.write(f"Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}")
        st.markdown(f'<div class="q-card"><p style="font-size: 28px; font-weight: bold; text-align: center;">{current_q}</p></div>', unsafe_allow_html=True)
        
        # Gumbi v igri (Tukaj uporabiva fiksne stolpce brez centriranja, da ostanejo v vrsti)
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
    else:
        st.balloons()
        st.markdown("<h2 style='text-align: center;'>Konec! ❤️</h2>", unsafe_allow_html=True)
        _, m, _ = st.columns([1, 2, 1])
        with m:
            if st.button("Domov"):
                st.session_state.page = "main"
                st.rerun()
