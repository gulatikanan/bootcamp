"""
Create an Object

Instructions:
Complete the exercise according to the requirements.
"""

# Define the Book class
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

# Create an object of the Book class
book1 = Book("1984", "Orwell")

# Print the attributes
print("Title:", book1.title)
print("Author:", book1.author)
