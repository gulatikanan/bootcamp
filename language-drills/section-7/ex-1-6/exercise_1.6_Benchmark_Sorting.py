"""
Benchmark Sorting

Instructions:
Complete the exercise according to the requirements.
"""

import timeit

# Built-in sort
sorted_time = timeit.timeit("sorted(range(1000000))", number=10)

# Custom sort function (e.g., using bubble sort)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

custom_sort_time = timeit.timeit("bubble_sort(list(range(1000000)))", setup="from __main__ import bubble_sort", number=10)

print(f"Built-in sorted time: {sorted_time} seconds")
print(f"Custom sort time: {custom_sort_time} seconds")

