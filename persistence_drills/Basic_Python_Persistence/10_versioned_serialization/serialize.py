"""Module: serialize.py
Author: Kanan"""

from collection import MyCollection

collection = MyCollection()
collection.add("Python")
collection.add("Data Science")
collection.add({"project": "AI Assistant", "status": "done"})

collection.save_to_file("collection.json")
print("✅ Collection serialized to collection.json")

