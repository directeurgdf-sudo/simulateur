
# Simulateur Excel → Web (Streamlit)

Ce modèle transforme un classeur Excel en mini application web via Streamlit.

## Déploiement (gratuit) sur Streamlit Community Cloud
1. Crée un dépôt GitHub et ajoute ces fichiers (`app.py`, `requirements.txt`, `config.json` facultatif).
2. Va sur https://share.streamlit.io/ (ou https://streamlit.io/cloud) et connecte ton dépôt.
3. Choisis `app.py` comme fichier principal, Python 3.10+.
4. Déploie : tu obtiens une URL publique `https://<ton-app>.streamlit.app` à partager.

### Notes importantes
- Les apps publiques sont **accessibles par simple lien**. Tu peux aussi restreindre l'accès via authentification OIDC si besoin.
- Les apps **hibernent après 12h** d'inactivité (premier accès les réveille).
- Limites typiques de la Community Cloud (févr. 2024) : **690 Mo à 2,7 Go de RAM**, **jusqu'à 2 vCPU**, **~50 Go de stockage**.
- Évite les fichiers très lourds ; mets en cache (`st.cache_data`) ou utilise une base.

## Configuration des champs
- Place un `config.json` à la racine pour mapper **entrées** ↔ **cellules** et lister les **sorties** à afficher.
- Par défaut, l'app fonctionne même sans `config.json` mais n'affichera pas de champs.

## Dépendances
- Streamlit, pandas, openpyxl

## Sécurité & confidentialité
- Les fichiers uploadés sont traités en mémoire par l'app et ne sont pas partagés par défaut. Vérifie ta politique si tu manipules des données sensibles.
