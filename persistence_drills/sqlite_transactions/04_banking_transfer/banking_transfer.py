import sqlite3
import os

class BankingDB:
    def __init__(self):
        base_path = r"D:\aganitha_bootcamp\persistence_drills\sqlite_basics\03_class_based_operations"
        self.db_name = os.path.join(base_path, "banking.db")
        self._create_accounts_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_accounts_table(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS accounts (
                        account_id INTEGER PRIMARY KEY,
                        balance REAL NOT NULL CHECK(balance >= 0)
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"❌ Error creating accounts table: {e}")

    def create_account(self, account_id, initial_balance=0):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO accounts (account_id, balance) VALUES (?, ?)",
                               (account_id, initial_balance))
                conn.commit()
                print(f"✅ Account {account_id} created with balance {initial_balance}.")
        except Exception as e:
            print(f"❌ Error creating account: {e}")

    def get_balance(self, account_id):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
                row = cursor.fetchone()
                if row:
                    return row[0]
                else:
                    print(f"❌ Account {account_id} not found.")
                    return None
        except Exception as e:
            print(f"❌ Error fetching balance: {e}")
            return None

    def transfer_funds(self, from_account, to_account, amount):
        if amount <= 0:
            print("❌ Transfer amount must be positive.")
            return

        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")

            # Check balances
            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (from_account,))
            from_balance = cursor.fetchone()
            if not from_balance:
                raise ValueError(f"From account {from_account} does not exist.")
            from_balance = from_balance[0]

            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (to_account,))
            to_balance = cursor.fetchone()
            if not to_balance:
                raise ValueError(f"To account {to_account} does not exist.")
            to_balance = to_balance[0]

            if from_balance < amount:
                raise ValueError(f"Insufficient funds in account {from_account}. Available: {from_balance}, Required: {amount}")

            # Debit from_account
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (amount, from_account))

            # Credit to_account
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (amount, to_account))

            conn.commit()
            print(f"✅ Transferred {amount} from account {from_account} to account {to_account}.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Transfer failed, transaction rolled back. Reason: {e}")
        finally:
            conn.close()

# Example usage
if __name__ == "__main__":
    bank_db = BankingDB()
    
    # Create accounts if not already created
    bank_db.create_account(1, 1000)
    bank_db.create_account(2, 500)

    print(f"Balance Account 1 before transfer: {bank_db.get_balance(1)}")
    print(f"Balance Account 2 before transfer: {bank_db.get_balance(2)}")

    # Successful transfer
    bank_db.transfer_funds(1, 2, 200)

    print(f"Balance Account 1 after transfer: {bank_db.get_balance(1)}")
    print(f"Balance Account 2 after transfer: {bank_db.get_balance(2)}")

    # Failed transfer due to insufficient funds
    bank_db.transfer_funds(2, 1, 1000)
