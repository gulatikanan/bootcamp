from typing import List, Iterator, Dict, Any, Optional
from processors.base import ObservableProcessor
from metrics.metrics_store import MetricsStore

class ObservablePipeline:
    """A pipeline that chains multiple observable processors together."""
    
    def __init__(self, processors: List[ObservableProcessor] = None, pipeline_id: Optional[str] = None):
        """
        Initialize the pipeline with a list of processors.
        
        Args:
            processors: List of processors to add to the pipeline
            pipeline_id: Optional ID for the pipeline
        """
        self.processors = processors or []
        self.pipeline_id = pipeline_id or "pipeline"
        self.metrics_store = MetricsStore()
    
    def add_processor(self, processor: ObservableProcessor) -> 'ObservablePipeline':
        """
        Add a processor to the pipeline.
        
        Args:
            processor: The processor to add
            
        Returns:
            The pipeline instance for method chaining
        """
        self.processors.append(processor)
        return self
    
    def process(self, input_stream: Iterator[str]) -> Iterator[str]:
        """
        Process the input stream through all processors in the pipeline.
        
        Args:
            input_stream: Iterator of input strings
            
        Returns:
            Iterator of processed strings
        """
        current_stream = input_stream
        
        for processor in self.processors:
            current_stream = processor.process(current_stream)
        
        return current_stream
    
    def process_text(self, text: str) -> str:
        """
        Process a string through the pipeline and return the result as a string.
        
        Args:
            text: Input text to process
            
        Returns:
            Processed text
        """
        lines = text.splitlines()
        result_lines = list(self.process(iter(lines)))
        return '\n'.join(result_lines)
    
    def enable_tracing(self, enabled: bool = True):
        """
        Enable or disable tracing for this pipeline.
        
        Args:
            enabled: Whether to enable tracing
        """
        self.metrics_store.set_tracing_enabled(enabled)