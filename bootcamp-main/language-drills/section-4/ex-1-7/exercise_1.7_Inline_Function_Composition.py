"""
Inline Function Composition

Instructions:
Complete the exercise according to the requirements.
"""

def compose(f, g):
    return lambda x: f(g(x))

# Example usage
f = lambda x: x + 1
g = lambda x: x * 2
composed_function = compose(f, g)
print(composed_function(3))  # Output: 7 (f(g(3)) = f(6) = 7)
