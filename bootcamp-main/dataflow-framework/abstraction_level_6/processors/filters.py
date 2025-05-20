from typing import Iterator
from processor_types import TaggedLine

def only_error(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    """
    Filter processor: pass through only lines tagged 'error' and terminate.

    Args:
        lines: Iterator of (tag, text) pairs.
    Yields:
        ('end', text) when tag == 'error'.
    """
    for tag, text in lines:
        if tag == 'error':
            yield 'end', text

def only_warn(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    """
    Filter processor: pass through only lines tagged 'warn' and terminate.

    Args:
        lines: Iterator of (tag, text) pairs.
    Yields:
        ('end', text) when tag == 'warn'.
    """
    for tag, text in lines:
        if tag == 'warn':
            yield 'end', text