import sqlite3
from datetime import datetime

def setup_initial_schema(conn):
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany("INSERT INTO users (name) VALUES (?)", [("Kanan",), ("XYZ",)])
    conn.commit()

def apply_migration(conn):
    # Create new table with the new schema
    conn.execute("""
        CREATE TABLE users_new (
            id INTEGER PRIMARY KEY,
            name TEXT,
            created_at TEXT
        )
    """)
    # Copy data and set created_at manually
    now = datetime.now().isoformat()
    for row in conn.execute("SELECT id, name FROM users"):
        conn.execute("INSERT INTO users_new (id, name, created_at) VALUES (?, ?, ?)",
                     (row[0], row[1], now))
    conn.commit()
    # Drop old table and rename new table
    conn.execute("DROP TABLE users")
    conn.execute("ALTER TABLE users_new RENAME TO users")
    conn.commit()

def show_users(conn):
    print("After migration:")
    for row in conn.execute("SELECT * FROM users"):
        print(row)

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_initial_schema(conn)

    print("Before migration:")
    for row in conn.execute("SELECT * FROM users"):
        print(row)

    apply_migration(conn)
    show_users(conn)