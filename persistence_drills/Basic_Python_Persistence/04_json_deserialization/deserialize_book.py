"""Module: deserialize.py
Author: Kanan"""

from book import Book

# Read from previously saved JSON file
with open("book.json", "r") as f:
    json_data = f.read()

# Convert JSON string to Book object
book = Book.from_json(json_data)

# Print book info
print("✅ Book deserialized from JSON:")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Year: {book.year}")

