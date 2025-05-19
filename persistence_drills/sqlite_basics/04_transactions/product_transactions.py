import sqlite3
import os

class Product:
    def __init__(self):
        base_path = r"D:\aganitha_bootcamp\persistence_drills\sqlite_basics\03_class_based_operations"
        self.db_name = os.path.join(base_path, "store.db")
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL CHECK(price > 0)
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"❌ Error creating table: {e}")

    def add_product(self, name, price):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Product price must be a positive number.")

        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("BEGIN")
                cursor.execute(
                    "INSERT INTO products (name, price) VALUES (?, ?)",
                    (name.strip(), price)
                )
                conn.commit()
                print(f"✅ Product '{name}' added successfully.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed: {e}")

    def update_price(self, product_id, new_price):
        if not isinstance(new_price, (int, float)) or new_price <= 0:
            raise ValueError("New price must be a positive number.")

        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("BEGIN")
                cursor.execute(
                    "UPDATE products SET price = ? WHERE id = ?",
                    (new_price, product_id)
                )
                conn.commit()
                print(f"🔁 Product ID {product_id} updated to ₹{new_price}.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed: {e}")

    def delete_product(self, product_id):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("BEGIN")
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
                conn.commit()
                print(f"🗑️ Product ID {product_id} deleted.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed: {e}")

    def list_products(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM products")
                rows = cursor.fetchall()
                print("\n📦 All Products:")
                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]}")
        except Exception as e:
            print(f"❌ Error fetching products: {e}")

# 🧪 Test Example
if __name__ == "__main__":
    pm = Product()

    # ✅ Add product
    pm.add_product("Notebook", 20)

    # ❌ Try adding invalid product
    try:
        pm.add_product("", -10)
    except ValueError as e:
        print("❗ Validation Error:", e)

    # ✅ Update
    pm.update_price(1, 25)

    # ✅ Delete
    pm.delete_product(1)

    # ✅ List
    pm.list_products()
