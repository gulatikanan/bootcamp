import sqlite3
# 4. Function to list all products
def list_products():
    try:
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()

        # --- SQL SELECT command ---
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()

        if rows:
            print("\n📦 Products in Store:")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]}")
        else:
            print("📭 No products found in the store.")

    except Exception as e:
        print(f"❌ Error reading products: {e}")
    
    finally:
        conn.close()

# 🔁 Call to display products
list_products()