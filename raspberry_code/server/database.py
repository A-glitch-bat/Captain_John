#--------------------------------

# Imports
import sqlite3
from datetime import datetime
#--------------------------------

# Database declaration
DB_NAME = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            error_type TEXT,
            message TEXT,
            traceback TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_error(error_type, message, traceback_str=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute("""
        INSERT INTO error_logs (timestamp, error_type, message, traceback)
        VALUES (?, ?, ?, ?)
    """, (timestamp, error_type, message, traceback_str))
    conn.commit()
    conn.close()

def get_all_error_logs(self):
    cursor = self.connection.cursor()
    cursor.execute('SELECT * FROM error_logs ORDER BY timestamp DESC')
    return cursor.fetchall()
#--------------------------------
