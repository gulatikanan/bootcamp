"""
Base classes and interfaces for stream processing.
"""
from abc import ABC, abstractmethod
from typing import Iterator, Any, Dict, Callable, TypeVar, Generic, Optional

T = TypeVar('T')

class StreamProcessor(ABC):
    """Base abstract class for all stream processors."""
    
    @abstractmethod
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process a stream of strings into another stream of strings.
        
        Args:
            stream: An iterator of strings to process
            
        Returns:
            An iterator of processed strings
        """
        pass


class ConfigurableProcessor(StreamProcessor):
    """Base class for processors that require initialization with configuration."""
    
    def __init__(self, **kwargs):
        """
        Initialize the processor with the given configuration.
        
        Args:
            **kwargs: Configuration options for the processor
        """
        self.config = kwargs
        self.initialize()
        
    def initialize(self):
        """
        Initialize processor state based on configuration.
        Override this in subclasses if needed.
        """
        pass


class StatefulProcessor(ConfigurableProcessor):
    """Base class for processors that maintain state between calls."""
    
    def __init__(self, **kwargs):
        """Initialize the processor with the given configuration."""
        self.state: Dict[str, Any] = {}
        super().__init__(**kwargs)
    
    def reset_state(self):
        """Reset the processor state to initial values."""
        self.state = {}
        self.initialize()