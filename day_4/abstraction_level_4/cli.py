import typer
from pathlib import Path
from core import run_pipeline
from pipeline import load_pipeline

app = typer.Typer()

@app.command()
def process(
        input: Path = typer.Option(...,help="Input file path"),
        output: Path = typer.Option(None, help="Output file path"),
        config: Path = typer.Option(..., help="Path to pipeline YAML config")
):
    if not input.exists():
        typer.echo(f"Input file {input} does not exist.")
        raise typer.Exit(code=1)

    # Read input lines as a stream
    with input.open("r") as f:
        lines = (line.rstrip("\n") for line in f)

        processors = load_pipeline(str(config))
        output_lines = run_pipeline(lines, processors)

        if output:
            with output.open("w") as out_file:
                for line in output_lines:
                    out_file.write(line + "\n")
        else:
            for line in output_lines:
                print(line)
