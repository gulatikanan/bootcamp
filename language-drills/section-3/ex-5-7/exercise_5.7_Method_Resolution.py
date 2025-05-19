"""
Method Resolution

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

class EBook(Book):
    @classmethod
    def from_string(cls, s: str):
        title, author, file_format = s.split('|')
        return cls(title, author, file_format)

# Test method resolution order (MRO)
book_str = "The Hobbit|J.R.R. Tolkien"
ebook_str = "The Hobbit|J.R.R. Tolkien|PDF"

book = Book.from_string(book_str)
ebook = EBook.from_string(ebook_str)

print(book.title)  # Output: The Hobbit
print(ebook.file_format)  # Output: PDF

