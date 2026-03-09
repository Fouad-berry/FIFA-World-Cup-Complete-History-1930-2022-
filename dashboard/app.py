
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

FLAGS_PATH = BASE_DIR / 'data/raw/flags_iso.csv'

FLAG_NAME_FIX = {
    "England": "United Kingdom of Great Britain and Northern Ireland (the)",
    "South Korea": "Korea (the Republic of)",
    "North Korea": "Korea (the Democratic People's Republic of)",
    "USA": "United States of America (the)",
    "United States": "United States of America (the)",
    "Iran": "Iran (Islamic Republic of)",
    "Russia": "Russian Federation (the)",
    "Czech Republic": "Czechia",
    "Ivory Coast": "Côte d'Ivoire",
    "Netherlands": "Netherlands (the)",
}

flags = pd.read_csv(FLAGS_PATH)

def add_flag_column(df, country_col):
    merged = df.reset_index()
    merged.columns = [country_col, 'count']
    merged[country_col] = merged[country_col].replace(FLAG_NAME_FIX)
    merged = merged.merge(flags[['Country', 'URL']], left_on=country_col, right_on='Country', how='left')
    merged['flag'] = merged['URL'].apply(lambda url: f"<img src='{url}' width='24'> " if pd.notnull(url) else "")
    merged['display'] = merged['flag'] + merged[country_col].astype(str)
    merged = merged.rename(columns={'display': 'Pays'})
    return merged[['Pays', 'count']]

def show_table_with_flags(df, country_col):
    merged = add_flag_column(df, country_col)
    st.markdown(
        merged.to_html(header=['Pays', 'Count'], index=False, escape=False),
        unsafe_allow_html=True
    )

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
            "Winner": st.column_config.TextColumn(width="medium"),
            "count": st.column_config.NumberColumn(width="small")
        },
        use_container_width=False,
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
    col1, col2 = st.columns([1,2])
    with col1:
        show_table_with_flags(winners, 'Winner')
    with col2:
        fig = plotly_doughnut(winners.index, winners.values, title="Top 5 Gagnants")
        st.plotly_chart(fig, width='content')
        
with tab2:
	st.header("Top 3 des pays hôtes")
	hosts = analysis.top_3_hosts(df)
	col1, col2 = st.columns([1,2])
	with col1:
		show_table_with_flags(hosts, 'Host')
	with col2:
		fig = plotly_doughnut(hosts.index, hosts.values, title="Top 3 Hôtes")
		st.plotly_chart(fig, width='content')

with tab3:
	st.header("Top 5 des pays qui ont accueillis ET gagné la même année")
	host_win = analysis.top_5_host_and_win(df)
	col1, col2 = st.columns([1,2])
	with col1:
		show_table_with_flags(host_win, 'Host')
	with col2:
		fig = plotly_doughnut(host_win.index, host_win.values, title="Top 5 Hôtes & Gagnants")
		st.plotly_chart(fig, width='content')

with tab4:
	st.header("Top 3 des pays qui ont fini à la 2ème place")
	runner_up = analysis.top_3_runner_up(df)
	col1, col2 = st.columns([1,2])
	with col1:
		show_table_with_flags(runner_up, 'Runner_Up')
	with col2:
		fig = plotly_doughnut(runner_up.index, runner_up.values, title="Top 3 2ème place")
		st.plotly_chart(fig, width='content')

with tab5:
	st.header("Top 3 des pays qui ont gagné la finale avec au moins 3 buts d'écart")
	big_wins = analysis.top_3_biggest_final_wins(df)
	col1, col2 = st.columns([1,2])
	with col1:
		show_table_with_flags(big_wins, 'Winner')
	with col2:
		fig = plotly_doughnut(big_wins.index, big_wins.values, title="Top 3 victoires 3+ buts")
		st.plotly_chart(fig, width='content')

with tab6:
	st.header("Tout les pays qui ont gagné la finale sans aller en Penalty")
	no_pen = analysis.top_win_no_penalty(df)
	col1, col2 = st.columns([1,2])
	with col1:
		show_table_with_flags(no_pen, 'Winner')
	with col2:
		fig = plotly_doughnut(no_pen.index, no_pen.values, title="Tout les pays qui ont gagné sans penalty")
		st.plotly_chart(fig, width='content')
