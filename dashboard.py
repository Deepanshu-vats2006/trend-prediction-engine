import streamlit as st
import pandas as pd
import sqlite3

from scrapers.google_trends import run_google_trends
from scrapers.youtube_trends import run_youtube_trends
from analysis.trend_score import calculate_final_score

DB_PATH = "database/trends.db"

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="Trend Prediction Dashboard",
    page_icon="📈",
    layout="wide"
)

# --------------------------
# CUSTOM CSS (MODERN UI)
# --------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #00FFD1;
}
.stButton>button {
    background-color: #00FFD1;
    color: black;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER
# --------------------------
st.title("🚀 Trend Prediction Dashboard")
st.write("Predict trending topics using Google + YouTube data")

# --------------------------
# SIDEBAR INPUT
# --------------------------
st.sidebar.header("🔍 Enter Keywords")

keywords_input = st.sidebar.text_input(
    "Keywords (comma separated, max 5)",
    "AI, Cricket, iPhone"
)

keywords = [k.strip() for k in keywords_input.split(",")]

# --------------------------
# RUN BUTTON
# --------------------------
if st.sidebar.button("🔥 Run Trend Engine"):

    with st.spinner("Collecting data..."):
        run_google_trends(keywords)
        run_youtube_trends(keywords)

    st.success("✅ Data collected and stored!")

# --------------------------
# LOAD DATA FROM DB
# --------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    google_df = pd.read_sql_query("SELECT * FROM google_trends", conn)
    youtube_df = pd.read_sql_query("SELECT * FROM youtube_trends", conn)

    conn.close()

    return google_df, youtube_df

google_df, youtube_df = load_data()

# --------------------------
# SHOW RAW DATA (OPTIONAL)
# --------------------------
with st.expander("📂 View Raw Data"):
    st.subheader("Google Trends")
    st.dataframe(google_df)

    st.subheader("YouTube Trends")
    st.dataframe(youtube_df)

# --------------------------
# FINAL SCORES
# --------------------------
st.subheader("🔥 Top Trending Keywords")

scores = calculate_final_score()

if scores:

    df_scores = pd.DataFrame(scores, columns=["Keyword", "Score"])

    col1, col2 = st.columns(2)

    # --------------------------
    # BAR CHART
    # --------------------------
    with col1:
        st.write("📊 Bar Chart")
        st.bar_chart(df_scores.set_index("Keyword"))

    # --------------------------
    # PIE CHART
    # --------------------------
    with col2:
        st.write("🥧 Pie Chart")
        st.pyplot(
            df_scores.set_index("Keyword").plot.pie(
                y="Score",
                autopct="%1.1f%%",
                legend=False
            ).figure
        )

    # --------------------------
    # TABLE
    # --------------------------
    st.subheader("📋 Ranking Table")
    st.dataframe(df_scores)

else:
    st.warning("⚠️ No data available yet. Run the engine first.")

# --------------------------
# FOOTER
# --------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")