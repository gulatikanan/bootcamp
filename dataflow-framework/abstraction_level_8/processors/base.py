import time
import uuid
from typing import Iterator, Protocol, Any, List, Dict, Optional
from abc import ABC, abstractmethod

from metrics.metrics_store import MetricsStore
from metrics.tracer import LineTracer

class StreamProcessor(Protocol):
    """Protocol defining the interface for stream processors."""
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """Process a stream of strings and yield processed strings."""
        ...

class ObservableProcessor(ABC):
    """
    Base class for processors that collect metrics and support tracing.
    Implements the StreamProcessor protocol.
    """
    
    def __init__(self, processor_id: Optional[str] = None, processor_type: str = "unknown"):
        """
        Initialize the processor with an ID and type.
        
        Args:
            processor_id: Unique identifier for this processor instance
            processor_type: Type of processor (e.g., "filter", "transform")
        """
        self.processor_id = processor_id or f"{processor_type}_{uuid.uuid4().hex[:8]}"
        self.processor_type = processor_type
        self.metrics_store = MetricsStore()
        self.metrics_store.register_processor(self.processor_id, self.processor_type)
    
    @abstractmethod
    def _process_line(self, line: str) -> Iterator[str]:
        """
        Process a single line and yield results.
        This method should be implemented by subclasses.
        """
        pass
    
    def process(self, stream: Iterator[str]) -> Iterator[str]:
        """
        Process a stream of strings with metrics collection.
        This implements the StreamProcessor protocol.
        """
        for line in stream:
            # Generate or extract trace ID
            trace_id = LineTracer.extract_trace_id(line) or LineTracer.generate_trace_id()
            
            # Record that we received a line
            self.metrics_store.update_lines_in(self.processor_id)
            self.metrics_store.add_trace(trace_id, self.processor_id, "start", line)
            
            try:
                # Process the line and measure time
                start_time = time.time()
                output_count = 0
                
                for result in self._process_line(line):
                    output_count += 1
                    self.metrics_store.update_lines_out(self.processor_id)
                    self.metrics_store.add_trace(trace_id, self.processor_id, "emit", line)
                    yield result
                
                # Record processing time
                processing_time = time.time() - start_time
                self.metrics_store.update_processing_time(self.processor_id, processing_time)
                
                # If no output was produced, record a drop
                if output_count == 0:
                    self.metrics_store.add_trace(trace_id, self.processor_id, "drop", line)
                
            except Exception as e:
                # Record errors
                error_message = str(e)
                self.metrics_store.record_error(self.processor_id, error_message)
                self.metrics_store.add_trace(trace_id, self.processor_id, "error", line)
                # Re-raise the exception
                raise