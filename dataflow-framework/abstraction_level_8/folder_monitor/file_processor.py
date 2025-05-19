import os
import time
import shutil
import threading
from typing import Optional, List, Dict, Any
from pathlib import Path

from metrics.metrics_store import MetricsStore
from pipeline.pipeline import ObservablePipeline

class FolderMonitor:
    """
    Monitors a folder for new files and processes them through a pipeline.
    Implements a folder-based queue with recovery capabilities.
    """
    
    def __init__(self, 
                 base_dir: str,
                 pipeline: ObservablePipeline,
                 output_dir: Optional[str] = None,
                 poll_interval: float = 1.0):
        """
        Initialize the folder monitor.
        
        Args:
            base_dir: Base directory for the folder queue
            pipeline: Pipeline to process files with
            output_dir: Optional directory to write processed output
            poll_interval: How often to check for new files (seconds)
        """
        self.base_dir = Path(base_dir)
        self.unprocessed_dir = self.base_dir / "unprocessed"
        self.underprocess_dir = self.base_dir / "underprocess"
        self.processed_dir = self.base_dir / "processed"
        self.output_dir = Path(output_dir) if output_dir else None
        
        self.pipeline = pipeline
        self.poll_interval = poll_interval
        self.running = False
        self.monitor_thread = None
        self.metrics_store = MetricsStore()
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create the necessary directory structure."""
        for directory in [self.unprocessed_dir, self.underprocess_dir, self.processed_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _recover_interrupted_files(self):
        """Move files from underprocess back to unprocessed on startup."""
        for file_path in self.underprocess_dir.glob("*"):
            if file_path.is_file():
                target_path = self.unprocessed_dir / file_path.name
                shutil.move(str(file_path), str(target_path))
                print(f"Recovered interrupted file: {file_path.name}")
    
    def _update_file_counts(self):
        """Update file count metrics."""
        unprocessed_count = sum(1 for _ in self.unprocessed_dir.glob("*") if _.is_file())
        underprocess_count = sum(1 for _ in self.underprocess_dir.glob("*") if _.is_file())
        processed_count = sum(1 for _ in self.processed_dir.glob("*") if _.is_file())
        
        self.metrics_store.update_file_counts(
            unprocessed=unprocessed_count,
            underprocess=underprocess_count,
            processed=processed_count
        )
    
    def _process_file(self, file_path: Path):
        """Process a single file through the pipeline."""
        try:
            # Move to underprocess
            underprocess_path = self.underprocess_dir / file_path.name
            shutil.move(str(file_path), str(underprocess_path))
            
            # Update metrics
            self._update_file_counts()
            self.metrics_store.set_current_file(file_path.name)
            
            print(f"Processing file: {file_path.name}")
            
            # Process the file
            with open(underprocess_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Process through pipeline
            results = list(self.pipeline.process(iter(lines)))
            
            # Write results if output directory is specified
            if self.output_dir:
                output_path = self.output_dir / f"{file_path.stem}_processed{file_path.suffix}"
                with open(output_path, 'w', encoding='utf-8') as f:
                    for line in results:
                        f.write(line + '\n')
                print(f"Results written to {output_path}")
            
            # Move to processed
            processed_path = self.processed_dir / file_path.name
            shutil.move(str(underprocess_path), str(processed_path))
            
            # Update metrics
            self.metrics_store.set_current_file(None)
            self.metrics_store.add_processed_file(file_path.name)
            self._update_file_counts()
            
            print(f"Completed processing file: {file_path.name}")
            
        except Exception as e:
            print(f"Error processing file {file_path.name}: {str(e)}")
            # In case of error, move back to unprocessed for retry
            if underprocess_path.exists():
                recovery_path = self.unprocessed_dir / file_path.name
                shutil.move(str(underprocess_path), str(recovery_path))
            
            self.metrics_store.set_current_file(None)
            self._update_file_counts()
    
    def _monitor_loop(self):
        """Main monitoring loop that checks for new files."""
        while self.running:
            try:
                # Update file counts
                self._update_file_counts()
                
                # Check for new files
                for file_path in sorted(self.unprocessed_dir.glob("*")):
                    if file_path.is_file():
                        self._process_file(file_path)
                
                # Sleep before next poll
                time.sleep(self.poll_interval)
                
            except Exception as e:
                print(f"Error in monitor loop: {str(e)}")
                # Continue monitoring even if there's an error
    
    def start(self):
        """Start the folder monitor."""
        if self.running:
            return  # Already running
        
        # Recover any interrupted files
        self._recover_interrupted_files()
        
        # Start monitoring
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print(f"Started monitoring {self.unprocessed_dir}")
    
    def stop(self):
        """Stop the folder monitor."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        print("Stopped folder monitoring")