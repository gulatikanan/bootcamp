from typing import Iterator, Callable, Optional
from processors.base import ObservableProcessor

def adapt_simple_processor(func: Callable[[str], str], processor_id: Optional[str] = None) -> ObservableProcessor:
    """
    Convert a simple str -> str function to an observable processor.
    This allows reusing existing simple processors with the new observable interface.
    
    Args:
        func: A function that takes a string and returns a string
        processor_id: Optional ID for the processor
        
    Returns:
        An ObservableProcessor that wraps the function
    """
    processor_type = func.__name__ if hasattr(func, "__name__") else "simple_processor"
    
    class SimpleProcessorAdapter(ObservableProcessor):
        def __init__(self):
            super().__init__(processor_id, processor_type)
        
        def _process_line(self, line: str) -> Iterator[str]:
            result = func(line)
            yield result
    
    return SimpleProcessorAdapter()

def observable_processor(func: Callable[[str], str]) -> Callable[[], ObservableProcessor]:
    """
    Decorator to convert a simple str -> str function to an observable processor factory.
    
    Example:
        @observable_processor
        def uppercase(line: str) -> str:
            return line.upper()
            
        pipeline.add_processor(uppercase())
    """
    def factory(processor_id: Optional[str] = None):
        return adapt_simple_processor(func, processor_id)
    return factory