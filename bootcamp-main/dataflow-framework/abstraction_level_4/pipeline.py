import importlib
import yaml
from processor_types import StreamProcessor
from processor_types import LineProcessor
from typing import Iterator, Any
from pathlib import Path

# pipeline.py
def load_pipeline(config_path: str) -> list[LineProcessor]:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    processors = []
    for step in config["pipeline"]:
        type_path = step["type"]
        options = step.get("config", {})

        module_path, func_name = type_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        processor_fn = getattr(module, func_name)

        if isinstance(processor_fn, type):
            # It's a class — instantiate it
            processor = processor_fn(**options)
        else:
            # It's a function — use it directly
            processor = processor_fn

        processors.append(processor)

    return processors
