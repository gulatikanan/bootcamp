"""
Field Descriptions

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., description="Unique identifier for the user.")
    name: str = Field(..., description="Full name of the user.")
    email: str = Field(..., description="User's email address.")
    age: int = Field(..., description="Age of the user.")

# Example Usage
user_data = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
}
user = User(**user_data)
print(user)
