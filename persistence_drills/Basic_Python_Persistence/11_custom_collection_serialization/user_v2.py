import json

class UserV2:
    def __init__(self, username="", email="N/A"):
        self.username = username
        self.email = email

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            self.username = data.get("username", "")
            self.email = data.get("email", "N/A")  # default if missing
