"""
Nested Models

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel

class Profile(BaseModel):
    bio: str
    website: str

class User(BaseModel):
    name: str
    age: int
    profile: Profile

# Example usage
profile_data = {"bio": "Software Developer", "website": "https://example.com"}
user_data = {"name": "Alice", "age": 30, "profile": profile_data}
user = User(**user_data)
print(user)
