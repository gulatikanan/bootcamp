"""
Pickle a Python Object

Instructions:
Complete the exercise according to the requirements.
"""
import pickle

# Python object
data = {"name": "Alice", "age": 30}

# Serialize with pickle
with open('data.pkl', 'wb') as file:
    pickle.dump(data, file)

# Deserialize with pickle
with open('data.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

print("Deserialized Data:", loaded_data)

