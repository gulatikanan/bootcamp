# CLI Commands

The `kanan-hello` package provides a command-line interface (CLI) with several commands. This page documents all available commands and their options.

## Getting Help

To see all available commands and options, run:

```
kanan-hello --help
```

Output:
```
Usage: kanan-hello [OPTIONS] COMMAND [ARGS]...

  A simple CLI application that says hello.

Options:
  --help  Show this message and exit.

Commands:
  hello   Prints a rich formatted greeting message.
  simple  Prints a simple greeting message without rich formatting.
```

## hello Command

The `hello` command prints a rich formatted greeting message.

### Usage

```
kanan-hello hello [NAME]
```

### Arguments

- `NAME`: Optional. The name to greet. If not provided, it will greet "World".

### Examples

```
# Greet the world with rich formatting
kanan-hello hello

# Greet a specific person with rich formatting
kanan-hello hello kanan
```

### Output

The command produces a beautifully formatted panel with the greeting message:

```
┌────────────────┐
│  Greeting      │
├────────────────┤
│ Hello, kanan! │
└────────────────┘
```

## simple Command

The `simple` command prints a simple greeting message without rich formatting.

### Usage

```
kanan-hello simple [NAME]
```

### Arguments

- `NAME`: Optional. The name to greet. If not provided, it will greet "World".

### Examples

```
# Greet the world with simple text
kanan-hello simple

# Greet a specific person with simple text
kanan-hello simple kanan
```

### Output

The command produces a simple text output:

```
Hello, kanan!
```

## Command Comparison

| Command | Formatting | Output |
|---------|------------|--------|
| `hello` | Rich       | Formatted panel with colors and borders |
| `simple` | Plain      | Simple text without formatting |

## Exit Codes

All commands return the following exit codes:

| Exit Code | Meaning |
|-----------|---------|
| 0         | Success |
| 1         | Error   |

## Environment Variables

The CLI does not currently use any environment variables.

## Future Commands

In future versions, we plan to add the following commands:

- `config`: Configure default settings
- `version`: Display version information
- `interactive`: Start an interactive greeting session