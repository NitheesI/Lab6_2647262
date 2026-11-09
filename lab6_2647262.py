import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cricket Player Analysis", layout="wide")

df = pd.read_csv("deliveries.csv")
df = df.rename(columns={"batsman": "batter"})

st.title("Cricket Player Analysis Dashboard")

st.sidebar.header("Filters")
teams = sorted(df["batting_team"].unique())
selected_teams = st.sidebar.multiselect("Select Teams", teams, default=teams)

min_over, max_over = int(df["over"].min()), int(df["over"].max())
over_range = st.sidebar.slider("Over Range", min_over, max_over, (min_over, max_over))

players = sorted(df["batter"].unique())
selected_player = st.sidebar.selectbox("Select Player", players)

df = df[df["batting_team"].isin(selected_teams)]
df = df[(df["over"] >= over_range[0]) & (df["over"] <= over_range[1])]

total_runs = df["total_runs"].sum()
total_matches = df["match_id"].nunique()
total_sixes = (df["batsman_runs"] == 6).sum()
total_fours = (df["batsman_runs"] == 4).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Matches", total_matches)
col2.metric("Total Runs", total_runs)
col3.metric("Fours", total_fours)
col4.metric("Sixes", total_sixes)

player_stats = df.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False)

tab1, tab2, tab3 = st.tabs(["Overview", "Charts", "Player Trend"])

with tab1:
    st.subheader("Data Sample")
    st.dataframe(df.head(50))

    with st.expander("Top 10 Run Scorers"):
        st.dataframe(player_stats.head(10))

with tab2:
    st.subheader("Top 10 Run Scorers")
    top10 = player_stats.head(10)
    fig1, ax1 = plt.subplots()
    ax1.bar(top10.index, top10.values)
    ax1.set_xticklabels(top10.index, rotation=45, ha="right")
    ax1.set_ylabel("Runs")
    st.pyplot(fig1)

    st.subheader("Runs vs Balls Faced (Top 50 Players)")
    balls = df.groupby("batter")["ball"].count()
    runs = df.groupby("batter")["batsman_runs"].sum()
    stats = pd.DataFrame({"balls": balls, "runs": runs}).sort_values("runs", ascending=False).head(50)
    fig2, ax2 = plt.subplots()
    ax2.scatter(stats["balls"], stats["runs"])
    ax2.set_xlabel("Balls Faced")
    ax2.set_ylabel("Runs Scored")
    st.pyplot(fig2)

with tab3:
    st.subheader(f"Over-wise Runs for {selected_player}")
    player_df = df[df["batter"] == selected_player]
    over_runs = player_df.groupby("over")["batsman_runs"].sum()
    fig3, ax3 = plt.subplots()
    ax3.plot(over_runs.index, over_runs.values, marker="o")
    ax3.set_xlabel("Over")
    ax3.set_ylabel("Runs")
    st.pyplot(fig3)