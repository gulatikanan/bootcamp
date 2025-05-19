"""Module: collection.py
Author: Kanan"""

import json

class MyCollection:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def to_json(self):
        return json.dumps(self.items)

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.to_json())

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        obj = cls()
        obj.items = data
        return obj

