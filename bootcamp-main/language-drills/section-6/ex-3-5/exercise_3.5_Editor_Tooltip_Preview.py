"""
Editor Tooltip Preview

Instructions:
Complete the exercise according to the requirements.
"""

from pydantic import BaseModel, Field

class User(BaseModel):
    """
    User model to represent the basic information of a user.
    This model is used to store user details like name, email, and age.
    """
    name: str = Field(..., description="User's full name", title="Full Name", example="John Doe")
    email: str = Field(..., description="User's email address", title="Email", example="john.doe@example.com")
    age: int = Field(..., ge=18, description="User's age, must be greater than or equal to 18", title="Age", example=30)

# Example usage of the User model
user = User(name="Jane Smith", email="jane.smith@example.com", age=25)

# Print out the user data
print(user)
