"""
Dataclass with Slots

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass(slots=True)
class User:
    name: str
    age: int
    country: str = "India"

# Example usage
user1 = User("Alice", 25)
print(user1)
