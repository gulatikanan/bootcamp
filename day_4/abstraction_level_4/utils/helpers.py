"""
Utility functions for stream processing.
"""
from typing import Iterator, List, Callable, Dict, Any
import time
import re
import functools


def stream_from_string(text: str) -> Iterator[str]:
    """
    Convert a multi-line string to a stream of lines.
    
    Args:
        text: Multi-line string
        
    Returns:
        Iterator yielding one line at a time
    """
    for line in text.splitlines():
        yield line


def stream_from_file(file_path: str) -> Iterator[str]:
    """
    Create a stream from a file.
    
    Args:
        file_path: Path to text file
        
    Returns:
        Iterator yielding one line at a time
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.rstrip('\n')


def stream_to_file(stream: Iterator[str], file_path: str):
    """
    Write a stream to a file.
    
    Args:
        stream: Iterator of strings
        file_path: Output file path
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in stream:
            f.write(line + '\n')


def timed_processing(func):
    """
    Decorator to time the execution of a processing function.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function that prints timing information
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} completed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def string_matcher(pattern: str, case_sensitive: bool = True) -> Callable[[str], bool]:
    """
    Create a function that matches strings against a pattern.
    
    Args:
        pattern: Regular expression pattern
        case_sensitive: Whether matching should be case-sensitive
        
    Returns:
        Function that takes a string and returns True if it matches
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    compiled = re.compile(pattern, flags)
    return lambda s: bool(compiled.search(s))


def collect_stream(stream: Iterator[str]) -> List[str]:
    """
    Collect all items from a stream into a list.
    
    Args:
        stream: Iterator of strings
        
    Returns:
        List of all strings from the stream
    """
    return list(stream)


def peek_stream(stream: Iterator[str], n: int = 5) -> List[str]:
    """
    Peek at the first n items in a stream without consuming it fully.
    
    Args:
        stream: Iterator of strings
        n: Number of items to peek
        
    Returns:
        List of up to n items from the stream
    """
    items = []
    for _ in range(n):
        try:
            item = next(stream)
            items.append(item)
        except StopIteration:
            break
    
    # Create a new stream with the peeked items followed by the rest
    new_stream = iter(items + list(stream))
    
    # Return the peeked items and update the stream reference