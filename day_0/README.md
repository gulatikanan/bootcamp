
# kanan-hello 🌟

A beginner-friendly, well-structured Python package to greet the world—available both as a library and via the command line interface, built with **Typer** and **Rich** for a delightful developer experience.

---

## 🚀 Installation Guide

Install directly from TestPyPI:

```bash
pip install -i https://test.pypi.org/simple/ kanan-hello==0.3.0
```

---

## 🌍 About the Project

`kanan-hello` is a compact Python module crafted to demonstrate:

* Adherence to clean coding practices
* How to build and use a Python package
* A visually engaging command-line interface
* Python publishing workflow via TestPyPI
* Virtual environment & dependency handling with `uv`

---

## ✨ Key Highlights

* 🔹 Simple `say_hello()` function for greetings
* 🔹 Enhanced terminal output using **rich**
* 🔹 Fully interactive CLI built with **typer**
* 🔹 Uses Python typing for better code clarity
* 🔹 Modular project structure
* 🔹 Easy TestPyPI installation

---

## 🗃️ Directory Layout

```
day_0/
├── kanan_hello/
│   ├── __init__.py        # Exposes public functions
│   ├── main.py            # Core logic and greeting logic
│   └── cli.py             # Command-line interface (Typer)
├── pyproject.toml         # Build configuration
├── README.md              # Project overview
└── dist/                  # Generated package files
```

---

## 📚 How to Use as a Library

```python
from kanan_hello import say_hello, print_rich_hello

print(say_hello())            # Output: Hello, World!
print(say_hello("Charlie"))   # Output: Hello, Charlie!

print_rich_hello("Daisy")     # Output with rich formatting
```

---

## 💻 Running via CLI

Once installed, try the following commands:

```bash
kanan-hello --help                  # See CLI options
kanan-hello hello                   # Fancy greeting to the world
kanan-hello hello Priya            # Personalized rich greeting
kanan-hello simple                 # Basic hello message
kanan-hello simple Aarav           # Basic personalized message
```

---

## 🔧 Commands Used in Setup

### 🧱 Project Initialization

```bash
pip install uv
uv init
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 📁 Module Setup

```bash
mkdir kanan_hello
touch kanan_hello/__init__.py
touch kanan_hello/main.py
touch kanan_hello/cli.py
touch pyproject.toml
touch README.md
```

### 🧪 Installing Dependencies

```bash
uv pip install rich typer
uv pip install build twine
```

### 📦 Packaging and Uploading

```bash
python -m build
python -m twine upload --repository testpypi dist/*
```

---

## 🎬 Demo Video

👉 Showcasing the CLI in action:
**\[Insert your Asciinema recording link here]**

---

## 👤 Author Info

**KANAN GULATI**
📧 [kanangulati7@gmail.com](mailto:kanangulati7@gmail.com)
🐙 GitHub: [github.com/gulatikanan](https://github.com/gulatikanan)
💼 LinkedIn: [linkedin.com/in/kanangulati](https://linkedin.com/in/kanangulati)

📅 *Last Updated: May 6, 2025*

---

## 📄 License

Distributed under the **MIT License**. For details, refer to the `LICENSE` file.

---

## 🧠 Pro Tips for Clean Python Code

* ✅ Annotate all functions with types
* ✅ Add docstrings for every public function
* ✅ Use linters like `ruff`, `flake8`, or `pylint`
* ✅ Integrate `mypy` for type checks
* ✅ For VS Code users:

  * Enable **Pylance**
  * Set Python type checking to **strict**

---

## 🤝 Contributions Welcome!

Pull requests are encouraged. Feel free to fork the repo, suggest changes, or improve features. Let’s build meaningful CLI tools together. 💫

---


