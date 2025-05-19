from collection import MyCollection

new_collection = MyCollection.from_file("collection.json")

print("✅ Collection loaded from file:")
print(new_collection.items)
