"""
Automatic Conversion

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user_data = {"name": "Alice", "age": "42"}  # The string "42" will automatically be converted to an integer
user = User(**user_data)
print(user)  # Will print: name='Alice' age=42
