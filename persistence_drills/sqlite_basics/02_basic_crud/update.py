# 5.Updating Data
import sqlite3

def update_product_price(product_id: int, new_price: float):
    try:
        # --- Validate new price ---
        if not isinstance(new_price, (int, float)) or new_price <= 0:
            raise ValueError("Price must be a positive number.")

        # --- Connect to database ---
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()

        # --- Execute update command ---
        cursor.execute('''
            UPDATE products
            SET price = ?
            WHERE id = ?
        ''', (new_price, product_id))

        conn.commit()

        # --- Check if product was updated ---
        if cursor.rowcount == 0:
            print(f"⚠️ No product found with ID {product_id}.")
        else:
            print(f"✅ Product ID {product_id} updated successfully to ₹{new_price}.")

    except Exception as e:
        print(f"❌ Error updating product: {e}")
    
    finally:
        conn.close()

# 🔁 Example usage
update_product_price(1, 2.0)  # Change Apple’s price to 2.0






