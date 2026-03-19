import sqlite3
from collections import defaultdict

DB_PATH = "database/trends.db"


def get_google_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT keyword, AVG(interest)
        FROM google_trends
        GROUP BY keyword
    """)

    data = cursor.fetchall()
    conn.close()

    return {row[0]: row[1] for row in data}


def get_youtube_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT keyword, COUNT(*)
        FROM youtube_trends
        GROUP BY keyword
    """)

    data = cursor.fetchall()
    conn.close()

    return {row[0]: row[1] for row in data}


def calculate_final_score():
    google_data = get_google_scores()
    youtube_data = get_youtube_scores()

    if not google_data and not youtube_data:
     return []
    
    # ✅ ADD THIS BLOCK HERE
    # Normalize Google scores
    if google_data:
        max_g = max(google_data.values())
        if max_g != 0:
            google_data = {k: v / max_g for k, v in google_data.items()}

    # Normalize YouTube scores
    if youtube_data:
        max_y = max(youtube_data.values())
        if max_y != 0:
            youtube_data = {k: v / max_y for k, v in youtube_data.items()}

    final_scores = defaultdict(int)

    # 🔥 Weight system (IMPORTANT)
    for keyword, score in google_data.items():
        final_scores[keyword] += score * 0.7   # Google = 70%

    for keyword, score in youtube_data.items():
     final_scores[keyword] += score * 0.3

    # Sort results
    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_scores


def show_top_trends():
    trends = calculate_final_score()
    if not trends:
        print("❌ No data available for analysis")
        return

    print("\n🔥 FINAL TREND SCORES:\n")

    for i, (keyword, score) in enumerate(trends[:10], start=1):
        print(f"{i}. {keyword} → {round(score, 2)}")