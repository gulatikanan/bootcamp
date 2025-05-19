"""Module: game.py
Author: Kanan"""

import json

class Game:
    def __init__(self, level=1, score=0):
        self.level = level
        self.score = score

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.__dict__, f)

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            self.__dict__.update(data)
