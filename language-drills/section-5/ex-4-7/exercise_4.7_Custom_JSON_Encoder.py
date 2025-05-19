"""
Custom JSON Encoder

Instructions:
Complete the exercise according to the requirements.
"""
import json
from datetime import datetime

# Custom JSON Encoder for datetime
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        return super().default(obj)

# Example usage
data = {"event": "meeting", "time": datetime.now()}
json_data = json.dumps(data, cls=CustomEncoder)
print("Serialized JSON with custom encoder:", json_data)
