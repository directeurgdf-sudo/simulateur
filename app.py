import streamlit as st
import pandas as pd

# --- CONFIG PAGE ---
st.set_page_config(page_title="Simulateur SAS Gîtes de France", layout="wide")

# --- CSS STYLE ---
st.markdown("""
<style>
/* Police générale */
html, body, [class*="css"] {
    font-family: 'Raleway', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #4bab77;
}
section[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] input {
    color: black !important;
}

/* Titre principal */
h1 {
    margin-top: -20px;   /* rapproche du haut */
    margin-bottom: 30px; /* espace avec les modèles */
}

/* Pills */
.pill {
    display:inline-block;
    padding:6px 18px;
    border-radius:20px;
    font-weight:600;
    margin-bottom:20px;
}
.pill-green {background:#4bab77; color:white;}
.pill-outline {border:2px solid #4bab77; color:#111827;}

/* Valeurs uniformes */
.big-val {
    font-size:1.6rem;        /* taille homogène */
    line-height:1.3;
    color:#111827;
    margin:2px 0 14px;
}

/* Accent vert pour les taux et "inclus" */
.accent {
    color:#4bab77;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.title("Simulateur des contributions à la SAS Gîtes de France")

# --- ENTRÉES ---
st.sidebar.markdown("### 🍏 Remplissez")

nb_sr = st.sidebar.number_input("Votre parc d'annonces en SR (exclusivités)", min_value=0, value=650, step=1, format="%d")
nb_rp = st.sidebar.number_input("Votre parc d'annonces en RP/PP (partagés)", min_value=0, value=300, step=1, format="%d")
loyers = st.sidebar.number_input("TOTAL des Loyers propriétaires (€)", min_value=0, value=4000000, step=1000, format="%d")
volontaire = st.sidebar.number_input("Votre contribution volontaire à la campagne de marque (€)", min_value=0, value=15000, step=100, format="%d")

# --- CALCULS ---
actuel_forfait = 22000
actuel_volontaire = volontaire
actuel_loyers = loyers * 0.0084
actuel_total = actuel_forfait + actuel_volontaire + actuel_loyers

mod2026_forfait = 22000
mod2026_volontaire = 0
mod2026_loyers = loyers * 0.0114
mod2026_total = mod2026_forfait + mod2026_volontaire + mod2026_loyers

diff_forfait = mod2026_forfait - actuel_forfait
diff_volontaire = mod2026_volontaire - actuel_volontaire
diff_loyers = mod2026_loyers - actuel_loyers
diff_total = mod2026_total - actuel_total

# --- AFFICHAGE ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='pill pill-green'>Modèle actuel</div>", unsafe_allow_html=True)
    st.write("Contributions forfaitaires")
    st.markdown(f"<div class='big-val'>{actuel_forfait:,.0f}</div>", unsafe_allow_html=True)
    st.write("Contribution à la campagne de Marque")
    st.markdown(f"<div class='big-val'>{actuel_volontaire:,.0f}</div>", unsafe_allow_html=True)
    st.write(f"Contribution sur les loyers <span class='accent'>0,84 %</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{actuel_loyers:,.0f}</div>", unsafe_allow_html=True)
    st.write("TOTAL")
    st.markdown(f"<div class='big-val'>{actuel_total:,.0f}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='pill pill-green'>Proposition de modèle 2026</div>", unsafe_allow_html=True)
    st.write("Contributions forfaitaires")
    st.markdown(f"<div class='big-val'>{mod2026_forfait:,.0f}</div>", unsafe_allow_html=True)
    st.write("Contribution à la campagne de Marque <span class='accent'>(inclus)</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{mod2026_volontaire:,.0f}</div>", unsafe_allow_html=True)
    st.write(f"Contribution sur les loyers <span class='accent'>1,14 %</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{mod2026_loyers:,.0f}</div>", unsafe_allow_html=True)
    st.write("TOTAL")
    st.markdown(f"<div class='big-val'>{mod2026_total:,.0f}</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='pill pill-outline'>Différence (2026 – actuel)</div>", unsafe_allow_html=True)
    st.write("Écart contributions forfaitaires")
    st.markdown(f"<div class='big-val'>{diff_forfait:,.0f}</div>", unsafe_allow_html=True)
    st.write("Écart contribution à la campagne")
    st.markdown(f"<div class='big-val'>{diff_volontaire:,.0f}</div>", unsafe_allow_html=True)
    st.write("Écart contribution loyers")
    st.markdown(f"<div class='big-val'>{diff_loyers:,.0f}</div>", unsafe_allow_html=True)
    st.write("ÉCART TOTAL")
    couleur = "#d33" if diff_total > 0 else "#4bab77"
    st.markdown(f"<div class='big-val' style='color:{couleur}'>{diff_total:,.0f}</div>", unsafe_allow_html=True)
