"""
Custom Method in Dataclass

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int = 0  # Default value for age

    def is_adult(self):
        return self.age >= 18  # Returns True if age is 18 or more

# Test object creation and calling the method
user1 = User(name="Alice", age=20)
print(user1.is_adult())  # Output: True

user2 = User(name="Bob", age=16)
print(user2.is_adult())  # Output: False
