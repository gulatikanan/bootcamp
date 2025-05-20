import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Query, Path
from fastapi.responses import FileResponse, JSONResponse

from src.config.settings import settings
from src.storage.models import Paper, Figure, Entity, Job, ProcessingStatus, JobType, EntityType
from src.storage import queries
from src.core.orchestrator import orchestrator
from src.core.jobs import job_manager
from src.api.auth import verify_api_key

# Set up logging
logger = logging.getLogger(__name__)

# Create routers
papers_router = APIRouter(prefix="/papers", tags=["papers"])
figures_router = APIRouter(prefix="/figures", tags=["figures"])
entities_router = APIRouter(prefix="/entities", tags=["entities"])
jobs_router = APIRouter(prefix="/jobs", tags=["jobs"])
export_router = APIRouter(prefix="/export", tags=["export"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Papers endpoints
@papers_router.post("", response_model=Job)
async def submit_papers(
    paper_ids: List[str],
    api_key: str = Depends(verify_api_key)
) -> Job:
    """
    Submit paper IDs for processing.
    """
    if not paper_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No paper IDs provided"
        )
    
    try:
        job = await orchestrator.process_papers(paper_ids)
        return job
    except Exception as e:
        logger.error(f"Error submitting papers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting papers: {str(e)}"
        )

@papers_router.post("/file", response_model=Job)
async def submit_papers_file(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
) -> Job:
    """
    Submit a file containing paper IDs for processing.
    """
    try:
        # Save file to temp directory
        temp_file_path = os.path.join(settings.temp_dir, file.filename)
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process file
        job = await orchestrator.process_paper_file(temp_file_path)
        
        # Clean up
        os.remove(temp_file_path)
        
        return job
    except Exception as e:
        logger.error(f"Error submitting papers file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting papers file: {str(e)}"
        )

@papers_router.get("", response_model=List[Paper])
async def list_papers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: Optional[ProcessingStatus] = None,
    api_key: str = Depends(verify_api_key)
) -> List[Paper]:
    """
    List all processed papers.
    """
    try:
        papers = queries.list_papers(limit=limit, offset=offset, status=status)
        return papers
    except Exception as e:
        logger.error(f"Error listing papers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing papers: {str(e)}"
        )

@papers_router.get("/{paper_id}", response_model=Paper)
async def get_paper(
    paper_id: str = Path(..., description="The ID of the paper"),
    api_key: str = Depends(verify_api_key)
) -> Paper:
    """
    Get details for a specific paper.
    """
    try:
        # Normalize paper ID
        if not paper_id.startswith("PMC"):
            paper_id = f"PMC{paper_id}"
        
        paper = queries.get_paper(paper_id)
        if paper is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Paper {paper_id} not found"
            )
        
        return paper
    except Exception as e:
        logger.error(f"Error getting paper {paper_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting paper: {str(e)}"
        )

@papers_router.get("/{paper_id}/figures", response_model=List[Figure])
async def get_paper_figures(
    paper_id: str = Path(..., description="The ID of the paper"),
    api_key: str = Depends(verify_api_key)
) -> List[Figure]:
    """
    Get figures for a specific paper.
    """
    try:
        # Normalize paper ID
        if not paper_id.startswith("PMC"):
            paper_id = f"PMC{paper_id}"
        
        # Check if paper exists
        paper = queries.get_paper(paper_id)
        if paper is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Paper {paper_id} not found"
            )
        
        figures = queries.get_figures_for_paper(paper_id)
        return figures
    except Exception as e:
        logger.error(f"Error getting figures for paper {paper_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting figures: {str(e)}"
        )

# Figures endpoints
@figures_router.get("", response_model=List[Figure])
async def list_figures(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    api_key: str = Depends(verify_api_key)
) -> List[Figure]:
    """
    List all figures.
    """
    try:
        # Get all papers
        papers = queries.list_papers(limit=limit, offset=offset)
        
        # Get figures for each paper
        figures = []
        for paper in papers:
            paper_figures = queries.get_figures_for_paper(paper.id)
            figures.extend(paper_figures)
        
        return figures
    except Exception as e:
        logger.error(f"Error listing figures: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing figures: {str(e)}"
        )

@figures_router.get("/{figure_id}", response_model=Figure)
async def get_figure(
    figure_id: str = Path(..., description="The ID of the figure"),
    api_key: str = Depends(verify_api_key)
) -> Figure:
    """
    Get details for a specific figure.
    """
    try:
        # Get all papers
        papers = queries.list_papers()
        
        # Get figures for each paper and find the one with matching ID
        for paper in papers:
            paper_figures = queries.get_figures_for_paper(paper.id)
            for figure in paper_figures:
                if figure.id == figure_id:
                    return figure
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Figure {figure_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting figure {figure_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting figure: {str(e)}"
        )

@figures_router.get("/{figure_id}/entities", response_model=List[Entity])
async def get_figure_entities(
    figure_id: str = Path(..., description="The ID of the figure"),
    api_key: str = Depends(verify_api_key)
) -> List[Entity]:
    """
    Get entities for a specific figure.
    """
    try:
        # Get all papers
        papers = queries.list_papers()
        
        # Get figures for each paper and find the one with matching ID
        figure_found = False
        for paper in papers:
            paper_figures = queries.get_figures_for_paper(paper.id)
            for figure in paper_figures:
                if figure.id == figure_id:
                    figure_found = True
                    break
            if figure_found:
                break
        
        if not figure_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Figure {figure_id} not found"
            )
        
        entities = queries.get_entities_for_figure(figure_id)
        return entities
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting entities for figure {figure_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting entities: {str(e)}"
        )

# Entities endpoints
@entities_router.get("", response_model=List[Entity])
async def list_entities(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    api_key: str = Depends(verify_api_key)
) -> List[Entity]:
    """
    List all entities.
    """
    try:
        # Get all papers
        papers = queries.list_papers()
        
        # Get figures for each paper
        figures = []
        for paper in papers:
            paper_figures = queries.get_figures_for_paper(paper.id)
            figures.extend(paper_figures)
        
        # Get entities for each figure
        entities = []
        for figure in figures:
            figure_entities = queries.get_entities_for_figure(figure.id)
            entities.extend(figure_entities)
        
        # Apply limit and offset
        start = min(offset, len(entities))
        end = min(offset + limit, len(entities))
        
        return entities[start:end]
    except Exception as e:
        logger.error(f"Error listing entities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing entities: {str(e)}"
        )

@entities_router.get("/{entity_type}", response_model=List[Entity])
async def list_entities_by_type(
    entity_type: EntityType = Path(..., description="The type of entity"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    api_key: str = Depends(verify_api_key)
) -> List[Entity]:
    """
    List entities of a specific type.
    """
    try:
        # Get all papers
        papers = queries.list_papers()
        
        # Get figures for each paper
        figures = []
        for paper in papers:
            paper_figures = queries.get_figures_for_paper(paper.id)
            figures.extend(paper_figures)
        
        # Get entities for each figure and filter by type
        entities = []
        for figure in figures:
            figure_entities = queries.get_entities_for_figure(figure.id)
            for entity in figure_entities:
                if entity.entity_type == entity_type:
                    entities.append(entity)
        
        # Apply limit and offset
        start = min(offset, len(entities))
        end = min(offset + limit, len(entities))
        
        return entities[start:end]
    except Exception as e:
        logger.error(f"Error listing entities of type {entity_type}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing entities: {str(e)}"
        )

# Jobs endpoints
@jobs_router.get("", response_model=List[Job])
async def list_jobs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: Optional[ProcessingStatus] = None,
    job_type: Optional[JobType] = None,
    api_key: str = Depends(verify_api_key)
) -> List[Job]:
    """
    List all jobs.
    """
    try:
        jobs = queries.list_jobs(limit=limit, offset=offset, status=status, job_type=job_type)
        return jobs
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing jobs: {str(e)}"
        )

@jobs_router.get("/{job_id}", response_model=Job)
async def get_job(
    job_id: str = Path(..., description="The ID of the job"),
    api_key: str = Depends(verify_api_key)
) -> Job:
    """
    Get details for a specific job.
    """
    try:
        job = job_manager.get_job_status(job_id)
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found"
            )
        
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting job: {str(e)}"
        )

@jobs_router.post("/{job_id}/cancel", response_model=Job)
async def cancel_job(
    job_id: str = Path(..., description="The ID of the job"),
    api_key: str = Depends(verify_api_key)
) -> Job:
    """
    Cancel a specific job.
    """
    try:
        job = await job_manager.cancel_job(job_id)
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found"
            )
        
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error canceling job {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error canceling job: {str(e)}"
        )

# Export endpoints
@export_router.get("/papers")
async def export_papers(
    format: str = Query("json", description="Export format (json or csv)"),
    api_key: str = Depends(verify_api_key)
):
    """
    Export papers data.
    """
    try:
        if format not in ["json", "csv"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid format: {format}. Must be 'json' or 'csv'."
            )
        
        # Create export directory if it doesn't exist
        export_dir = os.path.join(settings.temp_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate export file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"papers_{timestamp}.{format}"
        export_path = os.path.join(export_dir, filename)
        
        # Export data
        orchestrator.export_data("papers", format, export_path)
        
        # Return file
        return FileResponse(
            path=export_path,
            filename=filename,
            media_type="application/json" if format == "json" else "text/csv"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting papers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting papers: {str(e)}"
        )

@export_router.get("/figures")
async def export_figures(
    format: str = Query("json", description="Export format (json or csv)"),
    api_key: str = Depends(verify_api_key)
):
    """
    Export figures data.
    """
    try:
        if format not in ["json", "csv"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid format: {format}. Must be 'json' or 'csv'."
            )
        
        # Create export directory if it doesn't exist
        export_dir = os.path.join(settings.temp_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate export file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"figures_{timestamp}.{format}"
        export_path = os.path.join(export_dir, filename)
        
        # Export data
        orchestrator.export_data("figures", format, export_path)
        
        # Return file
        return FileResponse(
            path=export_path,
            filename=filename,
            media_type="application/json" if format == "json" else "text/csv"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting figures: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting figures: {str(e)}"
        )

@export_router.get("/entities")
async def export_entities(
    format: str = Query("json", description="Export format (json or csv)"),
    api_key: str = Depends(verify_api_key)
):
    """
    Export entities data.
    """
    try:
        if format not in ["json", "csv"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid format: {format}. Must be 'json' or 'csv'."
            )
        
        # Create export directory if it doesn't exist
        export_dir = os.path.join(settings.temp_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate export file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"entities_{timestamp}.{format}"
        export_path = os.path.join(export_dir, filename)
        
        # Export data
        orchestrator.export_data("entities", format, export_path)
        
        # Return file
        return FileResponse(
            path=export_path,
            filename=filename,
            media_type="application/json" if format == "json" else "text/csv"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting entities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting entities: {str(e)}"
        )

# Admin endpoints
@admin_router.get("/config")
async def get_config(
    api_key: str = Depends(verify_api_key)
):
    """
    Get current configuration.
    """
    try:
        # Return configuration (excluding sensitive data)
        config = {
            "app_name": settings.app_name,
            "environment": settings.environment,
            "log_level": settings.log_level,
            "temp_dir": settings.temp_dir,
            "api": {
                "host": settings.api.host,
                "port": settings.api.port,
                "workers": settings.api.workers,
                "enable_docs": settings.api.enable_docs
            },
            "security": {
                "auth_enabled": settings.security.auth_enabled,
                "auth_method": settings.security.auth_method,
                "token_expiration": settings.security.token_expiration
            },
            "storage": {
                "storage_type": settings.storage.storage_type,
                "duckdb_path": settings.storage.duckdb_path,
                "backup_enabled": settings.storage.backup_enabled,
                "backup_interval": settings.storage.backup_interval
            },
            "processing": {
                "extraction_workers": settings.processing.extraction_workers,
                "entity_detection_workers": settings.processing.entity_detection_workers,
                "batch_size": settings.processing.batch_size,
                "retry_limit": settings.processing.retry_limit,
                "retry_delay": settings.processing.retry_delay
            },
            "watched_folder": {
                "watched_folders": settings.watched_folder.watched_folders,
                "watch_interval": settings.watched_folder.watch_interval,
                "file_patterns": settings.watched_folder.file_patterns
            },
            "external_api": {
                "bioc_pmc_url": settings.external_api.bioc_pmc_url,
                "bioc_pmc_rate_limit": settings.external_api.bioc_pmc_rate_limit,
                "pubtator3_url": settings.external_api.pubtator3_url,
                "pubtator3_rate_limit": settings.external_api.pubtator3_rate_limit
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting configuration: {str(e)}"
        )

@admin_router.get("/stats")
async def get_stats(
    api_key: str = Depends(verify_api_key)
):
    """
    Get system statistics.
    """
    try:
        # Get counts from database
        session = queries.db.get_session()
        
        try:
            # Count papers by status
            papers_by_status = {}
            for status_value in ProcessingStatus:
                count = session.query(queries.PaperModel).filter(
                    queries.PaperModel.status == status_value
                ).count()
                papers_by_status[status_value.value] = count
            
            # Count figures
            figure_count = session.query(queries.FigureModel).count()
            
            # Count entities by type
            entities_by_type = {}
            for entity_type in EntityType:
                count = session.query(queries.EntityModel).filter(
                    queries.EntityModel.entity_type == entity_type
                ).count()
                entities_by_type[entity_type.value] = count
            
            # Count jobs by status
            jobs_by_status = {}
            for status_value in ProcessingStatus:
                count = session.query(queries.JobModel).filter(
                    queries.JobModel.status == status_value
                ).count()
                jobs_by_status[status_value.value] = count
            
            # Get database file size
            db_path = settings.storage.duckdb_path
            db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
            
            stats = {
                "papers": {
                    "total": sum(papers_by_status.values()),
                    "by_status": papers_by_status
                },
                "figures": {
                    "total": figure_count
                },
                "entities": {
                    "total": sum(entities_by_type.values()),
                    "by_type": entities_by_type
                },
                "jobs": {
                    "total": sum(jobs_by_status.values()),
                    "by_status": jobs_by_status
                },
                "database": {
                    "size_bytes": db_size,
                    "size_mb": round(db_size / (1024 * 1024), 2) if db_size > 0 else 0
                }
            }
            
            return stats
        finally:
            session.close()
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting statistics: {str(e)}"
        )