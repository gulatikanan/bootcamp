"""
Frozen Dataclass

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    age: int = 0

user1 = User(name="Alice", age=25)
print(user1)

# Trying to change the value will raise an error
# Uncommenting the line below will raise a FrozenInstanceError
# user1.age = 30
