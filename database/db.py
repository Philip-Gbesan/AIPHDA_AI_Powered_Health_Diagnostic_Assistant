import os
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database/dev.sqlite")

def get_connection():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=15,
        isolation_level=None,     # autocommit
        check_same_thread=False   # required for Flask
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

