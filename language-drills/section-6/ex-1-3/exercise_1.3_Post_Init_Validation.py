"""
Post Init Validation

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    country: str = "India"

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

# Example usage
try:
    user1 = User("Alice", -5)
except ValueError as e:
    print(e)  # Output: Age cannot be negative
