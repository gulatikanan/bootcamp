"""
Boolean Check

Instructions:
Complete the exercise according to the requirements.
"""

class Box:
    def __init__(self, items):
        self.items = items

    def __bool__(self):
        return bool(self.items)

box1 = Box([])
box2 = Box([1])
print(bool(box1))  # False
print(bool(box2))  # True
