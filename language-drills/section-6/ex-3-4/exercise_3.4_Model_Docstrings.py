"""
Model Docstrings

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel, Field

class User(BaseModel):
    """
    User model represents a user in the system with basic details.
    It includes personal information like name, email, and user ID.
    """

    id: int = Field(..., alias="user_id", description="Unique identifier for the user.")
    name: str = Field(..., description="Full name of the user.")
    email: str = Field(..., description="User's email address.")
    age: int = Field(..., description="Age of the user.")

# Example Usage
user_data = {
    "user_id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
}

# When using aliases, Pydantic automatically converts the input data to match the attribute name
user = User(**user_data)
print(user)
