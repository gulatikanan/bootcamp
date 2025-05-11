from typing import Iterator
from processor_types import TaggedLine

def snakecase(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    """
    Transform processor: convert text payloads to snake_case and terminate the flow.

    Args:
        lines: Iterator of (tag, text) pairs.
    Yields:
        ('end', text) with snake_cased payload.
    """
    for _, text in lines:
        normalized = '_'.join(text.split()).lower()
        yield 'end', normalized


def uppercase(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    """
    Transform processor: convert text payloads to uppercase and terminate the flow.

    Args:
        lines: Iterator of (tag, text) pairs.
    Yields:
        ('end', text) with uppercased payload.
    """
    for _, text in lines:
        yield 'end', text.upper()