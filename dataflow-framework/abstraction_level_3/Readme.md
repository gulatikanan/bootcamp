## Author: KANAN  
## Level: 3 — Configuration-Based Processing Pipeline
  
A flexible, modular Python application for text transformation that processes text files line-by-line and applies customizable processing sequences defined in YAML configuration files. Designed to scale from basic scripting to a comprehensive plugin architecture.

## 📋 Directory Layout

```
abstraction_level_3/
├── main.py               # Program entry point
├── cli.py                # Command line interface with Typer
├── core.py               # Processor pipeline application logic
├── pipeline.py           # YAML configuration loader for processor pipeline
├── processor_types.py    # Type definitions for processor functions
├── processors/           # Individual processor function modules
│   ├── upper.py          # Transforms text to UPPERCASE
│   └── snake.py          # Converts text to snake_case
└── pipeline.yaml         # Configuration file defining processor sequence
```

## ✨ Key Capabilities

* ✅ User-friendly command interface built with [Typer](https://typer.tiangolo.com/)
* ✅ User-defined processing steps via `pipeline.yaml`
* ✅ Runtime-loaded processing functions (lazy imports)
* ✅ Sequential multi-transformation support
* ✅ Output to console or saved to file
* ✅ Type-safe implementation with `ProcessorFn = Callable[[str], str]`

## 📦 Setup Instructions

```
pip install typer[all] python-dotenv pyyaml
```

## 🚀 Operation Guide

### Command-line execution:

```
python main.py --input input.txt --config pipeline.yaml
```

Or with file output:

```
python main.py --input input.txt --config pipeline.yaml --output result.txt
```

## 🔧 YAML Configuration Example

```
pipeline:
  - type: processors.snake.to_snakecase   # First converts to snake_case
  - type: processors.upper.to_uppercase   # Then converts to UPPERCASE
```

Functions are applied sequentially to each line in the input file.

## 📐 Processor Function Format

All processor functions follow this structure:

```python
# processor_types.py
ProcessorFn = Callable[[str], str]
```

This enables function composition into a processing pipeline:

```
def apply_pipeline(lines: Iterator[str], processors: list[ProcessorFn]) -> Iterator[str]:
    for line in lines:
        for processor in processors:
            line = processor(line)
        yield line
```

## 📚 Example Processors

### processors/snake.py

```
def to_snakecase(line: str) -> str:
    return line.strip().lower().replace(" ", "_")
```

### processors/upper.py

```
def to_uppercase(line: str) -> str:
    return line.strip().upper()
```

## 📊 Input / Output Examples

| Input (`input.txt`) | YAML Configuration               | Result         |
| ------------------- | -------------------------------- | -------------- |
| `Hello World`       | `to_uppercase`                   | `HELLO WORLD`  |
| `Hello World`       | `to_snakecase`                   | `hello_world`  |
| `Hello World`       | `to_snakecase` → `to_uppercase`  | `HELLO_WORLD`  |
| `   hi  there   `   | `to_snakecase` → `to_uppercase`  | `HI_THERE`     |

## 🚨 Error Management

If an invalid function path appears in the YAML configuration:

```
ImportError: Could not load processor processors.bad.path: No module named 'processors.bad'
```

The application will display a clear error message to help fix your `pipeline.yaml`.

---

## 💫 System Expansion

To create a new transformation:

1. Add a new file in `processors/` (example: `reverse.py`)
2. Create a `str -> str` function:

```
def reverse(line: str) -> str:
    return line[::-1]
```

3. Update `pipeline.yaml`:

```
pipeline:
  - type: processors.reverse.reverse
```

No modifications to core code required.

## ✓ Feature Verification

* [x] CLI supports `--config` YAML path parameter
* [x] All processors implement `str -> str` pattern
* [x] New processors can be added without core code changes
* [x] Uses dynamic module imports for flexibility
* [x] Well-organized directory structure and type system

## 📄 License Information

MIT License
