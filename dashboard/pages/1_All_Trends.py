import sys
import os

# 🔥 Force add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_connection

# ---------------- CONFIG ----------------
st.set_page_config(page_title="All Trends", layout="wide")

st.title("📊 All Trends Overview")

# ---------------- LOAD DATA ----------------
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM trends", conn)
conn.close()

if df.empty:
    st.warning("No data available in database")
    st.stop()

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# ---------------- FILTERS ----------------
st.sidebar.header("🔍 Filters")

# Platform filter
platforms = st.sidebar.multiselect(
    "Select Platform",
    options=df["platform"].unique(),
    default=df["platform"].unique()
)

# Keyword filter
keywords = st.sidebar.multiselect(
    "Select Topics",
    options=df["title"].unique(),
    default=df["title"].unique()
)

# Apply filters
df = df[(df["platform"].isin(platforms)) & (df["title"].isin(keywords))]

# ---------------- DATA TABLE ----------------
st.subheader("📋 Data Table")
st.dataframe(df, use_container_width=True)

# ---------------- TOP TRENDS ----------------
st.subheader("🔥 Top Trends")

top_df = (
    df.groupby("title")["trend_score"]
    .mean()
    .reset_index()
    .sort_values(by="trend_score", ascending=False)
    .head(10)
)

# ---------------- BAR + PIE ----------------
col1, col2 = st.columns(2)

with col1:
    fig_bar = px.bar(
        top_df,
        x="title",
        y="trend_score",
        title="Top 10 Trends"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(
        top_df,
        names="title",
        values="trend_score",
        title="Trend Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- LINE GRAPH ----------------
st.subheader("📈 Trend Growth Over Time")

line_df = (
    df.groupby(["timestamp", "title"])["trend_score"]
    .mean()
    .reset_index()
)

fig_line = px.line(
    line_df,
    x="timestamp",
    y="trend_score",
    color="title",
    title="Trend Growth Over Time"
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------- PLATFORM DISTRIBUTION ----------------
st.subheader("📊 Platform Distribution")

platform_df = df["platform"].value_counts().reset_index()
platform_df.columns = ["platform", "count"]

fig_platform = px.pie(
    platform_df,
    names="platform",
    values="count",
    title="Platform Share"
)

st.plotly_chart(fig_platform, use_container_width=True)