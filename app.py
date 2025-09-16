import streamlit as st

st.set_page_config(page_title="Simulateur SAS", page_icon="🏡", layout="wide")

# Titre principal
st.markdown(
    """
    # 🏡 Simulateur des contributions à la SAS Gîtes de France
    """
)

# Section Entrées
st.sidebar.header("✍️ Remplissez")
A = st.sidebar.number_input("NB GITES SR", min_value=0.0, step=1.0, value=674.0)
B = st.sidebar.number_input("NB GITES RP/PP", min_value=0.0, step=1.0, value=567.0)
C = st.sidebar.number_input("TOTAL des Loyers propriétaires (€)", min_value=0.0, step=1000.0, value=2642740.90, format="%.2f")
F = st.sidebar.number_input("Contribution volontaire à la campagne de Marque (€)", min_value=0.0, step=100.0, value=10000.0)

# Calculs (repris de ton Excel)
E = (A * 20) + (B * 30)
G = C * 0.0084
H = E + F + G
J = (A * 20) + (B * 30)
K = 0.0
L = C * 0.0114
M = J + K + L
O = M - H

# Résultats formatés
def fmt(val): 
    return f"{val:,.2f}".replace(",", " ").replace(".", ",")

st.subheader("📊 Résultats")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Contributions forfaitaires", fmt(E))
    st.metric("Contribution volontaire à la campagne de Marque", fmt(F))
    st.metric("Contribution sur les loyers 0,84%", fmt(G))
with col2:
    st.metric("TOTAL", fmt(H))
    st.metric("Contributions forfaitaires (RP/PP)", fmt(J))
    st.metric("Contribution volontaire RP/PP", fmt(K))
with col3:
    st.metric("Contribution sur les loyers 1,14%", fmt(L))
    st.metric("TOTAL (RP/PP)", fmt(M))
    st.metric("Différence", fmt(O))

st.caption("⚖️ Les formules sont celles de la ligne 4 de ton fichier Excel.")
