"""
Invoke Static Method

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        return len(isbn) == 13 or len(isbn) == 10

# Calling from the class
print(Book.validate_isbn("9783161484100"))  # Output: True

# Calling from an instance
book_instance = Book("1984", "George Orwell")
print(book_instance.validate_isbn("123456"))  # Output: False
