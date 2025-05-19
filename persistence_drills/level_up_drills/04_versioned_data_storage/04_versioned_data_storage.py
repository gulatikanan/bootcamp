# Versioned Data Storage

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE user_emails (
        user_id INTEGER,
        email TEXT,
        version INTEGER,
        updated_at TEXT DEFAULT (datetime('now')),
        PRIMARY KEY(user_id, version)
    )
""")

def update_email(user_id, email):
    cursor = conn.execute("SELECT MAX(version) FROM user_emails WHERE user_id = ?", (user_id,))
    version = (cursor.fetchone()[0] or 0) + 1
    conn.execute("INSERT INTO user_emails (user_id, email, version) VALUES (?, ?, ?)",
                 (user_id, email, version))
    conn.commit()

update_email(1, "xyz@a.com")
update_email(1, "xyz@b.com")

print("All versions:")
for row in conn.execute("SELECT * FROM user_emails"):
    print(row)

print("\nLatest version:")
for row in conn.execute("""
    SELECT * FROM user_emails
    WHERE (user_id, version) IN (
        SELECT user_id, MAX(version) FROM user_emails GROUP BY user_id
    )
"""):
    print(row)

conn.close()