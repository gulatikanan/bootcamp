import sqlite3

# Step 1: Connect to or create the database
def setup_database():
    # This line connects to store.db — creates the file if it doesn't exist
    conn = sqlite3.connect('store.db')

    print("✅ Database 'store.db' created or connected successfully.")

    # Closing the connection is important to avoid locks
    conn.close()

# Call the function
setup_database()
