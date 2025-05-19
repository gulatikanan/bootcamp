import sqlite3
import os

class Product:
    def __init__(self):
        # Set the absolute path
        base_path = r"D:\aganitha_bootcamp\persistence_drills\sqlite_basics\03_class_based_operations"
        self.db_name = os.path.join(base_path, "store.db")
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()

            # Create categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            ''')
            cursor.executemany(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                [('Fruits',), ('Vegetables',), ('Dairy',)]
            )

            # Create products table with category_id
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
        finally:
            conn.close()

    def add_product(self, name, price, category_name=None):
        try:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Product name must be a non-empty string.")
            if not isinstance(price, (int, float)) or price <= 0:
                raise ValueError("Product price must be a positive number.")

            conn = self._connect()
            cursor = conn.cursor()

            # Handle category
            category_id = None
            if category_name:
                cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
                cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
                result = cursor.fetchone()
                if result:
                    category_id = result[0]

            cursor.execute(
                "INSERT INTO products (name, price, category_id) VALUES (?, ?, ?)",
                (name.strip(), price, category_id)
            )

            conn.commit()
            print(f"✅ Product '{name}' added.")
        except Exception as e:
            print(f"❌ Error adding product: {e}")
        finally:
            conn.close()

    def list_products_with_categories(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.name, p.price, c.name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
            ''')
            rows = cursor.fetchall()
            print("\n📦 Products with Categories:")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]} | Category: {row[3] or 'Uncategorized'}")
        except Exception as e:
            print(f"❌ Error fetching joined data: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    pm = Product()
    pm.add_product("Apple", 3.5, "Fruits")
    pm.add_product("Carrot", 1.0, "Vegetables")
    pm.add_product("Milk", 2.5, "Dairy")

    pm.list_products_with_categories()
