import streamlit as st
from pathlib import Path
import re

# ---------------- Config ----------------
st.set_page_config(page_title="Simulateur SAS", page_icon="🏡", layout="wide")

# ---------------- Styles ----------------
BRAND_GREEN = "#4bab77"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700&display=swap');
* {{ font-family: 'Raleway', sans-serif; }}

/* Sidebar verte */
section[data-testid="stSidebar"] {{ background:{BRAND_GREEN} !important; }}
section[data-testid="stSidebar"] label {{ color:#fff !important; }}

/* Champs sidebar lisibles */
section[data-testid="stSidebar"] input[type="text"],
section[data-testid="stSidebar"] input[type="number"],
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stNumberInput input {{
  color:#1f2937 !important;
  background:#ffffff !important;
  border-radius:10px;
}}

/* Pills (sous-titres) */
.pill {{
  display:inline-block; background:{BRAND_GREEN}; color:#fff;
  padding:10px 14px; border-radius:20px; font-weight:700; font-size:1.05rem;
}}

/* Accent (pour les % verts + gras) */
.accent {{ color:{BRAND_GREEN}; font-weight:700; }}

/* Valeur colorée pour l'écart total */
.value-pos {{ color:#e03a3a; font-weight:700; font-size:2rem; }}
.value-neg {{ color:{BRAND_GREEN}; font-weight:700; font-size:2rem; }}
.label-small {{ color:#6b7280; text-transform:uppercase; letter-spacing:.04em; font-size:.9rem; }}
.hr {{ border-top:1px solid #e5e7eb; margin:16px 0; }}
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
    return f"{n:,}".replace(",", " ")

def parse_int(txt: str, fallback: int) -> int:
    if txt is None:
        return fallback
    digits = re.sub(r"[^\d]", "", str(txt))
    try:
        return int(digits) if digits != "" else fallback
    except ValueError:
        return fallback

def sidebar_number_with_grouping(label: str, default: int) -> int:
    shown = thousands(default)
    entered = st.sidebar.text_input(label, value=shown)
    return parse_int(entered, default)

# ---------------- Entrées ----------------
st.sidebar.header("✍️ Remplissez")
A = sidebar_number_with_grouping("Votre parc d'annonces en SR (exclusivités)", 650)
B = sidebar_number_with_grouping("Votre parc d'annonces en RP/PP (partagés)", 300)
C = sidebar_number_with_grouping("TOTAL des Loyers propriétaires (€)", 4_000_000)
F = sidebar_number_with_grouping("Votre contribution volontaire à la campagne de marque (€)", 15_000)

# ---------------- Calculs ----------------
# Modèle actuel
E = (A * 20) + (B * 30)
Fv = float(F)
G = float(C) * 0.0084  # 0,84 %
H = E + Fv + G

# Proposition de modèle 2026
J = (A * 20) + (B * 30)
K = 0.0
L = float(C) * 0.0114  # 1,14 %
M = J + K + L

# Différence
O = M - H
dE, dF, dG, dH = (J - E), (K - Fv), (L - G), O

# ---------------- 3 colonnes ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<span class="pill">Modèle actuel</span>', unsafe_allow_html=True)
    st.write("")  # petite marge
    st.metric("Contributions forfaitaires", euro(E))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(Fv))
    st.metric(f"Contribution sur les loyers <span class='accent'>0,84%</span>", euro(G), help="Taux appliqué sur les loyers propriétaires"),  # noqa: E501
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.metric("TOTAL", euro(H))

with col2:
    st.markdown('<span class="pill">Proposition de modèle 2026</span>', unsafe_allow_html=True)
    st.write("")
    st.metric("Contributions forfaitaires", euro(J))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", euro(K))
    st.metric(f"Contribution sur les loyers <span class='accent'>1,14%</span>", euro(L), help="Taux appliqué sur les loyers propriétaires"),  # noqa: E501
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.metric("TOTAL", euro(M))

with col3:
    st.markdown('<span class="pill">Différence (2026 – actuel)</span>', unsafe_allow_html=True)
    st.write("")
    st.metric("Écart contributions forfaitaires", euro(dE))
    st.metric("Écart contribution volontaire", euro(dF))
    st.metric("Écart contribution loyers", euro(dG))
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    # Écart total coloré selon signe
    if dH >= 0:
        st.markdown(f'<div class="label-small">Écart total</div><div class="value-pos">{euro(dH)}</div>', unsafe_allow_html=True)  # rouge
    else:
        st.markdown(f'<div class="label-small">Écart total</div><div class="value-neg">{euro(dH)}</div>', unsafe_allow_html=True)  # vert
