from typing import Iterator, Callable, Protocol

# Basic stream processor interface
class StreamProcessor(Protocol):
    def __call__(self, lines: Iterator[str]) -> Iterator[str]: ...

# Helper type for wrapping old str->str functions
class LineProcessor(Protocol):
    def __call__(self, lines: Iterator[str]) -> Iterator[str]: ...

