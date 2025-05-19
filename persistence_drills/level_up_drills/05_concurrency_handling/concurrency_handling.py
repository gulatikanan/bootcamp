# Concurrency and Race Condition Management

import sqlite3

conn = sqlite3.connect(":memory:", isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)")
conn.execute("INSERT INTO accounts VALUES (1, 4000), (2, 5000)")

def transfer_naive(from_id, to_id, amount):
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))

def transfer_safe(from_id, to_id, amount):
    with conn:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))

transfer_safe(1, 2, 100)

for row in conn.execute("SELECT * FROM accounts"):
    print(row)

conn.close()