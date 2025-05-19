"""
Field Aliases

Instructions:
Complete the exercise according to the requirements.
"""
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., alias="user_id", description="Unique identifier for the user.")
    name: str = Field(..., description="Full name of the user.")
    email: str = Field(..., description="User's email address.")
    age: int = Field(..., description="Age of the user.")

    class Config:
        allow_population_by_field_name = True  # Allow population using field name, not alias

# Example Usage
user_data = {
    "user_id": 1,  # Use the alias 'user_id' in the input data
    "name": "Bob",
    "email": "bob@example.com",
    "age": 25
}
user = User(**user_data)
print(user)
