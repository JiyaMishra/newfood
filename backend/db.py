import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "messwise.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            meal TEXT NOT NULL,
            food_item TEXT NOT NULL,
            predicted_consumers INTEGER,
            actual_consumers INTEGER,
            prepared_portions INTEGER,
            leftover_portions INTEGER
        )
    ''')
    conn.commit()
    conn.close()
