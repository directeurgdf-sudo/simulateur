import streamlit as st

# ---------- Configuration ----------
st.set_page_config(page_title="Simulateur SAS", page_icon="🏡", layout="wide")

# ---------- Style global : police Raleway + sidebar verte ----------
st.markdown(
    """
    <style>
    * {
        font-family: 'Raleway', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #4bab77 !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Logo + Titre ----------
col_logo, col_title = st.columns([1,4])
with col_logo:
    st.image("05_Logo_GITES DE FRANCE_100x100mm_3 Couleurs_RVB.png", width=100)
with col_title:
    st.markdown("# 🏡 Simulateur des contributions à la SAS Gîtes de France")

# ---------- Entrées ----------
st.sidebar.header("✍️ Remplissez")
A = st.sidebar.number_input("Votre parc d'annonces en SR (exclusivités)", min_value=0.0, step=1.0, value=674.0)
B = st.sidebar.number_input("Votre parc d'annonces en RP/PP (partagés)", min_value=0.0, step=1.0, value=567.0)
C = st.sidebar.number_input("TOTAL des Loyers propriétaires (€)", min_value=0.0, step=1000.0, value=2_642_740.90, format="%.2f")
F = st.sidebar.number_input("Contribution volontaire à la campagne de Marque (inclus) (€)", min_value=0.0, step=100.0, value=10_000.0, format="%.2f")

def fmt(val: float) -> str:
    return f"{val:,.2f}".replace(",", " ").replace(".", ",")

# ---------- Calculs modèle ACTUEL ----------
E = (A * 20) + (B * 30)  # contributions forfaitaires
Fv = F
G = C * 0.0084
H = E + Fv + G

# ---------- Calculs modèle 2026 ----------
J = (A * 20) + (B * 30)
K = 0.0
L = C * 0.0114
M = J + K + L

# ---------- Différence ----------
O = M - H

st.divider()

# ---------- Résultats ----------
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### 📘 Modèle actuel")
    st.metric("Contributions forfaitaires", fmt(E))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", fmt(Fv))
    st.metric("Contribution sur les loyers 0,84%", fmt(G))
    st.metric("TOTAL", fmt(H))

with col_b:
    st.markdown("### 📗 Modèle 2026")
    st.metric("Contributions forfaitaires", fmt(J))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", fmt(K))
    st.metric("Contribution sur les loyers 1,14%", fmt(L))
    st.metric("TOTAL", fmt(M))

with col_c:
    st.markdown("### 📙 Différence (2026 – actuel)")
    st.metric("Δ Contributions forfaitaires", fmt(J - E))
    st.metric("Δ Contribution volontaire (inclus)", fmt(K - Fv))
    st.metric("Δ Contribution loyers", fmt(L - G))
    st.metric("Δ TOTAL", fmt(O))
