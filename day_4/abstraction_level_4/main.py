"""
Main entry point for the stream processing system.
"""
import argparse
import sys
from typing import Dict, Type, List, Iterator

from stream_processing.core.base import StreamProcessor
from stream_processing.core.adapters import adapt_str_processor
from stream_processing.processors.basic import (
    IdentityProcessor, 
    FilterProcessor, 
    TransformProcessor,
    SplitProcessor,
    JoinProcessor
)
from stream_processing.processors.stateful import (
    LineCountProcessor,
    DuplicateDetectorProcessor,
    AggregatorProcessor,
    BufferProcessor
)
from stream_processing.pipeline.builder import Pipeline, PipelineBuilder
from stream_processing.config.parser import ConfigParser
from stream_processing.utils.helpers import (
    stream_from_file, 
    stream_to_file, 
    stream_from_string,
    timed_processing
)


def register_processors(registry: Dict[str, Type[StreamProcessor]]):
    """
    Register all available processors.
    
    Args:
        registry: Dictionary to register processors in
    """
    # Basic processors
    registry["identity"] = IdentityProcessor
    registry["filter"] = FilterProcessor
    registry["transform"] = TransformProcessor
    registry["split"] = SplitProcessor
    registry["join"] = JoinProcessor
    
    # Stateful processors
    registry["line_count"] = LineCountProcessor
    registry["duplicate_detector"] = DuplicateDetectorProcessor
    registry["aggregator"] = AggregatorProcessor
    registry["buffer"] = BufferProcessor


def build_default_pipeline() -> Pipeline:
    """
    Build a default pipeline for testing.
    
    Returns:
        A simple pipeline with some processors
    """
    pipeline = Pipeline()
    
    # Add some processors to the pipeline
    pipeline.add_processor(LineCountProcessor(pattern="Line {count}: {line}"))
    pipeline.add_processor(FilterProcessor(min_length=3))
    pipeline.add_processor(TransformProcessor(transform_func=lambda s: s.upper()))
    
    return pipeline


@timed_processing
def process_file(input_path: str, output_path: str, config_path: str = None):
    """
    Process a file using the stream processing system.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
        config_path: Optional path to config file
    """
    # Create processor registry
    registry = {}
    register_processors(registry)
    
    # Build pipeline from config or use default
    if config_path:
        parser = ConfigParser(registry)
        pipeline = parser.parse_file(config_path)
    else:
        pipeline = build_default_pipeline()
    
    # Process the file
    stream = stream_from_file(input_path)
    processed_stream = pipeline.process(stream)
    stream_to_file(processed_stream, output_path)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Stream Processing System")
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--config", "-c", help="Config file path")
    
    args = parser.parse_args()
    
    process_file(args.input, args.output, args.config)
    
    print(f"Processing complete. Output written to {args.output}")


if __name__ == "__main__":
    main()