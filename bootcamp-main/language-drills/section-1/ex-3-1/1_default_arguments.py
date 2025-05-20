# Default Arguments: Create greet(name="Guest") and test with and without passing a name.

def greet(name="Guest"):
    print(f"Hello, {name}")
greet()           # Hello, Guest
greet("Alice")    # Hello, Alice
