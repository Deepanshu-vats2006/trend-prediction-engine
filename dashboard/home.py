import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_connection
from auth import create_user, login_user
from history import save_history
import sys
import os

# 🔥 Force add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Trend Engine", layout="wide")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔐 Account")

choice = st.sidebar.radio("Select", ["Login", "Register"])

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if choice == "Register":
    if st.sidebar.button("Register"):
        if create_user(username, password):
            st.sidebar.success("Account created!")
        else:
            st.sidebar.error("User exists")

if choice == "Login":
    if st.sidebar.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.user = user[0]
            st.sidebar.success("Logged in")
        else:
            st.sidebar.error("Invalid credentials")

if st.session_state.user:
    if st.sidebar.button("Logout"):
        st.session_state.user = None

# ---------------- TITLE ----------------
st.title("🔥 Trend Engine Dashboard")

# ---------------- SEARCH ----------------
search = st.text_input("🔍 Enter topics (comma separated)", placeholder="ai, gold")

if search and st.session_state.user:

    topics = [t.strip().lower() for t in search.split(",")]

    save_history(st.session_state.user, search)

    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM trends", conn)
    conn.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df_filtered = df[df["title"].str.contains("|".join(topics), case=False)]

    if df_filtered.empty:
        st.warning("No data found")
        st.stop()

    # ---------------- METRICS ----------------
    st.subheader("📊 Trend Scores")

    cols = st.columns(len(topics))

    for i, topic in enumerate(topics):
        topic_df = df_filtered[df_filtered["title"].str.contains(topic, case=False)]
        score = round(topic_df["trend_score"].mean(), 2)

        cols[i].metric(label=topic.upper(), value=score)

    # ---------------- BAR + PIE ----------------
    st.subheader("📊 Comparison")

    compare_df = df_filtered.groupby("title")["trend_score"].mean().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(compare_df, x="title", y="trend_score")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(compare_df, names="title", values="trend_score")
        st.plotly_chart(fig_pie, use_container_width=True)

    # ---------------- LINE GRAPHS ----------------
    st.subheader("📈 Trend Growth Over Time")

    for topic in topics:
        topic_df = df[df["title"].str.contains(topic, case=False)]

        if not topic_df.empty:
            line_df = topic_df.groupby("timestamp")["trend_score"].mean().reset_index()

            st.markdown(f"### 🔹 {topic.upper()}")

            fig_line = px.line(line_df, x="timestamp", y="trend_score")
            st.plotly_chart(fig_line, use_container_width=True)