"""Module: user.py
Author: Kanan"""

import json

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # Sensitive
        self.email = email

    def to_safe_json(self):
        # Serialize only non-sensitive fields
        return json.dumps({
            "username": self.username,
            "email": self.email
        })
