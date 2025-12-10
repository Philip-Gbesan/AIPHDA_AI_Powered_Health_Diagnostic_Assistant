import sqlite3
from pathlib import Path

DB_PATH = "database/dev.sqlite"
SCHEMA_PATH = "database/schema.sql"
# SEED_PATH = "database/seed.sql"

def run_sql_file(cursor, filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

def init_db(seed=False):
    Path("database").mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load schema
    print("Applying database schema...")
    run_sql_file(cursor, SCHEMA_PATH)

    # # Optionally load seed data
    # if seed and Path(SEED_PATH).exists():
    #     print("Seeding database...")
    #     run_sql_file(cursor, SEED_PATH)

    conn.commit()
    conn.close()
    print("Database initialized successfully at", DB_PATH)


if __name__ == "__main__":
    init_db(seed=True)
