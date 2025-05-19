## Author: Kanan
## Level: 8 - Automated Folder Monitor and Recovery

This system implements a robust, self-running, fault-tolerant file processing tool that continuously monitors folders for new files, processes them through a configurable pipeline, and automatically recovers from failures.

## Motivation

Modern data processing systems need to handle files that arrive at unpredictable times:
- Log files from various applications
- Transaction batches from business systems
- User uploads and data submissions

This system addresses these needs with a **persistent, observable, recoverable processing loop** that runs autonomously and maintains processing state even through crashes or restarts.

## Features

- **Continuous Folder Monitoring**: Automatically detects and processes new files
- **Configurable Processing Pipeline**: Apply multiple transformations to your data
- **Fault Tolerance & Recovery**: Resumes interrupted work after crashes
- **Real-time Web Dashboard**: Monitor system status, metrics, and file processing
- **Observability**: Comprehensive metrics and traces for debugging
- **Thread Safety**: Properly handles concurrent operations

## Installation

```
# Clone the repository
git clone https://github.com/gulatikanan/bootcamp.git
cd AganithaBootcamp/day_4/abstraction_level_8

# Install dependencies
pip install fastapi uvicorn
```

## Folder Structure

The system uses a folder-based queue with the following structure:

```
watch_dir/
├── unprocessed/     # incoming files to watch 
├── underprocess/    # in-progress files
├── processed/       # completed successfully
```

## Usage

### Monitor a folder for files

```
python main.py --monitor ./watch_dir --trace --dashboard
```

### Monitor with custom output directory

```
python main.py --monitor ./watch_dir --output-dir ./results --trace --dashboard
```

### Use a custom configuration

```
python main.py --monitor ./watch_dir --config pipeline_config.json --trace --dashboard
```

### Process a single file (still supported)

```
python main.py --file input.txt --output result.txt --trace --dashboard
```

## File Lifecycle

1. Files are placed in the `unprocessed/` directory
2. The system moves them to `underprocess/` while processing
3. After successful processing, files are moved to `processed/`
4. If the system crashes during processing, files in `underprocess/` are moved back to `unprocessed/` on restart

## Architecture

### Core Components

- **FolderMonitor**: Watches for new files and manages the processing lifecycle
- **MetricsStore**: Singleton for storing metrics, traces, and file statistics
- **ObservableProcessor**: Base class for processors that collect metrics
- **Dashboard**: FastAPI web server for monitoring
- **ObservablePipeline**: Chains processors together

### Project Structure

```
level_8_automated_folder_monitor_and_recovery/
├── README.md
├── metrics/
│   ├── __init__.py
│   ├── metrics_store.py       # Metrics collection and storage
│   └── tracer.py              # Tracing functionality
├── processors/
│   ├── __init__.py
│   ├── base.py                # Base processor classes
│   ├── simple.py              # Simple processors (uppercase, filter, etc.)
│   └── stateful.py            # Stateful processors (counter, aggregator)
├── pipeline/
│   ├── __init__.py
│   └── pipeline.py            # Pipeline implementation
├── dashboard/
│   ├── __init__.py
│   └── server.py              # Web dashboard
├── config/
│   ├── __init__.py
│   └── config_loader.py       # Configuration handling
├── folder_monitor/
│   ├── __init__.py
│   └── file_processor.py      # Folder monitoring implementation
└── main.py                    # Entry point
```

### Recovery Mechanism

The system implements a robust recovery mechanism:

1. On startup, it checks for any files in the `underprocess/` directory
2. These files are moved back to `unprocessed/` for reprocessing
3. This ensures that no files are lost if the system crashes during processing

## Dashboard

The web dashboard is available at [http://localhost:8000](http://localhost:8000) when enabled with the `--dashboard` flag.

The dashboard includes:

- **File Processing Status**:
  - Number of files in each directory
  - Currently processing file
  - Recently processed files with timestamps
- **Processor Metrics**: Lines in/out, processing time, and error counts
- **Traces**: The path of lines through the system (when enabled with `--trace`)
- **Errors**: Recent errors with processor information

## Configuration

You can configure processors using a JSON file:

```
{
  "processors": [
    {
      "type": "line_counter",
      "id": "counter",
      "format": "Line {count}: {line}"
    },
    {
      "type": "uppercase",
      "id": "uppercase"
    },
    {
      "type": "filter",
      "id": "important_filter",
      "pattern": "important"
    }
  ]
}
```
## ✅ Checklist

* [x] Continuously monitors `unprocessed/`
* [x] Safely moves files through lifecycle (`underprocess/`, `processed/`)
* [x] Retries failed or interrupted files
* [x] Real-time dashboard reflects system state
* [x] System runs indefinitely, non-blocking
* [x] Configurable line processors
* [x] Supports trace + metrics
* [x] Fully fault-tolerant

## Design Considerations

- **Thread Safety**: All shared data is protected by locks to ensure thread safety
- **Non-Blocking**: The processing loop doesn't block the main thread
- **Idempotency**: The system assumes reprocessing files is harmless
- **Atomic File Operations**: Uses `shutil.move()` for safe file transitions

## Reflection

### Concurrent Instances

If two instances of this system run at once:
- They might try to process the same files
- This could lead to race conditions and duplicate processing
- Solutions include:
  - File locking mechanisms
  - A distributed lock manager
  - Assigning different files to different instances based on naming patterns

### Parallelization

To parallelize processing across threads or nodes:
- We could use a thread pool to process multiple files concurrently
- Each thread would need its own set of processors to avoid state conflicts
- A work queue could distribute files to worker threads/nodes
- Each worker would need its own `underprocess` directory

### Partial Files

If a file is only partially written when picked up:
- The system might process incomplete data
- Solutions include:
  - Using file locks during writing
  - Implementing a "ready" flag (e.g., a companion .ready file)
  - Checking file modification time and only processing files that haven't been modified for a certain period
  - Using atomic file operations (write to temp file, then rename)

## Next Steps

Future improvements could include:
- Implementing more sophisticated error handling and retry mechanisms
- Adding support for different file formats and schemas
- Implementing a more advanced routing system
- Adding support for distributed processing across multiple machines