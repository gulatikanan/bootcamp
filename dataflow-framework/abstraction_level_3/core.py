from typing import List, Callable

def process_file(input_path: str, processors: List[Callable[[str], str]]):
    with open(input_path, "r") as f:
        for line in f:
            for processor in processors:
                line = processor(line)
            print(line, end="")
