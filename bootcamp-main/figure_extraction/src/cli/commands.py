import os
import sys
import logging
import asyncio
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler

from src.config.settings import settings, initialize_directories
from src.storage.database import db
from src.storage.models import ProcessingStatus, JobType, EntityType
from src.core.orchestrator import orchestrator
from src.core.jobs import job_manager
from src.watcher.folder_watcher import FolderWatcher
from src.api.server import run_server

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("cli")

# Create Typer app
app = typer.Typer(help="Scientific Paper Extractor CLI")
papers_app = typer.Typer(help="Manage papers")
figures_app = typer.Typer(help="Manage figures")
entities_app = typer.Typer(help="Manage entities")
jobs_app = typer.Typer(help="Manage jobs")
export_app = typer.Typer(help="Export data")
admin_app = typer.Typer(help="Admin commands")

# Add sub-apps
app.add_typer(papers_app, name="papers")
app.add_typer(figures_app, name="figures")
app.add_typer(entities_app, name="entities")
app.add_typer(jobs_app, name="jobs")
app.add_typer(export_app, name="export")
app.add_typer(admin_app, name="admin")

# Create console
console = Console()

@app.callback()
def main():
    """
    Scientific Paper Extractor CLI.
    """
    # Initialize directories
    initialize_directories()
    
    # Initialize database
    db.initialize()

@app.command("serve")
def serve(
    host: str = typer.Option(settings.api.host, help="Host to bind to"),
    port: int = typer.Option(settings.api.port, help="Port to bind to"),
    workers: int = typer.Option(settings.api.workers, help="Number of worker processes"),
    log_level: str = typer.Option(settings.log_level, help="Log level")
):
    """
    Start the API server.
    """
    # Update settings
    settings.api.host = host
    settings.api.port = port
    settings.api.workers = workers
    settings.log_level = log_level
    
    console.print(f"Starting API server on {host}:{port}...")
    run_server()

@app.command("watch")
def watch(
    folders: List[str] = typer.Option(settings.watched_folder.watched_folders, help="Folders to watch"),
    interval: int = typer.Option(settings.watched_folder.watch_interval, help="Interval to check folders (seconds)"),
    patterns: List[str] = typer.Option(settings.watched_folder.file_patterns, help="File patterns to match")
):
    """
    Watch folders for files to process.
    """
    # Update settings
    settings.watched_folder.watched_folders = folders
    settings.watched_folder.watch_interval = interval
    settings.watched_folder.file_patterns = patterns
    
    # Create and start watcher
    watcher = FolderWatcher()
    
    console.print(f"Watching folders: {', '.join(folders)}")
    console.print(f"File patterns: {', '.join(patterns)}")
    console.print(f"Check interval: {interval} seconds")
    console.print("Press Ctrl+C to stop")
    
    try:
        watcher.start()
    except KeyboardInterrupt:
        console.print("Stopping watcher...")
        watcher.stop()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@papers_app.command("process")
def process_papers(
    paper_ids: List[str] = typer.Argument(..., help="Paper IDs to process"),
    wait: bool = typer.Option(False, help="Wait for processing to complete")
):
    """
    Process papers by ID.
    """
    try:
        # Create event loop
        loop = asyncio.get_event_loop()
        
        # Process papers
        job = loop.run_until_complete(orchestrator.process_papers(paper_ids))
        
        console.print(f"[bold green]Job created:[/bold green] {job.id}")
        console.print(f"Processing {job.total_papers} papers...")
        
        if wait:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"Processing job {job.id}", total=job.total_papers)
                
                while True:
                    # Get job status
                    job = job_manager.get_job_status(job.id)
                    
                    # Update progress
                    progress.update(task, completed=job.processed_papers + job.failed_papers)
                    
                    # Check if job is complete
                    if job.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED]:
                        break
                    
                    # Wait before checking again
                    loop.run_until_complete(asyncio.sleep(1))
                
                # Print final status
                if job.status == ProcessingStatus.COMPLETED:
                    console.print(f"[bold green]Job completed:[/bold green] {job.processed_papers} papers processed")
                else:
                    console.print(f"[bold red]Job failed:[/bold red] {job.failed_papers} papers failed")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@papers_app.command("process-file")
def process_papers_file(
    file_path: str = typer.Argument(..., help="Path to file containing paper IDs"),
    wait: bool = typer.Option(False, help="Wait for processing to complete")
):
    """
    Process papers from a file.
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            console.print(f"[bold red]Error:[/bold red] File not found: {file_path}")
            sys.exit(1)
        
        # Create event loop
        loop = asyncio.get_event_loop()
        
        # Process file
        job = loop.run_until_complete(orchestrator.process_paper_file(file_path))
        
        console.print(f"[bold green]Job created:[/bold green] {job.id}")
        console.print(f"Processing {job.total_papers} papers...")
        
        if wait:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"Processing job {job.id}", total=job.total_papers)
                
                while True:
                    # Get job status
                    job = job_manager.get_job_status(job.id)
                    
                    # Update progress
                    progress.update(task, completed=job.processed_papers + job.failed_papers)
                    
                    # Check if job is complete
                    if job.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED]:
                        break
                    
                    # Wait before checking again
                    loop.run_until_complete(asyncio.sleep(1))
                
                # Print final status
                if job.status == ProcessingStatus.COMPLETED:
                    console.print(f"[bold green]Job completed:[/bold green] {job.processed_papers} papers processed")
                else:
                    console.print(f"[bold red]Job failed:[/bold red] {job.failed_papers} papers failed")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@papers_app.command("list")
def list_papers(
    limit: int = typer.Option(10, help="Maximum number of papers to list"),
    status: Optional[ProcessingStatus] = typer.Option(None, help="Filter by status")
):
    """
    List processed papers.
    """
    try:
        # Get papers from database
        papers = db.get_session().query(db.PaperModel)
        
        if status is not None:
            papers = papers.filter(db.PaperModel.status == status)
        
        papers = papers.limit(limit).all()
        
        # Create table
        table = Table(title=f"Papers (showing {len(papers)} of {papers.count()})")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Status", style="magenta")
        table.add_column("Figures", style="yellow")
        
        # Add rows
        for paper in papers:
            figures = db.get_session().query(db.FigureModel).filter(db.FigureModel.paper_id == paper.id).count()
            table.add_row(
                paper.id,
                paper.title[:50] + "..." if len(paper.title) > 50 else paper.title,
                paper.status.value,
                str(figures)
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@papers_app.command("show")
def show_paper(
    paper_id: str = typer.Argument(..., help="Paper ID to show")
):
    """
    Show details for a specific paper.
    """
    try:
        # Normalize paper ID
        if not paper_id.startswith("PMC"):
            paper_id = f"PMC{paper_id}"
        
        # Get paper from database
        session = db.get_session()
        paper = session.query(db.PaperModel).filter(db.PaperModel.id == paper_id).first()
        
        if paper is None:
            console.print(f"[bold red]Error:[/bold red] Paper not found: {paper_id}")
            sys.exit(1)
        
        # Get figures
        figures = session.query(db.FigureModel).filter(db.FigureModel.paper_id == paper_id).all()
        
        # Print paper details
        console.print(f"[bold cyan]ID:[/bold cyan] {paper.id}")
        console.print(f"[bold cyan]Title:[/bold cyan] {paper.title}")
        console.print(f"[bold cyan]Status:[/bold cyan] {paper.status.value}")
        console.print(f"[bold cyan]Processed Date:[/bold cyan] {paper.processed_date}")
        console.print(f"[bold cyan]Source:[/bold cyan] {paper.source}")
        
        if paper.error_message:
            console.print(f"[bold red]Error:[/bold red] {paper.error_message}")
        
        console.print(f"[bold cyan]Abstract:[/bold cyan]")
        console.print(paper.abstract)
        
        console.print(f"\n[bold cyan]Figures:[/bold cyan] {len(figures)}")
        
        for i, figure in enumerate(figures):
            console.print(f"\n[bold green]Figure {figure.figure_number}:[/bold green]")
            console.print(f"[bold cyan]ID:[/bold cyan] {figure.id}")
            if figure.url:
                console.print(f"[bold cyan]URL:[/bold cyan] {figure.url}")
            
            # Get entities
            entities = session.query(db.EntityModel).filter(db.EntityModel.figure_id == figure.id).all()
            
            console.print(f"[bold cyan]Caption:[/bold cyan]")
            console.print(figure.caption)
            
            console.print(f"[bold cyan]Entities:[/bold cyan] {len(entities)}")
            
            if entities:
                entity_table = Table(show_header=True, header_style="bold magenta")
                entity_table.add_column("Text")
                entity_table.add_column("Type")
                entity_table.add_column("Position")
                entity_table.add_column("External ID")
                
                for entity in entities:
                    entity_table.add_row(
                        entity.entity_text,
                        entity.entity_type.value,
                        f"{entity.start_position}-{entity.end_position}",
                        entity.external_id or ""
                    )
                
                console.print(entity_table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@figures_app.command("list")
def list_figures(
    paper_id: Optional[str] = typer.Option(None, help="Filter by paper ID"),
    limit: int = typer.Option(10, help="Maximum number of figures to list")
):
    """
    List figures.
    """
    try:
        # Get figures from database
        session = db.get_session()
        query = session.query(db.FigureModel)
        
        if paper_id:
            # Normalize paper ID
            if not paper_id.startswith("PMC"):
                paper_id = f"PMC{paper_id}"
            
            query = query.filter(db.FigureModel.paper_id == paper_id)
        
        figures = query.limit(limit).all()
        
        # Create table
        table = Table(title=f"Figures (showing {len(figures)} of {query.count()})")
        table.add_column("ID", style="cyan")
        table.add_column("Paper ID", style="green")
        table.add_column("Figure #", style="magenta")
        table.add_column("Caption", style="yellow")
        table.add_column("Entities", style="blue")
        
        # Add rows
        for figure in figures:
            entities = session.query(db.EntityModel).filter(db.EntityModel.figure_id == figure.id).count()
            table.add_row(
                figure.id,
                figure.paper_id,
                str(figure.figure_number),
                figure.caption[:50] + "..." if len(figure.caption) > 50 else figure.caption,
                str(entities)
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@entities_app.command("list")
def list_entities(
    figure_id: Optional[str] = typer.Option(None, help="Filter by figure ID"),
    entity_type: Optional[EntityType] = typer.Option(None, help="Filter by entity type"),
    limit: int = typer.Option(10, help="Maximum number of entities to list")
):
    """
    List entities.
    """
    try:
        # Get entities from database
        session = db.get_session()
        query = session.query(db.EntityModel)
        
        if figure_id:
            query = query.filter(db.EntityModel.figure_id == figure_id)
        
        if entity_type:
            query = query.filter(db.EntityModel.entity_type == entity_type)
        
        entities = query.limit(limit).all()
        
        # Create table
        table = Table(title=f"Entities (showing {len(entities)} of {query.count()})")
        table.add_column("ID", style="cyan")
        table.add_column("Figure ID", style="green")
        table.add_column("Text", style="yellow")
        table.add_column("Type", style="magenta")
        table.add_column("Position", style="blue")
        
        # Add rows
        for entity in entities:
            table.add_row(
                entity.id,
                entity.figure_id,
                entity.entity_text[:30] + "..." if len(entity.entity_text) > 30 else entity.entity_text,
                entity.entity_type.value,
                f"{entity.start_position}-{entity.end_position}"
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@jobs_app.command("list")
def list_jobs(
    status: Optional[ProcessingStatus] = typer.Option(None, help="Filter by status"),
    job_type: Optional[JobType] = typer.Option(None, help="Filter by job type"),
    limit: int = typer.Option(10, help="Maximum number of jobs to list")
):
    """
    List jobs.
    """
    try:
        # Get jobs from database
        session = db.get_session()
        query = session.query(db.JobModel)
        
        if status:
            query = query.filter(db.JobModel.status == status)
        
        if job_type:
            query = query.filter(db.JobModel.job_type == job_type)
        
        jobs = query.limit(limit).all()
        
        # Create table
        table = Table(title=f"Jobs (showing {len(jobs)} of {query.count()})")
        table.add_column("ID", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Status", style="magenta")
        table.add_column("Created", style="yellow")
        table.add_column("Progress", style="blue")
        
        # Add rows
        for job in jobs:
            progress = f"{job.processed_papers}/{job.total_papers} ({job.failed_papers} failed)"
            table.add_row(
                job.id,
                job.job_type.value,
                job.status.value,
                job.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                progress
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@jobs_app.command("show")
def show_job(
    job_id: str = typer.Argument(..., help="Job ID to show")
):
    """
    Show details for a specific job.
    """
    try:
        # Get job from database
        job = job_manager.get_job_status(job_id)
        
        if job is None:
            console.print(f"[bold red]Error:[/bold red] Job not found: {job_id}")
            sys.exit(1)
        
        # Print job details
        console.print(f"[bold cyan]ID:[/bold cyan] {job.id}")
        console.print(f"[bold cyan]Type:[/bold cyan] {job.job_type.value}")
        console.print(f"[bold cyan]Status:[/bold cyan] {job.status.value}")
        console.print(f"[bold cyan]Created:[/bold cyan] {job.created_at}")
        
        if job.completed_at:
            console.print(f"[bold cyan]Completed:[/bold cyan] {job.completed_at}")
        
        console.print(f"[bold cyan]Progress:[/bold cyan] {job.processed_papers}/{job.total_papers} papers processed ({job.failed_papers} failed)")
        
        # Print paper IDs
        console.print(f"[bold cyan]Paper IDs:[/bold cyan]")
        for i, paper_id in enumerate(job.paper_ids):
            console.print(f"  {i+1}. {paper_id}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@jobs_app.command("cancel")
def cancel_job(
    job_id: str = typer.Argument(..., help="Job ID to cancel")
):
    """
    Cancel a specific job.
    """
    try:
        # Create event loop
        loop = asyncio.get_event_loop()
        
        # Cancel job
        job = loop.run_until_complete(job_manager.cancel_job(job_id))
        
        if job is None:
            console.print(f"[bold red]Error:[/bold red] Job not found: {job_id}")
            sys.exit(1)
        
        console.print(f"[bold green]Job cancelled:[/bold green] {job.id}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@export_app.command("papers")
def export_papers(
    output_path: str = typer.Argument(..., help="Path to output file"),
    format: str = typer.Option("json", help="Output format (json or csv)")
):
    """
    Export papers data.
    """
    try:
        if format not in ["json", "csv"]:
            console.print(f"[bold red]Error:[/bold red] Invalid format: {format}. Must be 'json' or 'csv'.")
            sys.exit(1)
        
        # Export data
        output_file = orchestrator.export_data("papers", format, output_path)
        
        console.print(f"[bold green]Papers exported to:[/bold green] {output_file}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@export_app.command("figures")
def export_figures(
    output_path: str = typer.Argument(..., help="Path to output file"),
    format: str = typer.Option("json", help="Output format (json or csv)")
):
    """
    Export figures data.
    """
    try:
        if format not in ["json", "csv"]:
            console.print(f"[bold red]Error:[/bold red] Invalid format: {format}. Must be 'json' or 'csv'.")
            sys.exit(1)
        
        # Export data
        output_file = orchestrator.export_data("figures", format, output_path)
        
        console.print(f"[bold green]Figures exported to:[/bold green] {output_file}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@export_app.command("entities")
def export_entities(
    output_path: str = typer.Argument(..., help="Path to output file"),
    format: str = typer.Option("json", help="Output format (json or csv)")
):
    """
    Export entities data.
    """
    try:
        if format not in ["json", "csv"]:
            console.print(f"[bold red]Error:[/bold red] Invalid format: {format}. Must be 'json' or 'csv'.")
            sys.exit(1)
        
        # Export data
        output_file = orchestrator.export_data("entities", format, output_path)
        
        console.print(f"[bold green]Entities exported to:[/bold green] {output_file}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@admin_app.command("backup")
def backup_database():
    """
    Backup the database.
    """
    try:
        # Backup database
        db.backup()
        
        console.print(f"[bold green]Database backed up[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@admin_app.command("config")
def show_config():
    """
    Show current configuration.
    """
    try:
        # Print configuration
        console.print("[bold cyan]Configuration:[/bold cyan]")
        
        console.print(f"[bold green]General:[/bold green]")
        console.print(f"  App Name: {settings.app_name}")
        console.print(f"  Environment: {settings.environment}")
        console.print(f"  Log Level: {settings.log_level}")
        console.print(f"  Temp Directory: {settings.temp_dir}")
        
        console.print(f"\n[bold green]API:[/bold green]")
        console.print(f"  Host: {settings.api.host}")
        console.print(f"  Port: {settings.api.port}")
        console.print(f"  Workers: {settings.api.workers}")
        console.print(f"  Enable Docs: {settings.api.enable_docs}")
        
        console.print(f"\n[bold green]Security:[/bold green]")
        console.print(f"  Auth Enabled: {settings.security.auth_enabled}")
        console.print(f"  Auth Method: {settings.security.auth_method}")
        console.print(f"  Token Expiration: {settings.security.token_expiration} seconds")
        console.print(f"  API Keys: {len(settings.security.api_keys)} configured")
        
        console.print(f"\n[bold green]Storage:[/bold green]")
        console.print(f"  Storage Type: {settings.storage.storage_type}")
        console.print(f"  DuckDB Path: {settings.storage.duckdb_path}")
        console.print(f"  Backup Enabled: {settings.storage.backup_enabled}")
        console.print(f"  Backup Interval: {settings.storage.backup_interval} hours")
        
        console.print(f"\n[bold green]Processing:[/bold green]")
        console.print(f"  Extraction Workers: {settings.processing.extraction_workers}")
        console.print(f"  Entity Detection Workers: {settings.processing.entity_detection_workers}")
        console.print(f"  Batch Size: {settings.processing.batch_size}")
        console.print(f"  Retry Limit: {settings.processing.retry_limit}")
        console.print(f"  Retry Delay: {settings.processing.retry_delay} seconds")
        
        console.print(f"\n[bold green]Watched Folder:[/bold green]")
        console.print(f"  Watched Folders: {', '.join(settings.watched_folder.watched_folders)}")
        console.print(f"  Watch Interval: {settings.watched_folder.watch_interval} seconds")
        console.print(f"  File Patterns: {', '.join(settings.watched_folder.file_patterns)}")
        
        console.print(f"\n[bold green]External API:[/bold green]")
        console.print(f"  BioC-PMC URL: {settings.external_api.bioc_pmc_url}")
        console.print(f"  BioC-PMC Rate Limit: {settings.external_api.bioc_pmc_rate_limit} requests/minute")
        console.print(f"  PubTator3 URL: {settings.external_api.pubtator3_url}")
        console.print(f"  PubTator3 Rate Limit: {settings.external_api.pubtator3_rate_limit} requests/minute")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@admin_app.command("stats")
def show_stats():
    """
    Show system statistics.
    """
    try:
        # Get counts from database
        session = db.get_session()
        
        try:
            # Count papers by status
            papers_by_status = {}
            for status_value in ProcessingStatus:
                count = session.query(db.PaperModel).filter(
                    db.PaperModel.status == status_value
                ).count()
                papers_by_status[status_value.value] = count
            
            # Count figures
            figure_count = session.query(db.FigureModel).count()
            
            # Count entities by type
            entities_by_type = {}
            for entity_type in EntityType:
                count = session.query(db.EntityModel).filter(
                    db.EntityModel.entity_type == entity_type
                ).count()
                entities_by_type[entity_type.value] = count
            
            # Count jobs by status
            jobs_by_status = {}
            for status_value in ProcessingStatus:
                count = session.query(db.JobModel).filter(
                    db.JobModel.status == status_value
                ).count()
                jobs_by_status[status_value.value] = count
            
            # Get database file size
            db_path = settings.storage.duckdb_path
            db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
            
            # Print statistics
            console.print("[bold cyan]System Statistics:[/bold cyan]")
            
            console.print(f"\n[bold green]Papers:[/bold green]")
            console.print(f"  Total: {sum(papers_by_status.values())}")
            for status, count in papers_by_status.items():
                console.print(f"  {status}: {count}")
            
            console.print(f"\n[bold green]Figures:[/bold green]")
            console.print(f"  Total: {figure_count}")
            
            console.print(f"\n[bold green]Entities:[/bold green]")
            console.print(f"  Total: {sum(entities_by_type.values())}")
            for entity_type, count in entities_by_type.items():
                console.print(f"  {entity_type}: {count}")
            
            console.print(f"\n[bold green]Jobs:[/bold green]")
            console.print(f"  Total: {sum(jobs_by_status.values())}")
            for status, count in jobs_by_status.items():
                console.print(f"  {status}: {count}")
            
            console.print(f"\n[bold green]Database:[/bold green]")
            console.print(f"  Size: {db_size} bytes ({round(db_size / (1024 * 1024), 2)} MB)")
        finally:
            session.close()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

def run_cli():
    """Run the CLI application."""
    app()

if __name__ == "__main__":
    run_cli()