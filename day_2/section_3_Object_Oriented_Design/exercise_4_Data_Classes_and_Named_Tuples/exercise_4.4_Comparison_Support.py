"""
Comparison Support

Instructions:
Complete the exercise according to the requirements.
"""

from dataclasses import dataclass
from collections import namedtuple

# Basic Dataclass
@dataclass
class User:
    name: str
    age: int = 0  # Default value for age

# Frozen Dataclass
@dataclass(frozen=True)
class UserFrozen:
    name: str
    age: int = 0

# Comparison support
user1 = User(name="Alice", age=20)
user2 = User(name="Alice", age=20)
print(user1 == user2)  # True

# Custom method in Dataclass
@dataclass
class UserWithMethod:
    name: str
    age: int = 0

    def is_adult(self):
        return self.age >= 18

user3 = UserWithMethod(name="Alice", age=20)
print(user3.is_adult())  # True

# NamedTuple basics
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)  # 1 2

# Inheritance in Dataclass
@dataclass
class AdminUser(User):
    access_level: str

admin = AdminUser(name="Admin", age=30, access_level="Super")
print(admin)  # AdminUser(name='Admin', age=30, access_level='Super')
