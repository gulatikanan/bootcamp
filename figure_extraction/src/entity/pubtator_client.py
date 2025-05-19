import logging
import time
import json
import httpx
from typing import Dict, List, Optional, Any

from src.config.settings import settings
from src.storage.models import EntityType

# Set up logging
logger = logging.getLogger(__name__)

class PubTator3Client:
    """Client for the PubTator3 API."""
    
    def __init__(self):
        self.base_url = settings.external_api.pubtator3_url
        self.rate_limit = settings.external_api.pubtator3_rate_limit
        self.last_request_time = 0
        
    def _respect_rate_limit(self):
        """Ensure we don't exceed the rate limit."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        # Calculate minimum time between requests based on rate limit
        min_interval = 60.0 / self.rate_limit  # seconds
        
        if time_since_last_request < min_interval:
            sleep_time = min_interval - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    async def detect_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect entities in text using the PubTator3 API.
        
        Args:
            text: The text to analyze
            
        Returns:
            A list of detected entities
        """
        self._respect_rate_limit()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/tag",
                    json={
                        "text": text,
                        "concepts": ["gene", "disease", "chemical", "species", "mutation", "cellline"]
                    },
                    timeout=30.0
                )
                
                response.raise_for_status()
                
                # Parse the JSON response
                result = response.json()
                
                # Extract entities
                entities = []
                if "denotations" in result:
                    for entity in result["denotations"]:
                        entity_type = self._map_entity_type(entity.get("obj"))
                        if entity_type:
                            entities.append({
                                "entity_text": entity.get("span", {}).get("text", ""),
                                "entity_type": entity_type,
                                "start_position": entity.get("span", {}).get("begin", 0),
                                "end_position": entity.get("span", {}).get("end", 0),
                                "external_id": entity.get("id", "")
                            })
                
                return entities
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error detecting entities: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error detecting entities: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error detecting entities: {e}")
            raise
    
    def _map_entity_type(self, pubtator_type: str) -> Optional[EntityType]:
        """
        Map PubTator entity type to our EntityType enum.
        
        Args:
            pubtator_type: The entity type from PubTator
            
        Returns:
            The corresponding EntityType or None if no match
        """
        type_mapping = {
            "Gene": EntityType.GENE,
            "Disease": EntityType.DISEASE,
            "Chemical": EntityType.CHEMICAL,
            "Species": EntityType.SPECIES,
            "Mutation": EntityType.MUTATION,
            "CellLine": EntityType.CELL_LINE
        }
        
        return type_mapping.get(pubtator_type)