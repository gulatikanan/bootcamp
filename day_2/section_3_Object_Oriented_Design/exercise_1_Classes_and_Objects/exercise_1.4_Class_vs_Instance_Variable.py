"""
Class vs Instance Variable

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    category = "Fiction"  # class variable

    def __init__(self, title, author):
        self.title = title
        self.author = author

book3 = Book("Brave New World", "Aldous Huxley")
print("Category:", book3.category)

