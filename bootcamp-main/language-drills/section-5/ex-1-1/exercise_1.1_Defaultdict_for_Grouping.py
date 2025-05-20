"""
Defaultdict for Grouping

Instructions:
Complete the exercise according to the requirements.
"""
import collections

# Group words by their first letter
words = ["apple", "banana", "cherry", "apricot", "blueberry"]
grouped = collections.defaultdict(list)

for word in words:
    grouped[word[0]].append(word)

print(grouped)
# Outputs: defaultdict(<class 'list'>, {'a': ['apple', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']})
