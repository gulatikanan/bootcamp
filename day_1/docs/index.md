# kanan-hello

![PyPI Version](https://img.shields.io/badge/pypi-v0.3.0-blue)
![Python Versions](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

Welcome to the documentation for `kanan-hello`, a comprehensive Python package that demonstrates clean code principles through a simple "Hello World" application with rich formatting and a command-line interface.

## Overview

This package serves as a practical example of Python best practices, including:

- Type annotations
- Rich console output
- Command-line interface development
- Modern package configuration
- Comprehensive documentation

---

## Quick Start

Install the package from TestPyPI:

From [TestPyPI](https://test.pypi.org/project/kanan-hello/0.3.0/):

```bash
pip install -i https://test.pypi.org/simple/ kanan-hello==0.3.0
````


Use as a library:

```python
from kanan_hello import say_hello, print_rich_hello

# Simple greeting
result = say_hello("kanan")
print(result)  # Output: Hello, kanan!

# Rich formatted greeting
print_rich_hello("kanan")  # Displays a fancy greeting panel
```

Use as a command-line tool:

```bash

# Rich formatted greeting

kanan-hello hello kanan

# Simple greeting

kanan-hello simple kanan
```
## Documentation Structure

This documentation is organized into the following sections:

- **User Guide**: Instructions for installing and using the package
- **Developer Guide**: Technical details about the package architecture and design
- **Reference**: API documentation and other reference materials
- **About**: Project information, changelog, and contribution guidelines

## Features

- ✅ Simple and intuitive API for greeting messages
- ✅ Rich text formatting for beautiful console output
- ✅ Command-line interface with multiple commands
- ✅ Type annotations for better IDE support and code quality
- ✅ Comprehensive documentation and examples
- ✅ Follows clean code principles and best practices

## Author

**kanan**

- Email: kanan@example.com
- GitHub: [github.com/kanan](https://github.com/gulatikanan)
- LinkedIn: [linkedin.com/in/kanan](https://linkedin.com/in/kanangulati)

---

<p align="center">
  <i>Last updated: May 6, 2025</i>
</p>