"""
Custom Validator

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel, validator, ValidationError

class User(BaseModel):
    name: str
    age: int

    @validator('name')
    def check_name_capitalization(cls, v):
        if not v[0].isupper():
            raise ValueError('Name must start with a capital letter.')
        return v

# Valid case
try:
    user_data = {"name": "Alice", "age": 25}
    user = User(**user_data)
    print(user)
except ValidationError as e:
    print("Validation error:", e)

# Invalid case: name doesn't start with a capital letter
try:
    user_data = {"name": "alice", "age": 25}  # Name doesn't start with a capital letter
    user = User(**user_data)
except ValidationError as e:
    print("Validation error:", e)  # Will show error because name doesn't start with a capital letter
