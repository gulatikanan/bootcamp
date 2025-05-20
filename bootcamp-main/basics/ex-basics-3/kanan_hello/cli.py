import typer
from typing import Optional
from .main import print_rich_hello, say_hello

app = typer.Typer(help="A simple CLI application that says hello.")

@app.command()
def hello(name: Optional[str] = typer.Argument(None, help="The name to greet")):
    """
    Prints a rich formatted greeting message.
    
    If no name is provided, it will greet the world.
    """
    print_rich_hello(name if name else "World")

@app.command()
def simple(name: Optional[str] = typer.Argument(None, help="The name to greet")):
    """
    Prints a simple greeting message without rich formatting.
    
    If no name is provided, it will greet the world.
    """
    typer.echo(say_hello(name if name else "World"))

def main():
    """
    Entry point for the CLI application.
    """
    app()

if __name__ == "__main__":
    main()