from typing import Iterator
from processor_types import StreamProcessor

def run_pipeline(lines: Iterator[str], processors: list[StreamProcessor]) -> Iterator[str]:
    for processor in processors:
        lines = processor(lines)
    return lines
