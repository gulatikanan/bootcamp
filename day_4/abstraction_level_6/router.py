import importlib
import inspect
import yaml
from pathlib import Path
from collections import deque
from typing import Dict, Iterator, Tuple
from processor_types import TaggedLine, StateProcessor, Tag

class RoutingError(Exception):
    """
    Raised when routing or processors configuration is invalid.
    """
    pass

class StateRouter:
    """
    Engine that routes TaggedLine items through processors based on tags.
    """
    def __init__(self, config_path: Path):
        """
        Load processors from YAML list of nodes.

        Args:
            config_path: Path to YAML config with 'nodes:'.
        Raises:
            RoutingError: if a processors import fails or is not callable.
        """
        cfg = yaml.safe_load(config_path.read_text(encoding='utf-8'))
        self.proc_map: Dict[Tag, StateProcessor] = {}

        for node in cfg.get('nodes', []):
            tag = node['tag']
            path = node['type']
            module_name, func_name = path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            proc_obj = getattr(module, func_name)
            # Instantiate if class
            proc = proc_obj() if inspect.isclass(proc_obj) else proc_obj
            if not callable(proc):
                raise RoutingError(f"Processor for tag '{tag}' is not callable")
            self.proc_map[tag] = proc

    def run(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """
        Consume, process, and route lines until all reach 'end'.

        Args:
            lines: Iterator of (tag, text), starting with tag 'start'.
        Yields:
            TaggedLine with tag 'end' for completed lines.

        Raises:
            RoutingError: on unknown tag or detected cycles.
        """
        queue = deque(lines)
        seen: Dict[Tuple[Tag, str], int] = {}

        while queue:
            tag, text = queue.popleft()
            if tag == 'end':
                yield tag, text
                continue

            key = (tag, text)
            seen[key] = seen.get(key, 0) + 1
            if seen[key] > 1000:
                raise RoutingError(f"Cycle detected on tag '{tag}'")

            if tag not in self.proc_map:
                raise RoutingError(f"No processors registered for tag '{tag}'")

            proc = self.proc_map[tag]
            for next_tag, next_text in proc(iter([(tag, text)])):
                queue.append((next_tag, next_text))