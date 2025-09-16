import streamlit as st
from pathlib import Path
import re

# ---------------- Config ----------------
st.set_page_config(page_title="Simulateur SAS", page_icon="🏡", layout="wide")

# ---------------- Styles ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700&display=swap');
* { font-family: 'Raleway', sans-serif; }

/* Sidebar verte */
section[data-testid="stSidebar"] { background:#4bab77 !important; }

/* Labels sidebar en blanc */
section[data-testid="stSidebar"] label { color:#fff !important; }

/* Champs de saisie : texte noir + fond blanc */
section[data-testid="stSidebar"] input[type="text"],
section[data-testid="stSidebar"] input[type="number"],
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stNumberInput input {
  color:#1f2937 !important;
  background:#ffffff !important;
  border-radius:10px;
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
        st.markdown("# Simulateur des contributions à la SAS Gîtes de France")
else:
    st.markdown("# Simulateur des contributions à la SAS Gîtes de France")

st.markdown(" ")  # saut de ligne après le titre

# ---------------- Utilitaires ----------------
def euro(x: float) -> str:
    """Format 1 234 567,89"""
    return f"{x:,.2f}".replace(",", " ").replace(".", ",")

def thousands(n: int) -> str:
    """1 234 567"""
    return f"{n:,}".replace(",", " ")

def parse_int(txt: str, fallback: int) -> int:
    """Conserve uniquement les chiffres ; fallback si vide/incorrect."""
    if txt is None:
        return fallback
    digits = re.sub(r"[^\d]", "", str(txt))
    try:
        return int(digits) if digits != "" else fallback
    except ValueError:
        return fallback

def sidebar_number_with_grouping(label: str, default: int) -> int:
    """Text input en sidebar avec séparateurs de milliers visibles."""
    shown = thousands(default)
    entered = st.sidebar.text_input(label, value=shown)
    val = parse_int(entered, default)
    # réécrit la valeur formatée si l'utilisateur l'a modifiée sans espaces
    # (pas obligatoire, mais garde un affichage propre aux prochains reruns)
    return val

# ---------------- Entrées (avec séparateurs de milliers) ----------------
st.sidebar.header("✍️ Remplissez")
A = sidebar_number_with_grouping("Votre parc d'annonces en SR (exclusivités)", 650)
B = sidebar_number_with_grouping("Votre parc d'annonces en RP/PP (partagés)", 300)
C = sidebar_number_with_grouping("TOTAL des Loyers propriétaires (€)", 4_000_000)
F = sidebar_number_with_grouping("Votre contribution volontaire à la campagne de marque (€)", 15_000)

# ---------------- Calculs ----------------
# Modèle actuel
E = (A * 20) + (B * 30)   # contributions forfaitaires
Fv = float(F)             # contribution volontaire (inclus)
G = float(C) * 0.0084     # 0,84 %
H = E + Fv + G            # total actuel

# Modèle 2026
J = (A * 20) + (B * 30)
K = 0.0
L = float(C) * 0.0114     # 1,14 %
M = J + K + L

# Différence
O = M - H
dE, dF, dG, dH = (J - E), (K - Fv), (L - G), O

# ---------------- Affichage en 3 colonnes ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Modèle actuel")
    st.metric("Contributions forfaitaires", euro(E))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(Fv))
    st.metric("Contribution sur les loyers 0,84%", euro(G))
    st.divider()
    st.metric("TOTAL", euro(H))

with col2:
    st.subheader("Modèle 2026")
    st.metric("Contributions forfaitaires", euro(J))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(K))
    st.metric("Contribution sur les loyers 1,14%", euro(L))
    st.divider()
    st.metric("TOTAL", euro(M))

with col3:
    st.subheader("Différence (2026 – actuel)")
    st.metric("Écart contributions forfaitaires", euro(dE))
    st.metric("Écart contribution volontaire", euro(dF))
    st.metric("Écart contribution loyers", euro(dG))
    st.divider()
    st.metric("Écart total", euro(dH))
