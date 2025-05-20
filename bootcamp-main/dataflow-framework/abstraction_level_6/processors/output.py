from typing import Iterator
from processor_types import TaggedLine

def terminal(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    """
    Terminal processors: retag all incoming lines to 'end', marking them complete.

    Args:
        lines: Iterator of (tag, text) pairs.
    Yields:
        ('end', text) for each input line.
    """
    for _, text in lines:
        yield 'end', text