#--------------------------------

# Imports
import sqlite3
import psutil
from datetime import datetime
#--------------------------------

# Database
DB_NAME = "system_info.db"

def init_db():
    """
    database structure
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Error logs
    c.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            error_type TEXT,
            message TEXT,
            traceback TEXT
        )
    """)
    # System performance logs
    c.execute("""
        CREATE TABLE IF NOT EXISTS system_performance (
            timestamp TEXT PRIMARY KEY,
            temperature REAL,
            cpu_percent REAL,
            memory_percent REAL
        )
    """)

    conn.commit()
    conn.close()
#--------------------------------

# Error log functions
def log_error(error_type, message, traceback_str=None):
    """
    log an error
    """
    timestamp = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO error_logs (timestamp, error_type, message, traceback)
            VALUES (?, ?, ?, ?)
        """, (timestamp, error_type, message, traceback_str))

def get_all_error_logs():
    """
    retrieve all errors
    """
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM error_logs ORDER BY timestamp DESC')
        return c.fetchall()
#--------------------------------

# System performance functions
def log_performance():
    """
    save performance stats
    """
    timestamp = datetime.now().isoformat()
    temperature = get_temperature()
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO system_performance (timestamp, temperature, cpu_percent, memory_percent)
            VALUES (?, ?, ?, ?)
        """, (timestamp, temperature, cpu, memory))
# sub-function ^
def get_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
            return int(temp_str) / 1000.0
    except FileNotFoundError:
        return None

def get_performance():
    """
    get performance logs
    """
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM system_performance ORDER BY timestamp DESC')
        return c.fetchall()
#--------------------------------
