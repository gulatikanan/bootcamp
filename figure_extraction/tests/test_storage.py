import pytest
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.storage.storage_service import StorageService
from src.models.database import Paper, Figure, Entity, Job


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    db = MagicMock(spec=Session)
    return db


@pytest.fixture
def storage_service(mock_db):
    """Create a storage service with a mock database."""
    return StorageService(mock_db)


@pytest.fixture
def sample_paper():
    """Create a sample paper object."""
    return Paper(
        id="PMC6267067",
        title="Test Paper Title",
        abstract="Test paper abstract for testing purposes.",
        processed_date=datetime.now(),
        source="PMC",
        status="completed",
        error_message=None
    )


@pytest.fixture
def sample_figure():
    """Create a sample figure object."""
    return Figure(
        id="fig_12345",
        paper_id="PMC6267067",
        figure_number=1,
        caption="Figure 1. Test caption with GATA4 gene mention.",
        url="https://example.com/figure1.jpg"
    )


@pytest.fixture
def sample_entity():
    """Create a sample entity object."""
    return Entity(
        id="ent_67890",
        figure_id="fig_12345",
        entity_text="GATA4",
        entity_type="Gene",
        start_position=28,
        end_position=33,
        external_id="2626"
    )


@pytest.fixture
def sample_job():
    """Create a sample job object."""
    return Job(
        id="job_54321",
        job_type="paper_processing",
        status="completed",
        created_at=datetime.now(),
        completed_at=datetime.now(),
        paper_ids=["PMC6267067"],
        total_papers=1,
        processed_papers=1,
        failed_papers=0
    )


class TestStorageService:
    """Tests for the storage service."""
    
    def test_init(self, mock_db):
        """Test service initialization."""
        service = StorageService(mock_db)
        assert service.db == mock_db
    
    def test_create_paper(self, storage_service, mock_db):
        """Test creating a paper."""
        # Prepare test data
        paper_data = {
            "id": "PMC6267067",
            "title": "Test Paper Title",
            "abstract": "Test paper abstract for testing purposes.",
            "source": "PMC"
        }
        
        # Call method
        result = storage_service.create_paper(paper_data)
        
        # Verify result
        assert result.id == paper_data["id"]
        assert result.title == paper_data["title"]
        assert result.abstract == paper_data["abstract"]
        assert result.source == paper_data["source"]
        assert result.status == "pending"  # Default status
        
        # Verify database operations
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)
    
    def test_create_paper_with_existing_id(self, storage_service, mock_db, sample_paper):
        """Test creating a paper with an existing ID."""
        # Mock get_paper to return existing paper
        storage_service.get_paper = MagicMock(return_value=sample_paper)
        
        # Prepare test data
        paper_data = {
            "id": "PMC6267067",
            "title": "Updated Paper Title",
            "abstract": "Updated abstract.",
            "source": "PMC"
        }
        
        # Call method
        result = storage_service.create_paper(paper_data)
        
        # Verify result is the existing paper
        assert result == sample_paper
        
        # Verify no database operations
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called()
    
    def test_get_paper(self, storage_service, mock_db, sample_paper):
        """Test getting a paper by ID."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = sample_paper
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_paper("PMC6267067")
        
        # Verify result
        assert result == sample_paper
        
        # Verify query
        mock_db.query.assert_called_once_with(Paper)
        mock_query.filter_by.assert_called_once_with(id="PMC6267067")
    
    def test_get_paper_not_found(self, storage_service, mock_db):
        """Test getting a non-existent paper."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_paper("nonexistent")
        
        # Verify result
        assert result is None
    
    def test_get_papers(self, storage_service, mock_db, sample_paper):
        """Test getting a list of papers."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.offset.return_value.limit.return_value.all.return_value = [sample_paper]
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_papers(skip=0, limit=10)
        
        # Verify result
        assert len(result) == 1
        assert result[0] == sample_paper
        
        # Verify query
        mock_db.query.assert_called_once_with(Paper)
        mock_query.offset.assert_called_once_with(0)
        mock_query.offset.return_value.limit.assert_called_once_with(10)
    
    def test_update_paper(self, storage_service, mock_db, sample_paper):
        """Test updating a paper."""
        # Mock get_paper to return existing paper
        storage_service.get_paper = MagicMock(return_value=sample_paper)
        
        # Prepare update data
        update_data = {
            "title": "Updated Paper Title",
            "status": "processing"
        }
        
        # Call method
        result = storage_service.update_paper("PMC6267067", update_data)
        
        # Verify result
        assert result.title == update_data["title"]
        assert result.status == update_data["status"]
        assert result.abstract == sample_paper.abstract  # Unchanged
        
        # Verify database operations
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)
    
    def test_update_paper_not_found(self, storage_service, mock_db):
        """Test updating a non-existent paper."""
        # Mock get_paper to return None
        storage_service.get_paper = MagicMock(return_value=None)
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            storage_service.update_paper("nonexistent", {"title": "Updated"})
        
        assert "Paper nonexistent not found" in str(excinfo.value)
        
        # Verify no database operations
        mock_db.commit.assert_not_called()
    
    def test_create_figure(self, storage_service, mock_db, sample_paper):
        """Test creating a figure."""
        # Mock get_paper to return existing paper
        storage_service.get_paper = MagicMock(return_value=sample_paper)
        
        # Prepare test data
        figure_data = {
            "figure_number": 1,
            "caption": "Figure 1. Test caption.",
            "url": "https://example.com/figure1.jpg"
        }
        
        # Mock uuid.uuid4
        with patch("uuid.uuid4", return_value=uuid.UUID("12345678-1234-5678-1234-567812345678")):
            # Call method
            result = storage_service.create_figure("PMC6267067", figure_data)
        
        # Verify result
        assert result.id == "12345678-1234-5678-1234-567812345678"
        assert result.paper_id == "PMC6267067"
        assert result.figure_number == figure_data["figure_number"]
        assert result.caption == figure_data["caption"]
        assert result.url == figure_data["url"]
        
        # Verify database operations
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)
    
    def test_create_figure_paper_not_found(self, storage_service, mock_db):
        """Test creating a figure for a non-existent paper."""
        # Mock get_paper to return None
        storage_service.get_paper = MagicMock(return_value=None)
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            storage_service.create_figure("nonexistent", {"figure_number": 1})
        
        assert "Paper nonexistent not found" in str(excinfo.value)
        
        # Verify no database operations
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called()
    
    def test_get_figure(self, storage_service, mock_db, sample_figure):
        """Test getting a figure by ID."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = sample_figure
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_figure("fig_12345")
        
        # Verify result
        assert result == sample_figure
        
        # Verify query
        mock_db.query.assert_called_once_with(Figure)
        mock_query.filter_by.assert_called_once_with(id="fig_12345")
    
    def test_get_figures_by_paper(self, storage_service, mock_db, sample_figure):
        """Test getting figures for a specific paper."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.all.return_value = [sample_figure]
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_figures_by_paper("PMC6267067")
        
        # Verify result
        assert len(result) == 1
        assert result[0] == sample_figure
        
        # Verify query
        mock_db.query.assert_called_once_with(Figure)
        mock_query.filter_by.assert_called_once_with(paper_id="PMC6267067")
    
    def test_create_entity(self, storage_service, mock_db, sample_figure):
        """Test creating an entity."""
        # Mock get_figure to return existing figure
        storage_service.get_figure = MagicMock(return_value=sample_figure)
        
        # Prepare test data
        entity_data = {
            "entity_text": "GATA4",
            "entity_type": "Gene",
            "start_position": 28,
            "end_position": 33,
            "external_id": "2626"
        }
        
        # Mock uuid.uuid4
        with patch("uuid.uuid4", return_value=uuid.UUID("87654321-8765-4321-8765-432187654321")):
            # Call method
            result = storage_service.create_entity("fig_12345", entity_data)
        
        # Verify result
        assert result.id == "87654321-8765-4321-8765-432187654321"
        assert result.figure_id == "fig_12345"
        assert result.entity_text == entity_data["entity_text"]
        assert result.entity_type == entity_data["entity_type"]
        assert result.start_position == entity_data["start_position"]
        assert result.end_position == entity_data["end_position"]
        assert result.external_id == entity_data["external_id"]
        
        # Verify database operations
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)
    
    def test_create_entity_figure_not_found(self, storage_service, mock_db):
        """Test creating an entity for a non-existent figure."""
        # Mock get_figure to return None
        storage_service.get_figure = MagicMock(return_value=None)
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            storage_service.create_entity("nonexistent", {"entity_text": "GATA4"})
        
        assert "Figure nonexistent not found" in str(excinfo.value)
        
        # Verify no database operations
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called()
    
    def test_get_entities_by_figure(self, storage_service, mock_db, sample_entity):
        """Test getting entities for a specific figure."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.all.return_value = [sample_entity]
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_entities_by_figure("fig_12345")
        
        # Verify result
        assert len(result) == 1
        assert result[0] == sample_entity
        
        # Verify query
        mock_db.query.assert_called_once_with(Entity)
        mock_query.filter_by.assert_called_once_with(figure_id="fig_12345")
    
    def test_get_entities_by_type(self, storage_service, mock_db, sample_entity):
        """Test getting entities of a specific type."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.offset.return_value.limit.return_value.all.return_value = [sample_entity]
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_entities(entity_type="Gene", skip=0, limit=10)
        
        # Verify result
        assert len(result) == 1
        assert result[0] == sample_entity
        
        # Verify query
        mock_db.query.assert_called_once_with(Entity)
        mock_query.filter_by.assert_called_once_with(entity_type="Gene")
        mock_query.filter_by.return_value.offset.assert_called_once_with(0)
        mock_query.filter_by.return_value.offset.return_value.limit.assert_called_once_with(10)
    
    def test_create_job(self, storage_service, mock_db):
        """Test creating a job."""
        # Prepare test data
        paper_ids = ["PMC6267067", "PMC6267068"]
        job_type = "paper_processing"
        
        # Mock uuid.uuid4
        with patch("uuid.uuid4", return_value=uuid.UUID("54321098-5432-1098-5432-109854321098")):
            # Call method
            result = storage_service.create_job(job_type, paper_ids)
        
        # Verify result
        assert result.id == "54321098-5432-1098-5432-109854321098"
        assert result.job_type == job_type
        assert result.status == "queued"
        assert result.paper_ids == paper_ids
        assert result.total_papers == 2
        assert result.processed_papers == 0
        assert result.failed_papers == 0
        
        # Verify database operations
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)
    
    def test_get_job(self, storage_service, mock_db, sample_job):
        """Test getting a job by ID."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = sample_job
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.get_job("job_54321")
        
        # Verify result
        assert result == sample_job
        
        # Verify query
        mock_db.query.assert_called_once_with(Job)
        mock_query.filter_by.assert_called_once_with(id="job_54321")
    
    def test_update_job(self, storage_service, mock_db, sample_job):
        """Test updating a job."""
        # Mock get_job to return existing job
        storage_service.get_job = MagicMock(return_value=sample_job)
        
        # Prepare update data
        update_data = {
            "status": "processing",
            "processed_papers": 1
        }
        
        # Call method
        result = storage_service.update_job("job_54321", update_data)
        
        # Verify result
        assert result.status == update_data["status"]
        assert result.processed_papers == update_data["processed_papers"]
        
        # Verify database operations
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)
    
    def test_update_job_not_found(self, storage_service, mock_db):
        """Test updating a non-existent job."""
        # Mock get_job to return None
        storage_service.get_job = MagicMock(return_value=None)
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            storage_service.update_job("nonexistent", {"status": "processing"})
        
        assert "Job nonexistent not found" in str(excinfo.value)
        
        # Verify no database operations
        mock_db.commit.assert_not_called()
    
    def test_count_papers(self, storage_service, mock_db):
        """Test counting papers."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.count.return_value = 10
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.count_papers()
        
        # Verify result
        assert result == 10
        
        # Verify query
        mock_db.query.assert_called_once_with(Paper)
        mock_query.count.assert_called_once()
    
    def test_count_figures(self, storage_service, mock_db):
        """Test counting figures."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.count.return_value = 20
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.count_figures()
        
        # Verify result
        assert result == 20
        
        # Verify query
        mock_db.query.assert_called_once_with(Figure)
        mock_query.count.assert_called_once()
    
    def test_count_entities(self, storage_service, mock_db):
        """Test counting entities."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.count.return_value = 30
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.count_entities()
        
        # Verify result
        assert result == 30
        
        # Verify query
        mock_db.query.assert_called_once_with(Entity)
        mock_query.count.assert_called_once()
    
    def test_count_entities_by_type(self, storage_service, mock_db):
        """Test counting entities of a specific type."""
        # Mock query result
        mock_query = MagicMock()
        mock_query.filter_by.return_value.count.return_value = 15
        mock_db.query.return_value = mock_query
        
        # Call method
        result = storage_service.count_entities(entity_type="Gene")
        
        # Verify result
        assert result == 15
        
        # Verify query
        mock_db.query.assert_called_once_with(Entity)
        mock_query.filter_by.assert_called_once_with(entity_type="Gene")
        mock_query.filter_by.return_value.count.assert_called_once()
    
    def test_database_error_handling(self, storage_service, mock_db):
        """Test handling of database errors."""
        # Mock database error
        mock_db.commit.side_effect = SQLAlchemyError("Database error")
        
        # Prepare test data
        paper_data = {
            "id": "PMC6267067",
            "title": "Test Paper Title",
            "abstract": "Test paper abstract for testing purposes.",
            "source": "PMC"
        }
        
        # Call method and expect exception
        with pytest.raises(SQLAlchemyError) as excinfo:
            storage_service.create_paper(paper_data)
        
        assert "Database error" in str(excinfo.value)
        
        # Verify rollback was called
        mock_db.rollback.assert_called_once()
    
    def test_close(self, storage_service, mock_db):
        """Test closing the database connection."""
        # Call method
        storage_service.close()
        
        # Verify database operations
        mock_db.close.assert_called_once()


class TestStorageServiceIntegration:
    """Integration tests for storage service."""
    
    def test_paper_figure_entity_relationship(self, storage_service, mock_db):
        """Test the relationship between papers, figures, and entities."""
        # Create paper
        paper_data = {
            "id": "PMC6267067",
            "title": "Test Paper Title",
            "abstract": "Test abstract",
            "source": "PMC"
        }
        paper = Paper(**paper_data, status="completed", processed_date=datetime.now())
        
        # Create figure
        figure_data = {
            "id": "fig_12345",
            "paper_id": "PMC6267067",
            "figure_number": 1,
            "caption": "Figure 1. Test caption with GATA4 gene mention.",
            "url": "https://example.com/figure1.jpg"
        }
        figure = Figure(**figure_data)
        
        # Create entity
        entity_data = {
            "id": "ent_67890",
            "figure_id": "fig_12345",
            "entity_text": "GATA4",
            "entity_type": "Gene",
            "start_position": 28,
            "end_position": 33,
            "external_id": "2626"
        }
        entity = Entity(**entity_data)
        
        # Set up relationships
        paper.figures = [figure]
        figure.entities = [entity]
        
        # Mock get_paper to return our paper with relationships
        storage_service.get_paper = MagicMock(return_value=paper)
        
        # Get paper with relationships
        result = storage_service.get_paper("PMC6267067")
        
        # Verify relationships
        assert len(result.figures) == 1
        assert result.figures[0].id == "fig_12345"
        assert len(result.figures[0].entities) == 1
        assert result.figures[0].entities[0].entity_text == "GATA4"
    
    def test_full_paper_processing_workflow(self, storage_service, mock_db):
        """Test the full workflow of processing a paper."""
        # Mock methods to simulate workflow
        with patch.object(storage_service, "create_paper") as mock_create_paper, \
             patch.object(storage_service, "create_figure") as mock_create_figure, \
             patch.object(storage_service, "create_entity") as mock_create_entity, \
             patch.object(storage_service, "create_job") as mock_create_job, \
             patch.object(storage_service, "update_job") as mock_update_job, \
             patch.object(storage_service, "update_paper") as mock_update_paper:
            
            # Set up mock returns
            mock_create_paper.return_value = Paper(id="PMC6267067", status="pending")
            mock_create_figure.return_value = Figure(id="fig_12345", paper_id="PMC6267067")
            mock_create_entity.return_value = Entity(id="ent_67890", figure_id="fig_12345")
            mock_create_job.return_value = Job(id="job_54321", status="queued")
            mock_update_job.return_value = Job(id="job_54321", status="completed")
            mock_update_paper.return_value = Paper(id="PMC6267067", status="completed")
            
            # Simulate workflow
            
            # 1. Create job
            job = storage_service.create_job("paper_processing", ["PMC6267067"])
            
            # 2. Update job to processing
            storage_service.update_job(job.id, {"status": "processing"})
            
            # 3. Create paper
            paper = storage_service.create_paper({
                "id": "PMC6267067",
                "title": "Test Paper Title",
                "abstract": "Test abstract",
                "source": "PMC"
            })
            
            # 4. Update paper to processing
            storage_service.update_paper(paper.id, {"status": "processing"})
            
            # 5. Create figure
            figure = storage_service.create_figure(paper.id, {
                "figure_number": 1,
                "caption": "Figure 1. Test caption with GATA4 gene mention.",
                "url": "https://example.com/figure1.jpg"
            })
            
            # 6. Create entity
            entity = storage_service.create_entity(figure.id, {
                "entity_text": "GATA4",
                "entity_type": "Gene",
                "start_position": 28,
                "end_position": 33,
                "external_id": "2626"
            })
            
            # 7. Update paper to completed
            storage_service.update_paper(paper.id, {"status": "completed"})
            
            # 8. Update job to completed
            storage_service.update_job(job.id, {
                "status": "completed",
                "processed_papers": 1
            })
            
            # Verify all methods were called
            mock_create_job.assert_called_once()
            mock_update_job.assert_called()
            mock_create_paper.assert_called_once()
            mock_update_paper.assert_called()
            mock_create_figure.assert_called_once()
            mock_create_entity.assert_called_once()


## 4. Extraction Service Tests

```python project="Scientific Publication Data Extraction" file="tests/test_extraction_service.py" type="code"
import pytest
import json
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime

from src.extraction.extraction_service import ExtractionService
from src.extraction.bioc_client import BioCClient
from src.entity_detection.pubtator_client import PubTatorClient
from src.storage.storage_service import StorageService
from src.models.database import Paper, Figure, Entity


@pytest.fixture
def mock_bioc_client():
    """Create a mock BioC client."""
    client = MagicMock(spec=BioCClient)
    return client


@pytest.fixture
def mock_pubtator_client():
    """Create a mock PubTator client."""
    client = MagicMock(spec=PubTatorClient)
    return client


@pytest.fixture
def mock_storage_service():
    """Create a mock storage service."""
    service = MagicMock(spec=StorageService)
    return service


@pytest.fixture
def extraction_service(mock_bioc_client, mock_pubtator_client, mock_storage_service):
    """Create an extraction service with mock dependencies."""
    return ExtractionService(
        db=None,  # Not used directly
        bioc_client=mock_bioc_client,
        pubtator_client=mock_pubtator_client,
        storage_service=mock_storage_service
    )


@pytest.fixture
def sample_paper_structure():
    """Sample paper structure from BioC client."""
    return {
        "paper_id": "PMC6267067",
        "title": "Test Paper Title",
        "abstract": "Test paper abstract for testing purposes.",
        "figures": [
            {
                "figure_id": "fig1",
                "figure_number": 1,
                "caption": "Figure 1. Test caption with GATA4 gene mention.",
                "url": "https://example.com/figure1.jpg"
            },
            {
                "figure_id": "fig2",
                "figure_number": 2,
                "caption": "Figure 2. Another test caption with NKX2-5 gene mention.",
                "url": "https://example.com/figure2.jpg"
            }
        ]
    }


@pytest.fixture
def sample_entities():
    """Sample entities from PubTator client."""
    return [
        {
            "entity_text": "GATA4",
            "entity_type": "Gene",
            "start_position": 28,
            "end_position": 33,
            "external_id": "2626"
        }
    ]


class TestExtractionService:
    """Tests for the extraction service."""
    
    def test_init(self, mock_bioc_client, mock_pubtator_client, mock_storage_service):
        """Test service initialization."""
        service = ExtractionService(
            db=None,
            bioc_client=mock_bioc_client,
            pubtator_client=mock_pubtator_client,
            storage_service=mock_storage_service
        )
        assert service.bioc_client == mock_bioc_client
        assert service.pubtator_client == mock_pubtator_client
        assert service.storage_service == mock_storage_service
    
    def test_init_with_db(self, mock_bioc_client, mock_pubtator_client, mock_storage_service):
        """Test service initialization with database session."""
        # Mock db session
        mock_db = MagicMock()
        
        # Mock storage service creation
        with patch("src.extraction.extraction_service.StorageService") as mock_storage_class:
            mock_storage_class.return_value = mock_storage_service
            
            # Create service
            service = ExtractionService(db=mock_db)
            
            # Verify storage service creation
            mock_storage_class.assert_called_once_with(mock_db)
            
            # Verify clients were created
            assert isinstance(service.bioc_client, BioCClient)
            assert isinstance(service.pubtator_client, PubTatorClient)
    
    def test_process_paper_success(self, extraction_service, mock_bioc_client, 
                                  mock_pubtator_client, mock_storage_service,
                                  sample_paper_structure, sample_entities):
        """Test successful paper processing."""
        # Mock client responses
        mock_bioc_client.get_paper_structure.return_value = sample_paper_structure
        mock_pubtator_client.detect_entities.return_value = sample_entities
        
        # Mock storage service responses
        mock_storage_service.get_paper.return_value = None  # Paper doesn't exist yet
        mock_storage_service.create_paper.return_value = Paper(
            id="PMC6267067",
            title="Test Paper Title",
            abstract="Test paper abstract for testing purposes.",
            status="processing"
        )
        mock_storage_service.create_figure.return_value = Figure(
            id="fig_12345",
            paper_id="PMC6267067",
            figure_number=1,
            caption="Figure 1. Test caption with GATA4 gene mention.",
            url="https://example.com/figure1.jpg"
        )
        mock_storage_service.create_entity.return_value = Entity(
            id="ent_67890",
            figure_id="fig_12345",
            entity_text="GATA4",
            entity_type="Gene",
            start_position=28,
            end_position=33,
            external_id="2626"
        )
        
        # Call method
        result = extraction_service.process_paper("PMC6267067")
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["status"] == "completed"
        assert result["figures_processed"] == 2
        
        # Verify client calls
        mock_bioc_client.get_paper_structure.assert_called_once_with("PMC6267067")
        assert mock_pubtator_client.detect_entities.call_count == 2  # Once for each figure
        
        # Verify storage service calls
        mock_storage_service.get_paper.assert_called_once_with("PMC6267067")
        mock_storage_service.create_paper.assert_called_once()
        assert mock_storage_service.create_figure.call_count == 2  # Once for each figure
        assert mock_storage_service.create_entity.call_count == 2  # Once for each figure (with one entity each)
        mock_storage_service.update_paper.assert_called_once_with(
            "PMC6267067", {"status": "completed", "processed_date": mock_storage_service.update_paper.call_args[0][1]["processed_date"]}
        )
    
    def test_process_paper_existing(self, extraction_service, mock_bioc_client, 
                                   mock_pubtator_client, mock_storage_service,
                                   sample_paper_structure, sample_entities):
        """Test processing an existing paper."""
        # Mock client responses
        mock_bioc_client.get_paper_structure.return_value = sample_paper_structure
        mock_pubtator_client.detect_entities.return_value = sample_entities
        
        # Mock storage service to return existing paper
        mock_storage_service.get_paper.return_value = Paper(
            id="PMC6267067",
            title="Existing Paper Title",
            abstract="Existing abstract",
            status="completed",
            processed_date=datetime.now()
        )
        
        # Call method
        result = extraction_service.process_paper("PMC6267067")
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["status"] == "skipped"
        assert "already processed" in result["message"]
        
        # Verify client calls
        mock_bioc_client.get_paper_structure.assert_not_called()
        mock_pubtator_client.detect_entities.assert_not_called()
        
        # Verify storage service calls
        mock_storage_service.get_paper.assert_called_once_with("PMC6267067")
        mock_storage_service.create_paper.assert_not_called()
        mock_storage_service.create_figure.assert_not_called()
        mock_storage_service.create_entity.assert_not_called()
        mock_storage_service.update_paper.assert_not_called()
    
    def test_process_paper_force_reprocess(self, extraction_service, mock_bioc_client, 
                                          mock_pubtator_client, mock_storage_service,
                                          sample_paper_structure, sample_entities):
        """Test forcing reprocessing of an existing paper."""
        # Mock client responses
        mock_bioc_client.get_paper_structure.return_value = sample_paper_structure
        mock_pubtator_client.detect_entities.return_value = sample_entities
        
        # Mock storage service to return existing paper
        mock_storage_service.get_paper.return_value = Paper(
            id="PMC6267067",
            title="Existing Paper Title",
            abstract="Existing abstract",
            status="completed",
            processed_date=datetime.now()
        )
        
        # Call method with force=True
        result = extraction_service.process_paper("PMC6267067", force=True)
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["status"] == "completed"
        assert result["figures_processed"] == 2
        
        # Verify client calls
        mock_bioc_client.get_paper_structure.assert_called_once_with("PMC6267067")
        assert mock_pubtator_client.detect_entities.call_count == 2  # Once for each figure
        
        # Verify storage service calls
        mock_storage_service.get_paper.assert_called_once_with("PMC6267067")
        mock_storage_service.update_paper.assert_called()  # Called to update paper status
        assert mock_storage_service.create_figure.call_count == 2  # Once for each figure
    
    def test_process_paper_bioc_error(self, extraction_service, mock_bioc_client, 
                                     mock_pubtator_client, mock_storage_service):
        """Test handling BioC client errors."""
        # Mock BioC client to raise error
        mock_bioc_client.get_paper_structure.side_effect = ValueError("API error")
        
        # Mock storage service
        mock_storage_service.get_paper.return_value = None  # Paper doesn't exist yet
        mock_storage_service.create_paper.return_value = Paper(
            id="PMC6267067",
            title=None,
            abstract=None,
            status="processing"
        )
        
        # Call method and expect exception
        with pytest.raises(ValueError) as excinfo:
            extraction_service.process_paper("PMC6267067")
        
        assert "API error" in str(excinfo.value)
        
        # Verify storage service calls
        mock_storage_service.get_paper.assert_called_once_with("PMC6267067")
        mock_storage_service.create_paper.assert_called_once()
        mock_storage_service.update_paper.assert_called_once_with(
            "PMC6267067", {"status": "failed", "error_message": "API error"}
        )
    
    def test_process_paper_pubtator_error(self, extraction_service, mock_bioc_client, 
                                         mock_pubtator_client, mock_storage_service,
                                         sample_paper_structure):
        """Test handling PubTator client errors."""
        # Mock client responses
        mock_bioc_client.get_paper_structure.return_value = sample_paper_structure
        mock_pubtator_client.detect_entities.side_effect = ValueError("API error")
        
        # Mock storage service
        mock_storage_service.get_paper.return_value = None  # Paper doesn't exist yet
        mock_storage_service.create_paper.return_value = Paper(
            id="PMC6267067",
            title="Test Paper Title",
            abstract="Test paper abstract for testing purposes.",
            status="processing"
        )
        mock_storage_service.create_figure.return_value = Figure(
            id="fig_12345",
            paper_id="PMC6267067",
            figure_number=1,
            caption="Figure 1. Test caption with GATA4 gene mention.",
            url="https://example.com/figure1.jpg"
        )
        
        # Call method
        with pytest.raises(ValueError) as excinfo:
            extraction_service.process_paper("PMC6267067")
        
        assert "API error" in str(excinfo.value)
        
        # Verify storage service calls
        mock_storage_service.update_paper.assert_called_with(
            "PMC6267067", {"status": "failed", "error_message": mock_storage_service.update_paper.call_args[0][1]["error_message"]}
        )
    
    def test_process_paper_normalize_id(self, extraction_service, mock_bioc_client):
        """Test normalizing paper ID."""
        # Call method with ID without PMC prefix
        with patch.object(extraction_service, "_process_paper_internal") as mock_process:
            mock_process.return_value = {"status": "completed"}
            extraction_service.process_paper("6267067")
        
        # Verify ID was normalized
        mock_bioc_client.get_paper_structure.assert_called_once_with("PMC6267067")
    
    def test_process_papers_batch(self, extraction_service):
        """Test processing a batch of papers."""
        # Mock process_paper method
        with patch.object(extraction_service, "process_paper") as mock_process:
            mock_process.side_effect = [
                {"paper_id": "PMC6267067", "status": "completed"},
                {"paper_id": "PMC6267068", "status": "completed"},
                {"paper_id": "PMC6267069", "status": "failed", "error_message": "Error"}
            ]
            
            # Call method
            results = extraction_service.process_papers(["PMC6267067", "PMC6267068", "PMC6267069"])
            
            # Verify results
            assert len(results) == 3
            assert results[0]["status"] == "completed"
            assert results[1]["status"] == "completed"
            assert results[2]["status"] == "failed"
            
            # Verify process_paper calls
            assert mock_process.call_count == 3
    
    def test_process_papers_from_file(self, extraction_service):
        """Test processing papers from a file."""
        # Mock file content
        file_content = """
        # Papers to process
        PMC6267067
        PMC6267068
        # Comment line
        PMC6267069
        """
        
        # Mock open function
        with patch("builtins.open", mock_open(read_data=file_content)):
            # Mock process_papers method
            with patch.object(extraction_service, "process_papers") as mock_process:
                mock_process.return_value = [
                    {"paper_id": "PMC6267067", "status": "completed"},
                    {"paper_id": "PMC6267068", "status": "completed"},
                    {"paper_id": "PMC6267069", "status": "completed"}
                ]
                
                # Call method
                results = extraction_service.process_papers_from_file("dummy_path")
                
                # Verify process_papers call
                mock_process.assert_called_once_with(["PMC6267067", "PMC6267068", "PMC6267069"])
                
                # Verify results
                assert len(results) == 3
    
    def test_process_papers_from_file_not_found(self, extraction_service):
        """Test handling file not found error."""
        # Mock open function to raise FileNotFoundError
        with patch("builtins.open", side_effect=FileNotFoundError()):
            # Call method and expect exception
            with pytest.raises(FileNotFoundError):
                extraction_service.process_papers_from_file("nonexistent_file")
    
    def test_extract_paper_ids_from_text(self, extraction_service):
        """Test extracting paper IDs from text."""
        # Test text with various formats
        text = """
        Here are some PMC IDs:
        PMC6267067
        6267068 (without prefix)
        PMC6267069 with some text
        Not a PMC ID: ABC123
        """
        
        # Call method
        result = extraction_service.extract_paper_ids_from_text(text)
        
        # Verify results
        assert len(result) == 3
        assert "PMC6267067" in result
        assert "PMC6267068" in result  # Should be normalized
        assert "PMC6267069" in result
        assert "ABC123" not in result
    
    def test_close(self, extraction_service, mock_storage_service):
        """Test closing the service."""
        # Call method
        extraction_service.close()
        
        # Verify storage service close was called
        mock_storage_service.close.assert_called_once()


class TestExtractionServiceIntegration:
    """Integration tests for extraction service."""
    
    def test_full_extraction_workflow(self):
        """Test the full extraction workflow with realistic data."""
        # Sample BioC XML response
        bioc_xml = """<?xml version="1.0" encoding="UTF-8"?>
        &lt;!DOCTYPE collection SYSTEM "BioC.dtd">
        <collection>
          <source>PubMed Central</source>
          <date>2023-05-19</date>
          <key>bioc.key</key>
          <document>
            <id>PMC6267067</id>
            <passage>
              <infon key="type">title</infon>
              <offset>0</offset>
              <text>Test Paper Title</text>
            </passage>
            <passage>
              <infon key="type">abstract</infon>
              <offset>105</offset>
              <text>Test paper abstract for testing purposes.</text>
            </passage>
            <passage>
              <infon key="type">figure</infon>
              <infon key="figure_id">fig1</infon>
              <infon key="figure_url">https://example.com/figure1.jpg</infon>
              <infon key="figure_number">1</infon>
              <offset>850</offset>
              <text>Figure 1. Test caption with GATA4 gene mention.</text>
            </passage>
          </document>
        </collection>
        """
        
        # Sample PubTator response
        pubtator_response = {
            "text": "Figure 1. Test caption with GATA4 gene mention.",
            "denotations": [
                {
                    "id": "1",
                    "span": {"begin": 28, "end": 33},
                    "obj": "Gene",
                    "text": "GATA4"
                }
            ]
        }
        
        # Create mocks
        mock_db = MagicMock()
        mock_bioc_client = MagicMock(spec=BioCClient)
        mock_pubtator_client = MagicMock(spec=PubTatorClient)
        mock_storage_service = MagicMock(spec=StorageService)
        
        # Configure mocks
        mock_bioc_client.get_paper_structure.return_value = {
            "paper_id": "PMC6267067",
            "title": "Test Paper Title",
            "abstract": "Test paper abstract for testing purposes.",
            "figures": [
                {
                    "figure_id": "fig1",
                    "figure_number": 1,
                    "caption": "Figure 1. Test caption with GATA4 gene mention.",
                    "url": "https://example.com/figure1.jpg"
                }
            ]
        }
        mock_pubtator_client.detect_entities.return_value = [
            {
                "entity_text": "GATA4",
                "entity_type": "Gene",
                "start_position": 28,
                "end_position": 33,
                "external_id": "2626"
            }
        ]
        mock_storage_service.get_paper.return_value = None
        
        # Create service
        service = ExtractionService(
            db=mock_db,
            bioc_client=mock_bioc_client,
            pubtator_client=mock_pubtator_client,
            storage_service=mock_storage_service
        )
        
        # Process paper
        result = service.process_paper("PMC6267067")
        
        # Verify result
        assert result["paper_id"] == "PMC6267067"
        assert result["status"] == "completed"
        assert result["figures_processed"] == 1
        
        # Verify storage service calls
        mock_storage_service.create_paper.assert_called_once()
        mock_storage_service.create_figure.assert_called_once()
        mock_storage_service.create_entity.assert_called_once()
        mock_storage_service.update_paper.assert_called_once()