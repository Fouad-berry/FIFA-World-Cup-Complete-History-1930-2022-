
import pandas as pd
import os
from pathlib import Path

# Toujours relatif à la racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / 'data/raw/FIFA_World_Cup_Results_All_Time_1930_2022.csv'
PROCESSED_PATH = BASE_DIR / 'data/processed/FIFA_World_Cup_Results_CLEAN.csv'

def clean_data():
	df = pd.read_csv(RAW_PATH)
	# Nettoyage :
	# - Uniformiser les noms de pays (ex: "West Germany" → "Germany")
	# - Corriger les types booléens
	# - Nettoyer les scores (remplacer '–' par '-')
	# - Supprimer les colonnes inutiles pour l'analyse
	df['Winner'] = df['Winner'].replace({'West Germany': 'Germany'})
	df['Runner_Up'] = df['Runner_Up'].replace({'West Germany': 'Germany'})
	df['Third_Place'] = df['Third_Place'].replace({'West Germany': 'Germany'})
	df['Fourth_Place'] = df['Fourth_Place'].replace({'West Germany': 'Germany'})
	df['Host'] = df['Host'].replace({'West Germany': 'Germany'})
	# Correction booléens
	for col in ['Went_To_Extra_Time', 'Decided_By_Penalties', 'Host_Won']:
		df[col] = df[col].astype(bool)
	# Nettoyage des scores
	df['Final_Score'] = df['Final_Score'].str.replace('–', '-')
	df['Regular_Time_Score'] = df['Regular_Time_Score'].str.replace('–', '-')
	# On garde les colonnes utiles
	keep = ['Year','Host','Winner','Runner_Up','Final_Score','Regular_Time_Score','Went_To_Extra_Time','Decided_By_Penalties','Host_Won']
	df_clean = df[keep]
	# Sauvegarde
	os.makedirs(PROCESSED_PATH.parent, exist_ok=True)
	df_clean.to_csv(PROCESSED_PATH, index=False)
	print(f"Données nettoyées sauvegardées dans {PROCESSED_PATH}")

if __name__ == '__main__':
	clean_data()
