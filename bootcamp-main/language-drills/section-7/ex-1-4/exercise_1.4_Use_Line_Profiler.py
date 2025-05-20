"""
Use Line Profiler

Instructions:
Complete the exercise according to the requirements.
"""

# Install line_profiler if not already installed:
# pip install line_profiler
# Decorate a function with @profile and run with kernprof
# @profile
def slow_function():
    total = 0
    for i in range(1000000):
        total += i * i
    return total
if __name__ == "__main__":
    slow_function()
# To profile the script, run it with kernprof:
# kernprof -l -v yourscript.py
