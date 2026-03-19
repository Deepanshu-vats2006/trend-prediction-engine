import sqlite3

def create_tables():
    conn = sqlite3.connect("database/trends.db")
    cursor = conn.cursor()

    # your CREATE TABLE code...

    conn.commit()
    conn.close()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS youtube_trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        video_id TEXT,
        title TEXT,
        channel TEXT,
        published_at TEXT,
        UNIQUE(video_id)
    )
    """)

    conn.commit()


def insert_google(keyword, date, interest):
    conn = sqlite3.connect("database/trends.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO google_trends (keyword, date, interest)
        VALUES (?, ?, ?)
    """, (keyword, date, interest))

    conn.commit()
    conn.close()


def insert_youtube(keyword, video_id, title, channel, published_at):
    conn = sqlite3.connect("database/trends.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO youtube_trends
        (keyword, video_id, title, channel, published_at)
        VALUES (?, ?, ?, ?, ?)
    """, (keyword, video_id, title, channel, published_at))

    conn.commit()
    conn.close()