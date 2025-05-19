"""
Alternative Constructor

Instructions:
Complete the exercise according to the requirements.
"""
import json

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(data['title'], data['author'])

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['title'], data['author'])

# Test the alternative constructors
json_data = '{"title": "Brave New World", "author": "Aldous Huxley"}'
book_from_json = Book.from_json(json_data)
print(book_from_json.title)  # Output: Brave New World

book_dict = {"title": "Fahrenheit 451", "author": "Ray Bradbury"}
book_from_dict = Book.from_dict(book_dict)
print(book_from_dict.title)  # Output: Fahrenheit 451

