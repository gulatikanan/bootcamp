"""
Hashing Support

Instructions:
Complete the exercise according to the requirements.
"""

def __hash__(self):
    return hash((self.title, self.author))
