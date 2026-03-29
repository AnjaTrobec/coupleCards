import streamlit as st
import pandas as pd
import random
import os

# --- KONFIGURACIJA STRANI ---
st.set_page_config(page_title="Najina Pot", page_icon="❤️")

# Meta oznake za iPhone "App" način
# --- CSS STIL (Popravek za polno širino in gumbe) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    /* Prisili Streamlit vsebino, da uporabi 100% širine */
    .block-container {{
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    .stApp {{ 
        background-color: {BG_COLOR}; 
    }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, button {{
        font-family: 'Patrick Hand', cursive !important;
        color: {TEXT_COLOR};
    }}

    /* Gumbi čez celo vrstico */
    .stButton {{
        width: 100%;
    }}

    .stButton>button {{
        background-color: {BTN_COLOR};
        color: {TEXT_COLOR};
        border-radius: 20px;
        border: none;
        font-weight: bold;
        width: 100% !important;
        min-width: 100% !important;
        display: block !important;
        margin: 10px 0 !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 26px !important;
        padding: 15px !important;
    }}

    /* Kartica z vprašanjem */
    .q-card {{
        background-color: {CARD_COLOR};
        padding: 40px;
        border-radius: 30px;
        border: 2px solid {BTN_COLOR};
        text-align: center;
        margin: 20px 0;
        min-height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }}

    .q-text {{ 
        font-size: 32px !important; 
        color: {TEXT_COLOR}; 
        font-weight: bold;
        font-family: 'Patrick Hand', cursive !important;
    }}
    </style>
    """, unsafe_allow_html=True)

FAVORITES_FILE = "favorites.txt"

# --- NALAGANJE PODATKOV ---
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

# --- INITIALIZE SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "main"
if 'index' not in st.session_state: st.session_state.index = 0
if 'deck' not in st.session_state: st.session_state.deck = []
if 'category' not in st.session_state: st.session_state.category = ""
if 'favorites' not in st.session_state: st.session_state.favorites = favorites

# --- FUNKCIJE ---
def save_favorites():
    try:
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            for fav in st.session_state.favorites:
                f.write(fav + "\n")
    except:
        pass

def toggle_fav(q):
    if q in st.session_state.favorites:
        st.session_state.favorites.remove(q)
    else:
        st.session_state.favorites.append(q)
    save_favorites()

# --- STRAN: GLAVNI MENI ---
if st.session_state.page == "main":
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>ČAS ZA POGOVOR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 24px;'>✨ Za povezanost na globlji ravni ✨</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # VEČJI NASLOV ZA KATEGORIJE
    st.markdown(f"<h2 style='text-align: center; color: {TEXT_COLOR}; font-size: 40px;'>IZBERI KATEGORIJO:</h2>", unsafe_allow_html=True)
    
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

# --- STRAN: IZBIRA ŠTEVILA KARTIC ---
elif st.session_state.page == "count_selection":
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.category}</h1>", unsafe_allow_html=True)
    count_options = [5, 10, "Vse"]
    
    st.markdown("<p style='text-align: center; font-size: 24px;'>Koliko kartic želita vleči?</p>", unsafe_allow_html=True)
    for opt in count_options:
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

# --- STRAN: IGRA (KARTICE) ---
elif st.session_state.page == "game":
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        
        st.markdown(f"<p style='text-align: center; font-size: 22px;'><b>{st.session_state.category}</b> ({st.session_state.index + 1} / {len(st.session_state.deck)})</p>", unsafe_allow_html=True)
        
        # Prikaz kartice
        st.markdown(f"""
            <div class="q-card">
                <p class="q-text">{current_q}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigacijski gumbi v eni vrstici
        col1, col2, col3, col4 = st.columns([1, 1, 0.6, 1.2])
        
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
    else:
        st.balloons()
        st.markdown("<h2 style='text-align: center; font-size: 40px;'>Prišla sta do konca! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Nazaj na začetek"):
            st.session_state.page = "main"
            st.rerun()
