"""
Update Object State

Instructions:
Complete the exercise according to the requirements.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def update_title(self, new_title):
        self.title = new_title

book4 = Book("Old Title", "Some Author")
print("Before:", book4.title)
book4.update_title("New Title")
print("After:", book4.title)
