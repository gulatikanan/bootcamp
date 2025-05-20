"""
Field Constraints

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel, conint, constr, ValidationError

# Define a User model with constraints
class User(BaseModel):
    name: constr(min_length=3)  # Ensures the name has a minimum length of 3 characters
    age: conint(gt=0)  # Ensures age is greater than 0

# Valid case: both name and age are valid
try:
    user_data = {"name": "Alice", "age": 30}
    user = User(**user_data)
    print(user)  # Should print: name='Alice' age=30
except ValidationError as e:
    print("Validation error:", e)

# Invalid case: name too short (less than 3 characters)
try:
    user_data = {"name": "Al", "age": 30}  # Name is less than 3 characters
    user = User(**user_data)
except ValidationError as e:
    print("Validation error:", e)  # Will show an error related to 'name'

# Invalid case: age less than or equal to 0
try:
    user_data = {"name": "Alice", "age": 0}  # Age is less than or equal to 0
    user = User(**user_data)
except ValidationError as e:
    print("Validation error:", e)  # Will show an error related to 'age'
