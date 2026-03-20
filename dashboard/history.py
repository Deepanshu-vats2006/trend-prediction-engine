import sys
import os

# 🔥 Force add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from database.db import get_connection
from datetime import datetime

# 💾 Save search history
def save_history(user_id, query):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO history (user_id, query, timestamp) VALUES (?, ?, ?)",
        (user_id, query, timestamp)
    )

    conn.commit()
    conn.close()


# 📥 Get history for a user
def get_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT query, timestamp
        FROM history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        """,
        (user_id,)
    )

    data = cursor.fetchall()
    conn.close()

    return data


# 🗑️ (Optional) Clear history for a user
def clear_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()