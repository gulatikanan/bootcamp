# Data Lifecycle Management

import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        deleted_at TEXT
    )
""")

conn.execute("INSERT INTO products (name) VALUES ('Apple')")
conn.execute("UPDATE products SET deleted_at = ? WHERE name = 'Apple'", (datetime.now().isoformat(),))
conn.commit()

print("Non-deleted products:")
for row in conn.execute("SELECT * FROM products WHERE deleted_at IS NULL"):
    print(row)

print("\nCleanup script running...")
conn.execute("DELETE FROM products WHERE deleted_at < ?", ((datetime.now() - timedelta(days=30)).isoformat(),))
conn.commit()

for row in conn.execute("SELECT * FROM products"):
    print(row)

conn.close()