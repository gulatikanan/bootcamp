"""
Basic stream processors.
"""
from typing import Iterator, List, Optional
import re

from ..core.base import StreamProcessor, ConfigurableProcessor


class IdentityProcessor(StreamProcessor):
    """A processor that passes input through unchanged."""
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Pass all input lines through unchanged.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Same strings unmodified
        """
        yield from stream


class FilterProcessor(ConfigurableProcessor):
    """A processor that filters lines based on a predicate."""
    
    def __init__(self, predicate=None, pattern=None, min_length=None, **kwargs):
        """
        Initialize the filter processor.
        
        Args:
            predicate: Optional function that takes a string and returns True/False
            pattern: Optional regex pattern string to match against
            min_length: Optional minimum length for lines to pass through
            **kwargs: Additional configuration
        """
        self.predicate = predicate
        self.pattern = re.compile(pattern) if pattern else None
        self.min_length = min_length
        super().__init__(**kwargs)
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Filter the stream based on configured criteria.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Filtered stream of strings
        """
        for line in stream:
            # Apply filters
            if self.min_length is not None and len(line) < self.min_length:
                continue
                
            if self.pattern is not None and not self.pattern.search(line):
                continue
                
            if self.predicate is not None and not self.predicate(line):
                continue
                
            yield line


class TransformProcessor(ConfigurableProcessor):
    """A processor that transforms lines using a provided function."""
    
    def __init__(self, transform_func=None, **kwargs):
        """
        Initialize with a transformation function.
        
        Args:
            transform_func: Function that takes a string and returns a transformed string
            **kwargs: Additional configuration
        """
        self.transform_func = transform_func
        super().__init__(**kwargs)
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Transform each line using the configured function.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream of transformed strings
        """
        for line in stream:
            if self.transform_func:
                result = self.transform_func(line)
                if result:  # Skip empty results
                    yield result
            else:
                yield line


class SplitProcessor(ConfigurableProcessor):
    """A processor that splits lines into multiple lines (fan-out)."""
    
    def __init__(self, delimiter=None, max_splits=-1, **kwargs):
        """
        Initialize with splitting parameters.
        
        Args:
            delimiter: String delimiter to split on
            max_splits: Maximum number of splits to perform
            **kwargs: Additional configuration
        """
        self.delimiter = delimiter or " "
        self.max_splits = max_splits
        super().__init__(**kwargs)
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Split each input line into multiple output lines.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream with each input line split into multiple lines
        """
        for line in stream:
            parts = line.split(self.delimiter, self.max_splits)
            for part in parts:
                if part:  # Skip empty parts
                    yield part.strip()


class JoinProcessor(ConfigurableProcessor):
    """A processor that joins multiple lines into one (fan-in)."""
    
    def __init__(self, count=2, delimiter=" ", **kwargs):
        """
        Initialize with joining parameters.
        
        Args:
            count: Number of lines to join together
            delimiter: String delimiter to join with
            **kwargs: Additional configuration
        """
        self.count = count
        self.delimiter = delimiter
        super().__init__(**kwargs)
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Join every N lines into a single line.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream with every N input lines joined
        """
        buffer: List[str] = []
        
        for line in stream:
            buffer.append(line)
            
            if len(buffer) >= self.count:
                yield self.delimiter.join(buffer)
                buffer = []
        
        # Don't forget any remaining lines
        if buffer:
            yield self.delimiter.join(buffer)