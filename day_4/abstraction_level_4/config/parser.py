"""
Configuration parser for stream processing pipelines.
"""
import json
import yaml
from typing import Dict, List, Any, Type, Union
import os

from ..core.base import StreamProcessor
from ..pipeline.builder import PipelineBuilder, Pipeline


class ConfigParser:
    """
    Parser for pipeline configuration files.
    """
    
    def __init__(self, processor_registry: Dict[str, Type[StreamProcessor]] = None):
        """
        Initialize with a registry of available processors.
        
        Args:
            processor_registry: Dictionary mapping processor names to classes
        """
        self.builder = PipelineBuilder(processor_registry)
    
    def register_processor(self, name: str, processor_class: Type[StreamProcessor]):
        """
        Register a processor class.
        
        Args:
            name: Name to register the processor under
            processor_class: StreamProcessor class
        """
        self.builder.register_processor(name, processor_class)
    
    def parse_file(self, config_path: str) -> Pipeline:
        """
        Parse a configuration file and build a pipeline.
        
        Args:
            config_path: Path to configuration file (JSON or YAML)
            
        Returns:
            Configured Pipeline instance
            
        Raises:
            ValueError: If file format is unsupported
        """
        _, ext = os.path.splitext(config_path)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if ext.lower() in ['.json']:
                config = json.load(f)
            elif ext.lower() in ['.yml', '.yaml']:
                config = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported config file format: {ext}")
        
        return self.parse_config(config)
    
    def parse_config(self, config: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Pipeline:
        """
        Parse a configuration dictionary and build a pipeline.
        
        Args:
            config: Configuration dictionary or list
            
        Returns:
            Configured Pipeline instance
        """
        # Handle both dict and list formats
        if isinstance(config, dict):
            if "processors" in config:
                # It's a container format
                processors_config = config["processors"]
            else:
                # Single processor in dict format
                processors_config = [config]
        else:
            # Already a list of processors
            processors_config = config
        
        return self.builder.build_pipeline(processors_config)