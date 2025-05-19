
## Author: KANAN  
## Level: 7 — Real-Time File Processing System

## Features

- **Modular Processing Engine**: Extensible pipeline for file processing
- **Stream-based Pipeline**: Process files as streams for efficiency
- **Tag-based Router**: Route files to different processors based on content
- **Web Dashboard**: Monitor system health and processing statistics
- **Folder Monitoring**: Automatically detect and process new files
- **Self-healing**: Recover from failures and continue processing
- **Dual Execution Modes**: Process a single file or watch a directory
- **Docker Support**: Run the system in a containerized environment
- **Comprehensive Metrics**: Track processing times, success rates, and more

## Quick Start

### Prerequisites

- Python 3.13
- Docker (optional)
- Make (optional, for Makefile usage)

### Installation

#### Local Installation

1. Clone the repository:

```bash
git clone https://github.com/gulatikanan/bootcamp.git
cd AGANITHA_BOOTCAMP
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create required directories:

```bash
mkdir -p watch_dir/unprocessed watch_dir/processed watch_dir/underprocess results
```

#### Docker Installation

Build and run using Docker:

```bash
# Build the image
docker build -t file-processor:latest .

# Run the container
docker run -p 8000:8000 -v $(pwd)/watch_dir:/app/watch_dir -v $(pwd)/results:/app/results file-processor:latest
```

On Windows (PowerShell):

```powershell
docker run -p 8000:8000 -v ${PWD}/watch_dir:/app/watch_dir -v ${PWD}/results:/app/results file-processor:latest
```

Or use Docker Compose:

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

## Usage

### Running the System

The system supports two operation modes:

#### 1. Watch Mode (Continuous)

Continuously monitors the `watch_dir/unprocessed/` directory for new files:

```bash
# Using Makefile
make run

# Using run.sh
./run.sh run

# Using Python directly
python main.py --watch
```

#### 2. Single File Mode (One-shot)

Processes a single file and exits:

```bash
# Using Makefile
make run-file FILE=path/to/file.txt

# Using run.sh
./run.sh run-file path/to/file.txt

# Using Python directly
python main.py --input path/to/file.txt
```

### Command Line Options

```
--watch                 Run in watch mode (monitor directory)
--input PATH            Process a single file at PATH
--config PATH           Path to configuration file (default: log_processor_config.json)
--debug                 Enable debug logging
--trace                 Enable trace logging (more verbose than debug)
```

### Common Operations

Use the Makefile or run.sh for common tasks:

```bash
# Show help
make help
./run.sh help

# Clean up processed files and logs
make clean
./run.sh clean

# Build Docker image
make build-docker
./run.sh build-docker

# Run in Docker container
make run-docker
./run.sh run-docker

# Build Python package
make build-package
./run.sh build-package

# Publish package to PyPI 
make publish-package
./run.sh publish-package
```

## File Upload Methods

Files can be uploaded to the system in several ways:

### 1. Direct File Drop

Place files directly in the monitored directory:

```bash
cp your_file.txt watch_dir/unprocessed/
```

### 2. FastAPI Upload Endpoint

Upload via HTTP:

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_file.txt"
```

### 3. Web Dashboard

Access the web dashboard at [http://localhost:8000](http://localhost:8000) and use the file upload interface.

### 4. Remote Sync (rsync)

Sync files from a remote system:

```bash
rsync -avz /path/to/source/files/ user@server:/path/to/watch_dir/unprocessed/
```

### 5. Sample Data Generation

Generate test files using the included utility:

```bash
python generate_sample_logs.py --count 5 --output watch_dir/unprocessed/
```

## API Endpoints

The system provides a REST API through the FastAPI dashboard server:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health status and metrics |
| `/stats` | GET | Processing statistics |
| `/files` | GET | List of processed files with status |
| `/upload` | POST | Upload a file for processing |

Example request to check system health:

```bash
curl -X GET "http://localhost:8000/health"
```

## Monitoring

### Local Monitoring

Access the dashboard at [http://localhost:8000](http://localhost:8000) to view system status, metrics, and processed files.

### Remote Monitoring

The system can be monitored using Better Uptime:

1. Create an account at [Better Uptime](https://betteruptime.com/)
2. Add a new monitor pointing to your system's `/health` endpoint
3. Configure alerts for downtime notifications

## Project Structure

```
final_wrapup/
├── config/                     # Configuration management
├── dashboard/                  # Web dashboard (FastAPI)
├── folder_monitor/             # Directory monitoring
├── metrics/                    # Metrics collection
├── pipeline/                   # Processing pipeline
├── processors/                 # File processors
├── results/                    # Output directory
├── watch_dir/                  # Directory structure for file monitoring
│   ├── processed/              # Successfully processed files
│   ├── underprocess/           # Files currently being processed
│   └── unprocessed/            # New files waiting to be processed
├── Dockerfile                  # Docker configuration
├── FINAL.md                    # Project reflection
├── Makefile                    # Commands for operations
├── README.md                   # This file
├── generate_sample_logs.py     # Utility script
├── log_processor_config.json   # Main configuration
├── main.py                     # Entry point
├── pipeline_config.json        # Pipeline configuration
├── requirements.txt            # Dependencies
├── run.sh                      # Shell script alternative
└── setup.py                    # Package setup
```

## Configuration

The system is configured via two main JSON files:

### Main Configuration (log_processor_config.json)

```json
{
  "watch_dir": "watch_dir",
  "processors": ["simple", "stateful"],
  "dashboard": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "recovery": {
    "enabled": true,
    "check_interval": 60
  }
}
```

### Pipeline Configuration (pipeline_config.json)

```json
{
  "pipeline": {
    "steps": [
      {
        "name": "parse",
        "processor": "simple"
      },
      {
        "name": "analyze",
        "processor": "stateful"
      }
    ]
  }
}
```

## Development

### Adding New Processors

1. Create a new processor class in the `processors/` directory:

```python
# processors/my_processor.py
from processors.base import BaseProcessor

class MyProcessor(BaseProcessor):
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "my_processor"
        
    def process(self, content, metadata=None):
        # Process the content
        processed_content = content.upper()
        return processed_content, metadata
```

2. Update the configuration to use your processor:

```json
{
  "processors": ["simple", "stateful", "my_processor"]
}
```

### Extending the Pipeline

Modify the pipeline_config.json file to add new steps:

```json
{
  "pipeline": {
    "steps": [
      {
        "name": "parse",
        "processor": "simple"
      },
      {
        "name": "analyze",
        "processor": "stateful"
      },
      {
        "name": "transform",
        "processor": "my_processor"
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues

#### Files Not Being Processed

- Check file permissions
- Verify correct directory placement
- Run with `--debug` flag to see more information
- Ensure watch mode is active

#### Dashboard Not Accessible

- Verify server is running
- Check port availability
- Ensure network access to port 8000
- Check logs for binding errors

#### Docker Issues

- Confirm Docker is running
- Check volume mounts
- Verify port mapping
- Check container logs

### Recovery Process

The system automatically recovers interrupted processing:

1. Files being processed during a crash are preserved in `watch_dir/underprocess/`
2. Upon restart, the system checks this directory and resumes processing
3. To manually trigger recovery: `python main.py --watch`

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for your changes
5. Run tests: `pytest`
6. Commit your changes: `git commit -am 'Add my feature'`
7. Push to the branch: `git push origin feature/my-feature`
8. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was developed as part of a multi-level learning exercise
- Thanks to all contributors and testers
- Special thanks to the open-source community for libraries used in this project
