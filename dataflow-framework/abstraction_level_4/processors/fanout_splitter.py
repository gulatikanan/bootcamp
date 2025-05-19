from typing import Iterator

class SplitLines:
    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    def __call__(self, lines: Iterator[str]) -> Iterator[str]:
        for line in lines:
            parts = line.strip().split(self.delimiter)
            for part in parts:
                yield part.strip()
