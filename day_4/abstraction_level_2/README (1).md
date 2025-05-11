## Author: KANAN  
## Level:** 2 -  Modular Structure and Standardized Processing

In this level, the previously monolithic script is refactored into a clean, modular design with clearly separated responsibilities. The code is organized into multiple Python modules, allowing better extensibility and maintainability.

## 🧱 Project Structure

```
abstraction_level_2/
├── main.py         # Entry point, wires up the CLI
├── cli.py          # Handles CLI logic using Typer
├── core.py         # Core logic: reading, processing, and writing
├── pipeline.py     # Chooses processor pipeline based on mode
├── custom_types.py        # Type definitions (ProcessorFn)
├── .env            # Contains default mode if not provided
├── input.txt       # Sample input file
├── output.txt      # Output written here
└── README.md       # You're reading it!
```

## 🔄 Supported Modes

| Mode        | Description                                     | Example Input | Output      |
| ----------- | ----------------------------------------------- | ------------- | ----------- |
| `uppercase` | Converts lines to uppercase                     | `i love py`   | `I LOVE PY` |
| `snakecase` | Replaces spaces with underscores and lowercases | `i love py`   | `i_love_py` |

More modes can be added by simply creating new processor functions in `core.py` and including them in `pipeline.py`.

## ✅ Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install typer python-dotenv
```

## 🚀 Running the Script

Make sure you are inside the `abstraction-level-2/` folder before running these commands.

### 📄 Testing Your Implementation

**1. Basic test with `uppercase` mode:**
```bash
python main.py --input test_input.txt --output test_output.txt --mode uppercase
```

**2. Test with `snakecase` mode:**
```bash
python main.py --input input.txt --output test_output.txt --mode snakecase
```

**3. Test with `both` processors:**
```bash
python main.py --input input.txt --output test_output.txt --mode both
```

**4. Test with shorthand options:**
```bash
python main.py -i input.txt -o test_output.txt -m both
```

**input.txt**
```
hello guys, 
python is great!
```
**Output:**
```
HELLO GUYS,
PYTHON IS GREAT!
```


## 📌 Notes

- If `--mode` is not provided, it will use the default mode from `.env`.
- If `--output` is not provided, output is printed to the console.
- You can easily add new processors by updating `core.py` and modifying the `get_processors()` function in `pipeline.py`.

## 📬 Contact

Feel free to reach out if you need help or have ideas to extend this engine further!
