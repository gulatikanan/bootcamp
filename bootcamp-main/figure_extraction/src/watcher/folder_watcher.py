import os
import time
import logging
import asyncio
import threading
from pathlib import Path
from typing import List, Dict, Any, Set

from src.config.settings import settings
from src.core.orchestrator import orchestrator

# Set up logging
logger = logging.getLogger(__name__)

class FolderWatcher:
    """Watch folders for files to process."""
    
    def __init__(self):
        self.folders = settings.watched_folder.watched_folders
        self.interval = settings.watched_folder.watch_interval
        self.patterns = settings.watched_folder.file_patterns
        self.processed_files = set()
        self.running = False
        self.thread = None
        self.loop = None
    
    def _match_pattern(self, filename: str) -> bool:
        """
        Check if a filename matches any of the patterns.
        
        Args:
            filename: The filename to check
            
        Returns:
            True if the filename matches any pattern, False otherwise
        """
        for pattern in self.patterns:
            if pattern.startswith("*."):
                # Extension pattern
                ext = pattern[1:]  # Remove the *
                if filename.endswith(ext):
                    return True
            elif "*" in pattern:
                # Other wildcard pattern
                import fnmatch
                if fnmatch.fnmatch(filename, pattern):
                    return True
            else:
                # Exact match
                if filename == pattern:
                    return True
        
        return False
    
    def _process_file(self, file_path: str):
        """
        Process a file.
        
        Args:
            file_path: Path to the file
        """
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Create a new event loop for this thread
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            
            # Process the file
            job = loop.run_until_complete(orchestrator.process_paper_file(file_path))
            
            logger.info(f"File {file_path} processed. Job ID: {job.id}")
            
            # Add to processed files
            self.processed_files.add(file_path)
            
            # Move file to processed folder
            processed_dir = os.path.join(os.path.dirname(file_path), "processed")
            os.makedirs(processed_dir, exist_ok=True)
            
            processed_path = os.path.join(processed_dir, os.path.basename(file_path))
            os.rename(file_path, processed_path)
            
            logger.info(f"File moved to: {processed_path}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            
            # Move file to failed folder
            failed_dir = os.path.join(os.path.dirname(file_path), "failed")
            os.makedirs(failed_dir, exist_ok=True)
            
            failed_path = os.path.join(failed_dir, os.path.basename(file_path))
            os.rename(file_path, failed_path)
            
            logger.error(f"File moved to: {failed_path}")
    
    def _watch_folders(self):
        """Watch folders for new files."""
        logger.info(f"Starting folder watcher. Watching folders: {', '.join(self.folders)}")
        
        while self.running:
            try:
                for folder in self.folders:
                    # Check if folder exists
                    if not os.path.exists(folder):
                        logger.warning(f"Folder does not exist: {folder}")
                        continue
                    
                    # Get all files in folder
                    for filename in os.listdir(folder):
                        file_path = os.path.join(folder, filename)
                        
                        # Skip directories and already processed files
                        if os.path.isdir(file_path) or file_path in self.processed_files:
                            continue
                        
                        # Check if file matches pattern
                        if self._match_pattern(filename):
                            # Process file in a separate thread
                            threading.Thread(target=self._process_file, args=(file_path,)).start()
                
                # Sleep before checking again
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error watching folders: {e}")
                time.sleep(self.interval)
    
    def start(self):
        """Start the folder watcher."""
        if self.running:
            logger.warning("Folder watcher is already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._watch_folders)
        self.thread.daemon = True
        self.thread.start()
        
        # Block main thread
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the folder watcher."""
        logger.info("Stopping folder watcher")
        self.running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5.0)