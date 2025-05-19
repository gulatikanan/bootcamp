from user_v2 import UserV2

user = UserV2()
user.load("user_v1.json")

print("✅ Loaded old user into new version class:")
print(f"Username: {user.username}")
print(f"Email: {user.email}")
