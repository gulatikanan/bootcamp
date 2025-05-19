"""
Equality Check

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False

    def __str__(self):
        return f"'{self.title}' by {self.author}"

# Create two book objects with the same data
book1 = Book("1984", "George Orwell")
book2 = Book("1984", "George Orwell")

# Check for equality
print(book1 == book2)  # True

