"""
Difference in Behavior

Instructions:
Complete the exercise according to the requirements.
"""
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @staticmethod
    def static_method():
        # Cannot access instance (`self`) or class (`cls`)
        print("This is a static method!")

    @classmethod
    def class_method(cls):
        # Can access class (`cls`) but not instance (`self`)
        print(f"This is a class method of {cls.__name__}")

# Test
Book.static_method()  # Works fine
# Book.static_method(self)  # Error: static method cannot access 'self'
Book.class_method()  # Works fine

