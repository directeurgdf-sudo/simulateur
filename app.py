import streamlit as st

st.set_page_config(page_title="Simulateur SAS", page_icon="🏡", layout="wide")

# ---------- Titre ----------
st.markdown("# 🏡 Simulateur des contributions à la SAS Gîtes de France")

# ---------- Entrées ----------
st.sidebar.header("✍️ Remplissez")
A = st.sidebar.number_input("NB GITES SR", min_value=0.0, step=1.0, value=674.0)
B = st.sidebar.number_input("NB GITES RP/PP", min_value=0.0, step=1.0, value=567.0)
C = st.sidebar.number_input("TOTAL des Loyers propriétaires (€)", min_value=0.0, step=1000.0, value=2_642_740.90, format="%.2f")
F = st.sidebar.number_input("Contribution volontaire à la campagne de Marque (€)", min_value=0.0, step=100.0, value=10_000.0, format="%.2f")

def fmt(val: float) -> str:
    return f"{val:,.2f}".replace(",", " ").replace(".", ",")

# ---------- Calculs modèle ACTUEL (E,F,G,H) ----------
E = (A * 20) + (B * 30)         # contributions forfaitaires
Fv = F                           # contribution volontaire (paramètre, inclus)
G = C * 0.0084                   # contribution sur loyers 0,84%
H = E + Fv + G                   # total actuel

# ---------- Calculs modèle 2026 (J,K,L,M) ----------
J = (A * 20) + (B * 30)         # contributions forfaitaires
K = 0.0                          # contribution volontaire (inclus) → valeur 0 dans ton fichier
L = C * 0.0114                   # contribution sur loyers 1,14%
M = J + K + L                    # total 2026

# ---------- Différence ----------
O = M - H                        # 2026 - actuel

st.divider()

# ---------- Affichage : 3 blocs ----------
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### 📘 Modèle actuel")
    st.metric("Contributions forfaitaires", fmt(E))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", fmt(Fv))
    st.metric("Contribution sur les loyers 0,84%", fmt(G))
    st.metric("TOTAL", fmt(H))

with col_b:
    st.markdown("### 📗 Modèle 2026")
    st.metric("Contributions forfaitaires", fmt(J))
    st.metric("Contribution volontaire à la campagne de Marque (inclus)", fmt(K))
    st.metric("Contribution sur les loyers 1,14%", fmt(L))
    st.metric("TOTAL", fmt(M))

with col_c:
    st.markdown("### 📙 Différence (2026 – actuel)")
    st.metric("Δ Contributions forfaitaires", fmt(J - E))
    st.metric("Δ Contribution volontaire (inclus)", fmt(K - Fv))
    st.metric("Δ Contribution loyers", fmt(L - G))
    st.metric("Δ TOTAL", fmt(O))

st.caption("Les formules reproduisent celles de la ligne 4 de ton fichier Excel. Le libellé “(inclus)” est conservé pour la contribution volontaire.")
