import typer
from pathlib import Path
from typing import Optional
from main import run

app = typer.Typer()

@app.command()
def main(
    input: Path = typer.Option(..., exists=True, help="Input file path"),
    config: Path = typer.Option(..., exists=True, help="Config YAML path"),
    output: Optional[Path] = typer.Option(None, help="Output file path; stdout if omitted"),
) -> None:
    """
    Command-line entrypoint: runs the state-based router.

    Args:
        input: Path to the log input file.
        config: Path to the YAML router configuration.
        output: Optional path for final output.
    """
    run(input, config, output)

if __name__ == '__main__':
    app()