import logging
import asyncio
import csv
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Set

from src.config.settings import settings
from src.storage.models import Paper, Figure, Entity, Job, ProcessingStatus
from src.storage import queries
from src.core.jobs import job_manager

# Set up logging
logger = logging.getLogger(__name__)

class Orchestrator:
    """Orchestrate the extraction and processing of papers."""
    
    def __init__(self):
        self.job_manager = job_manager
    
    async def process_papers(self, paper_ids: List[str]) -> Job:
        """
        Process a list of paper IDs.
        
        Args:
            paper_ids: List of paper IDs to process
            
        Returns:
            The created Job object
        """
        # Normalize paper IDs
        normalized_ids = []
        for paper_id in paper_ids:
            if paper_id.strip():
                if not paper_id.startswith("PMC"):
                    normalized_ids.append(f"PMC{paper_id}")
                else:
                    normalized_ids.append(paper_id)
        
        # Create and start extraction job
        job = await self.job_manager.create_extraction_job(normalized_ids)
        
        return job
    
    async def process_paper_file(self, file_path: str) -> Job:
        """
        Process a file containing paper IDs.
        
        Args:
            file_path: Path to the file
            
        Returns:
            The created Job object
        """
        paper_ids = []
        
        try:
            with open(file_path, 'r') as f:
                # Try to detect file format
                if file_path.endswith('.csv'):
                    # CSV file
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[0].strip():
                            paper_ids.append(row[0].strip())
                else:
                    # Text file, one ID per line
                    for line in f:
                        line = line.strip()
                        if line:
                            paper_ids.append(line)
            
            # Process the papers
            return await self.process_papers(paper_ids)
            
        except Exception as e:
            logger.error(f"Error processing paper file {file_path}: {e}")
            raise
    
    def export_data(self, data_type: str, output_format: str, output_path: str) -> str:
        """
        Export data to a file.
        
        Args:
            data_type: Type of data to export ('papers', 'figures', 'entities')
            output_format: Format of the output file ('json', 'csv')
            output_path: Path to the output file
            
        Returns:
            Path to the exported file
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Get data based on type
            if data_type == 'papers':
                data = queries.list_papers(limit=1000)
            elif data_type == 'figures':
                # Get all papers
                papers = queries.list_papers(limit=1000)
                
                # Get figures for each paper
                data = []
                for paper in papers:
                    figures = queries.get_figures_for_paper(paper.id)
                    data.extend(figures)
            elif data_type == 'entities':
                # Get all papers
                papers = queries.list_papers(limit=1000)
                
                # Get figures for each paper
                figures = []
                for paper in papers:
                    paper_figures = queries.get_figures_for_paper(paper.id)
                    figures.extend(paper_figures)
                
                # Get entities for each figure
                data = []
                for figure in figures:
                    entities = queries.get_entities_for_figure(figure.id)
                    data.extend(entities)
            else:
                raise ValueError(f"Invalid data type: {data_type}")
            
            # Export data based on format
            if output_format == 'json':
                with open(output_path, 'w') as f:
                    json_data = [item.dict() for item in data]
                    json.dump(json_data, f, indent=2, default=str)
            elif output_format == 'csv':
                if not data:
                    # Create empty file with headers
                    with open(output_path, 'w') as f:
                        if data_type == 'papers':
                            f.write("id,title,abstract,processed_date,source,status,error_message\n")
                        elif data_type == 'figures':
                            f.write("id,paper_id,figure_number,caption,url\n")
                        elif data_type == 'entities':
                            f.write("id,figure_id,entity_text,entity_type,start_position,end_position,external_id\n")
                else:
                    # Write data to CSV
                    with open(output_path, 'w', newline='') as f:
                        # Get field names from first item
                        fieldnames = data[0].dict().keys()
                        
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for item in data:
                            writer.writerow(item.dict())
            else:
                raise ValueError(f"Invalid output format: {output_format}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting {data_type} to {output_path}: {e}")
            raise

# Create singleton instance
orchestrator = Orchestrator()

def get_orchestrator() -> Orchestrator:
    """Get orchestrator instance."""
    return orchestrator