from typing import Iterator
from processor_types import TaggedLine

def tag_lines(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    """
    Initial processors: tag each raw input line based on keywords.

    Args:
        lines: Iterator of (tag, text) pairs; tag is ignored here.
    Yields:
        ("error", text) if "ERROR" in text,
        ("warn", text) if "WARN" in text,
        ("general", text) otherwise.
    """
    for _, line in lines:
        text = line.strip()
        if 'ERROR' in text:
            yield 'error', text
        elif 'WARN' in text:
            yield 'warn', text
        else:
            yield 'general', text