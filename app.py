import streamlit as st

st.set_page_config(layout="wide")

# --- Saisie utilisateur
sr = st.number_input("Votre parc d'annonces en SR (exclusivité)", min_value=0, value=150, step=1)
rp = st.number_input("Votre parc d'annonces en RP/PP (partagés)", min_value=0, value=300, step=1)
loyers = st.number_input("Total des loyers propriétaires (€)", min_value=0, value=4000000, step=1000)
volontaire_2025 = st.number_input(
    "Votre contribution volontaire à la campagne de marque 2025 HT (€)",  # <-- modif ici
    min_value=0, value=12400, step=100
)

# --- Calculs
forfait_2025 = sr * 20 + rp * 30
forfait_2026 = forfait_2025

loyers_2025 = loyers * 0.0084
loyers_2026 = loyers * 0.0115

total_2025 = forfait_2025 + volontaire_2025 + loyers_2025
total_2026 = forfait_2026 + loyers_2026

# --- Mise en colonnes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Modèle 2025")
    st.write("Contributions forfaitaires (1)")
    st.markdown(f"**{forfait_2025:,.0f}**".replace(",", " "))
    st.write("Contribution volontaire 2025")
    st.markdown(f"**{volontaire_2025:,.0f}**".replace(",", " "))
    st.write("Contribution sur les loyers 0.84 %")
    st.markdown(f"**{loyers_2025:,.0f}**".replace(",", " "))
    st.markdown("---")
    st.write("TOTAL (3)")
    st.markdown(f"## {total_2025:,.0f}".replace(",", " "))

with col2:
    st.markdown("### Proposition de modèle 2026")
    st.write("Contributions forfaitaires (1)")
    st.markdown(f"**{forfait_2026:,.0f}**".replace(",", " "))
    st.write("Contribution à la campagne de Marque *(inclus)*")
    st.markdown("**0**")
    st.write("Contribution sur les loyers 1.15 % (2)")
    st.markdown(f"**{loyers_2026:,.0f}**".replace(",", " "))
    st.markdown("---")
    st.write("TOTAL (3)")
    st.markdown(f"## {total_2026:,.0f}".replace(",", " "))

with col3:
    st.markdown("### Différence (2026 – 2025)")
    st.write("Écart contributions forfaitaires")
    st.markdown(f"**{forfait_2026 - forfait_2025:,.0f}**".replace(",", " "))
    st.write("Écart contribution à la campagne")
    st.markdown(f"**{-volontaire_2025:,.0f}**".replace(",", " "))
    st.write("Écart contribution loyers")
    st.markdown(f"**{loyers_2026 - loyers_2025:,.0f}**".replace(",", " "))
    st.markdown("---")
    st.write("ÉCART TOTAL")
    st.markdown(f"## {total_2026 - total_2025:,.0f}".replace(",", " "))

# --- Notes en bas
st.caption("(1) 20€/hébergement en SR, 30€/hébergement en RP/PP")
st.caption("(2) Augmentation du taux et suppression du plafonnement")
st.caption("(3) Hors plafonnement")  # <-- ajout ici
