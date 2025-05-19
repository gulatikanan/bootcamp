"""
Class Method

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @classmethod
    def from_string(cls, s: str):
        title, author = s.split('|')
        return cls(title, author)

# Test the class method
book_str = "The Great Gatsby|F. Scott Fitzgerald"
book = Book.from_string(book_str)
print(book.title)  # Output: The Great Gatsby
print(book.author)  # Output: F. Scott Fitzgerald
