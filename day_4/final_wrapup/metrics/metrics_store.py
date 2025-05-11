import time
import threading
from typing import Dict, List, Any, Optional, Set
from collections import deque

class MetricsStore:
    """
    Singleton class to store metrics and traces for all processors.
    Thread-safe and designed for concurrent access.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MetricsStore, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self):
        """Initialize the metrics store with empty collections."""
        # Metrics for each processor
        self.metrics: Dict[str, Dict[str, Any]] = {}
        
        # Trace storage with limited capacity
        self.traces: deque = deque(maxlen=1000)
        
        # Error storage with limited capacity
        self.errors: deque = deque(maxlen=100)
        
        # Flag to enable/disable tracing
        self.tracing_enabled = False
        
        # File processing statistics
        self.file_stats = {
            "unprocessed": 0,
            "underprocess": 0,
            "processed": 0,
            "current_file": None,
            "recent_files": deque(maxlen=10)  # Last 10 processed files
        }
        
        # Locks for thread safety
        self.metrics_lock = threading.Lock()
        self.traces_lock = threading.Lock()
        self.errors_lock = threading.Lock()
        self.file_stats_lock = threading.Lock()
    
    def register_processor(self, processor_id: str, processor_type: str):
        """Register a new processor in the metrics store."""
        with self.metrics_lock:
            if processor_id not in self.metrics:
                self.metrics[processor_id] = {
                    "type": processor_type,
                    "lines_in": 0,
                    "lines_out": 0,
                    "processing_time": 0,
                    "error_count": 0,
                    "last_processed": None
                }
    
    def update_lines_in(self, processor_id: str, count: int = 1):
        """Increment the count of lines received by a processor."""
        with self.metrics_lock:
            if processor_id in self.metrics:
                self.metrics[processor_id]["lines_in"] += count
                self.metrics[processor_id]["last_processed"] = time.time()
    
    def update_lines_out(self, processor_id: str, count: int = 1):
        """Increment the count of lines emitted by a processor."""
        with self.metrics_lock:
            if processor_id in self.metrics:
                self.metrics[processor_id]["lines_out"] += count
                self.metrics[processor_id]["last_processed"] = time.time()
    
    def update_processing_time(self, processor_id: str, duration: float):
        """Add processing time for a processor."""
        with self.metrics_lock:
            if processor_id in self.metrics:
                self.metrics[processor_id]["processing_time"] += duration
    
    def record_error(self, processor_id: str, error_message: str):
        """Record an error for a processor."""
        with self.metrics_lock:
            if processor_id in self.metrics:
                self.metrics[processor_id]["error_count"] += 1
        
        with self.errors_lock:
            self.errors.append({
                "timestamp": time.time(),
                "processor_id": processor_id,
                "message": error_message
            })
    
    def add_trace(self, line_id: str, processor_id: str, status: str, original_line: str):
        """Add a trace entry for a line passing through a processor."""
        if not self.tracing_enabled:
            return
            
        with self.traces_lock:
            # Find existing trace or create new one
            trace_entry = None
            for entry in self.traces:
                if entry["line_id"] == line_id:
                    trace_entry = entry
                    break
            
            if trace_entry is None:
                trace_entry = {
                    "line_id": line_id,
                    "original_line": original_line,
                    "path": [],
                    "start_time": time.time()
                }
                self.traces.append(trace_entry)
            
            # Add processor to path
            trace_entry["path"].append({
                "processor_id": processor_id,
                "status": status,
                "timestamp": time.time()
            })
    
    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get a copy of all metrics."""
        with self.metrics_lock:
            return {k: v.copy() for k, v in self.metrics.items()}
    
    def get_traces(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get a copy of recent traces, limited to the specified number."""
        with self.traces_lock:
            traces = list(self.traces)
            if limit and limit < len(traces):
                return traces[-limit:]
            return traces
    
    def get_errors(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get a copy of recent errors, limited to the specified number."""
        with self.errors_lock:
            errors = list(self.errors)
            if limit and limit < len(errors):
                return errors[-limit:]
            return errors
    
    def set_tracing_enabled(self, enabled: bool):
        """Enable or disable tracing."""
        self.tracing_enabled = enabled
    
    # File monitoring metrics methods
    
    def update_file_counts(self, unprocessed: int, underprocess: int, processed: int):
        """Update the counts of files in each directory."""
        with self.file_stats_lock:
            self.file_stats["unprocessed"] = unprocessed
            self.file_stats["underprocess"] = underprocess
            self.file_stats["processed"] = processed
    
    def set_current_file(self, filename: Optional[str]):
        """Set the name of the file currently being processed."""
        with self.file_stats_lock:
            self.file_stats["current_file"] = filename
    
    def add_processed_file(self, filename: str):
        """Add a file to the list of recently processed files."""
        with self.file_stats_lock:
            self.file_stats["recent_files"].append({
                "filename": filename,
                "timestamp": time.time()
            })
    
    def get_file_stats(self) -> Dict[str, Any]:
        """Get a copy of the file processing statistics."""
        with self.file_stats_lock:
            stats = self.file_stats.copy()
            stats["recent_files"] = list(stats["recent_files"])
            return stats