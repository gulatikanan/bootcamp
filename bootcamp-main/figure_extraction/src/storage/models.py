from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobType(str, Enum):
    EXTRACTION = "extraction"
    ENTITY_DETECTION = "entity_detection"
    EXPORT = "export"

class Paper(BaseModel):
    id: str
    title: str
    abstract: str
    processed_date: datetime = Field(default_factory=datetime.now)
    source: str = "PMC"
    status: ProcessingStatus = ProcessingStatus.PENDING
    error_message: Optional[str] = None

class Figure(BaseModel):
    id: str
    paper_id: str
    figure_number: int
    caption: str
    url: Optional[str] = None

class EntityType(str, Enum):
    GENE = "gene"
    DISEASE = "disease"
    CHEMICAL = "chemical"
    SPECIES = "species"
    MUTATION = "mutation"
    CELL_LINE = "cell_line"

class Entity(BaseModel):
    id: str
    figure_id: str
    entity_text: str
    entity_type: EntityType
    start_position: int
    end_position: int
    external_id: Optional[str] = None

class Job(BaseModel):
    id: str
    job_type: JobType
    status: ProcessingStatus = ProcessingStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    paper_ids: List[str]
    total_papers: int
    processed_papers: int = 0
    failed_papers: int = 0