import pickle

# Deserialize
with open("org.pkl", "rb") as f:
    manager = pickle.load(f)

print("✅ Organization deserialized:")
print("Manager:", manager.name)
for emp in manager.employees:
    print(f"Employee: {emp.name}, Reports to: {emp.manager.name}")
