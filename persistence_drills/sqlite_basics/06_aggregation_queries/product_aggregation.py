import sqlite3
import os

class Product:
    def __init__(self):
        base_path = r"D:\aganitha_bootcamp\persistence_drills\sqlite_basics\03_class_based_operations"
        self.db_name = os.path.join(base_path, "store.db")
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS products")
                cursor.execute("DROP TABLE IF EXISTS categories")

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL CHECK(price > 0),
                        category_id INTEGER,
                        FOREIGN KEY (category_id) REFERENCES categories(id)
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"❌ Error creating tables: {e}")

    def _get_or_create_category(self, category_name):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            row = cursor.fetchone()
            if row:
                return row[0]
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
            conn.commit()
            return cursor.lastrowid

    def add_product(self, name, price, category_name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Product price must be a positive number.")

        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("BEGIN")
                category_id = self._get_or_create_category(category_name)
                cursor.execute(
                    "INSERT INTO products (name, price, category_id) VALUES (?, ?, ?)",
                    (name.strip(), price, category_id)
                )
                conn.commit()
                print(f"✅ Product '{name}' added under '{category_name}' category.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding product: {e}")

    def list_products_with_categories(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT p.id, p.name, p.price, c.name AS category
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.id
                ''')
                rows = cursor.fetchall()
                print("\n📦 Products with Categories:")
                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]} | Category: {row[3]}")
        except Exception as e:
            print(f"❌ Error fetching joined data: {e}")

    # ✅ Step 13: Aggregation Query
    def get_total_inventory_value(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(price) FROM products")
                result = cursor.fetchone()
                total = result[0] if result[0] is not None else 0
                print(f"\n💰 Total Inventory Value: ₹{total}")
                return total
        except Exception as e:
            print(f"❌ Error calculating total inventory value: {e}")
            return 0

# 🧪 Test Example
if __name__ == "__main__":
    pm = Product()

    pm.add_product("Apple", 3.5, "Fruits")
    pm.add_product("Carrot", 1.0, "Vegetables")
    pm.add_product("Milk", 2.5, "Dairy")

    pm.list_products_with_categories()

    # ✅ Aggregation step
    pm.get_total_inventory_value()
