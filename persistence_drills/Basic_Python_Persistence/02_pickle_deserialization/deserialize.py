"""Module: deserialize.py
Author: Kanan"""

import pickle
from person import Person

# Read and deserialize the object from file
with open("person.pkl", "rb") as f:
    loaded_person = pickle.load(f)

# Print the object's data
print("✅ Person object deserialized from 'person.pkl'")
print("Name:", loaded_person.name)
print("Institutions:", loaded_person.institutions)
print("Colleagues:", loaded_person.colleagues)



#output: 
# ✅ Person object deserialized from 'person.pkl'
# Name: Kanan
# Institutions: ['Delhi University', 'IIT Delhi']
# Colleagues: ['Anurag', 'Sneha']