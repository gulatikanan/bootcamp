"""
Title and Examples

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel, Field
from typing import List

class User(BaseModel):
    id: int = Field(..., alias="user_id", description="Unique identifier for the user.", title="User ID", example=123)
    name: str = Field(..., description="Full name of the user.", title="User's Name", example="Alice")
    email: str = Field(..., description="User's email address.", title="Email Address", example="alice@example.com")
    age: int = Field(..., description="Age of the user.", title="User's Age", example=30)
    tags: List[str] = Field(default_factory=list, description="List of tags associated with the user.", example=["admin", "premium"])

# Example Usage
user_data = {
    "user_id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30,
    "tags": ["admin", "verified"]
}
user = User(**user_data)
print(user)
