from typing import Iterator

class LineCounter:
    def __init__(self, prefix: str = "Line"):
        self.count = 0
        self.prefix = prefix

    def __call__(self, lines: Iterator[str]) -> Iterator[str]:
        for line in lines:
            self.count += 1
            yield f"{self.prefix} {self.count}: {line.rstrip()}"
