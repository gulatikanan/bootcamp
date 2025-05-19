from typing import Iterator

def to_uppercase_line(line: str) -> str:
    return line.upper()

def to_uppercase(lines: Iterator[str]) -> Iterator[str]:
    for line in lines:
        yield to_uppercase_line(line)
