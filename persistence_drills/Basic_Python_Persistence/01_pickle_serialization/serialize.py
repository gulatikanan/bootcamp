"""Module: deserialize.py
Author: Kanan"""

import pickle
from person import Person

# Create an instance
person = Person(
    name="Kanan",
    institutions=["Delhi University", "IIT Delhi"],
    colleagues=["Anurag", "Sneha"]
)

# Serialize and write to file
with open("person.pkl", "wb") as f:
    pickle.dump(person, f)

print("✅ Person object serialized successfully to 'person.pkl'")
