"""
Isinstance with Inheritance

Instructions:
Complete the exercise according to the requirements.
"""

# Define the Book class
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def describe(self):
        return f"{self.title} by {self.author}"

# Define the Novel class inheriting from Book
class Novel(Book):
    def __init__(self, title, author, genre):
        super().__init__(title, author)  # Call the parent constructor
        self.genre = genre

    def describe(self):
        return f"Novel: {super().describe()} - Genre: {self.genre}"

# Create a Novel instance
novel1 = Novel("Pride and Prejudice", "Jane Austen", "Romance")

# Output description
print(novel1.describe())  # Novel: Pride and Prejudice by Jane Austen - Genre: Romance

# Check inheritance with isinstance
print("Is novel1 a Book?", isinstance(novel1, Book))  # True
