
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Ajout du dossier parent au PYTHONPATH pour l'import analysis
import pathlib
parent = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(parent))
from analysis import analysis


st.set_page_config(page_title="FIFA World Cup 1930-2022 Dashboard", layout="wide")
st.markdown("""
""", unsafe_allow_html=True)
st.title("FIFA World Cup 1930-2022 ⚽")
st.markdown("""
Tableau de bord interactif : analyses, classements et visualisations sur la Coupe du Monde de la FIFA (1930-2022).
""")


# Chargement des données nettoyées avec un chemin robuste
import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
DATA_PATH = BASE_DIR / 'data/processed/FIFA_World_Cup_Results_CLEAN.csv'
df = pd.read_csv(DATA_PATH)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
	"🏆 Top 5 Gagnants",
	"🌍 Top 3 Hôtes",
	"🏠🥇 Hôtes & Gagnés",
	"🥈 Top 3 2ème place",
	"⚡️ Victoires 3+ buts",
	"🚫🏅 Victoires sans penalty"
])

def show_table(data):
    st.dataframe(
        data,
        column_config={
            "count": st.column_config.NumberColumn("count", width="small")
        },
        use_container_width=False
    )

def plotly_doughnut(labels, values, title=None):
	fig = px.pie(
		names=labels,
		values=values,
		hole=0.5,
		title=title,
		color_discrete_sequence=px.colors.qualitative.Pastel
	)
	fig.update_traces(textinfo='percent+label', textfont_size=12, pull=[0.03]*len(labels))
	fig.update_layout(
		showlegend=False,
		margin=dict(l=10, r=10, t=40, b=10),
		height=350,
		width=350,
		title_font_size=16
	)
	return fig

with tab1:
	st.header("Top 5 des équipes qui ont le plus gagné")
	winners = analysis.top_5_winners(df)
	show_table(winners)
	col1, col2, col3 = st.columns([1,2,1])
	with col2:
		fig = plotly_doughnut(winners.index, winners.values, title="Top 5 Gagnants")
		st.plotly_chart(fig, width='content')

with tab2:
	st.header("Top 3 des pays hôtes")
	hosts = analysis.top_3_hosts(df)
	show_table(hosts)
	col1, col2, col3 = st.columns([1,2,1])
	with col2:
		fig = plotly_doughnut(hosts.index, hosts.values, title="Top 3 Hôtes")
		st.plotly_chart(fig, width='content')

with tab3:
	st.header("Top 3 des pays qui ont host ET gagné la même année")
	host_win = analysis.top_3_host_and_win(df)
	show_table(host_win)
	col1, col2, col3 = st.columns([1,2,1])
	with col2:
		fig = plotly_doughnut(host_win.index, host_win.values, title="Top 3 Host & Win")
		st.plotly_chart(fig, width='content')

with tab4:
	st.header("Top 3 des pays qui ont fini à la 2ème place")
	runner_up = analysis.top_3_runner_up(df)
	show_table(runner_up)
	col1, col2, col3 = st.columns([1,2,1])
	with col2:
		fig = plotly_doughnut(runner_up.index, runner_up.values, title="Top 3 2ème place")
		st.plotly_chart(fig, width='content')

with tab5:
	st.header("Top 3 des pays qui ont gagné la finale avec au moins 3 buts d'écart")
	big_wins = analysis.top_3_biggest_final_wins(df)
	show_table(big_wins)
	col1, col2, col3 = st.columns([1,2,1])
	with col2:
		fig = plotly_doughnut(big_wins.index, big_wins.values, title="Top 3 victoires 3+ buts")
		st.plotly_chart(fig, width='content')

with tab6:
	st.header("Top 3 des pays qui ont gagné la finale sans aller en Penalty")
	no_pen = analysis.top_3_win_no_penalty(df)
	show_table(no_pen)
	col1, col2, col3 = st.columns([1,2,1])
	with col2:
		fig = plotly_doughnut(no_pen.index, no_pen.values, title="Top 3 sans penalty")
		st.plotly_chart(fig, width='content')
