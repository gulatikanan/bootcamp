"""Module: serialize.py
Author: Kanan"""

from user import User

user = User("kanan", "supersecret123", "kanan@example.com")

# Serialize without password
safe_json = user.to_safe_json()

# Save to file
with open("user_safe.json", "w") as f:
    f.write(safe_json)

print("✅ User serialized without sensitive attributes:")
print(safe_json)
