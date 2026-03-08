# Fifa World Cup 1930-2022 Dashboard

Ce projet propose un tableau de bord interactif pour explorer les données de la Coupe du Monde de la FIFA de 1930 à 2022, avec analyses, visualisations et déploiement sur Netlify via Streamlit.

## Structure du projet

- `data/raw/` : jeux de données originaux
- `data/processed/` : jeux de données nettoyés
- `elt/` : scripts d'extraction, transformation, chargement
- `analysis/` : analyses et scripts statistiques
- `dashboard/` : application Streamlit

## Analyses prévues
- Top 5 des équipes les plus victorieuses
- Top 3 des pays ayant le plus accueilli la Coupe du Monde
- Top 3 des pays ayant accueilli et gagné la même année
- Top 3 des pays ayant le plus fini à la 2ème place
- Top 3 des victoires en finale avec au moins 3 buts d'écart
- Top 3 des victoires en finale sans penalty

## Lancement local

1. (Recommandé) Créer et activer un environnement virtuel :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```


2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Générer le fichier de données nettoyé (obligatoire avant de lancer le dashboard) :
   ```bash
   python elt/transform.py
   ```

4. Lancer le dashboard Streamlit :
   ```bash
   streamlit run dashboard/app.py
   ```

5. Ouvre le lien affiché dans le terminal (généralement http://localhost:8501) dans ton navigateur.

## Déploiement Netlify
Voir instructions dans le README ou le dashboard.
