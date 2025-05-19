
# Boundary Testing with Large Datasets

import sqlite3
import time

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")

def single_inserts(n):
    start = time.time()
    for i in range(n):
        conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", (f"Product{i}", i))
    conn.commit()
    return time.time() - start

def batch_insert(n):
    start = time.time()
    with conn:
        conn.executemany("INSERT INTO products (name, price) VALUES (?, ?)",
                         [(f"Product{i}", i) for i in range(n)])
    return time.time() - start

n = 100_000
print(f"Single inserts: {single_inserts(n):.2f} seconds")
conn.execute("DELETE FROM products")
print(f"Batch inserts: {batch_insert(n):.2f} seconds")

conn.close()
