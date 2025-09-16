import streamlit as st
import pandas as pd

# --- CONFIG PAGE ---
st.set_page_config(page_title="Simulateur SAS Gîtes de France", layout="wide")

# --- STYLE CSS ---
st.markdown("""
<style>
    body, input, label {
        font-family: 'Raleway', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #4bab77;
        color: white;
    }
    .stNumberInput label, .stTextInput label {
        color: white !important;
    }
    .pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin-bottom: 18px;
    }
    .pill-green { background-color: #4bab77; color: white; }
    .pill-outline { border: 2px solid #4bab77; color: black; background: transparent; }
    .big-val {
        font-size: 1.6rem;
        line-height: 1.3;
        color:#111827;
        margin: 2px 0 14px;
    }
    hr {
        border: none;
        border-top: 1px solid #ddd;
        margin: 14px 0;
    }
    .accent {
        color: #4bab77;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.markdown("<h1 style='text-align:center; margin-bottom:40px;'>Simulateur des contributions à la SAS Gîtes de France</h1>", unsafe_allow_html=True)

# --- INPUTS ---
st.sidebar.markdown("### 📝 Remplissez")

nb_gites_sr = st.sidebar.number_input("Votre parc d'annonces en SR (exclusivités)", min_value=0, value=650, step=1, format="%d")
nb_gites_rp = st.sidebar.number_input("Votre parc d'annonces en RP/PP (partagés)", min_value=0, value=300, step=1, format="%d")
total_loyers = st.sidebar.number_input("TOTAL des Loyers propriétaires (€)", min_value=0, value=4000000, step=1000, format="%d")
contrib_volontaire = st.sidebar.number_input("Votre contribution volontaire à la campagne de marque (€)", min_value=0, value=15000, step=500, format="%d")

# --- CALCULS ---
actuel_forfait = 22000
actuel_volontaire = contrib_volontaire
actuel_loyers = total_loyers * 0.0084
actuel_total = actuel_forfait + actuel_volontaire + actuel_loyers

nv_forfait = 22000
nv_volontaire = 0
nv_loyers = total_loyers * 0.0114
nv_total = nv_forfait + nv_volontaire + nv_loyers

diff_forfait = nv_forfait - actuel_forfait
diff_volontaire = nv_volontaire - actuel_volontaire
diff_loyers = nv_loyers - actuel_loyers
diff_total = nv_total - actuel_total

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
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("TOTAL")
    st.markdown(f"<div class='big-val'>{actuel_total:,.0f}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='pill pill-green'>Proposition de modèle 2026</div>", unsafe_allow_html=True)
    st.write("Contributions forfaitaires")
    st.markdown(f"<div class='big-val'>{nv_forfait:,.0f}</div>", unsafe_allow_html=True)
    st.write("Contribution à la campagne de Marque <span class='accent'>(inclus)</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{nv_volontaire:,.0f}</div>", unsafe_allow_html=True)
    st.write(f"Contribution sur les loyers <span class='accent'>1,14 %</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{nv_loyers:,.0f}</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("TOTAL")
    st.markdown(f"<div class='big-val'>{nv_total:,.0f}</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='pill pill-outline'>Différence (2026 – actuel)</div>", unsafe_allow_html=True)
    st.write("Écart contributions forfaitaires")
    st.markdown(f"<div class='big-val'>{diff_forfait:,.0f}</div>", unsafe_allow_html=True)
    st.write("Écart contribution à la campagne")
    st.markdown(f"<div class='big-val'>{diff_volontaire:,.0f}</div>", unsafe_allow_html=True)
    st.write("Écart contribution loyers")
    st.markdown(f"<div class='big-val'>{diff_loyers:,.0f}</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("ÉCART TOTAL")
    color = "red" if diff_total > 0 else "#4bab77"
    st.markdown(f"<div class='big-val' style='color:{color};'>{diff_total:,.0f}</div>", unsafe_allow_html=True)
