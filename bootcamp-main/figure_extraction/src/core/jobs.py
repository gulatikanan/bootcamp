import logging
import uuid
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional, Union

from src.config.settings import settings
from src.storage.models import Job, JobType, ProcessingStatus, Paper
from src.storage import queries
from src.extraction.extractor import PaperExtractor
from src.entity.detector import EntityDetector

# Set up logging
logger = logging.getLogger(__name__)

class JobManager:
    """Manage extraction and processing jobs."""
    
    def __init__(self):
        self.extractor = PaperExtractor()
        self.entity_detector = EntityDetector()
        self.running_jobs = {}
    
    async def create_extraction_job(self, paper_ids: List[str]) -> Job:
        """
        Create a new extraction job.
        
        Args:
            paper_ids: List of paper IDs to process
            
        Returns:
            The created Job object
        """
        # Create a unique job ID
        job_id = str(uuid.uuid4())
        
        # Create the job
        job = Job(
            id=job_id,
            job_type=JobType.EXTRACTION,
            status=ProcessingStatus.PENDING,
            paper_ids=paper_ids,
            total_papers=len(paper_ids),
            processed_papers=0,
            failed_papers=0
        )
        
        # Store the job
        stored_job = queries.create_job(job)
        
        # Start the job asynchronously
        asyncio.create_task(self._run_extraction_job(stored_job))
        
        return stored_job
    
    async def _run_extraction_job(self, job: Job):
        """
        Run an extraction job.
        
        Args:
            job: The Job object to run
        """
        logger.info(f"Starting extraction job {job.id} with {job.total_papers} papers")
        
        # Mark job as processing
        job = queries.update_job_status(job.id, ProcessingStatus.PROCESSING)
        self.running_jobs[job.id] = job
        
        processed_papers = 0
        failed_papers = 0
        
        try:
            # Process papers in batches
            batch_size = settings.processing.batch_size
            for i in range(0, len(job.paper_ids), batch_size):
                batch = job.paper_ids[i:i+batch_size]
                
                # Process batch concurrently
                tasks = [self.extractor.extract_and_store_paper(paper_id) for paper_id in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Count successes and failures
                for result in results:
                    if isinstance(result, Exception):
                        failed_papers += 1
                        logger.error(f"Paper extraction failed: {result}")
                    else:
                        processed_papers += 1
                        # Process entities for the paper's figures
                        try:
                            await self.entity_detector.process_paper_figures(result.id)
                        except Exception as e:
                            logger.error(f"Entity detection failed for paper {result.id}: {e}")
                
                # Update job status
                job = queries.update_job_status(
                    job.id, 
                    ProcessingStatus.PROCESSING,
                    processed_papers=processed_papers,
                    failed_papers=failed_papers
                )
            
            # Mark job as completed
            final_status = ProcessingStatus.COMPLETED if failed_papers == 0 else ProcessingStatus.FAILED
            job = queries.update_job_status(
                job.id, 
                final_status,
                processed_papers=processed_papers,
                failed_papers=failed_papers,
                completed_at=datetime.now()
            )
            
            logger.info(f"Extraction job {job.id} completed: {processed_papers} processed, {failed_papers} failed")
            
        except Exception as e:
            logger.error(f"Error running extraction job {job.id}: {e}")
            # Mark job as failed
            job = queries.update_job_status(
                job.id, 
                ProcessingStatus.FAILED,
                processed_papers=processed_papers,
                failed_papers=failed_papers + (job.total_papers - processed_papers - failed_papers),
                completed_at=datetime.now()
            )
        finally:
            # Remove job from running jobs
            if job.id in self.running_jobs:
                del self.running_jobs[job.id]
    
    def get_job_status(self, job_id: str) -> Optional[Job]:
        """
        Get the status of a job.
        
        Args:
            job_id: The ID of the job
            
        Returns:
            The Job object or None if not found
        """
        # Check running jobs first
        if job_id in self.running_jobs:
            return self.running_jobs[job_id]
        
        # Check database
        return queries.get_job(job_id)
    
    async def cancel_job(self, job_id: str) -> Optional[Job]:
        """
        Cancel a running job.
        
        Args:
            job_id: The ID of the job
            
        Returns:
            The updated Job object or None if not found
        """
        # Check if job is running
        if job_id not in self.running_jobs:
            # Check if job exists in database
            job = queries.get_job(job_id)
            if job is None:
                return None
            
            # If job is already completed or failed, return it
            if job.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED]:
                return job
        
        # Mark job as failed
        job = queries.update_job_status(
            job_id, 
            ProcessingStatus.FAILED,
            completed_at=datetime.now()
        )
        
        # Remove from running jobs
        if job_id in self.running_jobs:
            del self.running_jobs[job_id]
        
        return job

# Create singleton instance
job_manager = JobManager()

def get_job_manager() -> JobManager:
    """Get job manager instance."""
    return job_manager