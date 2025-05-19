"""
Subclassing

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def describe(self):
        return f"{self.title} by {self.author}"

# Subclassing
class Novel(Book):
    def __init__(self, title, author, genre):
        super().__init__(title, author)  # Call parent constructor
        self.genre = genre
