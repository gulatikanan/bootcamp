# Handling Large Binary Data

import sqlite3

# BLOB approach
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE user_images (id INTEGER PRIMARY KEY, image BLOB)")

with open("random.jpg", "rb") as f:
    conn.execute("INSERT INTO user_images (image) VALUES (?)", (f.read(),))

print("Inserted image as blob.")
conn.close()