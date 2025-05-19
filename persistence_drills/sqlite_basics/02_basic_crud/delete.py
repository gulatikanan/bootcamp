import sqlite3

# Step 6: Function to delete a product by ID
def delete_product(product_id: int):
    try:
        # --- Validate input ---
        if not isinstance(product_id, int):
            raise ValueError("Product ID must be an integer.")

        # --- Connect to database ---
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()

        # --- Execute DELETE command ---
        cursor.execute('''
            DELETE FROM products
            WHERE id = ?
        ''', (product_id,))

        conn.commit()

        # --- Check if product was deleted ---
        if cursor.rowcount == 0:
            print(f"⚠️ No product found with ID {product_id}.")
        else:
            print(f"✅ Product with ID {product_id} deleted successfully.")

    except Exception as e:
        print(f"❌ Error deleting product: {e}")
    
    finally:
        conn.close()

# 🔁 Example usage
delete_product(2)  # Delete Banana (ID 2)
