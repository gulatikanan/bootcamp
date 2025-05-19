import json
from typing import Dict, Any, List
from pathlib import Path

from processors.base import ObservableProcessor
from processors.stateful import LineCounter, LineJoiner, LineSplitter, FilterProcessor, TagRouter
from processors.simple import adapt_simple_processor
from pipeline.pipeline import ObservablePipeline

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        return json.load(f)

def create_processor_from_config(processor_config: Dict[str, Any]) -> ObservableProcessor:
    """
    Create a processor instance from a configuration dictionary.
    
    Args:
        processor_config: Configuration for the processor
        
    Returns:
        An ObservableProcessor instance
    """
    processor_type = processor_config.get("type")
    processor_id = processor_config.get("id")
    
    if processor_type == "line_counter":
        format_str = processor_config.get("format", "[{count}] {line}")
        return LineCounter(format_str=format_str, processor_id=processor_id)
    
    elif processor_type == "line_joiner":
        delimiter = processor_config.get("delimiter", " | ")
        return LineJoiner(delimiter=delimiter, processor_id=processor_id)
    
    elif processor_type == "line_splitter":
        delimiter = processor_config.get("delimiter", ",")
        return LineSplitter(delimiter=delimiter, processor_id=processor_id)
    
    elif processor_type == "filter":
        # This is a simplified example - in a real system,
        # you might use a more sophisticated approach to define filters
        pattern = processor_config.get("pattern", "")
        def filter_func(line: str) -> bool:
            return pattern in line
        return FilterProcessor(filter_func, processor_id=processor_id)
    
    elif processor_type == "uppercase":
        def uppercase(line: str) -> str:
            return line.upper()
        return adapt_simple_processor(uppercase, processor_id=processor_id)
    
    elif processor_type == "lowercase":
        def lowercase(line: str) -> str:
            return line.lower()
        return adapt_simple_processor(lowercase, processor_id=processor_id)
    
    elif processor_type == "tag_router":
        tag_field = processor_config.get("tag_field", 0)
        delimiter = processor_config.get("delimiter", ",")
        router = TagRouter(tag_field=tag_field, delimiter=delimiter, processor_id=processor_id)
        
        # Configure routes
        routes = processor_config.get("routes", {})
        for tag, route_config in routes.items():
            route_processor = create_processor_from_config(route_config)
            router.add_route(tag, route_processor)
        
        return router
    
    else:
        raise ValueError(f"Unknown processor type: {processor_type}")

def create_pipeline_from_config(config: Dict[str, Any]) -> ObservablePipeline:
    """
    Create a pipeline from a configuration dictionary.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        An ObservablePipeline instance
    """
    pipeline = ObservablePipeline()
    
    processors_config = config.get("processors", [])
    for processor_config in processors_config:
        processor = create_processor_from_config(processor_config)
        pipeline.add_processor(processor)
    
    return pipeline