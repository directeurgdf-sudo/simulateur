import streamlit as st
from pathlib import Path

# ---------------- Config ----------------
st.set_page_config(page_title="Simulateur SAS", page_icon="🏡", layout="wide")

# ---------------- Styles ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700&display=swap');
* { font-family: 'Raleway', sans-serif; }

/* Sidebar verte */
section[data-testid="stSidebar"] { background:#4bab77 !important; }

/* Labels et titres de la sidebar en blanc */
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3, 
section[data-testid="stSidebar"] label {
  color:#fff !important;
}

/* Champs de saisie : texte noir + fond blanc */
section[data-testid="stSidebar"] input[type="text"],
section[data-testid="stSidebar"] input[type="number"],
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stNumberInput input {
  color:#1f2937 !important;   /* texte sombre */
  background:#ffffff !important;
  border-radius:10px;
}

/* Placeholder lisible */
section[data-testid="stSidebar"] ::placeholder {
  color:#6b7280 !important;   /* gris */
  opacity:1;
}

/* Boutons +/- des number_input */
section[data-testid="stSidebar"] .stNumberInput button {
  color:#1f2937 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Logo + titre ----------------
LOGO_CANDIDATES = [
    Path("assets/logo-gites-de-france.png"),
    Path("logo-gites-de-france.png"),
    Path("05_Logo_GITES DE FRANCE_100x100mm_3 Couleurs_RVB.png"),
]
logo_path = next((p for p in LOGO_CANDIDATES if p.exists()), None)

if logo_path:
    c1, c2 = st.columns([1, 4])
    with c1:
        st.image(str(logo_path), width=90)
    with c2:
        st.markdown("# 🏡 Simulateur des contributions à la SAS Gîtes de France")
else:
    st.markdown("# 🏡 Simulateur des contributions à la SAS Gîtes de France")

# ---------------- Entrées ----------------
st.sidebar.header("✍️ Remplissez")
A = st.sidebar.number_input(
    "Votre parc d'annonces en SR (exclusivités)", min_value=0.0, step=1.0, value=674.0
)
B = st.sidebar.number_input(
    "Votre parc d'annonces en RP/PP (partagés)", min_value=0.0, step=1.0, value=567.0
)
C = st.sidebar.number_input(
    "TOTAL des Loyers propriétaires (€)",
    min_value=0.0,
    step=1000.0,
    value=2_642_740.90,
    format="%.2f",
)
F = st.sidebar.number_input(
    "Votre contribution volontaire à la campagne de marque (€)",
    min_value=0.0,
    step=100.0,
    value=10_000.0,
    format="%.2f",
)

# ---------------- Fonction format euro ----------------
def euro(x: float) -> str:
    return f"{x:,.2f}".replace(",", " ").replace(".", ",")

# ---------------- Calculs ----------------
# Modèle actuel (E,F,G,H)
E = (A * 20) + (B * 30)  # contributions forfaitaires
Fv = F                   # contribution volontaire
G = C * 0.0084           # 0,84 %
H = E + Fv + G           # total actuel

# Modèle 2026 (J,K,L,M)
J = (A * 20) + (B * 30)
K = 0.0
L = C * 0.0114           # 1,14 %
M = J + K + L

# Différence
O = M - H
dE, dF, dG, dH = (J - E), (K - Fv), (L - G), O

# ---------------- Affichage en 3 colonnes ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📘 Modèle actuel")
    st.metric("Contributions forfaitaires", euro(E))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(Fv))
    st.metric("Contribution sur les loyers 0,84%", euro(G))
    st.divider()
    st.metric("TOTAL", euro(H))

with col2:
    st.subheader("📗 Modèle 2026")
    st.metric("Contributions forfaitaires", euro(J))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(K))
    st.metric("Contribution sur les loyers 1,14%", euro(L))
    st.divider()
    st.metric("TOTAL", euro(M))

with col3:
    st.subheader("📙 Différence (2026 – actuel)")
    st.metric("Δ Contributions forfaitaires", euro(dE))
    st.metric("Δ Contribution volontaire (inclus)", euro(dF))
    st.metric("Δ Contribution loyers", euro(dG))
    st.divider()
    st.metric("Δ TOTAL", euro(dH))
