"""
Multiple Inheritance

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

    def __str__(self):
        return self.describe()

# Mixin class for audio functionality
class AudioMixin:
    def play_audio(self):
        # Assumes self.title is defined in the other base class (Book)
        return f"Playing audio for: {self.title}"

# AudioBook combines Book and AudioMixin
class AudioBook(Book, AudioMixin):
    def __init__(self, title, author, narrator):
        super().__init__(title, author)
        self.narrator = narrator

    def describe(self):
        return f"{self.title} by {self.author}, narrated by {self.narrator}"

audiobook = AudioBook("Atomic Habits", "James Clear", "Stephen Fry")

print(audiobook.describe())         # Atomic Habits by James Clear, narrated by Stephen Fry
print(audiobook.play_audio())       # Playing audio for: Atomic Habits
print(isinstance(audiobook, Book))  # True
print(isinstance(audiobook, AudioMixin))  # True
