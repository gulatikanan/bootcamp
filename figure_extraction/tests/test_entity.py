import pytest
import json
import httpx
from unittest.mock import MagicMock, patch, mock_open

from src.entity_detection.pubtator_client import PubTatorClient
from src.config.settings import Settings


@pytest.fixture
def sample_pubtator_response():
    """Sample PubTator API response."""
    return {
        "text": "Figure 2. Cardiac differentiation of human pluripotent stem cells.",
        "denotations": [
            {
                "id": "1",
                "span": {
                    "begin": 8,
                    "end": 15
                },
                "obj": "Disease",
                "text": "Cardiac"
            },
            {
                "id": "2",
                "span": {
                    "begin": 31,
                    "end": 36
                },
                "obj": "Species",
                "text": "human"
            },
            {
                "id": "3",
                "span": {
                    "begin": 37,
                    "end": 60
                },
                "obj": "CellLine",
                "text": "pluripotent stem cells"
            }
        ]
    }


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = MagicMock(spec=Settings)
    settings.pubtator3_url = "https://example.com/pubtator3/api/v1"
    settings.pubtator3_rate_limit = 30
    settings.retry_limit = 3
    settings.retry_delay = 1
    return settings


@pytest.fixture
def pubtator_client(mock_settings):
    """Create a PubTator client with mock settings."""
    with patch("src.entity_detection.pubtator_client.get_settings", return_value=mock_settings):
        client = PubTatorClient()
        return client


class TestPubTatorClient:
    """Tests for the PubTator client."""
    
    def test_init(self, pubtator_client, mock_settings):
        """Test client initialization."""
        assert pubtator_client.base_url == mock_settings.pubtator3_url
        assert pubtator_client.retry_limit == mock_settings.retry_limit
        assert pubtator_client.retry_delay == mock_settings.retry_delay
    
    @patch("httpx.Client.post")
    def test_detect_entities_success(self, mock_post, pubtator_client, sample_pubtator_response):
        """Test successful entity detection."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_pubtator_response
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call method
        text = "Figure 2. Cardiac differentiation of human pluripotent stem cells."
        result = pubtator_client.detect_entities(text)
        
        # Verify results
        assert len(result) == 3
        assert result[0]["entity_text"] == "Cardiac"
        assert result[0]["entity_type"] == "Disease"
        assert result[0]["start_position"] == 8
        assert result[0]["end_position"] == 15
        
        # Verify API call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["text"] == text
    
    @patch("httpx.Client.post")
    def test_detect_entities_with_entity_types(self, mock_post, pubtator_client, sample_pubtator_response):
        """Test entity detection with specific entity types."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_pubtator_response
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call method with specific entity types
        text = "Figure 2. Cardiac differentiation of human pluripotent stem cells."
        entity_types = ["Gene", "Disease"]
        result = pubtator_client.detect_entities(text, entity_types)
        
        # Verify API call includes entity types
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["text"] == text
        assert kwargs["json"]["concepts"] == entity_types
    
    @patch("httpx.Client.post")
    def test_detect_entities_http_error(self, mock_post, pubtator_client):
        """Test handling of HTTP errors."""
        # Mock HTTP error
        mock_post.side_effect = httpx.HTTPStatusError(
            "404 Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            pubtator_client.detect_entities("Test text")
        
        assert "Resource not found" in str(excinfo.value)
    
    @patch("httpx.Client.post")
    def test_detect_entities_retry_success(self, mock_post, pubtator_client, sample_pubtator_response):
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
        mock_success_response.json.return_value = sample_pubtator_response
        mock_success_response.raise_for_status = MagicMock()
        
        mock_post.side_effect = [mock_error_response, mock_success_response]
        
        # Call method
        result = pubtator_client.detect_entities("Test text")
        
        # Verify results
        assert len(result) == 3
        assert mock_post.call_count == 2
    
    @patch("httpx.Client.post")
    def test_detect_entities_empty_text(self, mock_post, pubtator_client):
        """Test handling of empty text."""
        # Call method with empty text
        result = pubtator_client.detect_entities("")
        
        # Verify no API call and empty result
        mock_post.assert_not_called()
        assert result == []
    
    @patch("httpx.Client.post")
    def test_detect_entities_no_entities_found(self, mock_post, pubtator_client):
        """Test handling of text with no entities."""
        # Mock response with no entities
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "text": "Figure 2. No entities here.",
            "denotations": []
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call method
        result = pubtator_client.detect_entities("Figure 2. No entities here.")
        
        # Verify empty result
        assert result == []
    
    @patch("httpx.Client.get")
    def test_check_availability(self, mock_get, pubtator_client):
        """Test checking API availability."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        result = pubtator_client.check_availability()
        
        # Verify result
        assert result is True
        mock_get.assert_called_once()
    
    @patch("httpx.Client.get")
    def test_check_availability_error(self, mock_get, pubtator_client):
        """Test checking API availability when API is down."""
        # Mock error
        mock_get.side_effect = httpx.HTTPStatusError(
            "503 Service Unavailable",
            request=MagicMock(),
            response=MagicMock(status_code=503)
        )
        
        # Call method
        result = pubtator_client.check_availability()
        
        # Verify result
        assert result is False
    
    def test_parse_entities(self, pubtator_client, sample_pubtator_response):
        """Test parsing entities from API response."""
        # Call method
        result = pubtator_client._parse_entities(sample_pubtator_response)
        
        # Verify results
        assert len(result) == 3
        assert result[0]["entity_text"] == "Cardiac"
        assert result[0]["entity_type"] == "Disease"
        assert result[0]["start_position"] == 8
        assert result[0]["end_position"] == 15
        assert "id" in result[0]
    
    def test_parse_entities_empty(self, pubtator_client):
        """Test parsing empty entity response."""
        # Call method with empty response
        result = pubtator_client._parse_entities({"text": "Test", "denotations": []})
        
        # Verify empty result
        assert result == []
    
    def test_parse_entities_missing_fields(self, pubtator_client):
        """Test parsing response with missing fields."""
        # Response with missing fields
        response = {
            "text": "Test",
            "denotations": [
                {
                    "id": "1",
                    # Missing span
                    "obj": "Disease",
                    "text": "Cardiac"
                }
            ]
        }
        
        # Call method and expect exception
        with pytest.raises(KeyError):
            pubtator_client._parse_entities(response)
    
    @patch("src.entity_detection.pubtator_client.RateLimiter")
    def test_rate_limiting(self, mock_rate_limiter_class, mock_settings):
        """Test rate limiting configuration."""
        # Create mock rate limiter
        mock_rate_limiter = MagicMock()
        mock_rate_limiter_class.return_value = mock_rate_limiter
        
        # Create client
        with patch("src.entity_detection.pubtator_client.get_settings", return_value=mock_settings):
            client = PubTatorClient()
        
        # Verify rate limiter configuration
        mock_rate_limiter_class.assert_called_once_with(mock_settings.pubtator3_rate_limit)
        
        # Mock HTTP response
        with patch("httpx.Client.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"text": "Test", "denotations": []}
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            
            # Call method
            client.detect_entities("Test text")
            
            # Verify rate limiter was used
            mock_rate_limiter.wait.assert_called_once()


class TestEntityDetectionIntegration:
    """Integration tests for entity detection."""
    
    @patch("httpx.Client.post")
    def test_detect_entities_integration(self, mock_post, pubtator_client):
        """Test entity detection with realistic data."""
        # Load sample response from file
        with patch("builtins.open", mock_open(read_data=json.dumps({
            "text": "Figure 2. Cardiac differentiation of human pluripotent stem cells. GATA4 and NKX2-5 are key transcription factors.",
            "denotations": [
                {
                    "id": "1",
                    "span": {"begin": 8, "end": 15},
                    "obj": "Disease",
                    "text": "Cardiac"
                },
                {
                    "id": "2",
                    "span": {"begin": 31, "end": 36},
                    "obj": "Species",
                    "text": "human"
                },
                {
                    "id": "3",
                    "span": {"begin": 37, "end": 60},
                    "obj": "CellLine",
                    "text": "pluripotent stem cells"
                },
                {
                    "id": "4",
                    "span": {"begin": 62, "end": 67},
                    "obj": "Gene",
                    "text": "GATA4"
                },
                {
                    "id": "5",
                    "span": {"begin": 72, "end": 78},
                    "obj": "Gene",
                    "text": "NKX2-5"
                }
            ]
        }))):
            # Mock response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = json.load(open("dummy_path"))
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            
            # Call method
            text = "Figure 2. Cardiac differentiation of human pluripotent stem cells. GATA4 and NKX2-5 are key transcription factors."
            result = pubtator_client.detect_entities(text)
            
            # Verify results
            assert len(result) == 5
            
            # Check gene entities
            gene_entities = [e for e in result if e["entity_type"] == "Gene"]
            assert len(gene_entities) == 2
            assert "GATA4" in [e["entity_text"] for e in gene_entities]
            assert "NKX2-5" in [e["entity_text"] for e in gene_entities]
            
            # Check disease entities
            disease_entities = [e for e in result if e["entity_type"] == "Disease"]
            assert len(disease_entities) == 1
            assert disease_entities[0]["entity_text"] == "Cardiac"
    
    def test_entity_type_filtering(self, pubtator_client):
        """Test filtering entities by type."""
        # Sample entities
        entities = [
            {"id": "1", "entity_text": "GATA4", "entity_type": "Gene"},
            {"id": "2", "entity_text": "Cardiac", "entity_type": "Disease"},
            {"id": "3", "entity_text": "human", "entity_type": "Species"},
            {"id": "4", "entity_text": "NKX2-5", "entity_type": "Gene"}
        ]
        
        # Mock detect_entities to return sample entities
        pubtator_client.detect_entities = MagicMock(return_value=entities)
        
        # Call method with Gene filter
        result = pubtator_client.detect_entities("Test text", entity_types=["Gene"])
        
        # Verify API call includes entity types
        pubtator_client.detect_entities.assert_called_once_with("Test text", entity_types=["Gene"])