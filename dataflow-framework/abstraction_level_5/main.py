# from engine import DAGEngine
# from config import pipeline_config

# if __name__ == "__main__":
#     input_lines = [
#         " ERROR: Disk failure",
#         " WARN: Low battery",
#         "User login successful",
#         " ERROR: Network down",
#         "System update complete"
#     ]

#     engine = DAGEngine(pipeline_config)
#     engine.run(input_lines)

from engine import DAGEngine
from config import pipeline_config

if __name__ == "__main__":
    input_lines = [
        " ERROR: Disk failure",
        " WARN: Low battery",
        "User login successful",
        " ERROR: Network down",
        "System update complete"
    ]

    engine = DAGEngine(pipeline_config)
    outputs = engine.run(input_lines)

    # Print the outputs
    for node, tagged_lines in outputs.items():
        print(f"--- Output from node: {node} ---")
        for tag, line in tagged_lines:
            print(f"[{tag}] {line}")
