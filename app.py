import streamlit as st
import re

# ---------------- Config ----------------
st.set_page_config(
    page_title="Simulateur départemental – Financement de la SAS Gîtes de France®",
    page_icon="🏡",
    layout="wide",
)

# ---------------- Styles ----------------
BRAND_GREEN = "#4bab77"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700&display=swap');
* {{ font-family: 'Raleway', sans-serif; }}

/* Titre */
.header-wrap {{ margin-top:-40px; margin-bottom:40px; }}

/* Sidebar */
section[data-testid="stSidebar"] {{ background:{BRAND_GREEN} !important; }}
section[data-testid="stSidebar"] label {{ color:#fff !important; }}
section[data-testid="stSidebar"] input {{
  color:#111827 !important; background:#fff !important; border-radius:8px;
}}

/* Pills */
.pill {{
  display:inline-block; padding:10px 14px; border-radius:20px;
  font-weight:700; font-size:1.05rem; margin-bottom:8px;
}}
.pill-green  {{ background:{BRAND_GREEN}; color:#fff; }}
.pill-outline{{ background:#fff; color:#111827; border:2px solid {BRAND_GREEN}; }}

/* Accents */
.accent {{ color:{BRAND_GREEN}; font-weight:800; }}

/* Valeurs (gabarit commun) */
.big-val {{
  font-size:1.6rem; line-height:1.3; color:#111827;
  margin:4px 0 14px; font-weight:500;
}}

/* Séparateur */
.hr {{ border-top:1px solid #e5e7eb; margin:16px 0; }}

/* Écart total : couleur uniquement (taille héritée de .big-val) */
.value-pos {{ color:{BRAND_GREEN}; font-weight:700; }}  /* utilisé pour NEGATIF */
.value-neg {{ color:#e03a3a; font-weight:700; }}       /* utilisé pour POSITIF */
.label-small {{ color:#6b7280; text-transform:uppercase; letter-spacing:.04em; font-size:.9rem; }}

/* Notes de bas de page */
.footnotes {{ color:#6b7280; font-size:.9rem; margin-top:8px; }}
.footnotes sup {{ margin-right:4px; }}
</style>
""", unsafe_allow_html=True)

# ---------------- Utilitaires ----------------
def euro(x: float) -> str:
    """Format 1 234 567,89 (espaces + virgule)"""
    return f"{x:,.2f}".replace(",", " ").replace(".", ",")

def euro_int(n: int) -> str:
    """Format 1234567 -> '1 234 567' (pour affichage dans la sidebar)"""
    return f"{n:,}".replace(",", " ")

def read_int_with_grouping(label: str, default: int, key: str) -> int:
    """
    Text input qui conserve les séparateurs de milliers pendant la saisie,
    avec callback on_change (évite StreamlitAPIException).
    """
    # Valeur initiale
    if key not in st.session_state or st.session_state[key] == "":
        st.session_state[key] = euro_int(default)

    # Callback qui reformate
    def _on_change():
        raw = st.session_state.get(key, "")
        digits = re.sub(r"[^\d]", "", raw or "")
        val = int(digits) if digits else 0
        st.session_state[key] = euro_int(val)

    # Widget
    st.sidebar.text_input(label, key=key, value=st.session_state[key], on_change=_on_change)

    # Valeur numérique pour calculs
    digits = re.sub(r"[^\d]", "", st.session_state.get(key, ""))
    return int(digits) if digits else default

def valeur(label_html: str, val: float):
    """Libellé (HTML autorisé) + valeur uniforme."""
    st.markdown(label_html, unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{euro(val)}</div>", unsafe_allow_html=True)

# ---------------- Titre ----------------
st.markdown("""
<div class="header-wrap">
  <h1>Simulateur départemental – Financement de la SAS Gîtes de France</h1>
</div>
""", unsafe_allow_html=True)

# ---------------- Entrées ----------------
st.sidebar.header("✍️ Remplissez")
A = read_int_with_grouping("Votre parc d'annonces en SR (exclusivité)", 650, key="A")
B = read_int_with_grouping("Votre parc d'annonces en RP/PP (partagés)", 300, key="B")
C = read_int_with_grouping("Total des loyers propriétaires (€)", 4_000_000, key="C")
F = read_int_with_grouping("Votre contribution volontaire à la campagne de marque 2025 (€)", 15_000, key="F")

# ---------------- Calculs ----------------
# Modèle 2025
E = (A * 20) + (B * 30)     # 20€/SR, 30€/RP/PP
Fv = float(F)               # contribution volontaire (2025)
G = float(C) * 0.0084       # 0,84 %
H = E + Fv + G              # total

# Proposition 2026
J = (A * 20) + (B * 30)     # mêmes forfaits
K = 0.0                     # campagne incluse
L = float(C) * 0.0115       # 1,15 %
M = J + K + L               # total

# Différences (2026 – 2025)
dE, dF, dG = (J - E), (K - Fv), (L - G)
dH = M - H

# ---------------- Affichage ----------------
# 1) Ligne "contenus" (hors TOTAL)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<span class="pill pill-green">Modèle 2025</span>', unsafe_allow_html=True)
    st.write("")
    valeur("Contributions forfaitaires<sup>(1)</sup>", E)
    valeur("Contribution volontaire 2025", Fv)
    valeur('Contribution sur les loyers <span class="accent">0,84&nbsp;%</span>', G)
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<span class="pill pill-green">Proposition de modèle 2026</span>', unsafe_allow_html=True)
    st.write("")
    valeur("Contributions forfaitaires<sup>(1)</sup>", J)
    valeur('Contribution à la campagne de Marque <span class="accent">(inclus)</span>', K)
    valeur('Contribution sur les loyers <span class="accent">1,15&nbsp;%</span><sup>(2)</sup>', L)
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<span class="pill pill-outline">Différence (2026 – 2025)</span>', unsafe_allow_html=True)
    st.write("")
    valeur("Écart contributions forfaitaires", dE)
    valeur("Écart contribution à la campagne", dF)
    valeur("Écart contribution loyers", dG)
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# 2) Ligne "TOTaux" — parfaitement alignée (même rangée)
tot1, tot2, tot3 = st.columns(3)

with tot1:
    st.markdown('<div class="label-small">TOTAL</div>', unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{euro(H)}</div>", unsafe_allow_html=True)

with tot2:
    st.markdown('<div class="label-small">TOTAL</div>', unsafe_allow_html=True)
    st.markdown(f"<div class='big-val'>{euro(M)}</div>", unsafe_allow_html=True)

with tot3:
    st.markdown('<div class="label-small">ÉCART TOTAL</div>', unsafe_allow_html=True)
    if dH < 0:
        prefix, klass = "–", "value-pos"   # vert
    else:
        prefix, klass = "+", "value-neg"   # rouge
    # Écart dans le même gabarit .big-val, couleur via <span>
    st.markdown(f"<div class='big-val'><span class='{klass}'>{prefix} {euro(abs(dH))}</span></div>", unsafe_allow_html=True)

# Notes (après)
st.markdown(
    "<div class='footnotes'>"
    "<div><sup>(1)</sup> 20€/hébergement en SR, 30€/hébergement en RP/PP</div>"
    "<div><sup>(2)</sup> Augmentation du taux et suppression du plafonnement</div>"
    "</div>",
    unsafe_allow_html=True
)
