"""
Add a Method

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author}"

book2 = Book("Animal Farm", "George Orwell")
print(book2.describe())
