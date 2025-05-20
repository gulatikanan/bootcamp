import typer
import os
from typing import Iterator, Optional
from dotenv import load_dotenv

app = typer.Typer()
load_dotenv()  # Load variables from .env

def read_lines(path: str) -> Iterator[str]:
    with open(path, 'r') as f:
        for line in f:
            yield line.rstrip('\n')

def transform_line(line: str, mode: str) -> str:
    line = line.strip()
    if mode == "uppercase":
        return line.upper()
    elif mode == "snakecase":
        return line.lower().replace(" ", "_")
    else:
        raise ValueError(f"Unsupported mode: {mode}")

def write_output(lines: Iterator[str], output_path: Optional[str]) -> None:
    if output_path:
        with open(output_path, 'w') as f:
            for line in lines:
                f.write(line + "\n")
    else:
        for line in lines:
            print(line)

@app.command()
def process(
    input: str = typer.Option(..., help="Input file path"),
    output: Optional[str] = typer.Option(None, help="Optional output file path"),
    mode: Optional[str] = typer.Option(None, help="Processing mode: uppercase or snakecase")
):
    selected_mode = mode or os.getenv("MODE", "uppercase")
    input_lines = read_lines(input)
    processed = (transform_line(line, selected_mode) for line in input_lines)
    write_output(processed, output)

if __name__ == "__main__":
    app()
