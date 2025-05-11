## Author: KANAN  
## Level: 7 — Observability and System Introspection


This level adds **real-time observability** to the stream processing system, making it transparent, measurable, and understandable.

## Features

- **Metrics Collection**: Track lines in/out, processing time, and errors for each processor
- **Execution Tracing**: Follow the journey of each line through the processing pipeline
- **Web Dashboard**: Real-time visualization of system metrics and traces
- **Thread-Safe Design**: Concurrent access to metrics from processing and dashboard threads
- **Configurable Pipeline**: JSON-based configuration for processor setup

## Real-World Motivation

In production systems:
- **Data engineers** want to know how many records passed through each node
- **Operators** want to see what part of the system is slow or overloaded
- **Developers** want to debug flows by seeing how a record moved through the DAG
- **Teams** want dashboards to monitor uptime, alerts, and live status

Similar to tools like:
- Apache Spark's UI
- Airflow's DAG view
- Kubernetes dashboard
- Prometheus + Grafana

## Installation

```bash
# Install dependencies
pip install fastapi uvicorn
```

## File Structure

```
abstraction_level_7/
├── README.md
├── metrics/
│   ├── __init__.py
│   ├── metrics_store.py     # Centralized storage for metrics and traces
│   └── tracer.py            # Trace collection and management
├── processors/
│   ├── __init__.py
│   ├── base.py              # Observable processor base class
│   ├── simple.py            # Basic processors (filter, uppercase, etc.)
│   └── stateful.py          # Processors with state (counter, router)
├── pipeline/
│   ├── __init__.py
│   └── pipeline.py          # Main pipeline implementation
├── dashboard/
│   ├── __init__.py
│   └── server.py            # FastAPI web dashboard
├── config/
│   ├── __init__.py
│   └── config_loader.py     # JSON configuration handler
└── main.py                  # Entry point and CLI
```

## Core Features

### 1. Metrics Layer
- Count of lines received and emitted per processor
- Processing time per processor
- Number of exceptions or errors
- All metrics accessible via API endpoints

### 2. Execution Tracing
- Each line optionally carries a trace of its journey (e.g., `["start", "warn", "end"]`)
- Traces stored for a recent window (last 1000 lines)
- Optional `--trace` flag enables this feature

### 3. Web Dashboard
- Built using **FastAPI**
- Runs on a separate thread while processing continues
- Exposes endpoints:
  - `/stats`: Live processor metrics
  - `/trace`: Recent traces (top 100)
  - `/errors`: Processor-level error logs
- Simple JSON or HTML/JS interface

### 4. Concurrency Design
- Dashboard reads from shared memory structures
- Uses `threading` and locks for thread safety
- System remains responsive during processing

## Usage

### Process a file with tracing and dashboard

```bash
python main.py --file input.txt --output result.txt --trace --dashboard
```

### Use a custom configuration

```bash
python main.py --file input.txt --config pipeline_config.json --trace --dashboard
```

### Just run the dashboard (for demonstration)

```bash
python main.py --dashboard
```

## Dashboard

The web dashboard is available at [http://localhost:8000](http://localhost:8000) when enabled with the `--dashboard` flag.

The dashboard provides:

- **Processor Metrics** (`/stats`): Lines in/out, processing time, and error counts
- **Traces** (`/trace`): The path of lines through the system (when enabled with `--trace`)
- **Errors** (`/errors`): Recent errors with processor information

## Configuration

You can configure processors using a JSON file:

```json
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

## Example Scenario

Imagine processing a log file with different log levels (INFO, WARN, ERROR). With the observability system, you can:

1. See how many lines were tagged as `error`, `warn`, `info`
2. Measure how long it took to process them
3. Track which path each line took through the DAG
4. Identify which processor is slowest or throwing errors

You can visit `http://localhost:8000/stats` to immediately answer these questions.

## Architecture

### Core Components

- **MetricsStore**: Singleton for storing metrics and traces
- **ObservableProcessor**: Base class for processors that collect metrics
- **Dashboard**: FastAPI web server for monitoring
- **ObservablePipeline**: Chains processors together

### Metrics Collection

Each processor collects:

- Count of lines received
- Count of lines emitted
- Processing time
- Errors

### Tracing

When enabled with the `--trace` flag, the system tracks:

- The original line content
- Each processor the line passes through
- The status at each step (start, emit, drop, error)

### Thread Safety

All metrics and trace data are protected by locks to ensure thread safety when accessed concurrently by:

- The main processing thread
- The dashboard server thread

## Multi-Machine Considerations

In a distributed environment:

- Centralized metrics repository (like Prometheus or InfluxDB)
- Distributed tracing with correlation IDs
- Aggregation of metrics from multiple nodes
- Network latency compensation in measurements

## Production Improvements

For a production system:

- Historical metrics with time-series graphs
- Alerting capabilities for error conditions
- User authentication and role-based access
- Detailed resource utilization metrics (CPU, memory)
- Drill-down capabilities for specific traces or errors
- Export features for offline analysis
