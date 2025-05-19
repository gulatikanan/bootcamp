# Contributing to kanan-hello

Thank you for considering contributing to kanan-hello! This document outlines the process for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Any relevant logs or screenshots
- Your environment (Python version, OS, etc.)

### Suggesting Enhancements

If you have an idea for an enhancement, please create an issue on GitHub with the following information:

- A clear, descriptive title
- A detailed description of the proposed enhancement
- Any relevant examples or mockups
- Why this enhancement would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes
4. Add or update tests as necessary
5. Update documentation as necessary
6. Submit a pull request

## Development Setup

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

4. Install development dependencies:
   ```
   pip install pytest black isort mypy
   ```

## Coding Standards

- Use type annotations for all functions and methods
- Follow PEP 8 style guidelines
- Write docstrings for all public functions, methods, and classes
- Keep functions short and focused
- Use meaningful variable and function names
- Add tests for new functionality

## Testing

Run tests with pytest:


```
pytest
```

## Documentation

Update documentation as necessary:

1. Update docstrings in the code
2. Update the README.md file
3. Update or add documentation in the docs/ directory

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in the present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable

## Review Process

1. All pull requests will be reviewed by a maintainer
2. Feedback may be provided for changes or improvements
3. Once approved, the pull request will be merged

## Thank You!

Your contributions are greatly appreciated. Thank you for helping to improve kanan-hello!