import sqlite3

DB_PATH = "database/trends.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # 🔥 Unified trends table (VERY IMPORTANT)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        platform TEXT,
        trend_score REAL,
        timestamp TEXT
    )
    """)

    # Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        query TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# 🔥 INSERT TREND (COMMON FUNCTION)
def insert_trend(title, platform, score, timestamp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO trends (title, platform, trend_score, timestamp)
    VALUES (?, ?, ?, ?)
    """, (title, platform, score, timestamp))

    conn.commit()
    conn.close()