import sqlite3
import os

class CustomerDB:
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
                    CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"❌ Error creating customers table: {e}")

    def insert_customers_transaction(self, customers):
        """
        Insert multiple customers in a single transaction.

        :param customers: List of tuples [(name, email), ...]
        """
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")

            for name, email in customers:
                if not name.strip():
                    raise ValueError("Customer name cannot be empty.")
                if not email.strip():
                    raise ValueError("Customer email cannot be empty.")
                cursor.execute(
                    "INSERT INTO customers (name, email) VALUES (?, ?)",
                    (name.strip(), email.strip())
                )
            conn.commit()
            print(f"✅ Transaction committed: {len(customers)} customers inserted.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed, rolled back. Error: {e}")
        finally:
            conn.close()


# Test example
if __name__ == "__main__":
    cust_db = CustomerDB()

    # Define multiple customers to insert
    customers_to_add = [
        ("Alice Johnson", "alice.johnson@example.com"),
        ("Bob Smith", "bob.smith@example.com"),
        ("Charlie Brown", "charlie.brown@example.com"),
    ]

    cust_db.insert_customers_transaction(customers_to_add)
