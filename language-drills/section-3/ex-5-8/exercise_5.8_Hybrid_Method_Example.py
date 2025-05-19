"""
Hybrid Method Example

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        # Validate ISBN (static, does not need an instance)
        return len(isbn) == 13 or len(isbn) == 10

    @classmethod
    def from_string(cls, s: str):
        # Parse string into a Book (class method, allows subclassing)
        title, author = s.split('|')
        return cls(title, author)

    def display_info(self):
        # Instance method to display book info
        print(f"Title: {self.title}, Author: {self.author}")

# Usage of static, class, and instance methods
isbn = "9783161484100"
if Book.validate_isbn(isbn):  # Static method for ISBN validation
    book_str = "To Kill a Mockingbird|Harper Lee"
    book = Book.from_string(book_str)  # Class method to create a Book
    book.display_info()  # Instance method to display info
