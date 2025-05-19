import json

class UserV1:
    def __init__(self, username):
        self.username = username

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.__dict__, f)
