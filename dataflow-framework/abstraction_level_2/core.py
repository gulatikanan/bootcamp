from typing import Iterator
from custom_types import ProcessorFn



def to_uppercase(line: str) -> str:
    return line.strip().upper()

def to_snakecase(line: str) -> str:
    return line.strip().lower().replace(" ", "_")

def read_lines(path: str) -> Iterator[str]:
    with open(path, "r") as f:
        for line in f:
            yield line

def process_lines(lines: Iterator[str], processors: list[ProcessorFn]) -> Iterator[str]:
    for line in lines:
        for processor in processors:
            line = processor(line)
        yield line

def write_output(lines: Iterator[str], output_path: str | None) -> None:
    if output_path:
        with open(output_path, "w") as f:
            for line in lines:
                f.write(line + "\n")
    else:
        for line in lines:
            print(line)
