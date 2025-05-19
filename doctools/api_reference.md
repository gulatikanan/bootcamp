# API Reference
This page documents the public API of the `kanan-hello` package.
## Core Module
### say_hello
```
def say_hello(name: str = "World") -> str:
    """
    Returns a greeting message for the given name.
    Args:
        name: The name to greet. Defaults to "World".
    Returns:
        A greeting string.
    """
```
**Example:**
```
from kanan_hello import print_rich_hello
# Default greeting with rich formatting
print_rich_hello()  # Displays: Hello, World! in a fancy panel
# Custom greeting with rich formatting
print_rich_hello("kanan")  # Displays: Hello, kanan! in a fancy panel
```
## CLI Module
The CLI module is not typically imported directly but is used through the command-line interface.
### hello command
```
kanan-hello hello [NAME]
```
Prints a rich formatted greeting message. If no name is provided, it will greet the world.
**Arguments:**
- `NAME`: Optional. The name to greet.
**Example:**
```
kanan-hello hello
kanan-hello hello kanan
```
### simple command
```
kanan-hello simple [NAME]
```
Prints a simple greeting message without rich formatting. If no name is provided, it will greet the world.
**Arguments:**
- `NAME`: Optional. The name to greet.
**Example:**
```
kanan-hello simple
kanan-hello simple kanan
```
## Internal Structure
The package is structured as follows:
```
kanan_hello/
├── __init__.py      # Exports say_hello and print_rich_hello
├── main.py          # Contains core functionality
└── cli.py           # Implements the command-line interface
```
The `__init__.py` file exports the main functions:
```
from .main import say_hello, print_rich_hello
__all__ = ["say_hello", "print_rich_hello"]
```
This means you can import these functions directly from the package:
```
from kanan_hello import say_hello, print_rich_hello
```