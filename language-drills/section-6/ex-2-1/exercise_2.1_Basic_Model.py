"""
Basic Model

Instructions:
Complete the exercise according to the requirements.
"""
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Example usage
user_data = {"name": "Alice", "age": 30}
user = User(**user_data)
print(user)
