# Installation

This guide covers how to install the `kanan-hello` package and its dependencies.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installing from TestPyPI

The package is currently available on TestPyPI. You can install it using pip:

```
pip install -i https://test.pypi.org/simple/ kanan-hello==0.3.0
``` 

## Verifying Installation

After installation, you can verify that the package is installed correctly by running:

```
kanan-hello --help
```

You should see output similar to:

```
Usage: kanan-hello [OPTIONS] COMMAND [ARGS]...

  A simple CLI application that says hello.

Options:
  --help  Show this message and exit.

Commands:
  hello   Prints a rich formatted greeting message.
  simple  Prints a simple greeting message without rich formatting.
```

## Dependencies

The package automatically installs the following dependencies:

- **rich**: For formatted console output
- **typer**: For command-line interface

## Development Installation

If you want to contribute to the package or modify it for your own use, you can install it in development mode:

1. Clone the repository:
   ```
   git clone https://github.com/gulatikanan/bootcamp.git
   cd day_0/kanan-hello
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```
   pip install -e .
   ```

## Troubleshooting

### Package Not Found

If you encounter a "Package not found" error, make sure you're using the TestPyPI URL:

```
pip install -i https://test.pypi.org/simple/ kanan-hello==0.3.0
```

### Command Not Found

If the `kanan-hello` command is not found after installation, check that your Python scripts directory is in your PATH. You may need to restart your terminal or command prompt.

### Dependency Conflicts

If you encounter dependency conflicts, you can try installing in an isolated environment:

```
python -m venv fresh-env
source fresh-env/bin/activate  # On Windows: fresh-env\Scripts\activate
pip install -i https://test.pypi.org/simple/ kanan-hello==0.3.0
```