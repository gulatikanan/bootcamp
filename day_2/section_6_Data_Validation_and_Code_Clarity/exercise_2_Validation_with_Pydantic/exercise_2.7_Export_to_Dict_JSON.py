"""
Export to Dict JSON

Instructions:
Complete the exercise according to the requirements.
"""
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user_data = {"name": "Alice", "age": 30}
user = User(**user_data)

# Convert to dict
user_dict = user.dict()
print(user_dict)  # Will print the dictionary representation

# Convert to JSON string
user_json = user.json()
print(user_json)  # Will print the JSON string
