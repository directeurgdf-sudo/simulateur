import streamlit as st

st.set_page_config(page_title="Simulateur", page_icon="🧮")
st.title("🧮 Simulateur Contributions")

st.sidebar.header("Paramètres")
A = st.sidebar.number_input("NB GITES SR", min_value=0.0, step=1.0, value=674.0)
B = st.sidebar.number_input("NB GITES RP/PP", min_value=0.0, step=1.0, value=567.0)
C = st.sidebar.number_input("TOTAL des Loyers propriétaires (€)", min_value=0.0, step=1000.0, value=2642740.90, format="%.2f")

# Calculs
E = (A * 20) + (B * 30)
F = 10000.0
G = C * 0.0084
H = E + F + G
J = (A * 20) + (B * 30)
K = 0.0
L = C * 0.0114
M = J + K + L
O = M - H

st.subheader("Résultats")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("contributions forfaitaires", f"{E:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("Contribution volontaire à la campagne de Marque", f"{F:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("Contribution sur les loyers 0,84%", f"{G:,.2f}".replace(",", " ").replace(".", ","))
with col2:
    st.metric("TOTAL", f"{H:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("contributions forfaitaires (RP/PP)", f"{J:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("Contribution volontaire à la campagne de Marque (RP/PP)", f"{K:,.2f}".replace(",", " ").replace(".", ","))
with col3:
    st.metric("Contribution sur les loyers 1,14%", f"{L:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("TOTAL (RP/PP)", f"{M:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("Différence", f"{O:,.2f}".replace(",", " ").replace(".", ","))

st.caption("Les formules reproduisent celles de ta feuille (ligne 4).")
