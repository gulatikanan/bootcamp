# Usage Guide

This guide explains how to use the `kanan-hello` package, both as a library in your Python code and as a command-line tool.

## Using as a Library

### Basic Usage
```
from kanan_hello import say_hello

# Default greeting
result = say_hello()
print(result)  # Output: Hello, World!

# Custom greeting
result = say_hello("kanan")
print(result)  # Output: Hello, kanan!
```

### Rich Formatted Output

```
from kanan_hello import print_rich_hello

# Default greeting with rich formatting
print_rich_hello()  # Displays a fancy greeting panel for "World"

# Custom greeting with rich formatting
print_rich_hello("kanan")  # Displays a fancy greeting panel for "kanan"
```

### Complete Example

```
from kanan_hello import say_hello, print_rich_hello

def main():
    # Simple greeting
    message = say_hello("User")
    print(f"Simple greeting: {message}")
    
    # Rich formatted greeting
    print("Rich formatted greeting:")
    print_rich_hello("User")

if __name__ == "__main__":
    main()
```

## Using as a Command-Line Tool

After installing the package, you can use it from the command line.

### Getting Help

```
kanan-hello --help
```



This will display the available commands and options.

### Rich Formatted Greeting

```
# Greet the world
kanan-hello hello

# Greet a specific person
kanan-hello hello kanan
```

### Simple Text Greeting

```

# Greet the world

kanan-hello simple

# Greet a specific person

kanan-hello simple kanan

```

## Integration Examples

### Using in a Script

```
#!/usr/bin/env python3
import sys
from kanan_hello import say_hello, print_rich_hello

def main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = "World"
    
    print(f"Simple greeting: {say_hello(name)}")
    print("\nRich greeting:")
    print_rich_hello(name)

if __name__ == "__main__":
    main()
```

### Using in a Larger Application

```
from kanan_hello import print_rich_hello

class GreetingService:
    def __init__(self, default_name="Guest"):
        self.default_name = default_name
    
    def greet_user(self, name=None):
        """Greet a user with a rich formatted message."""
        if name is None:
            name = self.default_name
        print_rich_hello(name)

# Usage
service = GreetingService("Default User")
service.greet_user()  # Greets "Default User"
service.greet_user("kanan")  # Greets "kanan"
```

## Best Practices

1. **Import Only What You Need**: Import specific functions rather than the entire package.
2. **Handle Exceptions**: Although the current functions don't raise exceptions, it's good practice to handle potential errors.
3. **Use Type Hints**: When extending the functionality, continue using type hints for better IDE support.
4. **Document Your Code**: Add docstrings to your functions that use this package.

## Limitations

- The package is designed for demonstration purposes and has limited functionality.
- Rich formatting only works in terminals that support ANSI color codes.




