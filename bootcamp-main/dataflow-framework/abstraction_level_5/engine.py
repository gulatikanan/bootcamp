from collections import defaultdict
from typing import Dict, Callable, Iterator, List
from typing import Tuple
TaggedLine = Tuple[str, str]



class DAGEngine:
    def __init__(self, config: Dict[str, Dict]):
        self.config = config
        self.processors: Dict[str, Callable[[Iterator[TaggedLine]], Iterator[TaggedLine]]] = {}
        self.edges: Dict[str, List[str]] = defaultdict(list)
        self.outputs: Dict[str, List[TaggedLine]] = defaultdict(list)

        for name, info in config.items():
            self.processors[name] = info["processor"]
            for out_tag, dest_nodes in info.get("routes", {}).items():
                self.edges[name].extend(dest_nodes)

    def run(self, input_lines: List[str]):
        queue: Dict[str, List[TaggedLine]] = defaultdict(list)
        for line in input_lines:
            queue["start"].append(("start", line))

        while queue:
            current = next(iter(queue))
            lines = queue.pop(current)
            processor = self.processors.get(current)
            if not processor:
                continue

            output = list(processor(iter(lines)))
            for tag, line in output:
                for next_node in self.config.get(current, {}).get("routes", {}).get(tag, []):
                    queue[next_node].append((tag, line))
                if not self.config.get(current, {}).get("routes", {}).get(tag):
                    self.outputs[current].append((tag, line))

        return self.outputs
