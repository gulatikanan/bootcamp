"""
JSON Dump Load

Instructions:
Complete the exercise according to the requirements.
"""

import json

# Python dict
data = {"name": "Alice", "age": 30}

# Serialize to JSON string
json_data = json.dumps(data)
print("Serialized JSON:", json_data)

# Deserialize back to Python object
loaded_data = json.loads(json_data)
print("Deserialized Data:", loaded_data)

