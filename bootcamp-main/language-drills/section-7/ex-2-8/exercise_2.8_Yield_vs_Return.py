"""
Yield vs Return

Instructions:
Complete the exercise according to the requirements.
"""

def even_numbers(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

for num in even_numbers(10):
    print(num)
