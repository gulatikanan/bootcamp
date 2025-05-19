"""
Polymorphism in Action

Instructions:
Complete the exercise according to the requirements.
"""
# Base Book class
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def describe(self):
        return f"{self.title} by {self.author}"

# Novel subclass inheriting from Book
class Novel(Book):
    def __init__(self, title, author, genre):
        super().__init__(title, author)
        self.genre = genre

    def describe(self):
        return f"Novel: {super().describe()} - Genre: {self.genre}"

# Create instances
book1 = Book("1984", "George Orwell")
novel2 = Novel("To Kill a Mockingbird", "Harper Lee", "Fiction")

# Polymorphism in action
for item in [book1, novel2]:
    print(item.describe())
