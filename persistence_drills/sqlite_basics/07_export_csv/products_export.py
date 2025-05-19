import sqlite3
import os
import csv

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
                cursor.execute(
                    "INSERT INTO products (name, price) VALUES (?, ?)",
                    (name.strip(), price)
                )
                conn.commit()
                print(f"✅ Product '{name}' added.")
        except Exception as e:
            print(f"❌ Error adding product: {e}")

    def export_products_to_csv(self, csv_path):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM products")
                rows = cursor.fetchall()
                if not rows:
                    print("⚠️ No data to export.")
                    return
                # Get column names for header
                column_names = [description[0] for description in cursor.description]

            with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(column_names)  # write header
                writer.writerows(rows)          # write data rows

            print(f"✅ Data exported successfully to '{csv_path}'.")
        except Exception as e:
            print(f"❌ Error exporting data to CSV: {e}")

# 🧪 Test Example
if __name__ == "__main__":
    pm = Product()

    # Add some sample products (if needed)
    pm.add_product("Orange", 2.3)
    pm.add_product("Banana", 1.1)

    # Export to CSV
    csv_file_path = r"D:\aganitha_bootcamp\persistence_drills\sqlite_basics\07_export_csv\products_export.csv"
    pm.export_products_to_csv(csv_file_path)
