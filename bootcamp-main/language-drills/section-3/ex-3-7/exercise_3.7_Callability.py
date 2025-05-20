"""
Callability

Instructions:
Complete the exercise according to the requirements.
"""

class Greeter:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print(f"Hello, {self.name}!")

g = Greeter("Alice")
g()  # Calls __call__
