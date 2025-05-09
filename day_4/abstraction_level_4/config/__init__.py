# stream_processing/__init__.py
"""Stream processing system package."""

from .core.base import StreamProcessor, ConfigurableProcessor, StatefulProcessor
from .pipeline.builder import Pipeline, PipelineBuilder

__version__ = "0.1.0"

# stream_processing/core/__init__.py
"""Core components for stream processing."""

from .base import StreamProcessor, ConfigurableProcessor, StatefulProcessor
from .adapters import str_processor_adapter, adapt_str_processor, FunctionProcessor

# stream_processing/processors/__init__.py
"""Stream processors implementation."""

from .basic import (
    IdentityProcessor, 
    FilterProcessor, 
    TransformProcessor,
    SplitProcessor,
    JoinProcessor
)

from .stateful import (
    LineCountProcessor,
    DuplicateDetectorProcessor,
    AggregatorProcessor,
    BufferProcessor
)

# stream_processing/pipeline/__init__.py
"""Pipeline components for stream processing."""

from .builder import Pipeline, PipelineBuilder

# stream_processing/config/__init__.py
"""Configuration components for stream processing."""

from .parser import ConfigParser

# stream_processing/utils/__init__.py
"""Utility components for stream processing."""

from .helpers import (
    stream_from_string,
    stream_from_file,
    stream_to_file,
    timed_processing,
    string_matcher,
    collect_stream,
    peek_stream
)