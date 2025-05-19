"""
Check Type

Instructions:
Complete the exercise according to the requirements.
"""

# Define the Book class
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

# Create an object of the Book class
book7 = Book("Brave New World", "Aldous Huxley")

# Check if book7 is an instance of Book
print("Is book7 a Book?", isinstance(book7, Book))  # True
