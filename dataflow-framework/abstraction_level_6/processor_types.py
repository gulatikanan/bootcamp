from typing import Iterator, Tuple, Callable

# A tag name representing a processing state
Tag = str

# A line paired with its tag
TaggedLine = Tuple[Tag, str]

# A stateful processor: consumes TaggedLine stream, emits new TaggedLine stream
StateProcessor = Callable[[Iterator[TaggedLine]], Iterator[TaggedLine]]