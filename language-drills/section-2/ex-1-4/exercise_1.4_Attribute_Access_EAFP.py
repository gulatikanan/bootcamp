class Person:
    def __init__(self, name):
        self.name = name

p = Person("Alice")

# EAFP: Use getattr with fallback
age = getattr(p, 'age', 'Unknown')
print("Age:", age)
