import pytest
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, patch, mock_open
import httpx
import re

from src.extraction.bioc_client import BioCClient
from src.config.settings import Settings
from src.utils.rate_limiter import RateLimiter


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = MagicMock(spec=Settings)
    settings.bioc_api_url = "https://example.com/bioc/api"
    settings.bioc_rate_limit = 30
    settings.retry_limit = 3
    settings.retry_delay = 1
    return settings


@pytest.fixture
def bioc_client(mock_settings):
    """Create a BioC client with mock settings."""
    with patch("src.extraction.bioc_client.get_settings", return_value=mock_settings):
        client = BioCClient()
        return client


@pytest.fixture
def sample_bioc_xml():
    """Sample BioC XML response."""
    return """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE collection SYSTEM "BioC.dtd">
    <collection>
      <source>PubMed Central</source>
      <date>2023-05-19</date>
      <key>bioc.key</key>
      <document>
        <id>PMC6267067</id>
        <passage>
          <infon key="type">title</infon>
          <offset>0</offset>
          <text>Cardiac Regeneration: Biological and Therapeutic Implications</text>
        </passage>
        <passage>
          <infon key="type">abstract</infon>
          <offset>105</offset>
          <text>Heart failure remains a leading cause of morbidity and mortality worldwide. This review discusses recent advances in cardiac regeneration research.</text>
        </passage>
        <passage>
          <infon key="type">figure</infon>
          <infon key="figure_id">fig1</infon>
          <infon key="figure_url">https://example.com/figure1.jpg</infon>
          <infon key="figure_number">1</infon>
          <offset>850</offset>
          <text>Figure 1. Cardiac differentiation of human pluripotent stem cells. GATA4 and NKX2-5 are key transcription factors.</text>
        </passage>
        <passage>
          <infon key="type">figure</infon>
          <infon key="figure_id">fig2</infon>
          <infon key="figure_url">https://example.com/figure2.jpg</infon>
          <infon key="figure_number">2</infon>
          <offset>1250</offset>
          <text>Figure 2. Signaling pathways involved in cardiomyocyte proliferation.</text>
        </passage>
      </document>
    </collection>
    """


class TestBioCClient:
    """Tests for the BioC client."""
    
    def test_init(self, bioc_client, mock_settings):
        """Test client initialization."""
        assert bioc_client.base_url == mock_settings.bioc_api_url
        assert bioc_client.retry_limit == mock_settings.retry_limit
        assert bioc_client.retry_delay == mock_settings.retry_delay
        assert isinstance(bioc_client.rate_limiter, RateLimiter)
    
    @patch("httpx.Client.get")
    def test_get_paper_xml_success(self, mock_get, bioc_client, sample_bioc_xml):
        """Test successful retrieval of paper XML."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = sample_bioc_xml
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        result = bioc_client.get_paper_xml("PMC6267067")
        
        # Verify result
        assert result == sample_bioc_xml
        
        # Verify API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "PMC6267067" in kwargs["url"]
    
    @patch("httpx.Client.get")
    def test_get_paper_xml_http_error(self, mock_get, bioc_client):
        """Test handling of HTTP errors."""
        # Mock HTTP error
        mock_get.side_effect = httpx.HTTPStatusError(
            "404 Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            bioc_client.get_paper_xml("PMC6267067")
        
        assert "Resource not found" in str(excinfo.value)
    
    @patch("httpx.Client.get")
    def test_get_paper_xml_retry_success(self, mock_get, bioc_client, sample_bioc_xml):
        """Test successful retry after temporary failure."""
        # First call fails, second succeeds
        mock_error_response = MagicMock()
        mock_error_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "503 Service Unavailable",
            request=MagicMock(),
            response=MagicMock(status_code=503)
        )
        
        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.text = sample_bioc_xml
        mock_success_response.raise_for_status = MagicMock()
        
        mock_get.side_effect = [mock_error_response, mock_success_response]
        
        # Call method
        result = bioc_client.get_paper_xml("PMC6267067")
        
        # Verify result
        assert result == sample_bioc_xml
        assert mock_get.call_count == 2
    
    @patch("httpx.Client.get")
    def test_get_paper_xml_normalize_id(self, mock_get, bioc_client, sample_bioc_xml):
        """Test normalizing paper ID."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = sample_bioc_xml
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method with ID without PMC prefix
        bioc_client.get_paper_xml("6267067")
        
        # Verify API call with normalized ID
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "PMC6267067" in kwargs["url"]
    
    def test_parse_paper_xml(self, bioc_client, sample_bioc_xml):
        """Test parsing paper XML."""
        # Call method
        result = bioc_client._parse_paper_xml(sample_bioc_xml)
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["title"] == "Cardiac Regeneration: Biological and Therapeutic Implications"
        assert "Heart failure remains" in result["abstract"]
        assert len(result["figures"]) == 2
        
        # Verify first figure
        fig1 = result["figures"][0]
        assert fig1["figure_id"] == "fig1"
        assert fig1["figure_number"] == 1
        assert "Cardiac differentiation" in fig1["caption"]
        assert fig1["url"] == "https://example.com/figure1.jpg"
        
        # Verify second figure
        fig2 = result["figures"][1]
        assert fig2["figure_id"] == "fig2"
        assert fig2["figure_number"] == 2
        assert "Signaling pathways" in fig2["caption"]
        assert fig2["url"] == "https://example.com/figure2.jpg"
    
    def test_parse_paper_xml_missing_fields(self, bioc_client):
        """Test parsing XML with missing fields."""
        # XML with missing title
        xml_missing_title = """<?xml version="1.0" encoding="UTF-8"?>
        <collection>
          <document>
            <id>PMC6267067</id>
            <passage>
              <infon key="type">abstract</infon>
              <text>Abstract text</text>
            </passage>
          </document>
        </collection>
        """
        
        # Call method
        result = bioc_client._parse_paper_xml(xml_missing_title)
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["title"] == ""  # Empty string for missing title
        assert result["abstract"] == "Abstract text"
        assert result["figures"] == []  # No figures
    
    def test_parse_paper_xml_invalid_xml(self, bioc_client):
        """Test parsing invalid XML."""
        # Invalid XML
        invalid_xml = "This is not XML"
        
        # Call method and expect exception
        with pytest.raises(ET.ParseError):
            bioc_client._parse_paper_xml(invalid_xml)
    
    def test_parse_paper_xml_missing_document(self, bioc_client):
        """Test parsing XML with missing document element."""
        # XML with missing document
        xml_missing_document = """<?xml version="1.0" encoding="UTF-8"?>
        <collection>
          <source>PubMed Central</source>
        </collection>
        """
        
        # Call method
        result = bioc_client._parse_paper_xml(xml_missing_document)
        
        # Verify result is empty
        assert result["paper_id"] == ""
        assert result["title"] == ""
        assert result["abstract"] == ""
        assert result["figures"] == []
    
    @patch("src.extraction.bioc_client.BioCClient.get_paper_xml")
    def test_get_paper_structure(self, mock_get_xml, bioc_client, sample_bioc_xml):
        """Test getting paper structure."""
        # Mock get_paper_xml
        mock_get_xml.return_value = sample_bioc_xml
        
        # Call method
        result = bioc_client.get_paper_structure("PMC6267067")
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["title"] == "Cardiac Regeneration: Biological and Therapeutic Implications"
        assert "Heart failure remains" in result["abstract"]
        assert len(result["figures"]) == 2
        
        # Verify get_paper_xml call
        mock_get_xml.assert_called_once_with("PMC6267067")
    
    @patch("src.extraction.bioc_client.BioCClient.get_paper_xml")
    def test_get_paper_structure_error(self, mock_get_xml, bioc_client):
        """Test handling errors in get_paper_structure."""
        # Mock get_paper_xml to raise error
        mock_get_xml.side_effect = ValueError("API error")
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            bioc_client.get_paper_structure("PMC6267067")
        
        assert "API error" in str(excinfo.value)
    
    @patch("httpx.Client.get")
    def test_check_availability(self, mock_get, bioc_client):
        """Test checking API availability."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        result = bioc_client.check_availability()
        
        # Verify result
        assert result is True
        mock_get.assert_called_once()
    
    @patch("httpx.Client.get")
    def test_check_availability_error(self, mock_get, bioc_client):
        """Test checking API availability when API is down."""
        # Mock error
        mock_get.side_effect = httpx.HTTPStatusError(
            "503 Service Unavailable",
            request=MagicMock(),
            response=MagicMock(status_code=503)
        )
        
        # Call method
        result = bioc_client.check_availability()
        
        # Verify result
        assert result is False
    
    @patch("src.extraction.bioc_client.RateLimiter")
    def test_rate_limiting(self, mock_rate_limiter_class, mock_settings):
        """Test rate limiting configuration."""
        # Create mock rate limiter
        mock_rate_limiter = MagicMock()
        mock_rate_limiter_class.return_value = mock_rate_limiter
        
        # Create client
        with patch("src.extraction.bioc_client.get_settings", return_value=mock_settings):
            client = BioCClient()
        
        # Verify rate limiter configuration
        mock_rate_limiter_class.assert_called_once_with(mock_settings.bioc_rate_limit)
        
        # Mock HTTP response
        with patch("httpx.Client.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "<collection></collection>"
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response
            
            # Call method
            client.get_paper_xml("PMC6267067")
            
            # Verify rate limiter was used
            mock_rate_limiter.wait.assert_called_once()
    
    def test_extract_figure_info(self, bioc_client):
        """Test extracting figure information from passage."""
        # Create mock passage element
        passage = ET.Element("passage")
        
        # Add infon elements
        figure_type = ET.SubElement(passage, "infon")
        figure_type.set("key", "type")
        figure_type.text = "figure"
        
        figure_id = ET.SubElement(passage, "infon")
        figure_id.set("key", "figure_id")
        figure_id.text = "fig1"
        
        figure_url = ET.SubElement(passage, "infon")
        figure_url.set("key", "figure_url")
        figure_url.text = "https://example.com/figure1.jpg"
        
        figure_number = ET.SubElement(passage, "infon")
        figure_number.set("key", "figure_number")
        figure_number.text = "1"
        
        # Add text element
        text = ET.SubElement(passage, "text")
        text.text = "Figure 1. Test caption."
        
        # Call method
        result = bioc_client._extract_figure_info(passage)
        
        # Verify result
        assert result["figure_id"] == "fig1"
        assert result["figure_number"] == 1
        assert result["caption"] == "Figure 1. Test caption."
        assert result["url"] == "https://example.com/figure1.jpg"
    
    def test_extract_figure_info_missing_fields(self, bioc_client):
        """Test extracting figure information with missing fields."""
        # Create mock passage element with missing fields
        passage = ET.Element("passage")
        
        # Add infon elements (missing figure_url)
        figure_type = ET.SubElement(passage, "infon")
        figure_type.set("key", "type")
        figure_type.text = "figure"
        
        figure_id = ET.SubElement(passage, "infon")
        figure_id.set("key", "figure_id")
        figure_id.text = "fig1"
        
        # Add text element
        text = ET.SubElement(passage, "text")
        text.text = "Figure 1. Test caption."
        
        # Call method
        result = bioc_client._extract_figure_info(passage)
        
        # Verify result
        assert result["figure_id"] == "fig1"
        assert result["figure_number"] is None  # Missing
        assert result["caption"] == "Figure 1. Test caption."
        assert result["url"] == ""  # Missing
    
    def test_normalize_paper_id(self, bioc_client):
        """Test normalizing paper ID."""
        # Test cases
        test_cases = [
            ("PMC6267067", "PMC6267067"),  # Already has prefix
            ("6267067", "PMC6267067"),      # Missing prefix
            ("pmc6267067", "PMC6267067"),   # Lowercase prefix
            ("PMC 6267067", "PMC6267067"),  # Space in prefix
            ("", ""),                       # Empty string
            (None, "")                      # None
        ]
        
        # Test each case
        for input_id, expected_output in test_cases:
            result = bioc_client._normalize_paper_id(input_id)
            assert result == expected_output


class TestBioCClientIntegration:
    """Integration tests for BioC client."""
    
    @patch("httpx.Client.get")
    def test_full_paper_extraction(self, mock_get, bioc_client, sample_bioc_xml):
        """Test the full paper extraction workflow."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = sample_bioc_xml
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        result = bioc_client.get_paper_structure("PMC6267067")
        
        # Verify paper metadata
        assert result["paper_id"] == "PMC6267067"
        assert result["title"] == "Cardiac Regeneration: Biological and Therapeutic Implications"
        assert "Heart failure remains" in result["abstract"]
        
        # Verify figures
        assert len(result["figures"]) == 2
        
        # Check first figure
        assert result["figures"][0]["figure_id"] == "fig1"
        assert result["figures"][0]["figure_number"] == 1
        assert "GATA4" in result["figures"][0]["caption"]
        assert "NKX2-5" in result["figures"][0]["caption"]
        
        # Check second figure
        assert result["figures"][1]["figure_id"] == "fig2"
        assert result["figures"][1]["figure_number"] == 2
        assert "Signaling pathways" in result["figures"][1]["caption"]
    
    @patch("httpx.Client.get")
    def test_extract_figures_with_entities(self, mock_get, bioc_client, sample_bioc_xml):
        """Test extracting figures with potential entities."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = sample_bioc_xml
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        result = bioc_client.get_paper_structure("PMC6267067")
        
        # Extract figures with gene mentions
        gene_figures = [fig for fig in result["figures"] if re.search(r'GATA4|NKX2-5', fig["caption"])]
        
        # Verify gene figures
        assert len(gene_figures) == 1
        assert gene_figures[0]["figure_id"] == "fig1"
        assert "GATA4" in gene_figures[0]["caption"]
        assert "NKX2-5" in gene_figures[0]["caption"]
    
    def test_handle_complex_xml(self, bioc_client):
        """Test handling complex XML with nested elements."""
        # Complex XML with nested elements
        complex_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <collection>
          <document>
            <id>PMC6267067</id>
            <passage>
              <infon key="type">title</infon>
              <text>Complex Title</text>
            </passage>
            <passage>
              <infon key="type">figure</infon>
              <infon key="figure_id">fig1</infon>
              <infon key="figure_url">https://example.com/figure1.jpg</infon>
              <text>Figure with <bold>formatted</bold> text and <italic>styling</italic>.</text>
            </passage>
          </document>
        </collection>
        """
        
        # Call method
        result = bioc_client._parse_paper_xml(complex_xml)
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["title"] == "Complex Title"
        assert len(result["figures"]) == 1
        assert "Figure with" in result["figures"][0]["caption"]