import json
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Type, TypeVar

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_

from src.storage.database import db, PaperModel, FigureModel, EntityModel, JobModel
from src.storage.models import Paper, Figure, Entity, Job, ProcessingStatus, JobType, EntityType

# Set up logging
logger = logging.getLogger(__name__)

# Generic type for Pydantic models
T = TypeVar('T', Paper, Figure, Entity, Job)

def create_paper(paper: Paper, session: Optional[Session] = None) -> Paper:
    """Create a new paper record."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        paper_model = PaperModel(
            id=paper.id,
            title=paper.title,
            abstract=paper.abstract,
            processed_date=paper.processed_date,
            source=paper.source,
            status=paper.status,
            error_message=paper.error_message
        )
        
        session.add(paper_model)
        session.commit()
        session.refresh(paper_model)
        
        return Paper.parse_obj(paper_model.__dict__)
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating paper: {e}")
        raise
    finally:
        if close_session:
            session.close()

def get_paper(paper_id: str, session: Optional[Session] = None) -> Optional[Paper]:
    """Get a paper by ID."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        paper_model = session.query(PaperModel).filter(PaperModel.id == paper_id).first()
        
        if paper_model is None:
            return None
        
        return Paper.parse_obj(paper_model.__dict__)
    finally:
        if close_session:
            session.close()

def list_papers(
    limit: int = 100, 
    offset: int = 0, 
    status: Optional[ProcessingStatus] = None,
    session: Optional[Session] = None
) -> List[Paper]:
    """List papers with optional filtering."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        query = session.query(PaperModel)
        
        if status is not None:
            query = query.filter(PaperModel.status == status)
        
        paper_models = query.limit(limit).offset(offset).all()
        
        return [Paper.parse_obj(model.__dict__) for model in paper_models]
    finally:
        if close_session:
            session.close()

def update_paper_status(
    paper_id: str, 
    status: ProcessingStatus, 
    error_message: Optional[str] = None,
    session: Optional[Session] = None
) -> Optional[Paper]:
    """Update a paper's status."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        paper_model = session.query(PaperModel).filter(PaperModel.id == paper_id).first()
        
        if paper_model is None:
            return None
        
        paper_model.status = status
        if error_message is not None:
            paper_model.error_message = error_message
        
        session.commit()
        session.refresh(paper_model)
        
        return Paper.parse_obj(paper_model.__dict__)
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating paper status: {e}")
        raise
    finally:
        if close_session:
            session.close()

def create_figure(figure: Figure, session: Optional[Session] = None) -> Figure:
    """Create a new figure record."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        figure_model = FigureModel(
            id=figure.id,
            paper_id=figure.paper_id,
            figure_number=figure.figure_number,
            caption=figure.caption,
            url=figure.url
        )
        
        session.add(figure_model)
        session.commit()
        session.refresh(figure_model)
        
        return Figure.parse_obj(figure_model.__dict__)
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating figure: {e}")
        raise
    finally:
        if close_session:
            session.close()

def get_figures_for_paper(paper_id: str, session: Optional[Session] = None) -> List[Figure]:
    """Get all figures for a paper."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        figure_models = session.query(FigureModel).filter(FigureModel.paper_id == paper_id).all()
        
        return [Figure.parse_obj(model.__dict__) for model in figure_models]
    finally:
        if close_session:
            session.close()

def create_entity(entity: Entity, session: Optional[Session] = None) -> Entity:
    """Create a new entity record."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        entity_model = EntityModel(
            id=entity.id,
            figure_id=entity.figure_id,
            entity_text=entity.entity_text,
            entity_type=entity.entity_type,
            start_position=entity.start_position,
            end_position=entity.end_position,
            external_id=entity.external_id
        )
        
        session.add(entity_model)
        session.commit()
        session.refresh(entity_model)
        
        return Entity.parse_obj(entity_model.__dict__)
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating entity: {e}")
        raise
    finally:
        if close_session:
            session.close()

def get_entities_for_figure(figure_id: str, session: Optional[Session] = None) -> List[Entity]:
    """Get all entities for a figure."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        entity_models = session.query(EntityModel).filter(EntityModel.figure_id == figure_id).all()
        
        return [Entity.parse_obj(model.__dict__) for model in entity_models]
    finally:
        if close_session:
            session.close()

def create_job(job: Job, session: Optional[Session] = None) -> Job:
    """Create a new job record."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        job_model = JobModel(
            id=job.id,
            job_type=job.job_type,
            status=job.status,
            created_at=job.created_at,
            completed_at=job.completed_at,
            paper_ids=json.dumps(job.paper_ids),
            total_papers=job.total_papers,
            processed_papers=job.processed_papers,
            failed_papers=job.failed_papers
        )
        
        session.add(job_model)
        session.commit()
        session.refresh(job_model)
        
        # Convert paper_ids back from JSON
        job_dict = job_model.__dict__
        job_dict['paper_ids'] = json.loads(job_dict['paper_ids'])
        
        return Job.parse_obj(job_dict)
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating job: {e}")
        raise
    finally:
        if close_session:
            session.close()

def get_job(job_id: str, session: Optional[Session] = None) -> Optional[Job]:
    """Get a job by ID."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        job_model = session.query(JobModel).filter(JobModel.id == job_id).first()
        
        if job_model is None:
            return None
        
        # Convert paper_ids from JSON
        job_dict = job_model.__dict__
        job_dict['paper_ids'] = json.loads(job_dict['paper_ids'])
        
        return Job.parse_obj(job_dict)
    finally:
        if close_session:
            session.close()

def update_job_status(
    job_id: str, 
    status: ProcessingStatus, 
    processed_papers: Optional[int] = None,
    failed_papers: Optional[int] = None,
    completed_at: Optional[datetime] = None,
    session: Optional[Session] = None
) -> Optional[Job]:
    """Update a job's status."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        job_model = session.query(JobModel).filter(JobModel.id == job_id).first()
        
        if job_model is None:
            return None
        
        job_model.status = status
        
        if processed_papers is not None:
            job_model.processed_papers = processed_papers
        
        if failed_papers is not None:
            job_model.failed_papers = failed_papers
        
        if completed_at is not None:
            job_model.completed_at = completed_at
        elif status == ProcessingStatus.COMPLETED or status == ProcessingStatus.FAILED:
            job_model.completed_at = datetime.now()
        
        session.commit()
        session.refresh(job_model)
        
        # Convert paper_ids from JSON
        job_dict = job_model.__dict__
        job_dict['paper_ids'] = json.loads(job_dict['paper_ids'])
        
        return Job.parse_obj(job_dict)
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating job status: {e}")
        raise
    finally:
        if close_session:
            session.close()

def list_jobs(
    limit: int = 100, 
    offset: int = 0, 
    status: Optional[ProcessingStatus] = None,
    job_type: Optional[JobType] = None,
    session: Optional[Session] = None
) -> List[Job]:
    """List jobs with optional filtering."""
    close_session = False
    if session is None:
        session = db.get_session()
        close_session = True
    
    try:
        query = session.query(JobModel)
        
        if status is not None:
            query = query.filter(JobModel.status == status)
        
        if job_type is not None:
            query = query.filter(JobModel.job_type == job_type)
        
        job_models = query.limit(limit).offset(offset).all()
        
        jobs = []
        for model in job_models:
            # Convert paper_ids from JSON
            job_dict = model.__dict__
            job_dict['paper_ids'] = json.loads(job_dict['paper_ids'])
            jobs.append(Job.parse_obj(job_dict))
        
        return jobs
    finally:
        if close_session:
            session.close()