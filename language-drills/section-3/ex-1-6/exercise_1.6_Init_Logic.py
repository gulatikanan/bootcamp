"""
Init Logic

Instructions:
Complete the exercise according to the requirements.
"""
class Book:
    def __init__(self, title="Unknown Title", author="Unknown Author"):
        self.title = title
        self.author = author

book5 = Book()
print(book5.describe())  # Will show default title and author

book6 = Book("Sapiens", "Yuval Noah Harari")
print(book6.describe())
