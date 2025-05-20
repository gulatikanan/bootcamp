## Author: KANAN  
## Level: 4 — Stream Processing Framework

## Introduction

**Stream Processing Framework** implements **iterator-based data handling**, enabling processors to:

* Process data as continuous streams (`Iterator[str]`)
* Generate **variable output volume** - from none to multiple lines per input
* Preserve **context between operations** across the data stream
* Accept **custom parameters** through configuration files

This architecture serves as the groundwork for sophisticated data transformation pipelines supporting **multiple outputs**, **input aggregation**, and **memory-aware processing**.

---

## Key Capabilities

* Stream-oriented processor interface: `Iterator[str] → Iterator[str]`
* Backward compatibility with existing `str → str` processors through adapter patterns
* **Multiple output generation** (such as tokenizing sentences)
* **Context preservation** (like sequential numbering)
* Per-processor parameterization via `pipeline.yaml`

---

## Project Structure

```
abstraction-level-4/
├── main.py
├── cli.py
├── core.py
├── pipeline.py
├── types.py
├── pipeline.yaml
└── processors/
    ├── upper.py              # to_uppercase: str → str
    ├── snake.py              # to_snakecase: str → str
    ├── fanout_splitter.py    # SplitLines: stream-based, fan-out
    └── stateful_counter.py   # LineCounter: stream-based, stateful
```

---

## Implementation Details

The `pipeline.yaml` specifies processing stages using fully qualified module paths and optional parameters:

```yaml
pipeline:
  - type: processors.stateful_counter.LineCounter
    config:
      prefix: "Line"
  - type: processors.upper.to_uppercase
  - type: processors.fanout_splitter.SplitLines
    config:
      delimiter: " "
```

This configuration creates a **3-stage streaming pipeline**:

1. **LineCounter** – Annotates each line with `"Line {n}:"`
2. **to\_uppercase** – Transforms text to uppercase
3. **SplitLines** – Segments each line into multiple outputs using spaces as separators

---

## Sample Input (`input.txt`)
```
Hello World
PytHoN is SureLy gREAt
PiplInes Are GoOd 
```

---

## Result

```
LINE
1:
HELLO
WORLD
LINE
2:
PYTHON
IS
SURELY
GREAT
LINE
3:
PIPLINES
ARE
GOOD
```

Each input line undergoes:

1. Sequential numbering (e.g., `Line 1:`)
2. Case normalization to uppercase
3. Decomposition into separate lines at space boundaries

---

## Usage Instructions

```bash
python main.py --input input.txt --config pipeline.yaml
```

---

## Implementation Verification

* [x] Processors implement `Iterator[str] -> Iterator[str]` interface
* [x] Legacy `str -> str` functions integrated through decorator patterns
* [x] `LineCounter` retains state and prepends sequence numbers
* [x] `SplitLines` implements one-to-many transformation
* [x] Configuration parameters correctly passed to processor instances
* [x] Individual processors support independent testing