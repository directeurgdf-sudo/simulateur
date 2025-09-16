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

/* Grille des modèles */
.models { display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 10px; }

/* Cartes */
.card { border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 18px rgba(0,0,0,.08); }
.card h3 { margin: 0 0 8px 0; font-weight: 700; }
.item { margin: 10px 0 6px; color: rgba(0,0,0,.70); font-size: 0.95rem; }
.val { font-size: 1.8rem; font-weight: 700; color: #172b4d; }

/* Couleurs par colonne */
.card.actual { background: #eef7ff; }    /* bleu très clair */
.card.future { background: #eefcf0; }    /* vert très clair */
.card.diff   { background: #fff3e8; }    /* orange très clair */

/* En-tête titre + logo */
.header { display:flex; align-items:center; gap:14px; margin-bottom: 8px; }
.header img { width:72px; height:auto; }

hr { border: none; border-top: 1px solid #e9ecef; margin: 18px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------- Logo + titre ----------------
LOGO_CANDIDATES = [
    Path("assets/logo-gites-de-france.png"),
    Path("logo-gites-de-france.png"),
    Path("05_Logo_GITES DE FRANCE_100x100mm_3 Couleurs_RVB.png"),
]
logo_path = next((p for p in LOGO_CANDIDATES if p.exists()), None)

st.markdown('<div class="header">{}<h1>Simulateur des contributions à la SAS Gîtes de France</h1></div>'.format(
    f'<img src="{logo_path.as_posix()}"/>' if logo_path else ""
), unsafe_allow_html=True)

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
E = (A * 20) + (B * 30)      # contributions forfaitaires
Fv = F                       # contribution volontaire (inclus)
G = C * 0.0084               # 0,84%
H = E + Fv + G               # total actuel

# Modèle 2026 (J,K,L,M)
J = (A * 20) + (B * 30)
K = 0.0
L = C * 0.0114               # 1,14%
M = J + K + L

# Différence
O       = M - H
dE, dF, dG, dH = (J-E), (K-Fv), (L-G), (O)

# ---------------- Cartes ----------------
st.markdown('<div class="models">', unsafe_allow_html=True)

# Carte 1 — Modèle actuel
st.markdown(f"""
<div class="card actual">
  <h3>📘 Modèle actuel</h3>
  <div class="item">Contributions forfaitaires</div>
  <div class="val">{euro(E)}</div>
  <div class="item">Contribution volontaire à la campagne de Marque (inclus)</div>
  <div class="val">{euro(Fv)}</div>
  <div class="item">Contribution sur les loyers 0,84%</div>
  <div class="val">{euro(G)}</div>
  <hr/>
  <div class="item">TOTAL</div>
  <div class="val">{euro(H)}</div>
</div>
""", unsafe_allow_html=True)

# Carte 2 — Modèle 2026
st.markdown(f"""
<div class="card future">
  <h3>📗 Modèle 2026</h3>
  <div class="item">Contributions forfaitaires</div>
  <div class="val">{euro(J)}</div>
  <div class="item">Contribution volontaire à la campagne de Marque (inclus)</div>
  <div class="val">{euro(K)}</div>
  <div class="item">Contribution sur les loyers 1,14%</div>
  <div class="val">{euro(L)}</div>
  <hr/>
  <div class="item">TOTAL</div>
  <div class="val">{euro(M)}</div>
</div>
""", unsafe_allow_html=True)

# Carte 3 — Différence
st.markdown(f"""
<div class="card diff">
  <h3>📙 Différence (2026 – actuel)</h3>
  <div class="item">Δ Contributions forfaitaires</div>
  <div class="val">{euro(dE)}</div>
  <div class="item">Δ Contribution volontaire (inclus)</div>
  <div class="val">{euro(dF)}</div>
  <div class="item">Δ Contribution loyers</div>
  <div class="val">{euro(dG)}</div>
  <hr/>
  <div class="item">Δ TOTAL</div>
  <div class="val">{euro(dH)}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
