import sqlite3

DB_PATH = "database/trends.db"

def get_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, AVG(trend_score)
    FROM trends
    GROUP BY title
    """)

    data = cursor.fetchall()
    conn.close()

    return sorted(data, key=lambda x: x[1], reverse=True)


def show_top_trends():
    trends = get_scores()

    if not trends:
        print("❌ No data available")
        return

    print("\n🔥 FINAL TREND SCORES:\n")

    for i, (title, score) in enumerate(trends[:10], start=1):
        print(f"{i}. {title} → {round(score, 2)}")