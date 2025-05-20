# Filter with Comprehension: Extract even-length strings from ["hi", "hello", "bye"].

words = ["hi", "hello", "bye"]
print([w for w in words if len(w) % 2 == 0])  # ['hi']
