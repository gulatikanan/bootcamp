"""
Adapters for converting str->str processors to stream processors.
"""
from typing import Iterator, Callable
from functools import wraps

from .base import StreamProcessor


def str_processor_adapter(func: Callable[[str], str]) -> Callable[[Iterator[str]], Iterator[str]]:
    """
    Decorator/adapter to convert a simple str->str processor function 
    to a stream-compatible function.
    
    Args:
        func: A function that takes a string and returns a string
        
    Returns:
        A function that takes a stream of strings and yields processed strings
    """
    @wraps(func)
    def wrapper(stream: Iterator[str]) -> Iterator[str]:
        for line in stream:
            processed = func(line)
            if processed:  # Skip empty results
                yield processed
    return wrapper


class FunctionProcessor(StreamProcessor):
    """
    Adapter class that converts a str->str function to a StreamProcessor.
    """
    
    def __init__(self, func: Callable[[str], str]):
        """
        Initialize with a str->str processor function.
        
        Args:
            func: A function that takes a string and returns a string
        """
        self.func = func
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process the stream using the wrapped function.
        
        Args:
            stream: An iterator of strings
            
        Returns:
            An iterator of processed strings
        """
        for line in stream:
            processed = self.func(line)
            if processed:  # Skip empty results
                yield processed


def adapt_str_processor(func: Callable[[str], str]) -> StreamProcessor:
    """
    Convert a str->str function to a StreamProcessor instance.
    
    Args:
        func: A function that takes a string and returns a string
        
    Returns:
        A StreamProcessor that wraps the function
    """
    return FunctionProcessor(func)