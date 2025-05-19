import logging
import uuid
import asyncio
from typing import List, Dict, Any, Optional

from src.config.settings import settings
from src.entity.pubtator_client import PubTator3Client
from src.storage.models import Figure, Entity, EntityType
from src.storage import queries

# Set up logging
logger = logging.getLogger(__name__)

class EntityDetector:
    """Detect entities in figure captions."""
    
    def __init__(self):
        self.pubtator_client = PubTator3Client()
    
    async def detect_entities_in_caption(self, figure: Figure) -> List[Entity]:
        """
        Detect entities in a figure caption.
        
        Args:
            figure: The Figure object containing the caption
            
        Returns:
            A list of detected Entity objects
        """
        try:
            logger.info(f"Detecting entities in figure {figure.id}")
            
            # Get entities from PubTator3 API
            entity_data = await self.pubtator_client.detect_entities(figure.caption)
            
            # Create Entity objects
            entities = []
            for data in entity_data:
                entity = Entity(
                    id=str(uuid.uuid4()),
                    figure_id=figure.id,
                    entity_text=data["entity_text"],
                    entity_type=data["entity_type"],
                    start_position=data["start_position"],
                    end_position=data["end_position"],
                    external_id=data["external_id"] if data["external_id"] else None
                )
                entities.append(entity)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error detecting entities in figure {figure.id}: {e}")
            return []
    
    async def detect_and_store_entities(self, figure: Figure) -> List[Entity]:
        """
        Detect entities in a figure caption and store them in the database.
        
        Args:
            figure: The Figure object containing the caption
            
        Returns:
            A list of stored Entity objects
        """
        # Detect entities
        entities = await self.detect_entities_in_caption(figure)
        
        # Store in database
        session = queries.db.get_session()
        try:
            stored_entities = []
            for entity in entities:
                stored_entity = queries.create_entity(entity, session)
                stored_entities.append(stored_entity)
            
            return stored_entities
        except Exception as e:
            logger.error(f"Error storing entities for figure {figure.id}: {e}")
            raise
        finally:
            session.close()
    
    async def process_paper_figures(self, paper_id: str) -> Dict[str, int]:
        """
        Process all figures for a paper and detect entities.
        
        Args:
            paper_id: The ID of the paper
            
        Returns:
            A dictionary with counts of processed figures and entities
        """
        session = queries.db.get_session()
        try:
            # Get all figures for the paper
            figures = queries.get_figures_for_paper(paper_id, session)
            
            entity_count = 0
            for figure in figures:
                # Detect and store entities
                entities = await self.detect_and_store_entities(figure)
                entity_count += len(entities)
            
            return {
                "processed_figures": len(figures),
                "detected_entities": entity_count
            }
        except Exception as e:
            logger.error(f"Error processing figures for paper {paper_id}: {e}")
            raise
        finally:
            session.close()