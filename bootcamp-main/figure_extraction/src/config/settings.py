import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseSettings, Field

class APISettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    enable_docs: bool = True

class SecuritySettings(BaseSettings):
    auth_enabled: bool = True
    auth_method: str = "35aa77c01dd8293a8d9f563fdc9f58ea6409"  # "api_key" or "password"
    api_keys: List[str] = []
    token_expiration: int = 3600  # seconds

class StorageSettings(BaseSettings):
    storage_type: str = "duckdb"
    duckdb_path: str = "data/papers.duckdb"
    backup_enabled: bool = True
    backup_interval: int = 24  # hours

class ProcessingSettings(BaseSettings):
    extraction_workers: int = 2
    entity_detection_workers: int = 2
    batch_size: int = 10
    retry_limit: int = 3
    retry_delay: int = 5  # seconds

class WatchedFolderSettings(BaseSettings):
    watched_folders: List[str] = ["data/input"]
    watch_interval: int = 30  # seconds
    file_patterns: List[str] = ["*.txt", "*.csv"]

class ExternalAPISettings(BaseSettings):
    bioc_pmc_url: str = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi"
    bioc_pmc_rate_limit: int = 10  # requests per minute
    pubtator3_url: str = "https://www.ncbi.nlm.nih.gov/research/pubtator3/api/v1"
    pubtator3_rate_limit: int = 10  # requests per minute

class Settings(BaseSettings):
    app_name: str = "Scientific Paper Extractor"
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    temp_dir: str = "data/temp"
    
    api: APISettings = APISettings()
    security: SecuritySettings = SecuritySettings()
    storage: StorageSettings = StorageSettings()
    processing: ProcessingSettings = ProcessingSettings()
    watched_folder: WatchedFolderSettings = WatchedFolderSettings()
    external_api: ExternalAPISettings = ExternalAPISettings()
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

def get_settings() -> Settings:
    """Get application settings, with environment variable overrides."""
    return Settings()

# Create singleton instance
settings = get_settings()

def initialize_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        Path(settings.temp_dir),
        Path(settings.storage.duckdb_path).parent,
        *[Path(folder) for folder in settings.watched_folder.watched_folders]
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)