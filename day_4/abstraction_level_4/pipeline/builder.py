"""
Pipeline construction for stream processors.
"""
from typing import List, Dict, Any, Iterator, Callable, Union, Type

from ..core.base import StreamProcessor
from ..core.adapters import adapt_str_processor


class Pipeline:
    """
    A pipeline of stream processors that can be executed in sequence.
    """
    
    def __init__(self, processors: List[StreamProcessor] = None):
        """
        Initialize with optional list of processors.
        
        Args:
            processors: List of StreamProcessor instances
        """
        self.processors = processors or []
    
    def add_processor(self, processor: StreamProcessor) -> 'Pipeline':
        """
        Add a processor to the pipeline.
        
        Args:
            processor: StreamProcessor instance
            
        Returns:
            Self for chaining
        """
        self.processors.append(processor)
        return self
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process a stream through the entire pipeline.
        
        Args:
            stream: Input stream of strings
            
        Returns:
            Stream of fully processed strings
        """
        result = stream
        for processor in self.processors:
            result = processor.process(result)
        return result
    
    def process_string(self, text: str) -> List[str]:
        """
        Process a single string through the pipeline.
        
        Args:
            text: Input string
            
        Returns:
            List of processed strings
        """
        # Convert string to a single-item stream
        stream = iter([text])
        result = list(self.process(stream))
        return result

    def process_lines(self, lines: List[str]) -> List[str]:
        """
        Process a list of strings through the pipeline.
        
        Args:
            lines: List of input strings
            
        Returns:
            List of processed strings
        """
        stream = iter(lines)
        result = list(self.process(stream))
        return result
    
    def process_file(self, input_path: str, output_path: str = None) -> List[str]:
        """
        Process a file through the pipeline.
        
        Args:
            input_path: Path to input file
            output_path: Optional path to output file
            
        Returns:
            List of processed lines
        """
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Process lines
        result = self.process_lines(lines)
        
        # Write to output file if specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                for line in result:
                    f.write(line + '\n')
        
        return result


class PipelineBuilder:
    """
    Builder for creating pipelines from configuration.
    """
    
    def __init__(self, processor_registry: Dict[str, Type[StreamProcessor]] = None):
        """
        Initialize with a registry of available processors.
        
        Args:
            processor_registry: Dictionary mapping processor names to classes
        """
        self.processor_registry = processor_registry or {}
    
    def register_processor(self, name: str, processor_class: Type[StreamProcessor]):
        """
        Register a processor class.
        
        Args:
            name: Name to register the processor under
            processor_class: StreamProcessor class
        """
        self.processor_registry[name] = processor_class
    
    def create_processor(self, processor_type: str, config: Dict[str, Any] = None) -> StreamProcessor:
        """
        Create a processor instance from configuration.
        
        Args:
            processor_type: Type name of the processor
            config: Configuration for the processor
            
        Returns:
            Configured StreamProcessor instance
            
        Raises:
            ValueError: If processor type is not registered
        """
        if processor_type not in self.processor_registry:
            raise ValueError(f"Unknown processor type: {processor_type}")
        
        processor_class = self.processor_registry[processor_type]
        config = config or {}
        
        return processor_class(**config)
    
    def build_pipeline(self, config: List[Dict[str, Any]]) -> Pipeline:
        """
        Build a pipeline from configuration.
        
        Args:
            config: List of processor configurations
            
        Returns:
            Configured Pipeline instance
        """
        pipeline = Pipeline()
        
        for processor_config in config:
            processor_type = processor_config.pop("type")
            processor = self.create_processor(processor_type, processor_config)
            pipeline.add_processor(processor)
        
        return pipeline