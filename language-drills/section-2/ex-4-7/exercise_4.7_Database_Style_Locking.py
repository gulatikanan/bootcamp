"""
Database Style Locking

Instructions:
Complete the exercise according to the requirements.
"""
class DBConnection:
    def __enter__(self):
        print("DB connected.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("DB disconnected.")

with DBConnection():
    print("Performing DB operations...")
