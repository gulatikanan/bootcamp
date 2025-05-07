"""
Factory Default for Lists

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    name: str
    age: int
    tags: List[str] = field(default_factory=list)

# Example usage
user1 = User("Alice", 25)
print(user1.tags)  # Output: []
