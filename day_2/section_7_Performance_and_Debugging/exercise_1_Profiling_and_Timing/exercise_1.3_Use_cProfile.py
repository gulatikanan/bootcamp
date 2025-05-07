"""
Use cProfile

Instructions:
Complete the exercise according to the requirements.
"""

def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

def fast_function():
    return sum(range(1000000))

if __name__ == "__main__":
    slow_function()
    fast_function()

#run the following command
# python -m cProfile -s time yourscript.py



