"""
Optional and Defaults

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

# Try passing incorrect data
try:
    user_data = {"name": "Bob", "age": "not a number"}  # age is a string, should be an integer
    user = User(**user_data)
except ValidationError as e:
    print("Validation error:", e)  # Will show the error related to 'age'
