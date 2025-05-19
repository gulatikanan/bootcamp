import sqlite3
import os

class ProductDB:
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

    def batch_insert_products(self, product_list):
        """
        Insert multiple products in a single transaction.
        Rolls back if any insert fails.

        :param product_list: List of tuples [(name, price), ...]
        """
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")

            for name, price in product_list:
                # Data validation
                if not isinstance(name, str) or not name.strip():
                    raise ValueError(f"Invalid product name: {name}")
                if not (isinstance(price, (int, float)) and price > 0):
                    raise ValueError(f"Invalid product price: {price}")

                cursor.execute(
                    "INSERT INTO products (name, price) VALUES (?, ?)",
                    (name.strip(), price)
                )
            conn.commit()
            print(f"✅ Successfully inserted {len(product_list)} products.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed, rolled back. Error: {e}")
        finally:
            conn.close()

# Example usage
if __name__ == "__main__":
    product_db = ProductDB()
    products_to_add = [
        ("Product A", 12.5),
        ("Product B", 7.99),
        ("Product C", 15.0),
    ]
    product_db.batch_insert_products(products_to_add)

    # Try inserting invalid data to test rollback
    invalid_products = [
        ("Good Product", 10),
        ("", 20),  # Invalid name
        ("Another Product", -5),  # Invalid price
    ]
    product_db.batch_insert_products(invalid_products)
