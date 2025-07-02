import sqlite3
import os
from datetime import datetime
import pandas as pd

# Inisialisasi DB saat pertama
def init_db(db_path="sidilan.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pict TEXT NOT NULL,
            object_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            cctv_location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan data
def save_to_db(pict_path, cctv_location, object_id, db_path="sidilan.db"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO violations (pict, object_id, timestamp, cctv_location)
        VALUES (?, ?, ?, ?)
    ''', (pict_path, object_id, timestamp, cctv_location))
    conn.commit()
    conn.close()
    print(f"[DB] Saved to database: {pict_path}, {cctv_location}, {timestamp}")

def export_to_csv(db_path="sidilan.db", out_path="violations.csv"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM violations", conn)
    df.to_csv(out_path, index=False)
    conn.close()

def get_last_object_id(db_path="sidilan.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT MAX(object_id) FROM violations")
    result = c.fetchone()
    conn.close()
    return result[0] if result[0] is not None else 0