import pandas as pd
from collections import Counter

DATA_PATH = '../data/raw/FIFA_World_Cup_Results_All_Time_1930_2022.csv'

def load_data(path=DATA_PATH):
	return pd.read_csv(path)

# 1. Top 5 des équipes qui ont le plus gagnés
def top_5_winners(df):
	return df['Winner'].value_counts().head(5)

# 2. Top 3 des pays qui ont le plus host la coupe du monde
def top_3_hosts(df):
	hosts = df['Host'].str.split(' / |, ', expand=True).stack()
	return hosts.value_counts().head(3)

# 3. Top 5 des pays qui ont host ET gagné la même année
def top_5_host_and_win(df):
	host_win = df[df['Host_Won'] == True]
	return host_win['Host'].value_counts().head(5)

# 4. Top 3 des pays qui ont le plus fini à la 2ème place
def top_3_runner_up(df):
	return df['Runner_Up'].value_counts().head(3)

# 5. Top 3 des pays qui ont gagné la finale avec au moins 3 buts d'écart
def top_3_biggest_final_wins(df):
	def goal_diff(row):
		score = row['Regular_Time_Score'].replace('–', '-').split('-')
		try:
			diff = abs(int(score[0]) - int(score[1]))
		except:
			diff = 0
		return diff
	df['Goal_Diff'] = df.apply(goal_diff, axis=1)
	big_wins = df[df['Goal_Diff'] >= 3]
	return big_wins['Winner'].value_counts().head(3)

# 6. Tout pays qui ont gagné la finale sans aller en Penalty
def top_win_no_penalty(df):
	no_pen = df[df['Decided_By_Penalties'] == False]
	return no_pen['Winner'].value_counts()

if __name__ == '__main__':
	df = load_data()
	print('Top 5 équipes les plus victorieuses:')
	print(top_5_winners(df))
	print('\nTop 3 pays hôtes:')
	print(top_3_hosts(df))
	print('\nTop 5 pays host & win:')
	print(top_5_host_and_win(df))
	print('\nTop 3 runner-up:')
	print(top_3_runner_up(df))
	print('\nTop 3 victoires avec 3 buts d\'écart:')
	print(top_3_biggest_final_wins(df))
	print('\nTop 3 victoires sans penalty:')
	print(top_win_no_penalty(df))
