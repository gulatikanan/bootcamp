"""
Inheritance in Dataclass

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

# Base User class
@dataclass
class User:
    name: str
    age: int = 0  # Default value for age

# AdminUser class inherits from User
@dataclass
class AdminUser(User):
    access_level: str

# Test inheritance
admin = AdminUser(name="Admin", age=30, access_level="Super")
print(admin)  # Output: AdminUser(name='Admin', age=30, access_level='Super')
