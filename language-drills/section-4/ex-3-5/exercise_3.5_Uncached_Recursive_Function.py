"""
Uncached Recursive Function

Instructions:
Complete the exercise according to the requirements.
"""

from functools import lru_cache
import time

# Recursive Fibonacci function without caching
def fib_uncached(n):
    if n <= 1:
        return n
    return fib_uncached(n - 1) + fib_uncached(n - 2)

# Recursive Fibonacci function with caching using lru_cache
@lru_cache(maxsize=None)  # Unlimited cache size
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

# Test the uncached Fibonacci function
start_time = time.time()
print(f"Uncached Fibonacci (fib_uncached(35)): {fib_uncached(35)}")
print(f"Uncached Fibonacci time: {time.time() - start_time:.6f} seconds")

# Test the cached Fibonacci function
start_time = time.time()
print(f"Cached Fibonacci (fib_cached(35)): {fib_cached(35)}")
print(f"Cached Fibonacci time: {time.time() - start_time:.6f} seconds")
