# Set Comprehension: From "hello world", get all unique vowels.

print({ch for ch in "hello world" if ch in "aeiou"})  # {'e', 'o'}
