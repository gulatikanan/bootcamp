"""
Override Method

Instructions:
Complete the exercise according to the requirements.
"""

def describe(self):
        # Call the parent describe method using super()
        return "Novel: " + super().describe() + f" | Genre: {self.genre}"

