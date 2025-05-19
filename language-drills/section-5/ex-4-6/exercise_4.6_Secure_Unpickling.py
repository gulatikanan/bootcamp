"""
Secure Unpickling

Instructions:
Complete the exercise according to the requirements.
"""

import pickle

# Dangerous unpickling (potentially unsafe)
with open('data.pkl', 'rb') as file:
    loaded_data = pickle.load(file)  # Don't unpickle untrusted data!
    
# Safe alternatives
import json

with open('data.json', 'r') as file:
    data = json.load(file)  # Safer to use with untrusted data

