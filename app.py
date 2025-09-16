import streamlit as st

# ---------------- Config ----------------
st.set_page_config(page_title="Simulateur SAS Gîtes de France", page_icon="🏡", layout="wide")

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
section[data-testid="stSidebar"] input {{ color:#111827 !important; background:#fff !important; }}

/* Pills */
.pill {{
  display:inline-block; padding:10px 14px; border-radius:20px;
  font-weight:700; font-size:1.05rem; margin-bottom:8px;
}}
.pill-green {{ background:{BRAND_GREEN}; color:#fff; }}
.pill-outline {{ background:#fff; color:#111827; border:2px solid {BRAND_GREEN}; }}

/* Texte en vert (taux, inclus) */
.accent {{ color:{BRAND_GREEN}; font-weight:800; }}

/* Valeurs uniformes */
.big-val {{
  font-size:1.6rem; line-height:1.3; color:#111827;
  margin:4px 0 14px; font-weight:500;
}}

/* Lignes de séparation */
.hr {{ border-top:1px solid #e5e7eb; margin:16px 0; }}

/* Écart total */
.value-pos {{ color:#e03a3a; font-weight:700; font-size:2rem; }}
.value-neg {{ color:{BRAND_GREEN}; font-weight:700; font-size:2rem; }}
.label-small {{ color:#6b7280; text-transform:uppercase; letter-spacing:.04em; font-size:.9rem; }}
</style>
""", unsafe_allow_html=True)

# ---------------- Utilitaires ----------------
def euro(x: float) -> str:
    """Format 1 234 567,89"""
    return f"{x:,.2f}".replace(",", " ").replace(".", ",")

def valeur(label_html: str, val: float):
    """Libellé (HTML autorisé) + valeur uniforme."""
    st.markdown(label_html, unsafe_allow_html=True)                     # <= ici le HTML est rendu
    st.markdown(f"<div class='big-val'>{euro(val)}</div>", unsafe_allow_html=True)

# ---------------- Titre ----------------
st.markdown("""
<div class="header-wrap">
  <h1>Simulateur des contributions à la SAS Gîtes de France</h1>
</div>
""", unsafe_allow_html=True)

# ---------------- Entrées ----------------
st.sidebar.header("✍️ Remplissez")

# Si tu veux aussi des séparateurs sur les compteurs A/B, garde read_int_with_grouping ;
# sinon tu peux remettre number_input pour eux.
A = read_int_with_grouping("Votre parc d'annonces en SR (exclusivités)", 650)
B = read_int_with_grouping("Votre parc d'annonces en RP/PP (partagés)", 300)

# Montants en € avec séparateurs
C = read_int_with_grouping("TOTAL des Loyers propriétaires (€)", 4_000_000)
F = read_int_with_grouping("Votre contribution volontaire à la campagne de marque (€)", 15_000)


# ---------------- Calculs ----------------
E = (A * 20) + (B * 30)          # forfaitaires actuel
Fv = float(F)                     # campagne actuel
G = float(C) * 0.0084             # 0,84 %
H = E + Fv + G

J = (A * 20) + (B * 30)          # forfaitaires 2026
K = 0.0                           # campagne 2026 (inclus)
L = float(C) * 0.0114             # 1,14 %
M = J + K + L

dE, dF, dG = (J - E), (K - Fv), (L - G)
dH = M - H

# ---------------- Affichage ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<span class="pill pill-green">Modèle actuel</span>', unsafe_allow_html=True)
    st.write("")
    valeur("Contributions forfaitaires", E)
    valeur("Contribution à la campagne de Marque", Fv)
    valeur('Contribution sur les loyers <span class="accent">0,84&nbsp;%</span>', G)
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    valeur("TOTAL", H)

with col2:
    st.markdown('<span class="pill pill-green">Proposition de modèle 2026</span>', unsafe_allow_html=True)
    st.write("")
    valeur("Contributions forfaitaires", J)
    valeur('Contribution à la campagne de Marque <span class="accent">(inclus)</span>', K)
    valeur('Contribution sur les loyers <span class="accent">1,14&nbsp;%</span>', L)
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    valeur("TOTAL", M)

with col3:
    st.markdown('<span class="pill pill-outline">Différence (2026 – actuel)</span>', unsafe_allow_html=True)
    st.write("")
    valeur("Écart contributions forfaitaires", dE)
    valeur("Écart contribution à la campagne", dF)
    valeur("Écart contribution loyers", dG)
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="label-small">ÉCART TOTAL</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='{'value-pos' if dH >= 0 else 'value-neg'}'>{euro(dH)}</div>",
        unsafe_allow_html=True
    )
