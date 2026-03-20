import hashlib
from database.db import get_connection
import sys
import os

# 🔥 Force add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# 🔐 Hash password (IMPORTANT)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# 👤 Register user
def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


# 🔓 Login user
def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed_password)
    )

    user = cursor.fetchone()
    conn.close()

    return user