import streamlit as st
import pandas as pd
import random
import os


st.markdown("""
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Najina Pot", page_icon="❤️")

BG_COLOR = "#f5f2ee"      # (0.96, 0.93, 0.90)
CARD_COLOR = "#fff2f5"    # (1, 0.95, 0.96)
BTN_COLOR = "#f2bfc9"     # (0.95, 0.75, 0.80)
TEXT_COLOR = "#993366"    # (0.6, 0.2, 0.4)

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_COLOR}; }}
    h1, h2, h3, p {{ color: {TEXT_COLOR}; font-family: 'Comic Sans MS', cursive; }}
    .stButton>button {{
        background-color: {BTN_COLOR};
        color: {TEXT_COLOR};
        border-radius: 20px;
        border: none;
        font-weight: bold;
        width: 100%;
    }}
    .q-card {{
        background-color: {CARD_COLOR};
        padding: 40px;
        border-radius: 30px;
        border: 2px solid {BTN_COLOR};
        text-align: center;
        margin: 20px 0;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .q-text {{ font-size: 28px; color: {TEXT_COLOR}; font-weight: bold; }}
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
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            favs = [line.strip() for line in f.readlines() if line.strip()]
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
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        for fav in st.session_state.favorites:
            f.write(fav + "\n")

def toggle_fav(q):
    if q in st.session_state.favorites:
        st.session_state.favorites.remove(q)
    else:
        st.session_state.favorites.append(q)
    save_favorites()

# --- STRAN: GLAVNI MENI ---
if st.session_state.page == "main":
    st.markdown("<h1 style='text-align: center;'>ČAS ZA POGOVOR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>✨ Za povezanost na globji ravni ✨</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("IZBERI KATEGORIJO:")
    
    categories = sorted([c for c in questions.keys()])
    for cat in categories:
        if st.button(cat.upper()):
            st.session_state.category = cat
            st.session_state.page = "count_selection"
            st.rerun()
            
    if st.session_state.favorites:
        if st.button("⭐ PRILJUBLJENE", type="primary"):
            st.session_state.category = "PRILJUBLJENE"
            st.session_state.deck = st.session_state.favorites.copy()
            random.shuffle(st.session_state.deck)
            st.session_state.index = 0
            st.session_state.page = "game"
            st.rerun()

# --- STRAN: IZBIRA ŠTEVILA KARTIC ---
elif st.session_state.page == "count_selection":
    st.title(f"Kategorija: {st.session_state.category}")
    count_options = [5, 10, "Vse"]
    
    st.write("Koliko kartic želita vleči?")
    for opt in count_options:
        if st.button(f"Igraj {opt} kartic"):
            q_list = questions[st.session_state.category]
            n = len(q_list) if opt == "Vse" else opt
            st.session_state.deck = random.sample(q_list, min(n, len(q_list)))
            st.session_state.index = 0
            st.session_state.page = "game"
            st.rerun()
    
    if st.button("< Nazaj na kategorije"):
        st.session_state.page = "main"
        st.rerun()

# --- STRAN: IGRA (KARTICE) ---
elif st.session_state.page == "game":
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        
        st.write(f"**{st.session_state.category}** ({st.session_state.index + 1} / {len(st.session_state.deck)})")
        
        # Prikaz kartice
        st.markdown(f"""
            <div class="q-card">
                <p class="q-text">{current_q}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigacijski gumbi
        col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])
        
        with col1:
            if st.button("< Nazaj"):
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
        st.markdown("<h2 style='text-align: center;'>Prišla sta do konca! ❤️</h2>", unsafe_allow_html=True)
        if st.button("Nazaj na začetek", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()
