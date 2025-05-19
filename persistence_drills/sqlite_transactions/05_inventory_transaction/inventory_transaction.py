import sqlite3
import os
from datetime import datetime

class InventoryDB:
    def __init__(self):
        base_path = r"D:\aganitha_bootcamp\persistence_drills\sqlite_basics\03_class_based_operations"
        self.db_name = os.path.join(base_path, "inventory.db")
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                # Create products table with inventory count
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL NOT NULL CHECK(price >= 0),
                        inventory_count INTEGER NOT NULL DEFAULT 0 CHECK(inventory_count >= 0)
                    )
                ''')
                # Create inventory_log table for audit trail
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS inventory_log (
                        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER NOT NULL,
                        change_amount INTEGER NOT NULL,
                        change_reason TEXT NOT NULL,
                        change_time TEXT NOT NULL,
                        FOREIGN KEY(product_id) REFERENCES products(product_id)
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"❌ Error creating tables: {e}")

    def add_product(self, product_id, name, price, inventory_count=0):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO products (product_id, name, price, inventory_count)
                    VALUES (?, ?, ?, ?)
                ''', (product_id, name, price, inventory_count))
                conn.commit()
                print(f"✅ Added product {name} with inventory {inventory_count}.")
        except Exception as e:
            print(f"❌ Error adding product: {e}")

    def update_inventory(self, product_id, change_amount, change_reason):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")

            # Check current inventory
            cursor.execute("SELECT inventory_count FROM products WHERE product_id = ?", (product_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Product ID {product_id} does not exist.")
            current_inventory = row[0]

            new_inventory = current_inventory + change_amount
            if new_inventory < 0:
                raise ValueError(f"Inventory cannot be negative. Current: {current_inventory}, Change: {change_amount}")

            # Update inventory count
            cursor.execute("UPDATE products SET inventory_count = ? WHERE product_id = ?", (new_inventory, product_id))

            # Insert log entry
            now = datetime.utcnow().isoformat()
            cursor.execute('''
                INSERT INTO inventory_log (product_id, change_amount, change_reason, change_time)
                VALUES (?, ?, ?, ?)
            ''', (product_id, change_amount, change_reason, now))

            conn.commit()
            print(f"✅ Inventory updated by {change_amount} for product {product_id}. Reason: {change_reason}")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed, rolled back. Reason: {e}")
        finally:
            conn.close()

    def get_inventory(self, product_id):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT inventory_count FROM products WHERE product_id = ?", (product_id,))
                row = cursor.fetchone()
                if row:
                    return row[0]
                else:
                    print(f"❌ Product {product_id} not found.")
                    return None
        except Exception as e:
            print(f"❌ Error fetching inventory: {e}")
            return None

# Example usage
if __name__ == "__main__":
    db = InventoryDB()

    # Add sample product
    db.add_product(101, "Widget", 10.99, 50)

    # Update inventory: Add 20 items (stock received)
    db.update_inventory(101, 20, "Restocked")

    # Update inventory: Remove 10 items (sale)
    db.update_inventory(101, -10, "Sold 10 units")

    # Attempt to reduce more than available (should rollback)
    db.update_inventory(101, -100, "Attempt to sell too many")

    print(f"Final inventory for product 101: {db.get_inventory(101)}")
