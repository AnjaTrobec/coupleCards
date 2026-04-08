import streamlit as st
import pandas as pd
import random

# 1. KONFIGURACIJA STRANI
st.set_page_config(page_title="Najina Pot", page_icon="❤️", layout="wide")

# 2. DEFINICIJA BARV IN STILA
BG_COLOR = "#f5f2ee"      
CARD_COLOR = "#fff2f5"    
BTN_COLOR = "#f2bfc9"     
TEXT_COLOR = "#993366"    

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
    
    .stApp {{ background-color: {BG_COLOR}; }}
    
    .block-container {{ 
        max-width: 800px !important; 
        padding: 0 !important; 
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
    
    [data-testid="stVerticalBlock"] > div {{
        display: flex !important; 
        flex-direction: column !important;
        align-items: center !important; 
        justify-content: center !important; 
        width: 100% !important;
    }}
    
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
    
    .q-card {{
        background-color: {CARD_COLOR}; 
        padding: 30px; 
        border-radius: 30px;
        border: 2px solid {BTN_COLOR}; 
        text-align: center; 
        margin: 15px auto;
        min-height: 250px; 
        max-width: 500px; 
        display: flex;
        align-items: center; 
        justify-content: center;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.03);
    }}
    
    /* Skrije privzete Streamlit elemente */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# 3. NALAGANJE PODATKOV
@st.cache_data
def load_questions():
    try:
        # Naloži CSV in očisti imena stolpcev
        df = pd.read_csv("cards.csv", encoding="utf-8")
        df.columns = df.columns.str.strip()
        
        # Slovar po kategorijah
        data = df.groupby("EDITION")["QUESTION"].apply(list).to_dict()
        # Seznam vseh vprašanj za MIX
        all_q = df["QUESTION"].tolist()
        return data, all_q
    except Exception as e:
        st.error(f"Napaka pri branju datoteke cards.csv: {e}")
        return {}, []

questions_dict, all_questions_list = load_questions()

# 4. SHRANJEVANJE STANJA (Session State)
if 'page' not in st.session_state: st.session_state.page = "main"
if 'index' not in st.session_state: st.session_state.index = 0
if 'deck' not in st.session_state: st.session_state.deck = []
if 'category' not in st.session_state: st.session_state.category = ""

# Animacija srčkov ob koncu
def trigger_custom_hearts():
    heart_html = ""
    for i in range(25):
        left = random.randint(0, 100)
        delay = random.uniform(0, 3)
        heart_html += f'<div style="position:fixed; left:{left}%; bottom:-50px; font-size:35px; animation: hearts-fly 4s {delay}s linear forwards; z-index:9999;">❤️</div>'
    
    st.markdown(f"""
        <style>
        @keyframes hearts-fly {{
            0% {{bottom:-50px; opacity:1;}}
            100% {{bottom:110vh; opacity:0;}}
        }}
        </style>
        {heart_html}
    """, unsafe_allow_html=True)

# --- STRANI APLIKACIJE ---

# STRAN 1: Glavni meni
if st.session_state.page == "main":
    st.markdown('<div class="header-section"><h1>ČAS ZA POGOVOR</h1><p>✨ Za povezanost na globlji ravni ✨</p></div>', unsafe_allow_html=True)
    st.markdown("## IZBERI KATEGORIJO:")
    
    # Izpis kategorij iz CSV
    for cat in sorted(questions_dict.keys()):
        if st.button(cat.upper(), key=f"cat_{cat}"):
            st.session_state.category = cat
            st.session_state.page = "count_selection"
            st.rerun()
            
    st.markdown("---")
    # Gumb za Naključni Mix
    if st.button("🎲 NAKLJUČNI MIX", key="btn_mix"):
        st.session_state.category = "NAKLJUČNI MIX"
        st.session_state.page = "count_selection"
        st.rerun()

# STRAN 2: Izbira števila vprašanj
elif st.session_state.page == "count_selection":
    st.markdown(f'<div class="header-section"><h1>{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    st.markdown("### Koliko kartic želita?")
    
    # Določitev nabora vprašanj
    if st.session_state.category == "NAKLJUČNI MIX":
        pool = all_questions_list
    else:
        pool = questions_dict.get(st.session_state.category, [])

    # Možnosti za izbor
    options = {"1 na hitro": 1, "5": 5, "10": 10}
    
    for label, count in options.items():
        if st.button(label, key=f"count_{label}"):
            # Naključna izbira brez ponavljanja
            st.session_state.deck = random.sample(pool, min(count, len(pool)))
            st.session_state.index = 0
            st.session_state.page = "game"
            st.rerun()
            
    if st.button("🏠 NAZAJ"):
        st.session_state.page = "main"
        st.rerun()

# STRAN 3: Igra s karticami
elif st.session_state.page == "game":
    st.markdown(f'<div class="header-section"><h1>{st.session_state.category}</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.index < len(st.session_state.deck):
        current_q = st.session_state.deck[st.session_state.index]
        
        st.write(f"Kartica {st.session_state.index + 1} od {len(st.session_state.deck)}")
        st.markdown(f'<div class="q-card"><p style="font-size: 28px; font-weight: bold; line-height: 1.4;">{current_q}</p></div>', unsafe_allow_html=True)
        
        # Dinamični gumbi (prikazani le, ko so smiselni)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.index > 0:
                if st.button("⬅️"):
                    st.session_state.index -= 1
                    st.rerun()
            else:
                st.write("") # Ohranja poravnavo desnega gumba

        with col2:
            is_last = st.session_state.index == len(st.session_state.deck) - 1
            label = "Konec igre" if is_last else "➡️"
            if st.button(label):
                st.session_state.index += 1
                st.rerun()

        st.markdown("---")
        if st.button("🏠 KONČAJ"):
            st.session_state.page = "main"
            st.rerun()
            
    else:
        # Konec igre
        trigger_custom_hearts()
        st.markdown("<h2 style='margin-top: 50px;'>Prišla sta do konca! ❤️</h2>", unsafe_allow_html=True)
        st.markdown("<p><i>Odnos ne raste tam, kjer sta si dva v vsem podobna, ampak tam, kjer se varno pogovarjata o vsem, v čemer sta si različna.</i></p>", unsafe_allow_html=True)
        if st.button("🏠 NAZAJ NA ZAČETEK"):
            st.session_state.page = "main"
            st.rerun()
