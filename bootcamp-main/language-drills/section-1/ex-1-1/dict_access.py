user = {"name": "Alice"}
print(user.get("name"))           # Alice
print(user.get("age", "N/A"))     # N/A

user.setdefault("age", 25)

print(user)  # {'name': 'Alice', 'age': 25}
