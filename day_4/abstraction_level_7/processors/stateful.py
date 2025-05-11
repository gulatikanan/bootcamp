from typing import Iterator, List, Optional, Dict, Any, Callable
from processors.base import ObservableProcessor

class LineCounter(ObservableProcessor):
    """Processor that counts lines and prepends the count to each line."""
    
    def __init__(self, format_str: str = "[{count}] {line}", processor_id: Optional[str] = None):
        super().__init__(processor_id, "line_counter")
        self.count = 0
        self.format_str = format_str
    
    def _process_line(self, line: str) -> Iterator[str]:
        self.count += 1
        yield self.format_str.format(count=self.count, line=line)

class LineJoiner(ObservableProcessor):
    """Processor that joins pairs of lines together (fan-in)."""
    
    def __init__(self, delimiter: str = " | ", processor_id: Optional[str] = None):
        super().__init__(processor_id, "line_joiner")
        self.buffer: Optional[str] = None
        self.delimiter = delimiter
    
    def _process_line(self, line: str) -> Iterator[str]:
        if self.buffer is None:
            self.buffer = line
            # No output yet
        else:
            joined_line = f"{self.buffer}{self.delimiter}{line}"
            self.buffer = None
            yield joined_line

class LineSplitter(ObservableProcessor):
    """Processor that splits lines on a delimiter and emits multiple lines (fan-out)."""
    
    def __init__(self, delimiter: str = ",", processor_id: Optional[str] = None):
        super().__init__(processor_id, "line_splitter")
        self.delimiter = delimiter
    
    def _process_line(self, line: str) -> Iterator[str]:
        for part in line.split(self.delimiter):
            if part.strip():  # Skip empty parts
                yield part.strip()

class FilterProcessor(ObservableProcessor):
    """Processor that filters lines based on a predicate."""
    
    def __init__(self, predicate: Callable[[str], bool], processor_id: Optional[str] = None):
        super().__init__(processor_id, "filter_processor")
        self.predicate = predicate
    
    def _process_line(self, line: str) -> Iterator[str]:
        if self.predicate(line):
            yield line

class TagRouter(ObservableProcessor):
    """
    Routes lines to different processors based on tags.
    This is a DAG node that can have multiple outputs.
    """
    
    def __init__(self, tag_field: int = 0, delimiter: str = ",", processor_id: Optional[str] = None):
        super().__init__(processor_id, "tag_router")
        self.tag_field = tag_field
        self.delimiter = delimiter
        self.routes = {}  # tag -> processor
        
    def add_route(self, tag: str, processor: ObservableProcessor):
        """Add a route for a specific tag."""
        self.routes[tag] = processor
        return self
    
    def _process_line(self, line: str) -> Iterator[str]:
        parts = line.split(self.delimiter)
        if len(parts) > self.tag_field:
            tag = parts[self.tag_field].strip()
            if tag in self.routes:
                # Route to the appropriate processor
                processor = self.routes[tag]
                # We would process through the processor here,
                # but this is simplified for the example
                yield line
            else:
                # No route found, pass through
                yield line
        else:
            # Not enough fields, pass through
            yield line