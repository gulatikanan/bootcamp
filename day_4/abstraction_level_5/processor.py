from typing import Iterator
from typing import Tuple
TaggedLine = Tuple[str, str]



def trim(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for tag, line in lines:
        yield (tag, line.strip())


def tagger(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for _, line in lines:
        if "ERROR" in line:
            yield ("error", line)
        elif "WARN" in line:
            yield ("warn", line)
        else:
            yield ("general", line)


class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        for tag, line in lines:
            self.count += 1
            yield (tag, f"[COUNT={self.count}] {line}")


def archive(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for tag, line in lines:
        yield (tag, f"[ARCHIVED] {line}")


def formatter(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for tag, line in lines:
        yield (tag, f"[INFO] {line}")


def printer(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for tag, line in lines:
        print(f"{tag.upper()}: {line}")
        yield (tag, line)
