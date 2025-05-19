import os
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Type, TypeVar

import duckdb
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

from src.config.settings import settings
from src.storage.models import Paper, Figure, Entity, Job, ProcessingStatus, JobType, EntityType

# Set up logging
logger = logging.getLogger(__name__)

# Create SQLAlchemy Base
Base = declarative_base()

# Define SQLAlchemy models
class PaperModel(Base):
    __tablename__ = "papers"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=False)
    processed_date = Column(DateTime, default=datetime.now)
    source = Column(String, default="PMC")
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    error_message = Column(Text, nullable=True)
    
    figures = relationship("FigureModel", back_populates="paper", cascade="all, delete-orphan")

class FigureModel(Base):
    __tablename__ = "figures"
    
    id = Column(String, primary_key=True)
    paper_id = Column(String, ForeignKey("papers.id"), nullable=False)
    figure_number = Column(Integer, nullable=False)
    caption = Column(Text, nullable=False)
    url = Column(String, nullable=True)
    
    paper = relationship("PaperModel", back_populates="figures")
    entities = relationship("EntityModel", back_populates="figure", cascade="all, delete-orphan")

class EntityModel(Base):
    __tablename__ = "entities"
    
    id = Column(String, primary_key=True)
    figure_id = Column(String, ForeignKey("figures.id"), nullable=False)
    entity_text = Column(String, nullable=False)
    entity_type = Column(Enum(EntityType), nullable=False)
    start_position = Column(Integer, nullable=False)
    end_position = Column(Integer, nullable=False)
    external_id = Column(String, nullable=True)
    
    figure = relationship("FigureModel", back_populates="entities")

class JobModel(Base):
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True)
    job_type = Column(Enum(JobType), nullable=False)
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    paper_ids = Column(Text, nullable=False)  # Stored as JSON
    total_papers = Column(Integer, nullable=False)
    processed_papers = Column(Integer, default=0)
    failed_papers = Column(Integer, default=0)

class Database:
    def __init__(self):
        self.db_path = settings.storage.duckdb_path
        self._ensure_db_directory()
        self.engine = create_engine(f"duckdb:///{self.db_path}")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def initialize(self):
        """Initialize the database schema."""
        Base.metadata.create_all(self.engine)
        logger.info(f"Database initialized at {self.db_path}")
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    def backup(self):
        """Create a backup of the database."""
        if not settings.storage.backup_enabled:
            return
        
        backup_dir = Path(self.db_path).parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"papers_{timestamp}.duckdb"
        
        # Use DuckDB's built-in backup functionality
        conn = duckdb.connect(self.db_path)
        conn.execute(f"EXPORT DATABASE '{backup_path}'")
        conn.close()
        
        logger.info(f"Database backed up to {backup_path}")

# Create singleton instance
db = Database()

def get_db():
    """Get database instance."""
    return db