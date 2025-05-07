"""
Custom Object

"""

class FlexiblePerson:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        return f"{item} not found"

person = FlexiblePerson("Alice")
print(person.name)     # Alice
print(person.age)      # age not found
