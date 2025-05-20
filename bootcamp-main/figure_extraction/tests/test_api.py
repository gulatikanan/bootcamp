import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import uuid

from src.api.main import app
from src.models.database import Paper, Figure, Entity, Job
from src.storage.storage_service import StorageService

# Create test client
client = TestClient(app)

# Mock API key for testing
TEST_API_KEY = "test_api_key_12345"
TEST_HEADERS = {"X-API-Key": TEST_API_KEY}

# Sample data for tests
SAMPLE_PAPER_ID = "PMC6267067"
SAMPLE_FIGURE_ID = "fig_12345"
SAMPLE_JOB_ID = "job_54321"


@pytest.fixture
def mock_storage_service():
    """Fixture to create a mock storage service."""
    mock_service = MagicMock(spec=StorageService)
    
    # Mock paper data
    mock_paper = Paper(
        id=SAMPLE_PAPER_ID,
        title="Test Paper Title",
        abstract="Test paper abstract for testing purposes.",
        processed_date="2023-05-19T14:30:45",
        source="PMC",
        status="completed",
        error_message=None
    )
    
    # Mock figure data
    mock_figure = Figure(
        id=SAMPLE_FIGURE_ID,
        paper_id=SAMPLE_PAPER_ID,
        figure_number=1,
        caption="Figure 1. Test caption with GATA4 gene mention.",
       
    )
    
    # Mock entity data
    mock_entity = Entity(
        id="ent_67890",
        figure_id=SAMPLE_FIGURE_ID,
        entity_text="GATA4",
        entity_type="Gene",
        start_position=28,
        end_position=33,
        external_id="2626"
    )
    
    # Mock job data
    mock_job = Job(
        id=SAMPLE_JOB_ID,
        job_type="paper_processing",
        status="completed",
        created_at="2023-05-19T14:25:30",
        completed_at="2023-05-19T14:30:45",
        paper_ids=[SAMPLE_PAPER_ID],
        total_papers=1,
        processed_papers=1,
        failed_papers=0
    )
    
    # Configure mock methods
    mock_service.get_paper.return_value = mock_paper
    mock_service.get_papers.return_value = [mock_paper]
    mock_service.get_figure.return_value = mock_figure
    mock_service.get_figures.return_value = [mock_figure]
    mock_service.get_figures_by_paper.return_value = [mock_figure]
    mock_service.get_entity.return_value = mock_entity
    mock_service.get_entities.return_value = [mock_entity]
    mock_service.get_entities_by_figure.return_value = [mock_entity]
    mock_service.get_job.return_value = mock_job
    mock_service.get_jobs.return_value = [mock_job]
    mock_service.create_job.return_value = mock_job
    mock_service.update_job.return_value = mock_job
    mock_service.count_papers.return_value = 1
    mock_service.count_figures.return_value = 1
    mock_service.count_entities.return_value = 1
    
    return mock_service


@pytest.fixture
def mock_auth_service():
    """Fixture to mock the authentication service."""
    with patch("src.api.main.authenticate_api_key") as mock_auth:
        mock_auth.return_value = {"user_id": "test_user", "role": "admin"}
        yield mock_auth


class TestAuthEndpoints:
    """Tests for authentication endpoints."""
    
    def test_get_token_valid_credentials(self, mock_auth_service):
        """Test getting a token with valid credentials."""
        response = client.post(
            "/api/v1/auth/token",
            json={"username": "test_user", "password": "test_password"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    def test_get_token_invalid_credentials(self, mock_auth_service):
        """Test getting a token with invalid credentials."""
        mock_auth_service.return_value = None
        response = client.post(
            "/api/v1/auth/token",
            json={"username": "invalid_user", "password": "invalid_password"}
        )
        assert response.status_code == 401
        assert "detail" in response.json()


class TestPaperEndpoints:
    """Tests for paper-related endpoints."""
    
    @patch("src.api.main.get_storage_service")
    def test_submit_papers(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test submitting papers for processing."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.post(
            "/api/v1/papers",
            headers=TEST_HEADERS,
            json={"paper_ids": [SAMPLE_PAPER_ID]}
        )
        
        assert response.status_code == 202
        assert "job_id" in response.json()
        assert response.json()["job_id"] == SAMPLE_JOB_ID
        mock_storage_service.create_job.assert_called_once_with(
            "paper_processing", [SAMPLE_PAPER_ID]
        )
    
    @patch("src.api.main.get_storage_service")
    def test_get_papers(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a list of papers."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/papers",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert "items" in response.json()
        assert "total" in response.json()
        assert len(response.json()["items"]) == 1
        assert response.json()["items"][0]["id"] == SAMPLE_PAPER_ID
        mock_storage_service.get_papers.assert_called_once()
    
    @patch("src.api.main.get_storage_service")
    def test_get_paper(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a specific paper."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            f"/api/v1/papers/{SAMPLE_PAPER_ID}",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.json()["id"] == SAMPLE_PAPER_ID
        assert "title" in response.json()
        assert "abstract" in response.json()
        mock_storage_service.get_paper.assert_called_once_with(SAMPLE_PAPER_ID)
    
    @patch("src.api.main.get_storage_service")
    def test_get_paper_not_found(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a non-existent paper."""
        mock_get_storage.return_value = mock_storage_service
        mock_storage_service.get_paper.return_value = None
        
        response = client.get(
            "/api/v1/papers/nonexistent",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 404
        assert "detail" in response.json()
    
    @patch("src.api.main.get_storage_service")
    def test_get_paper_figures(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting figures for a specific paper."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            f"/api/v1/papers/{SAMPLE_PAPER_ID}/figures",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == SAMPLE_FIGURE_ID
        assert response.json()[0]["paper_id"] == SAMPLE_PAPER_ID
        mock_storage_service.get_figures_by_paper.assert_called_once_with(SAMPLE_PAPER_ID)


class TestFigureEndpoints:
    """Tests for figure-related endpoints."""
    
    @patch("src.api.main.get_storage_service")
    def test_get_figures(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a list of figures."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/figures",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert "items" in response.json()
        assert "total" in response.json()
        assert len(response.json()["items"]) == 1
        assert response.json()["items"][0]["id"] == SAMPLE_FIGURE_ID
        mock_storage_service.get_figures.assert_called_once()
    
    @patch("src.api.main.get_storage_service")
    def test_get_figure(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a specific figure."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            f"/api/v1/figures/{SAMPLE_FIGURE_ID}",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.json()["id"] == SAMPLE_FIGURE_ID
        assert "caption" in response.json()
        assert "url" in response.json()
        mock_storage_service.get_figure.assert_called_once_with(SAMPLE_FIGURE_ID)
    
    @patch("src.api.main.get_storage_service")
    def test_get_figure_not_found(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a non-existent figure."""
        mock_get_storage.return_value = mock_storage_service
        mock_storage_service.get_figure.return_value = None
        
        response = client.get(
            "/api/v1/figures/nonexistent",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 404
        assert "detail" in response.json()
    
    @patch("src.api.main.get_storage_service")
    def test_get_figure_entities(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting entities for a specific figure."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            f"/api/v1/figures/{SAMPLE_FIGURE_ID}/entities",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
        assert response.json()[0]["entity_text"] == "GATA4"
        assert response.json()[0]["entity_type"] == "Gene"
        mock_storage_service.get_entities_by_figure.assert_called_once_with(SAMPLE_FIGURE_ID)


class TestEntityEndpoints:
    """Tests for entity-related endpoints."""
    
    @patch("src.api.main.get_storage_service")
    def test_get_entities(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a list of entities."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/entities",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert "items" in response.json()
        assert "total" in response.json()
        assert len(response.json()["items"]) == 1
        assert response.json()["items"][0]["entity_text"] == "GATA4"
        mock_storage_service.get_entities.assert_called_once()
    
    @patch("src.api.main.get_storage_service")
    def test_get_entities_by_type(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting entities of a specific type."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/entities/Gene",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert "items" in response.json()
        assert "total" in response.json()
        assert len(response.json()["items"]) == 1
        assert response.json()["items"][0]["entity_type"] == "Gene"
        mock_storage_service.get_entities.assert_called_once_with(entity_type="Gene", skip=0, limit=10)


class TestJobEndpoints:
    """Tests for job-related endpoints."""
    
    @patch("src.api.main.get_storage_service")
    def test_get_jobs(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a list of jobs."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/jobs",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert "items" in response.json()
        assert "total" in response.json()
        assert len(response.json()["items"]) == 1
        assert response.json()["items"][0]["id"] == SAMPLE_JOB_ID
        mock_storage_service.get_jobs.assert_called_once()
    
    @patch("src.api.main.get_storage_service")
    def test_get_job(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a specific job."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            f"/api/v1/jobs/{SAMPLE_JOB_ID}",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.json()["id"] == SAMPLE_JOB_ID
        assert "status" in response.json()
        assert "job_type" in response.json()
        mock_storage_service.get_job.assert_called_once_with(SAMPLE_JOB_ID)
    
    @patch("src.api.main.get_storage_service")
    def test_get_job_not_found(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting a non-existent job."""
        mock_get_storage.return_value = mock_storage_service
        mock_storage_service.get_job.return_value = None
        
        response = client.get(
            "/api/v1/jobs/nonexistent",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 404
        assert "detail" in response.json()
    
    @patch("src.api.main.get_storage_service")
    def test_cancel_job(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test cancelling a job."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.post(
            f"/api/v1/jobs/{SAMPLE_JOB_ID}/cancel",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.json()["id"] == SAMPLE_JOB_ID
        assert "status" in response.json()
        mock_storage_service.update_job.assert_called_once_with(
            SAMPLE_JOB_ID, {"status": "cancelled"}
        )


class TestExportEndpoints:
    """Tests for export-related endpoints."""
    
    @patch("src.api.main.get_storage_service")
    def test_export_papers_json(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test exporting papers as JSON."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/export/papers?format=json",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == SAMPLE_PAPER_ID
    
    @patch("src.api.main.get_storage_service")
    def test_export_papers_csv(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test exporting papers as CSV."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/export/papers?format=csv",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/csv"
        assert "id,title,abstract" in response.text
        assert SAMPLE_PAPER_ID in response.text
    
    @patch("src.api.main.get_storage_service")
    def test_export_figures_json(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test exporting figures as JSON."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/export/figures?format=json",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == SAMPLE_FIGURE_ID
    
    @patch("src.api.main.get_storage_service")
    def test_export_entities_json(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test exporting entities as JSON."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/export/entities?format=json",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["entity_text"] == "GATA4"


class TestAdminEndpoints:
    """Tests for admin-related endpoints."""
    
    @patch("src.api.main.get_config")
    def test_get_config(self, mock_get_config, mock_auth_service):
        """Test getting the current configuration."""
        mock_get_config.return_value = {
            "app_name": "Scientific Publication Data Extraction",
            "environment": "testing",
            "log_level": "INFO"
        }
        
        response = client.get(
            "/api/v1/admin/config",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert "app_name" in response.json()
        assert "environment" in response.json()
        assert response.json()["environment"] == "testing"
    
    @patch("src.api.main.update_config")
    def test_update_config(self, mock_update_config, mock_auth_service):
        """Test updating the configuration."""
        mock_update_config.return_value = {
            "app_name": "Scientific Publication Data Extraction",
            "environment": "production",
            "log_level": "WARNING"
        }
        
        response = client.put(
            "/api/v1/admin/config",
            headers=TEST_HEADERS,
            json={"environment": "production", "log_level": "WARNING"}
        )
        
        assert response.status_code == 200
        assert "environment" in response.json()
        assert response.json()["environment"] == "production"
        assert response.json()["log_level"] == "WARNING"
        mock_update_config.assert_called_once_with({"environment": "production", "log_level": "WARNING"})
    
    @patch("src.api.main.get_storage_service")
    def test_get_stats(self, mock_get_storage, mock_storage_service, mock_auth_service):
        """Test getting system statistics."""
        mock_get_storage.return_value = mock_storage_service
        
        response = client.get(
            "/api/v1/admin/stats",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        assert "papers_count" in response.json()
        assert "figures_count" in response.json()
        assert "entities_count" in response.json()
        assert response.json()["papers_count"] == 1
        assert response.json()["figures_count"] == 1
        assert response.json()["entities_count"] == 1