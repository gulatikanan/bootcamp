"""
Default Values

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int = 0  # Default value for age

# Test object creation
user1 = User(name="Alice")
print(user1)  # Output: User(name='Alice', age=0)
