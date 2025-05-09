"""
Stateful stream processors.
"""
from typing import Iterator, List, Dict, Any, Optional
import re

from ..core.base import StatefulProcessor


class LineCountProcessor(StatefulProcessor):
    """A processor that counts and annotates lines with their sequence number."""
    
    def __init__(self, pattern="{count}: {line}", start_count=1, **kwargs):
        """
        Initialize with formatting options.
        
        Args:
            pattern: Format string with {count} and {line} placeholders
            start_count: Initial value for the counter
            **kwargs: Additional configuration
        """
        self.pattern = pattern
        self.start_count = start_count
        super().__init__(**kwargs)
    
    def initialize(self):
        """Initialize the counter state."""
        self.state["count"] = self.start_count
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process stream, adding line numbers to each line.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream of numbered lines
        """
        for line in stream:
            count = self.state["count"]
            yield self.pattern.format(count=count, line=line)
            self.state["count"] += 1


class DuplicateDetectorProcessor(StatefulProcessor):
    """A processor that detects and handles duplicate lines."""
    
    def __init__(self, 
                 mode="skip", 
                 memory_size=None,
                 mark_as="DUPLICATE", 
                 **kwargs):
        """
        Initialize with duplication handling options.
        
        Args:
            mode: How to handle duplicates: "skip", "mark", or "count"
            memory_size: How many previous lines to remember (None = unlimited)
            mark_as: Text to add to duplicates in "mark" mode
            **kwargs: Additional configuration
        """
        self.mode = mode
        self.memory_size = memory_size
        self.mark_as = mark_as
        super().__init__(**kwargs)
    
    def initialize(self):
        """Initialize the seen-items state."""
        self.state["seen"] = set()
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process stream, handling duplicates according to configuration.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream with duplicates handled according to mode
        """
        for line in stream:
            # Check if we've seen this line before
            is_duplicate = line in self.state["seen"]
            
            # Add to seen set
            self.state["seen"].add(line)
            
            # Limit memory if needed
            if self.memory_size and len(self.state["seen"]) > self.memory_size:
                # This is not ideal as we can't control which item is removed
                # A better approach would be to use a deque or ordered dict
                self.state["seen"].pop()
            
            # Handle according to mode
            if is_duplicate:
                if self.mode == "skip":
                    continue  # Skip this line
                elif self.mode == "mark":
                    yield f"{line} {self.mark_as}"
                elif self.mode == "count":
                    # Count duplicates and yield line with count
                    if "counts" not in self.state:
                        self.state["counts"] = {}
                    
                    if line not in self.state["counts"]:
                        self.state["counts"][line] = 1
                    
                    self.state["counts"][line] += 1
                    yield f"{line} ({self.state['counts'][line]})"
            else:
                if self.mode == "count":
                    # Initialize count for this line
                    if "counts" not in self.state:
                        self.state["counts"] = {}
                    self.state["counts"][line] = 1
                    yield f"{line} (1)"
                else:
                    yield line


class AggregatorProcessor(StatefulProcessor):
    """A processor that aggregates statistics on the stream."""
    
    def __init__(self, 
                 operations=None,
                 window=None, 
                 emit_partial=False,
                 reset_after_emit=True,
                 **kwargs):
        """
        Initialize with aggregation options.
        
        Args:
            operations: List of operations to perform (sum, avg, min, max, count)
            window: Number of lines to aggregate before emitting results
            emit_partial: Whether to emit partial results on end of stream
            reset_after_emit: Whether to reset stats after emitting
            **kwargs: Additional configuration
        """
        self.operations = operations or ["count"]
        self.window = window
        self.emit_partial = emit_partial
        self.reset_after_emit = reset_after_emit
        super().__init__(**kwargs)
    
    def initialize(self):
        """Initialize aggregation state."""
        self.state["count"] = 0
        self.state["sum"] = 0
        self.state["values"] = []
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process stream, aggregating statistics.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream of aggregation results
        """
        for line in stream:
            # Try to convert line to a number for numeric operations
            try:
                value = float(line.strip())
                self.state["sum"] += value
                self.state["values"].append(value)
            except ValueError:
                # Just count non-numeric lines
                pass
            
            self.state["count"] += 1
            
            # Check if we've reached the window size
            if self.window and self.state["count"] >= self.window:
                for result in self._emit_results():
                    yield result
                
                if self.reset_after_emit:
                    self.reset_state()
        
        # Emit any remaining results if configured
        if self.emit_partial and self.state["count"] > 0:
            for result in self._emit_results():
                yield result
    
    def _emit_results(self):
        """Generate results based on configured operations."""
        results = []
        
        for op in self.operations:
            if op == "count":
                results.append(f"Count: {self.state['count']}")
            
            elif op == "sum" and self.state["values"]:
                results.append(f"Sum: {self.state['sum']}")
            
            elif op == "avg" and self.state["values"]:
                avg = self.state["sum"] / len(self.state["values"])
                results.append(f"Average: {avg:.2f}")
            
            elif op == "min" and self.state["values"]:
                results.append(f"Min: {min(self.state['values'])}")
            
            elif op == "max" and self.state["values"]:
                results.append(f"Max: {max(self.state['values'])}")
        
        return results


class BufferProcessor(StatefulProcessor):
    """A processor that buffers lines and applies operations on groups."""
    
    def __init__(self, 
                 buffer_size=10,
                 buffer_condition=None,
                 sort=False,
                 reverse=False,
                 unique=False,
                 **kwargs):
        """
        Initialize with buffer options.
        
        Args:
            buffer_size: Number of lines to buffer before processing
            buffer_condition: Function that decides when to process buffer
            sort: Whether to sort buffered lines
            reverse: Whether to reverse sort order
            unique: Whether to remove duplicates
            **kwargs: Additional configuration
        """
        self.buffer_size = buffer_size
        self.buffer_condition = buffer_condition
        self.sort = sort
        self.reverse = reverse
        self.unique = unique
        super().__init__(**kwargs)
    
    def initialize(self):
        """Initialize buffer state."""
        self.state["buffer"] = []
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process stream using buffering.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream of processed buffer contents
        """
        for line in stream:
            buffer = self.state["buffer"]
            buffer.append(line)
            
            # Check if it's time to process the buffer
            should_process = len(buffer) >= self.buffer_size
            if self.buffer_condition:
                should_process = should_process or self.buffer_condition(line, buffer)
            
            if should_process:
                for result in self._process_buffer():
                    yield result
                self.state["buffer"] = []
        
        # Process any remaining buffer contents
        if self.state["buffer"]:
            for result in self._process_buffer():
                yield result
    
    def _process_buffer(self):
        """Process the current buffer according to configuration."""
        buffer = self.state["buffer"]
        
        # Apply configured operations
        if self.unique:
            buffer = list(dict.fromkeys(buffer))  # Preserves order
        
        if self.sort:
            buffer.sort(reverse=self.reverse)
        
        return buffer