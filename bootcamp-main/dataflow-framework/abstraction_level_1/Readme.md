## Author: KANAN  
## Level: 1 - Parameters and CLI Interface

## 📝 Overview

In this level, the script becomes a configurable command-line tool using the `typer` library and environment variables.

## 🚀 Features

- Accepts CLI arguments using `typer`
  - `--input`: required input file path
  - `--output`: optional output file path
  - `--mode`: optional mode (default from `.env`)
- Loads default mode from `.env` file using `python-dotenv`
- Supports two transformation modes:
  - `uppercase`: convert text to uppercase
  - `snakecase`: replace spaces with underscores and convert to lowercase

## 📄 File Structure

```
abstraction_level_1/
├── input.txt
├── .env
└── process.py
```

## ⚙️ Setup

Install dependencies:

```bash
pip install typer[all] python-dotenv
```

## 💡 Example Usage

```bash
# Using default mode from .env (uppercase)
python process.py --input input.txt

# Write output to a file
 python process.py --input input.txt --output result.txt

# Override mode to snakecase
python process.py --input input.txt --mode snakecase

# Write output to a file
python process.py --input input.txt --output result_snake.txt
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

## 📂 .env File

```
MODE=uppercase
```

## ✅ Checklist

- [x] CLI interface with `typer`
- [x] Defaults loaded from `.env`
- [x] Supports `uppercase` and `snakecase` modes
- [x] Can write to file or print to stdout
- [x] Logic is separated into clean functions
