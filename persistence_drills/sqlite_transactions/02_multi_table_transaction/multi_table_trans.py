import sqlite3
import os

class OrderDB:
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
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name TEXT NOT NULL,
                        status TEXT NOT NULL
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS order_details (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        product_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        FOREIGN KEY(order_id) REFERENCES orders(id)
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"❌ Error creating tables: {e}")

    def update_order_and_details(self, order_id, new_status, new_quantity):
        """
        Update order status and order_details quantity in one transaction.

        :param order_id: int, id of the order to update
        :param new_status: str, new status for the order
        :param new_quantity: int, new quantity for order details
        """
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")

            # Update orders table
            cursor.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (new_status, order_id)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"No order found with id {order_id}")

            # Update order_details table
            cursor.execute(
                "UPDATE order_details SET quantity = ? WHERE order_id = ?",
                (new_quantity, order_id)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"No order details found for order_id {order_id}")

            conn.commit()
            print(f"✅ Transaction committed: Order {order_id} updated.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed, rolled back. Error: {e}")
        finally:
            conn.close()


# Test example
if __name__ == "__main__":
    order_db = OrderDB()

    # For testing, first insert dummy order and order details (only if not exist)
    with order_db._connect() as conn:
        cur = conn.cursor()
        # Insert dummy order if not exist
        cur.execute("SELECT id FROM orders WHERE id = 1")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO orders (customer_name, status) VALUES (?, ?)", ("John Doe", "Pending"))
            order_id = cur.lastrowid
            cur.execute("INSERT INTO order_details (order_id, product_name, quantity) VALUES (?, ?, ?)",
                        (order_id, "Widget", 10))
            conn.commit()

    # Now update in transaction
    order_db.update_order_and_details(order_id=1, new_status="Shipped", new_quantity=20)
