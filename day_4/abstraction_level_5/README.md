## Author: KANAN  
## Level 5: DAG Routing and Conditional Flows

A content-aware, DAG-based text processing engine that supports conditional routing, tagging, and fan-in/fan-out flows. Each line can dynamically follow different paths in the pipeline based on tags assigned by processors. This enables real-world workflows like log routing, categorization, and complex branching—all defined in a config file.



## 📁 Project Structure

```
abstraction_level_5/
├── main.py           # Entry point: read input, invoke engine, write output
├── engine.py         # DAG engine to route and process tagged lines
├── processor.py      # Stream processors (trim, tag, count, format, etc.)
├── config.py         # Loads processor DAG and routing rules from config
├── types.py          # Shared type definitions (e.g., TaggedLine)
├── input.txt         # Input data lines
├── output.txt        # Final output written here
└── dag_config.yaml   # DAG config defining nodes, tags, and routing
```

---

## ⚙️ Features

* ✅ DAG-based routing (each processor is a node)
* ✅ Processors can emit `(tag, line)` tuples
* ✅ Conditional branching based on tags (`errors`, `warnings`, `general`)
* ✅ Fan-out and fan-in routing logic
* ✅ YAML-configurable flow: no hardcoded logic
* ✅ Reusable and testable processors
* ✅ Supports stateful processors like counters and accumulators


## 📌 Installation

```
pip install typer[all] pyyaml
```



## 🧪 Example Usage

```
python main.py --input input.txt --config dag_config.yaml --output output.txt
```

### Input lines (in `input.txt`):

```
ERROR: Disk full
WARNING: High memory usage
INFO: System operational
ERROR: Unauthorized access attempt
```
### Output lines (in `output.txt`):

```
[INFO] Count of errors: 2
[INFO] Count of warnings: 1
ERROR archived: Disk full
ERROR archived: Unauthorized access attempt
General Message: System operational
```



## 🧱 YAML DAG Config Example

```
nodes:
  trim:
    type: processor.trim

  tagger:
    type: processor.tagger
    inputs: [trim]

  error_counter:
    type: processor.count_errors
    inputs: [tagger]
    tags: [error]

  archiver:
    type: processor.archive_errors
    inputs: [error_counter]
    tags: [error]

  warning_tally:
    type: processor.tally_warnings
    inputs: [tagger]
    tags: [warning]

  formatter:
    type: processor.format_general
    inputs: [tagger]
    tags: [general]

  output:
    type: processor.output_collector
    inputs: [archiver, warning_tally, formatter]
```



## 🧠 Processor Signature

```
# types.py
TaggedLine = tuple[str, str]
StreamProcessor = Callable[[Iterator[TaggedLine]], Iterator[TaggedLine]]
```

Processors receive a stream of `(tag, line)` and yield processed `(tag, line)` outputs.



## 🧱 Sample Processors

### `processor.py`

```
def trim(lines):
    for tag, line in lines:
        yield tag, line.strip()

def tagger(lines):
    for _, line in lines:
        if line.startswith("ERROR"):
            yield "error", line
        elif line.startswith("WARNING"):
            yield "warning", line
        else:
            yield "general", line

def count_errors(lines):
    count = 0
    for tag, line in lines:
        count += 1
    yield "info", f"Count of errors: {count}"

def archive_errors(lines):
    for tag, line in lines:
        msg = line.replace("ERROR: ", "ERROR archived: ")
        yield "output", msg

def tally_warnings(lines):
    count = sum(1 for _ in lines)
    yield "output", f"[INFO] Count of warnings: {count}"

def format_general(lines):
    for tag, line in lines:
        yield "output", f"General Message: {line.replace('INFO: ', '')}"

def output_collector(lines):
    for tag, line in lines:
        yield tag, line  # Pass through
```



## 📥 Input / Output Examples

| Input Line                   | Tag     | Output Line                           |
| ---------------------------- | ------- | ------------------------------------- |
| `ERROR: Disk full`           | error   | `ERROR archived: Disk full`           |
| `ERROR: Unauthorized access` | error   | `ERROR archived: Unauthorized access` |
| `WARNING: High memory usage` | warning | `[INFO] Count of warnings: 1`         |
| `INFO: System operational`   | general | `General Message: System operational` |
| *(derived)*                  | info    | `[INFO] Count of errors: 2`           |



## 🔁 DAG Flow Overview

```
      ┌────────┐
      │  trim  │
      └──┬─────┘
         │
      ┌──▼─────┐
      │ tagger │
      └─┬─┬──┬─┘
    error │ warning │ general
         ▼        ▼        ▼
  ┌──────────┐   ┌────────────┐   ┌──────────────┐
  │count_errs│   │tally_warns │   │format_general│
  └────┬─────┘   └────┬───────┘   └──────┬───────┘
       ▼             ▼                  ▼
   ┌────────┐     ┌────────┐       ┌────────────┐
   │archive │     │output  │       │   output   │
   └────┬───┘     └────────┘       └────┬───────┘
        └──────────────────────────────┘
                   ↓
              Final Output
```



## ✅ Checklist

* [x] Lines routed conditionally based on content
* [x] Supports fan-out and fan-in flows
* [x] YAML-defined DAG config
* [x] Processors yield `(tag, line)`
* [x] Custom processors can be easily added
* [x] Testable routing engine with stream input



## 📜 License

MIT License