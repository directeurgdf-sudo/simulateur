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
section[data-testid="stSidebar"] * { color:#fff !important; }

/* Cards blanches (pas de fonds colorés -> pas de "barres") */
.card {
  background: #fff;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 6px 18px rgba(0,0,0,.08);
  margin-bottom: 20px;
  border: 1px solid rgba(0,0,0,.06);
}
.card h3 { margin-top: 0; font-weight: 700; }
.card hr { border: none; border-top:1px solid rgba(0,0,0,.08); margin:14px 0; }

/* Bordure gauche colorée pour différencier les 3 colonnes */
.card.actual { border-left: 8px solid #4da3ff; }  /* bleu */
.card.future { border-left: 8px solid #62c787; }  /* vert */
.card.diff   { border-left: 8px solid #ffa85c; }  /* orange */

/* Sécurité : annule tout éventuel fond résiduel */
.card.actual, .card.future, .card.diff { background: #fff !important; }
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
    col_logo, col_title = st.columns([1,4])
    with col_logo:
        st.image(str(logo_path), width=90)
    with col_title:
        st.markdown("# 🏡 Simulateur des contributions à la SAS Gîtes de France")
else:
    st.markdown("# 🏡 Simulateur des contributions à la SAS Gîtes de France")

# ---------------- Entrées ----------------
st.sidebar.header("✍️ Remplissez")
A = st.sidebar.number_input("Votre parc d'annonces en SR (exclusivités)", min_value=0.0, step=1.0, value=674.0)
B = st.sidebar.number_input("Votre parc d'annonces en RP/PP (partagés)",   min_value=0.0, step=1.0, value=567.0)
C = st.sidebar.number_input("TOTAL des Loyers propriétaires (€)",           min_value=0.0, step=1000.0, value=2_642_740.90, format="%.2f")
F = st.sidebar.number_input("Votre contribution volontaire à la campagne de marque (€)", min_value=0.0, step=100.0, value=10_000.0, format="%.2f")

def euro(x: float) -> str:
    return f"{x:,.2f}".replace(",", " ").replace(".", ",")

# ---------------- Calculs ----------------
# Modèle actuel (E,F,G,H)
E = (A * 20) + (B * 30)
Fv = F
G = C * 0.0084
H = E + Fv + G

# Modèle 2026 (J,K,L,M)
J = (A * 20) + (B * 30)
K = 0.0
L = C * 0.0114
M = J + K + L

# Différence
O       = M - H
dE, dF, dG, dH = (J-E), (K-Fv), (L-G), (O)

# ---------------- Affichage en 3 colonnes ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card actual">', unsafe_allow_html=True)
    st.markdown("### 📘 Modèle actuel")
    st.metric("Contributions forfaitaires", euro(E))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(Fv))
    st.metric("Contribution sur les loyers 0,84%", euro(G))
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.metric("TOTAL", euro(H))
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card future">', unsafe_allow_html=True)
    st.markdown("### 📗 Modèle 2026")
    st.metric("Contributions forfaitaires", euro(J))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(K))
    st.metric("Contribution sur les loyers 1,14%", euro(L))
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.metric("TOTAL", euro(M))
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card diff">', unsafe_allow_html=True)
    st.markdown("### 📙 Différence (2026 – actuel)")
    st.metric("Δ Contributions forfaitaires", euro(dE))
    st.metric("Δ Contribution volontaire (inclus)", euro(dF))
    st.metric("Δ Contribution loyers", euro(dG))
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.metric("Δ TOTAL", euro(dH))
    st.markdown("</div>", unsafe_allow_html=True)
