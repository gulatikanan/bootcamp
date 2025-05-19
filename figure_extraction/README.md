
# Scientific Publication Data Extraction System

A comprehensive system for extracting and managing data from scientific publications, focusing on figure captions and related entities.

---

## Overview

The Scientific Publication Data Extraction System is designed to extract, process, and provide access to valuable metadata from scientific publications. The system focuses on extracting titles, abstracts, figure captions, figure URLs, and identifying key entities (such as genes, diseases, etc.) mentioned in figure captions.

Initially targeting PubMed Central (PMC) publications, the system architecture is designed to be extensible to additional data sources in the future.

---

## Features

- Extract title, abstract, figure captions, and figure URLs from scientific publications  
- Identify key entities (genes, diseases, chemicals, etc.) mentioned in figure captions  
- Store extracted data in DuckDB for efficient querying  
- Provide REST API for programmatic data access  
- Command-line interface for data processing and management  
- Watched folder for automatic processing of files containing paper IDs  
- Docker deployment support for easy setup and scaling  
- Export capabilities in JSON and CSV formats  
- Comprehensive logging and error handling  
- Rate limiting for external API calls  

---

## Requirements

- Python 3.9 or higher  
- Windows 11 (or other OS with appropriate adjustments)  
- Docker (optional, for containerized deployment)  

---

## Installation

### Option 1: Local Setup

Clone the repository:

```bash
git clone https://github.com/your-org/scientific-publication-extraction.git
cd scientific-publication-extraction
```

2. Set up a virtual environment:

```shellscript
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Unix/Linux
```


3. Install dependencies:

```shellscript
pip install -r requirements.txt
```


4. Run the setup script:

```shellscript
python setup_windows.py
```


5. Create a `.env` file based on `.env.example` and adjust settings as needed.


### Option 2: Docker Setup

1. Clone the repository:

```shellscript
git clone https://github.com/your-org/scientific-publication-extraction.git
cd scientific-publication-extraction
```


2. Build and start the Docker containers:

```shellscript
docker-compose build
docker-compose up -d
```




## Usage

### Command Line Interface

The system provides a comprehensive command-line interface for data processing and management.

#### Process Papers

Process papers to extract figure captions and entities:

```shellscript
# Process a single paper
python -m src.cli.main process PMC6267067

# Process multiple papers
python -m src.cli.main process PMC6267067 PMC6267068

# Process papers from a file
python -m src.cli.main process --file papers.txt

# Process papers and wait for completion
python -m src.cli.main process PMC6267067 --wait
```

#### Export Data

Export extracted data in JSON or CSV format:

```shellscript
# Export papers to JSON
python -m src.cli.main export papers --format json --output papers.json

# Export figures to CSV
python -m src.cli.main export figures --format csv --output figures.csv

# Export entities to JSON
python -m src.cli.main export entities --format json --output entities.json
```

#### Configure System

Configure system settings:

```shellscript
# Show current configuration
python -m src.cli.main config show

# Update configuration
python -m src.cli.main config set api_port 8080

# Reset configuration to defaults
python -m src.cli.main config reset
```

#### Watch Folders

Watch folders for files containing paper IDs:

```shellscript
# Start watching folders
python -m src.cli.main watch

# Start watching specific folders
python -m src.cli.main watch --folders data/input1 data/input2
```

### REST API

The system provides a RESTful API for programmatic access to the extracted data.

#### Start the API Server

```shellscript
python -m src.cli.main serve
```

The API server will start on [http://localhost:8000](http://localhost:8000) by default.

#### API Endpoints

- **Authentication**

- `POST /api/v1/auth/token` - Get API token with credentials



- **Papers**

- `POST /api/v1/papers` - Submit paper IDs for processing
- `GET /api/v1/papers` - List all processed papers
- `GET /api/v1/papers/{paper_id}` - Get details for specific paper
- `GET /api/v1/papers/{paper_id}/figures` - Get figures for specific paper



- **Figures**

- `GET /api/v1/figures` - List all figures
- `GET /api/v1/figures/{figure_id}` - Get specific figure details
- `GET /api/v1/figures/{figure_id}/entities` - Get entities for specific figure



- **Entities**

- `GET /api/v1/entities` - List all entities
- `GET /api/v1/entities/{type}` - List entities of specific type



- **Jobs**

- `GET /api/v1/jobs` - List all jobs
- `GET /api/v1/jobs/{job_id}` - Get specific job status
- `POST /api/v1/jobs/{job_id}/cancel` - Cancel specific job



- **Export**

- `GET /api/v1/export/papers` - Export papers data (CSV/JSON)
- `GET /api/v1/export/figures` - Export figures data (CSV/JSON)
- `GET /api/v1/export/entities` - Export entities data (CSV/JSON)



- **Admin**

- `GET /api/v1/admin/config` - Get current configuration
- `PUT /api/v1/admin/config` - Update configuration
- `GET /api/v1/admin/stats` - Get system statistics





#### API Authentication

The API uses API key authentication. Include the API key in the `X-API-Key` header:

```shellscript
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/papers
```

### Watched Folder

The system can automatically process files placed in specified directories:

1. Place a text file containing paper IDs (one per line) in a watched folder (default: `data/input`).
2. The system will automatically detect the file and process the paper IDs.
3. Processing results will be available via the CLI or API.


## Expected Output

### Paper Data

```json
{
  "id": "PMC6267067",
  "title": "Example Paper Title",
  "abstract": "This is an example abstract...",
  "processed_date": "2023-05-19T14:30:45",
  "source": "PMC",
  "status": "completed",
  "error_message": null
}
```

### Figure Data

```json
{
  "id": "f1",
  "paper_id": "PMC6267067",
  "figure_number": 1,
  "caption": "Figure 1: Example figure caption describing the experiment...",
  "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6267067/figure/fig1/"
}
```

### Entity Data

```json
{
  "id": "e1",
  "figure_id": "f1",
  "entity_text": "TP53",
  "entity_type": "gene",
  "start_position": 42,
  "end_position": 46,
  "external_id": "7157"
}
```

## Docker Configuration

The system includes Docker and Docker Compose configurations for easy deployment.

### Docker Compose Services

- **app**: Main application container for CLI commands
- **api**: API server container
- **worker**: Worker container for background processing
- **redis**: Redis container for task queue


### Docker Compose Commands

```shellscript
# Build containers
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run CLI commands
docker-compose run app process PMC6267067

# Stop all services
docker-compose down
```

### Docker Environment Variables

Docker environment variables can be set in the `docker-compose.yml` file:

```yaml
environment:
  - LOG_LEVEL=INFO
  - API_HOST=0.0.0.0
  - API_PORT=8000
  - DUCKDB_PATH=/app/data/db/publications.duckdb
```

## Configuration

The system can be configured using environment variables or a `.env` file.

### Configuration Options

- **General Settings**

- `APP_NAME`: Application name
- `ENVIRONMENT`: Development, testing, or production
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `TEMP_DIR`: Directory for temporary files



- **API Settings**

- `API_HOST`: Host to bind API server
- `API_PORT`: Port to bind API server
- `API_WORKERS`: Number of worker processes
- `ENABLE_DOCS`: Enable/disable API documentation



- **Security Settings**

- `AUTH_ENABLED`: Enable/disable authentication
- `AUTH_METHOD`: "api_key" or "password"
- `API_KEYS`: List of valid API keys
- `TOKEN_EXPIRATION`: Token expiration time in seconds



- **Storage Settings**

- `STORAGE_TYPE`: "duckdb" (default, expandable)
- `DUCKDB_PATH`: Path to DuckDB file
- `BACKUP_ENABLED`: Enable/disable backups
- `BACKUP_INTERVAL`: Backup interval in hours



- **Processing Settings**

- `EXTRACTION_WORKERS`: Number of extraction workers
- `ENTITY_DETECTION_WORKERS`: Number of entity detection workers
- `BATCH_SIZE`: Number of papers to process in a batch
- `RETRY_LIMIT`: Number of retries for failed API calls
- `RETRY_DELAY`: Delay between retries in seconds



- **Watched Folder Settings**

- `WATCHED_FOLDERS`: List of folders to watch
- `WATCH_INTERVAL`: Interval to check folders in seconds
- `FILE_PATTERNS`: List of file patterns to process



- **External API Settings**

- `BIOC_PMC_URL`: URL for BioC-PMC API
- `BIOC_PMC_RATE_LIMIT`: Rate limit for BioC-PMC API
- `PUBTATOR3_URL`: URL for PubTator3 API
- `PUBTATOR3_RATE_LIMIT`: Rate limit for PubTator3 API





## Troubleshooting

### Common Issues

- **API Server Not Starting**

- Check if another process is using the port
- Verify all dependencies are installed
- Check configuration file for errors



- **Database Connection Error**

- Verify database file path
- Check file permissions
- Restore from backup if corrupted



- **Paper Processing Failures**

- Check external API status
- Adjust rate limiting settings
- Verify paper ID format
- Increase timeout settings



- **High Memory Usage**

- Adjust batch size
- Check for memory leaks
- Implement pagination for large responses



- **Slow API Response**

- Optimize database queries
- Scale resources
- Implement caching





### Logs

Check the logs for detailed error information:

```shellscript
# View application logs
cat logs/app.log

# View API server logs
cat logs/api.log

# View worker logs
cat logs/worker.log
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## License

This project is licensed under the MIT License - see the LICENSE file for details.
