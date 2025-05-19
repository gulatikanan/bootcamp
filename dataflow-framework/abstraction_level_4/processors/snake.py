import re
from typing import Iterator

def to_snakecase_line(line: str) -> str:
    # Convert "Hello World" -> "hello_world"
    return re.sub(r"\W+", "_", line.strip()).lower()

def to_snakecase(lines: Iterator[str]) -> Iterator[str]:
    for line in lines:
        yield to_snakecase_line(line)
