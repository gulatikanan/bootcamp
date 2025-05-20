"""
Frozen Dataclass

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True)
class User:
    name: str
    age: int
    country: str = "India"

# Example usage
user1 = User("Alice", 25)
print(user1)

try:
    user1.age = 30  # Attempting to modify an immutable field will raise an error
except FrozenInstanceError as e:
    print(e)  # Output: cannot assign to field 'age'
