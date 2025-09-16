import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Simulateur SAS", page_icon="🏡", layout="wide")

# Police + sidebar verte uniquement (pas d'autres styles)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700&display=swap');
* { font-family: 'Raleway', sans-serif; }
section[data-testid="stSidebar"] { background:#4bab77 !important; }
section[data-testid="stSidebar"] * { color:#fff !important; }
</style>
""", unsafe_allow_html=True)

# Logo si dispo, sinon titre seul
LOGO_CANDIDATES = [
    Path("assets/logo-gites-de-france.png"),
    Path("logo-gites-de-france.png"),
    Path("05_Logo_GITES DE FRANCE_100x100mm_3 Couleurs_RVB.png"),
]
logo_path = next((p for p in LOGO_CANDIDATES if p.exists()), None)

if logo_path:
    c1, c2 = st.columns([1,4])
    with c1: st.image(str(logo_path), width=90)
    with c2
