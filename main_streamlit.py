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

# 3. STABILEN CSS ZA IPHONE (Fiksna višina belega dela)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    .stApp {{ background-color: {BG_COLOR}; }}
    
    .block-container {{
        max-width: 800px !important;
        padding: 0 !important;
    }}

    /* HEADER - Fiksno belo polje, ki se razteza čez robove */
    .header-section {{
        background-color: #ffffff !important;
        padding: 30px 0 !important;
        text-align: center;
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        border-bottom: 3px solid {BTN_COLOR};
        margin-bottom: 30px;
        min-height: 180px; /* Dovolj visoko, da objame vse */
    }}

    .top-icon-container img {{
        max-width: 50px !important;
        margin: 0 auto 10px auto !important;
        display: block !important;
    }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR} !important;
        text-align: center !important;
    }}

    /* CENTRIRANJE VSEGA POD HEADERJEM */
    [data-testid="stVerticalBlock"] > div {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }}

    /* GUMBI */
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
    }}

    /* MANJŠI GUMB MENI V HEADERJU */
    .menu-btn-top div.stButton > button {{
        max-width: 110px !important;
        font-size: 16px !important;
        padding: 5px !important;
        margin-bottom: 15px !important;
    }}

    /* ANIMACIJA LETEČIH SRČKOV */
    @keyframes hearts-fly {{
        0% {{ bottom: -50px; opacity: 1; }}
        100% {{ bottom: 110vh; opacity: 0; }}
    }}
    .heart-particle {{
        position: fixed;
        color: #ff4b4b;
        font-size: 35px;
        pointer-events: none;
        z-index: 99999 !important;
        animation: hearts-fly 4s linear forwards;
    }}

    .game-mode [data-testid="stHorizontalBlock"] {{
        flex-direction: row !important;
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
    }}

    .q-card {{
        background-color: {CARD_COLOR};
        padding: 30px;
        border-radius: 30px;
        border: 2px solid {BTN_COLOR};
        min-height: 200px;
        max-width: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

def trigger_custom_hearts():
    heart_html = ""
    for i in range(25):
        left_pos = random.randint(5, 95)
        delay = random.uniform(0, 2)
        heart_html += f'<div class="heart-particle" style="left: {left_pos}%; animation-delay: {delay}s;">❤️</div>'
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

if st.session_state.page == "main":
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    if os.path.exists("heart.png"):
        st.markdown('<div class="top-icon-container">', unsafe_allow_html=True)
        st.image("heart.png", width=50)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-size: 42px; margin: 0;">ČAS ZA NAJU</h1><p style="font-size: 18px; margin-top: 5px; opacity: 0.8;">✨ Pogovor, ki povezuje ✨</p></div>', unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='font-size: 32px; margin-bottom: 20px; margin-top: 20px;'>IZBERI KATEGORIJO:</h2>", unsafe_allow_html=True)
    for cat in sorted(questions.keys()):
        if st.button(cat.upper()):
            st.session_state.category = cat
            st.session_state.page = "count_selection"
            st.rerun()
            
    if st.session_state.favorites:
        st.write("---")
        if st.button("❤️ PRILJUBLJENE"):
            st.session_state.category = "PRILJUBLJENE"
            st.session_state.deck = st.session_state.favorites.copy()
            random.shuffle(st.session_state.deck)
            st.session_state.index = 0
            st.session_state.page = "game"
            st.rerun()

elif st.session_state.page == "count_selection":
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    st.markdown('<div class="menu-btn-top">', unsafe_allow_html=True)
    if st.button("Meni"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-size: 38px; margin: 0;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 24px; margin-top: 30px;">Koliko kartic?</p>', unsafe_allow_html=True)
    for opt in [5, 10, "Vse"]:
        if st.button(f"Igraj {opt}"):
            q_list = questions[st.session_state.category]
            n = len(q_list) if opt == "Vse" else opt
            st.session_state.deck = random.sample(q_list, min(n, len(q_list)))
            st.session_state.index = 0
            st.session_state.page = "game"
            st.rerun()

elif st.session_state.page == "game":
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    st.markdown('<div class="menu-btn-top">', unsafe_allow_html=True)
    if st.button("Meni"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-size: 34px; margin: 0;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)

    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.write(f"Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}")
        st.markdown(f'<div class="q-card"><p style="font-size: 26px; font-weight: bold;">{current_q}</p></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="game-mode">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 0.8, 1.2])
        with c1:
            if st.button("<"):
                if st.session_state.index > 0:
                    st.session_state.index -= 1
                    st.rerun()
        with c2:
            is_f = current_q in st.session_state.favorites
            heart_icon = "❤️" if is_f else "🤍"
            if st.button(heart_icon):
                toggle_fav(current_q)
                st.rerun()
        with c3:
            if st.button("Naprej"):
                st.session_state.index += 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        trigger_custom_hearts()
        st.markdown("<h2 style='margin-top: 30px;'>Konec! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Domov"):
            st.session_state.page = "main"
            st.rerun()
