import logging
import time
import httpx
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Tuple

from src.config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

class BioCPMCClient:
    """Client for the BioC-PMC API."""
    
    def __init__(self):
        self.base_url = settings.external_api.bioc_pmc_url
        self.rate_limit = settings.external_api.bioc_pmc_rate_limit
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
    
    async def get_paper_structure(self, paper_id: str) -> Dict[str, Any]:
        """
        Get the structure of a paper from the BioC-PMC API.
        
        Args:
            paper_id: The PMC ID of the paper (e.g., "PMC123456")
            
        Returns:
            A dictionary containing the paper structure
        """
        # Ensure paper_id is in the correct format
        if not paper_id.startswith("PMC"):
            paper_id = f"PMC{paper_id}"
        
        self._respect_rate_limit()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/retrieve",
                    params={
                        "id": paper_id,
                        "format": "xml"
                    },
                    timeout=30.0
                )
                
                response.raise_for_status()
                
                # Parse the XML response
                return self._parse_bioc_xml(response.text)
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for paper {paper_id}: {e}")
            if e.response.status_code == 404:
                raise ValueError(f"Paper {paper_id} not found")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error for paper {paper_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error for paper {paper_id}: {e}")
            raise
    
    def _parse_bioc_xml(self, xml_text: str) -> Dict[str, Any]:
        """
        Parse the BioC XML response.
        
        Args:
            xml_text: The XML response from the BioC-PMC API
            
        Returns:
            A dictionary containing the parsed paper structure
        """
        try:
            # Parse XML
            root = ET.fromstring(xml_text)
            
            # Initialize result structure
            result = {
                "title": "",
                "abstract": "",
                "figures": []
            }
            
            # Find document element
            document = root.find(".//document")
            if document is None:
                raise ValueError("No document element found in XML")
            
            # Extract title
            title_elem = document.find(".//passage[infon='title']/text")
            if title_elem is not None:
                result["title"] = title_elem.text
            
            # Extract abstract
            abstract_passages = document.findall(".//passage[infon='abstract']/text")
            abstract_texts = [p.text for p in abstract_passages if p.text]
            result["abstract"] = " ".join(abstract_texts)
            
            # Extract figures
            figure_num = 1
            for fig_elem in document.findall(".//passage[infon='figure']"):
                caption_elem = fig_elem.find("text")
                if caption_elem is not None and caption_elem.text:
                    figure = {
                        "figure_number": figure_num,
                        "caption": caption_elem.text,
                        "url": None
                    }
                    
                    # Try to find figure URL
                    url_elem = fig_elem.find("infon[@key='url']")
                    if url_elem is not None and url_elem.text:
                        figure["url"] = url_elem.text
                    
                    result["figures"].append(figure)
                    figure_num += 1
            
            return result
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            raise ValueError(f"Failed to parse XML response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error parsing XML: {e}")
            raise