"""
Lru Cache Memoization

Instructions:
Complete the exercise according to the requirements.
"""
from functools import lru_cache

@lru_cache(maxsize=None)  # Unlimited cache
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Test
print(fib(10))  # Output: 55 (Fibonacci of 10)
