"""
Counter Basics

Instructions:
Complete the exercise according to the requirements.
"""
import collections

# Count character frequencies in "hello world"
word = "hello world"
counter = collections.Counter(word)

print(counter)
# Outputs: Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
