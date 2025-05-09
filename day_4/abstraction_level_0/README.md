# Abstraction Level 0 – Basic Script

## 📝 Overview

This is the foundational step of the project. At this level, the goal is to create a simple, one-off Python script that:

- Reads lines from `stdin`
- Strips leading and trailing whitespace
- Converts each line to uppercase
- Prints the result to `stdout`

No functions or advanced features — just a straightforward script.

## 📄 File Structure

```
abstraction-level-0/
├── input.txt
└── process.py
```

## 🚀 How to Run

Make sure you are in the `abstraction-level-0` folder, then run the following command in your terminal:

```bash
cat input.txt | python process.py
```

## 💡 Example

**input.txt**
```
 i love python  
```

**Command:**
```bash
cat input.txt | python process.py
```

**Output:**
```
I lOVE PYTHON
```

## ✅ Checklist

- [x] Produces the expected output for a sample file
- [x] Runs without errors from the command line
- [x] Sequential, top-to-bottom script (no functions)