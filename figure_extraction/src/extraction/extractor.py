import logging
import uuid
import asyncio
from typing import List, Dict, Any, Optional, Tuple

from src.config.settings import settings
from src.extraction.bioc_client import BioCPMCClient
from src.storage.models import Paper, Figure, ProcessingStatus
from src.storage import queries

# Set up logging
logger = logging.getLogger(__name__)

class PaperExtractor:
    """Extract paper metadata from PMC."""
    
    def __init__(self):
        self.bioc_client = BioCPMCClient()
    
    async def extract_paper(self, paper_id: str) -> Tuple[Paper, List[Figure]]:
        """
        Extract paper metadata from PMC.
        
        Args:
            paper_id: The PMC ID of the paper
            
        Returns:
            A tuple containing the paper and its figures
        """
        try:
            # Normalize paper ID
            if paper_id.startswith("PMC"):
                normalized_id = paper_id
            else:
                normalized_id = f"PMC{paper_id}"
            
            logger.info(f"Extracting paper {normalized_id}")
            
            # Get paper structure from BioC-PMC API
            paper_structure = await self.bioc_client.get_paper_structure(normalized_id)
            
            # Create Paper object
            paper = Paper(
                id=normalized_id,
                title=paper_structure["title"],
                abstract=paper_structure["abstract"],
                source="PMC",
                status=ProcessingStatus.COMPLETED
            )
            
            # Create Figure objects
            figures = []
            for fig_data in paper_structure["figures"]:
                figure = Figure(
                    id=str(uuid.uuid4()),
                    paper_id=normalized_id,
                    figure_number=fig_data["figure_number"],
                    caption=fig_data["caption"],
                    url=fig_data["url"]
                )
                figures.append(figure)
            
            return paper, figures
            
        except ValueError as e:
            logger.error(f"Extraction error for paper {paper_id}: {e}")
            # Create a Paper object with error status
            paper = Paper(
                id=paper_id if paper_id.startswith("PMC") else f"PMC{paper_id}",
                title="",
                abstract="",
                source="PMC",
                status=ProcessingStatus.FAILED,
                error_message=str(e)
            )
            return paper, []
        except Exception as e:
            logger.error(f"Unexpected error extracting paper {paper_id}: {e}")
            # Create a Paper object with error status
            paper = Paper(
                id=paper_id if paper_id.startswith("PMC") else f"PMC{paper_id}",
                title="",
                abstract="",
                source="PMC",
                status=ProcessingStatus.FAILED,
                error_message=f"Unexpected error: {str(e)}"
            )
            return paper, []
    
    async def extract_and_store_paper(self, paper_id: str) -> Paper:
        """
        Extract paper metadata and store it in the database.
        
        Args:
            paper_id: The PMC ID of the paper
            
        Returns:
            The stored Paper object
        """
        # Extract paper and figures
        paper, figures = await self.extract_paper(paper_id)
        
        # Store in database
        session = queries.db.get_session()
        try:
            # Store paper
            stored_paper = queries.create_paper(paper, session)
            
            # Store figures
            for figure in figures:
                queries.create_figure(figure, session)
            
            return stored_paper
        except Exception as e:
            logger.error(f"Error storing paper {paper_id}: {e}")
            # Update paper status to failed
            paper.status = ProcessingStatus.FAILED
            paper.error_message = f"Error storing paper: {str(e)}"
            queries.update_paper_status(
                paper.id, 
                ProcessingStatus.FAILED, 
                error_message=paper.error_message,
                session=session
            )
            raise
        finally:
            session.close()