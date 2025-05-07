"""
Custom Container

Instructions:
Complete the exercise according to the requirements.
"""

class Library:
    def __init__(self):
        self.books = []

    def add(self, book):
        self.books.append(book)

    def __len__(self):
        return len(self.books)
