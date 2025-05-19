import sqlite3

class Product:
    def __init__(self, db_name='store.db'):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL CHECK(price > 0)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error creating table: {e}")
        finally:
            conn.close()

    def add_product(self, name, price):
        try:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Name must be a non-empty string.")
            if not isinstance(price, (int, float)) or price <= 0:
                raise ValueError("Price must be a positive number.")

            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name.strip(), price))
            conn.commit()
            print(f"✅ Product '{name}' added with price ₹{price}.")
        except Exception as e:
            print(f"❌ Error adding product: {e}")
        finally:
            conn.close()

    def list_products(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products')
            rows = cursor.fetchall()
            if rows:
                print("\n📦 Products List:")
                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]}")
            else:
                print("📭 No products found.")
        except Exception as e:
            print(f"❌ Error fetching products: {e}")
        finally:
            conn.close()

    def update_price(self, product_id, new_price):
        try:
            if not isinstance(new_price, (int, float)) or new_price <= 0:
                raise ValueError("Price must be a positive number.")
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('UPDATE products SET price = ? WHERE id = ?', (new_price, product_id))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"⚠️ No product found with ID {product_id}.")
            else:
                print(f"✅ Updated product ID {product_id} price to ₹{new_price}.")
        except Exception as e:
            print(f"❌ Error updating product: {e}")
        finally:
            conn.close()

    def delete_product(self, product_id):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"⚠️ No product found with ID {product_id}.")
            else:
                print(f"✅ Deleted product with ID {product_id}.")
        except Exception as e:
            print(f"❌ Error deleting product: {e}")
        finally:
            conn.close()

    def search_products(self, name_fragment):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            query = "SELECT * FROM products WHERE name LIKE ?"
            cursor.execute(query, ('%' + name_fragment + '%',))
            rows = cursor.fetchall()
            if rows:
                print(f"\n🔍 Search results for '{name_fragment}':")
                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]}")
            else:
                print(f"📭 No products found matching '{name_fragment}'.")
        except Exception as e:
            print(f"❌ Error searching products: {e}")
        finally:
            conn.close()


# Example usage
if __name__ == "__main__":
    pm = Product()
    pm.add_product("Mango", 1.5)
    pm.list_products()
    pm.update_price(1, 2.2)
    pm.search_products("Man")
    pm.delete_product(1)
    pm.list_products()
