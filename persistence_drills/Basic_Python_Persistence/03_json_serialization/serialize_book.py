"""Module: serialize.py
Author: Kanan"""

from book import Book

# Create Book instance
book = Book("Atomic Habits", "James Clear", 2018)

# Serialize to JSON
json_string = book.to_json()

# Save to file (optional)
with open("book.json", "w") as f:
    f.write(json_string)

# Print JSON
print("✅ Book serialized to JSON:")
print(json_string)
