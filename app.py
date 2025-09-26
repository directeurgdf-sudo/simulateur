# app.py
import streamlit as st

# -------------------------------
# Réglages & styles
# -------------------------------
st.set_page_config(page_title="Simulateur – Financement SAS Gîtes de France", layout="wide")

CUSTOM_CSS = """
<style>
/* Police tabulaire + alignement à droite pour tous les montants */
.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
/* Titres pastille */
.pill {
  display:inline-flex;align-items:center;gap:.5rem;
  padding:.35rem .9rem;border:2px solid #2e7d32;border-radius:999px;
  color:#2e7d32;font-weight:700;
}
.pill--dark { border-color:#2e7d32; background:#2e7d32; color:#fff; }
.subtle { color:#6b7280; font-size:.82rem; }
.hr { border-top:1px solid #e5e7eb; margin:.75rem 0; }
.card { border:1px solid #e5e7eb; border-radius:1rem; padding:1rem 1.25rem; }
.caption { color:#6b7280; font-size:.8rem; }
.leftpane .stNumberInput>div>div>input,
.leftpane .stTextInput>div>div>input { font-variant-numeric: tabular-nums; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------
# Helpers
# -------------------------------
def eur(x: float) -> str:
    """Format EUR fr-FR (espaces milliers, virgule décimale)."""
    s = f"{x:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s}"

def signed_eur(delta: float) -> str:
    sign = "+" if delta > 0 else ("−" if delta < 0 else "±")
    return f"{sign} {eur(abs(delta))}"

# Hypothèses (doc)
FORFAIT_SR = 20.0
FORFAIT_RP = 30.0
TAUX_2025 = 0.0084  # 0,84 %
TAUX_2026 = 0.0115  # 1,15 %

# -------------------------------
# UI – Colonne gauche (inputs)
# -------------------------------
with st.sidebar:
    st.markdown("## 🧮 Remplissez", help="Saisissez vos données départements")
    st.markdown('<div class="leftpane">', unsafe_allow_html=True)

    sr = st.number_input("Votre parc d'annonces en SR (exclusivité)",
                         min_value=0, step=1, value=150)
    rp = st.number_input("Votre parc d'annonces en RP/PP (partagés)",
                         min_value=0, step=1, value=300)
    loyers = st.number_input("Total des loyers propriétaires (€)",
                             min_value=0, step=1000, value=4_000_000)
    volontaire_2025 = st.number_input("Votre contribution volontaire à la campagne de marque 2025 **HT (€)**",
                                      min_value=0, step=100, value=12_400,
                                      help="Affichée HT. En 2026, cette contribution est indiquée comme « incluse » (0 €).")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Calculs
# -------------------------------
forfait_2025 = sr * FORFAIT_SR + rp * FORFAIT_RP
forfait_2026 = sr * FORFAIT_SR + rp * FORFAIT_RP  # inchangé

campagne_2025 = float(volontaire_2025)
campagne_2026 = 0.0  # inclus

loyers_2025 = loyers * TAUX_2025
loyers_2026 = loyers * TAUX_2026

total_2025 = forfait_2025 + campagne_2025 + loyers_2025
total_2026 = forfait_2026 + campagne_2026 + loyers_2026

# Différences
diff_forfait = forfait_2026 - forfait_2025
diff_campagne = campagne_2026 - campagne_2025
diff_loyers = loyers_2026 - loyers_2025
diff_total = total_2026 - total_2025

# -------------------------------
# UI – 3 colonnes
# -------------------------------
c1, c2, c3 = st.columns((1, 1, 1))

with c1:
    st.markdown('<div class="pill">Modèle 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("**Contributions forfaitaires**  <span class='subtle'>(1)</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{eur(forfait_2025)}</div>", unsafe_allow_html=True)

    st.markdown("**Contribution volontaire 2025**", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{eur(campagne_2025)}</div>", unsafe_allow_html=True)

    st.markdown(f"**Contribution sur les loyers** <span class='subtle'>{TAUX_2025*100:.2f} %</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{eur(loyers_2025)}</div>", unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown("**TOTAL**", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.9rem'>{eur(total_2025)}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="pill">Proposition de modèle 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("**Contributions forfaitaires**  <span class='subtle'>(1)</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{eur(forfait_2026)}</div>", unsafe_allow_html=True)

    st.markdown("**Contribution à la campagne de Marque** <span class='subtle'>(inclus)</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{eur(campagne_2026)}</div>", unsafe_allow_html=True)

    st.markdown(f"**Contribution sur les loyers** <span class='subtle'>{TAUX_2026*100:.2f} %</span>  <span class='subtle'>(2)</span>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{eur(loyers_2026)}</div>", unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown("**TOTAL**  <span class='subtle'>(3)</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.9rem'>{eur(total_2026)}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="pill">Différence (2026 – 2025)</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("**Écart contributions forfaitaires**", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{signed_eur(diff_forfait)}</div>", unsafe_allow_html=True)

    st.markdown("**Écart contribution à la campagne**", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{signed_eur(diff_campagne)}</div>", unsafe_allow_html=True)

    st.markdown("**Écart contribution loyers**", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.6rem'>{signed_eur(diff_loyers)}</div>", unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown("**ÉCART TOTAL**", unsafe_allow_html=True)
    st.markdown(f"<div class='num' style='font-size:1.9rem'>{signed_eur(diff_total)}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Notes de bas de tableau
# -------------------------------
st.markdown("---")
st.markdown("**(1)** 20€/hébergement en **SR**, 30€/hébergement en **RP/PP**", unsafe_allow_html=True)
st.markdown("**(2)** Augmentation du taux et suppression du plafonnement", unsafe_allow_html=True)
st.markdown("**(3)** Hors plafonnement", unsafe_allow_html=True)
