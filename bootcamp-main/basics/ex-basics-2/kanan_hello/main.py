from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Create a console instance
console = Console()

def say_hello(name: str = "World") -> str:
    """
    Returns a greeting message for the given name.
    
    Args:
        name: The name to greet. Defaults to "World".
        
    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"

def print_rich_hello(name: str = "World") -> None:
    """
    Prints a rich formatted greeting message.
    
    Args:
        name: The name to greet. Defaults to "World".
    """
    greeting = say_hello(name)
    text = Text(greeting, style="bold green")
    console.print(Panel(text, border_style="blue", title="Greeting"))

def main() -> None:
    """
    Main function that prints a rich greeting.
    """
    print_rich_hello()

if __name__ == "__main__":
    main()