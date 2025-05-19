# 2. Creating a Table
import sqlite3

def create_products_table():
    # Connect to the database
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()

    # SQL command to create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0)
        )
    ''')

    # Commit the changes and close connection
    conn.commit()
    conn.close()

    print("✅ Table 'products' created successfully.")

# Call the function
create_products_table()