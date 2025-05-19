"""Module: book.py
Author: Kanan"""

import json

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def to_json(self):
        # Convert to JSON using __dict__ to get all instance attributes
        return json.dumps(self.__dict__)
