def say_hello(name: str = "World") -> str:
    """
    Returns a greeting message for the given name.
    
    Args:
        name: The name to greet. Defaults to "World".
        
    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"

def main() -> None:
    """
    Main function that prints a greeting.
    """
    print(say_hello())

if __name__ == "__main__":
    main()