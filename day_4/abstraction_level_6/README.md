## Author: **KANAN**
## Level 6: State-Based Routing System
A powerful, tag-driven text processing engine inspired by finite state machines. Each input line dynamically flows through a set of registered processors based on its current tag, supporting fan-out, fan-in, loops, and conditional logic. Routing is defined via a YAML config for maximum flexibility and modularity.


## 📁 Project Structure

```
abstraction_level_6/
├── main.py               # Reads input, runs router, writes output
├── cli.py                # CLI interface using Typer
├── router.py             # Core routing engine based on tag transitions
├── processor_types.py    # Shared type aliases
├── processors/           # Modular processors
│   ├── start.py          # Tags raw input as error/warn/general
│   ├── filters.py        # Filters for 'error', 'warn'
│   ├── formatters.py     # snake_case and UPPERCASE transforms
│   └── output.py         # 'end' terminal handler
├── config.yaml           # YAML config defining routing graph
└── input.txt             # Sample input file
```



## ⚙️ Features

* ✅ Declarative YAML config for dynamic tag-based routing
* ✅ Each processor registered under a tag
* ✅ Fan-out: one input → many processors
* ✅ Fan-in: multiple sources → one tag
* ✅ Cyclic routing support (guarded by loop detection)
* ✅ Fully pluggable processors (function or class-based)
* ✅ Clean CLI using [Typer](https://typer.tiangolo.com/)
* ✅ Intelligent output formatting (Info / Warnings / Errors)



## 📌 Installation

```
pip install typer[all] pyyaml
```

---

## 🧪 Example Usage

```
python main.py --input input.txt --config config.yaml
```

Or with output file:

```
python main.py --input input.txt --config config.yaml --output output.txt
```

---

## 🧱 YAML Routing Config Example

```
nodes:
  - tag: start
    type: processors.start.tag_lines
  - tag: error
    type: processors.filters.only_error
  - tag: warn
    type: processors.filters.only_warn
  - tag: general
    type: processors.formatters.snakecase
  - tag: end
    type: processors.output.terminal
```

Each processor consumes lines with its associated tag and emits new `(tag, line)` pairs that route dynamically.


## 📝 Processor Signature

```
# processor_types.py
TaggedLine = Tuple[str, str]
StateProcessor = Callable[[Iterator[TaggedLine]], Iterator[TaggedLine]]
```

Every processor accepts a stream of `(tag, line)` and emits a stream of `(tag, line)` — enabling flexible state transitions.



## 📂 Sample Processors

### processors/start.py

```
def tag_lines(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for _, line in lines:
        if 'ERROR' in line:
            yield 'error', line
        elif 'WARN' in line:
            yield 'warn', line
        else:
            yield 'general', line
```

### processors/filters.py

```
def only_error(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for tag, text in lines:
        if tag == 'error':
            yield 'end', text
```

### processors/formatters.py

```
def snakecase(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for _, text in lines:
        yield 'end', '_'.join(text.split()).lower()
```



## 📥 Input / Output Examples

| Input Line                                     | Routed Through        | Final Output (end)                             |
| ---------------------------------------------- | --------------------- | ---------------------------------------------- |
| \[INFO] User authentication completed          | start → general → end | \[info]\_user\_authentication\_completed       |
| \[WARNING] High memory usage detected          | start → warn → end    | \[WARNING] High memory usage detected          |
| \[ERROR] Unable to write to configuration file | start → error → end   | \[ERROR] Unable to write to configuration file |



## 🧯 Error Handling

| Error Condition                | What Happens                              |
| ------------------------------ | ----------------------------------------- |
| Unknown tag emitted            | Raises `RoutingError` with tag info       |
| Processor is not callable      | Raises `RoutingError` during config load  |
| Infinite routing loop detected | Raises `RoutingError` (after 1000 cycles) |
| Invalid module path in config  | Raises ImportError with full traceback    |



## 💡 Extending the Router

To add a new tag or processing step:

1. Create a new file or function in `processors/`
2. Example: reverse every general line

```
# processors/transformers.py
def reverse(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
    for tag, text in lines:
        yield 'end', text[::-1]
```

3. Add to config:

```
- tag: general
  type: processors.transformers.reverse
```

No changes needed in `main.py` or `router.py`.



## ✅ Checklist

* [x] Tag-based routing engine with dynamic transitions
* [x] Guards against infinite routing cycles
* [x] Supports fan-in / fan-out topologies
* [x] Pluggable, dynamic processor registration
* [x] CLI-compatible and config-driven


## 📜 License

MIT License