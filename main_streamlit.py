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

# 3. CSS STIL - TOTALNI FIX ZA VRSTICO NA IPHONU
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    .stApp {{ background-color: {BG_COLOR}; overflow-x: hidden !important; }}
    
    .block-container {{
        max-width: 100% !important; 
        padding: 0 10px !important;
    }}

    .header-section {{
        background-color: #ffffff;
        padding: 40px 0 30px 0;
        text-align: center;
        width: 100vw; 
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

    /* --- IPHONE NAVIGATION BAR FIX --- */
    .custom-nav-bar {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 20px !important;
        width: 100% !important;
        margin: 20px 0 !important;
    }}

    .nav-icon-btn {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 50% !important; /* Okrogli gumbi za ikone */
        width: 60px !important;
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 28px !important;
        text-decoration: none !important;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.1) !important;
        border: none !important;
        cursor: pointer !important;
    }}

    /* SPLOŠNI GUMBI (Meni, Kategorije) */
    div.stButton > button {{
        background-color: {BTN_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 25px !important;
        border: none !important;
        width: 100% !important;
        max-width: 280px !important; 
        font-size: 20px !important;
        padding: 10px !important;
        margin: 5px auto !important;
    }}

    .q-card {{
        background-color: {CARD_COLOR};
        padding: 30px;
        border-radius: 30px;
        border: 2px solid {BTN_COLOR};
        margin: 15px auto;
        min-height: 200px;
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
        left = random.randint(5, 95)
        delay = random.uniform(0, 2)
        heart_html += f'<div style="position:fixed; left:{left}%; bottom:-50px; color:#ff4b4b; font-size:30px; z-index:9999; animation: fly 4s {delay}s linear forwards;">❤️</div>'
    st.markdown(heart_html + "<style>@keyframes fly {0%{bottom:-50px; opacity:1;} 100%{bottom:110vh; opacity:0;}}</style>", unsafe_allow_html=True)

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
    st.markdown(f'<div class="header-section"><h1 style="font-size: 42px; margin: 0;">ČAS ZA POGOVOR</h1><p style="font-size: 18px; margin-top: 5px; opacity: 0.8;">✨ Za povezanost ✨</p></div>', unsafe_allow_html=True)
    st.markdown(f"<h2 style='font-size: 32px; margin-bottom: 20px;'>IZBERI KATEGORIJO:</h2>", unsafe_allow_html=True)
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
    st.write("---")
    if st.button("🏠 NAZAJ"):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "game":
    st.markdown(f'<div class="header-section"><h1 style="font-size: 34px; margin: 0;">{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        st.write(f"Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}")
        st.markdown(f'<div class="q-card"><p style="font-size: 24px; font-weight: bold;">{current_q}</p></div>', unsafe_allow_html=True)
        
        # --- DOKONČNA REŠITEV ZA VRSTICO (BREZ st.columns) ---
        # Ustvarimo tri stolpce, a jih prisilimo v vrstico z novim CSS razredom
        c1, c2, c3 = st.columns([1, 1, 1])
        
        # Na iPhonu st.columns včasih še vedno prelamlja, zato uporabiva tole:
        with c1:
            if st.button("⬅️", key="prev"):
                if st.session_state.index > 0:
                    st.session_state.index -= 1
                    st.rerun()
        with c2:
            is_f = current_q in st.session_state.favorites
            if st.button("❤️" if is_f else "🤍", key="fav"):
                toggle_fav(current_q)
                st.rerun()
        with c3:
            if st.button("➡️", key="next"):
                st.session_state.index += 1
                st.rerun()

        # Prisilimo te tri gumbe v vrsto z uporabo CSS selektorja za točno to vrstico
        st.markdown("""
            <style>
            [data-testid="stHorizontalBlock"] {
                flex-direction: row !important;
                display: flex !important;
                flex-wrap: nowrap !important;
                justify-content: center !important;
            }
            [data-testid="column"] {
                width: 30% !important;
                flex: 1 1 30% !important;
                min-width: 0 !important;
            }
            </style>
            """, unsafe_allow_html=True)

        st.write("---")
        if st.button("🏠 MENI"):
            st.session_state.page = "main"
            st.rerun()
            
    else:
        trigger_custom_hearts()
        st.markdown("<h2 style='margin-top: 30px;'>Konec! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Domov"):
            st.session_state.page = "main"
            st.rerun()
