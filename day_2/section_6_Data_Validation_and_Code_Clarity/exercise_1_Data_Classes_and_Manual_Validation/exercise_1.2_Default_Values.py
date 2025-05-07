"""
Default Values

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    country: str = "India"  # Default value

# Example usage
user1 = User("Alice", 25)
print(user1)  # Output: User(name='Alice', age=25, country='India')
