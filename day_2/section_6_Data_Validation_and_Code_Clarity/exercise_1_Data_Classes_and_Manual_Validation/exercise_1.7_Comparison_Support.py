"""
Comparison Support

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    country: str = "India"

# Example usage
user1 = User("Alice", 25)
user2 = User("Alice", 25)
user3 = User("Bob", 30)

print(user1 == user2)  # Output: True
print(user1 == user3)  # Output: False
