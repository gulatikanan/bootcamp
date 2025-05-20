import yaml
import importlib
from types_ import ProcessorFn

def load_pipeline(config_path: str) -> list[ProcessorFn]:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    processors = []
    for step in config["pipeline"]:
        import_path = step["type"]
        try:
            module_path, func_name = import_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            func = getattr(module, func_name)
            if not callable(func):
                raise TypeError(f"{import_path} is not callable.")
            processors.append(func)
        except (ImportError, AttributeError, TypeError) as e:
            raise ImportError(f"Error loading processor '{import_path}': {e}")
    return processors
