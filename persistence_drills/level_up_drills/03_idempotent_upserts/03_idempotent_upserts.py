# Idempotent Upserts (SQLite version)

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT UNIQUE, price REAL)")
conn.commit()

def upsert_product(name, price):
    conn.execute("""
        INSERT INTO products (name, price)
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET price=excluded.price
    """, (name, price))
    conn.commit()

upsert_product("Apple", 45.5)
upsert_product("Apple", 56.9)

for row in conn.execute("SELECT * FROM products"):
    print(row)

conn.close()