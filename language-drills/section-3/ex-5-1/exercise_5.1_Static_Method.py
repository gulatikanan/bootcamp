"""
Static Method

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        # Check if the ISBN has a valid length (10 or 13 digits for simplicity)
        return len(isbn) == 13 or len(isbn) == 10

# Test the static method
isbn1 = "9783161484100"
isbn2 = "123456"

print(Book.validate_isbn(isbn1))  # Output: True
print(Book.validate_isbn(isbn2))  # Output: False
