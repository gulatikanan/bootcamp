"""
Custom Method

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    country: str = "India"

    def is_adult(self):
        return self.age >= 18

# Example usage
user1 = User("Alice", 25)
print(user1.is_adult())  # Output: True
