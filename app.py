import streamlit as st

st.set_page_config(page_title="Simulateur", page_icon="🧮")

st.title("🧮 Simulateur (3 entrées → résultats)")

st.sidebar.header("Paramètres")
A = st.sidebar.number_input("Entrée A", min_value=0.0, step=1.0, value=674.0)
B = st.sidebar.number_input("Entrée B", min_value=0.0, step=1.0, value=567.0)
C = st.sidebar.number_input("Entrée C", min_value=0.0, step=1000.0, value=2642740.90, format="%.2f")

# Calculs (équivalents à ta feuille Feuil1 !)
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
    st.metric("E4", f"{E:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("F4", f"{F:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("G4", f"{G:,.2f}".replace(",", " ").replace(".", ","))
with col2:
    st.metric("H4", f"{H:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("J4", f"{J:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("K4", f"{K:,.2f}".replace(",", " ").replace(".", ","))
with col3:
    st.metric("L4", f"{L:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("M4", f"{M:,.2f}".replace(",", " ").replace(".", ","))
    st.metric("O4", f"{O:,.2f}".replace(",", " ").replace(".", ","))

st.caption("Les formules reproduisent celles de ta feuille (ligne 4).")
