import sqlite3

# 3. Inserting Data
def insert_product(name: str, price: float):
    try:
        # --- Data validation ---
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")

        # --- Connect to the database ---
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()

        # --- SQL INSERT command ---
        cursor.execute('''
            INSERT INTO products (name, price)
            VALUES (?, ?)
        ''', (name.strip(), price))

        conn.commit()
        print(f"✅ Product '{name}' inserted successfully with price {price}.")

    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        conn.close()

# 🔁 Sample insert calls
insert_product("Apple", 1.2)
insert_product("Banana", 0.5)
