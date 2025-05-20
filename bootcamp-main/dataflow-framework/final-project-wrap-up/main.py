# import argparse
# import time
# import sys
# import os
# from pathlib import Path
# from typing import List, Dict, Any, Optional

# from metrics.metrics_store import MetricsStore
# from processors.simple import adapt_simple_processor, observable_processor
# from processors.stateful import LineCounter, LineJoiner, LineSplitter, FilterProcessor
# from pipeline.pipeline import ObservablePipeline
# from dashboard.server import Dashboard
# from folder_monitor.file_processor import FolderMonitor
# from config.config_loader import load_config, create_pipeline_from_config

# def create_sample_pipeline() -> ObservablePipeline:
#     """Create a sample pipeline with various processors."""
#     pipeline = ObservablePipeline()
    
#     # Add processors
#     pipeline.add_processor(LineCounter(processor_id="counter"))
    
#     # Add a simple processor using the adapter
#     @observable_processor
#     def uppercase(line: str) -> str:
#         return line.upper()
    
#     pipeline.add_processor(uppercase(processor_id="uppercase"))
    
#     # Add a filter processor
#     def is_important(line: str) -> bool:
#         return "important" in line.lower() or "error" in line.lower()
    
#     pipeline.add_processor(FilterProcessor(is_important, processor_id="important_filter"))
    
#     # Add a line splitter
#     pipeline.add_processor(LineSplitter(delimiter="|", processor_id="splitter"))
    
#     return pipeline

# def process_file(file_path: str, pipeline: ObservablePipeline, output_path: Optional[str] = None) -> None:
#     """Process a single file through the pipeline."""
#     try:
#         print(f"Processing file: {file_path}")
#         with open(file_path, 'r', encoding='utf-8') as f:
#             lines = f.readlines()
        
#         print(f"Read {len(lines)} lines from file")
#         results = list(pipeline.process(iter(lines)))
#         print(f"Processed {len(results)} lines")
        
#         if output_path:
#             with open(output_path, 'w', encoding='utf-8') as f:
#                 for line in results:
#                     f.write(line + '\n')
#             print(f"Results written to {output_path}")
#         else:
#             for line in results:
#                 print(line)
    
#     except Exception as e:
#         print(f"Error processing file: {str(e)}")
#         sys.exit(1)

# def main():
#     parser = argparse.ArgumentParser(description="Stream Processing System with Folder Monitoring")
#     parser.add_argument("--file", help="Process a single file")
#     parser.add_argument("--output", help="Output file for processed results")
#     parser.add_argument("--config", help="Path to configuration file")
#     parser.add_argument("--trace", action="store_true", help="Enable tracing")
#     parser.add_argument("--dashboard", action="store_true", help="Start the web dashboard")
#     parser.add_argument("--dashboard-port", type=int, default=8000, help="Dashboard port")
#     parser.add_argument("--monitor", help="Directory to monitor for files")
#     parser.add_argument("--output-dir", help="Directory for processed output files")
#     parser.add_argument("--poll-interval", type=float, default=1.0, help="Polling interval in seconds")
    
#     args = parser.parse_args()
    
#     # Create pipeline
#     if args.config:
#         config = load_config(args.config)
#         pipeline = create_pipeline_from_config(config)
#     else:
#         pipeline = create_sample_pipeline()
    
#     # Configure tracing
#     metrics_store = MetricsStore()
#     metrics_store.set_tracing_enabled(args.trace)
    
#     # Start dashboard if requested
#     dashboard = None
#     if args.dashboard:
#         dashboard = Dashboard(port=args.dashboard_port)
#         dashboard.start()
#         print(f"Dashboard started at http://localhost:{args.dashboard_port}")
#         # Give the dashboard time to start
#         time.sleep(1)
    
#     # Process a file, monitor a directory, or show help
#     if args.file:
#         process_file(args.file, pipeline, args.output)
        
#         # If dashboard is running, keep the main thread alive
#         if args.dashboard:
#             print("\nProcessing complete. Dashboard is still running.")
#             print("Visit http://localhost:8000 to view metrics and traces.")
#             print("Press Ctrl+C to exit")
#             try:
#                 while True:
#                     time.sleep(1)
#             except KeyboardInterrupt:
#                 print("Shutting down...")
    
#     elif args.monitor:
#         # Start folder monitor
#         monitor = FolderMonitor(
#             base_dir=args.monitor,
#             pipeline=pipeline,
#             output_dir=args.output_dir,
#             poll_interval=args.poll_interval
#         )
#         monitor.start()
        
#         print(f"\nFolder monitor started.")
#         print(f"Watching for files in: {os.path.join(args.monitor, 'unprocessed')}")
#         if args.dashboard:
#             print(f"Dashboard available at: http://localhost:{args.dashboard_port}")
#         print("Press Ctrl+C to exit")
        
#         try:
#             # Keep the main thread alive
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("Shutting down...")
#             monitor.stop()
    
#     else:
#         # If no file or monitor is specified and dashboard is running, keep the main thread alive
#         if args.dashboard:
#             # Generate some sample data for the dashboard
#             print("No input file or monitor directory specified. Generating sample data for dashboard...")
#             sample_lines = [
#                 "INFO: This is a sample log line",
#                 "ERROR: This is an error message",
#                 "WARNING: This is a warning",
#                 "INFO|This is a pipe-delimited line"
#             ]
#             pipeline.process(iter(sample_lines))
            
#             print("\nDashboard is running with sample data.")
#             print("Visit http://localhost:8000 to view metrics and traces.")
#             print("Press Ctrl+C to exit")
#             try:
#                 while True:
#                     time.sleep(1)
#             except KeyboardInterrupt:
#                 print("Shutting down...")
#         else:
#             parser.print_help()

# if __name__ == "__main__":
#     main()

import argparse
import logging
import os
import sys
import time
import json
from pathlib import Path
import threading
import signal
# config/config_loader.py
from config.config_loader import load_config
from folder_monitor.file_processor import FolderMonitor
from dashboard.server import Dashboard
from metrics.metrics_store import MetricsStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle termination signals for graceful shutdown"""
    global running
    logger.info("Shutdown signal received, gracefully shutting down...")
    running = False

def process_single_file(file_path, config):
    """Process a single file and exit"""
    logger.info(f"Processing single file: {file_path}")
    
    # Initialize components
    metrics_store = MetricsStore()
    file_processor = FolderMonitor(config, metrics_store)
    
    # Process the file
    if os.path.exists(file_path):
        try:
            result = file_processor.process_file(file_path)
            logger.info(f"File processed successfully: {result}")
            return True
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return False
    else:
        logger.error(f"File not found: {file_path}")
        return False

def watch_directory(config):
    """Watch directory for new files and process them"""
    logger.info("Starting directory watch mode")
    
    # Initialize components
    metrics_store = MetricsStore()
    file_processor = FolderMonitor(config, metrics_store)
    
    # Start dashboard server in a separate thread
    dashboard_thread = threading.Thread(
        target=Dashboard,
        args=(metrics_store, file_processor, config),
        daemon=True
    )
    dashboard_thread.start()
    
    # Create required directories if they don't exist
    watch_dir = Path(config.get('watch_dir', 'watch_dir'))
    unprocessed_dir = watch_dir / 'unprocessed'
    processed_dir = watch_dir / 'processed'
    underprocess_dir = watch_dir / 'underprocess'
    
    for directory in [unprocessed_dir, processed_dir, underprocess_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Watching directory: {unprocessed_dir}")
    
    # Main watch loop
    global running
    while running:
        try:
            # Check for new files
            for file_path in unprocessed_dir.glob('*'):
                if file_path.is_file():
                    logger.info(f"Found new file: {file_path}")
                    try:
                        file_processor.process_file(str(file_path))
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {e}")
            
            # Check for recovery
            file_processor.check_for_recovery()
            
            # Sleep to avoid high CPU usage
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error in watch loop: {e}")
            time.sleep(5)  # Sleep longer on error
    
    logger.info("Watch mode terminated")

def main():
    """Main entry point with CLI argument parsing"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='File Processing System')
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--watch', action='store_true', help='Watch directory mode')
    mode_group.add_argument('--input', type=str, help='Process a single file')
    
    parser.add_argument('--config', type=str, default='log_processor_config.json',
                        help='Path to configuration file')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--trace', action='store_true', help='Enable trace logging')
    
    args = parser.parse_args()
    
    # Set logging level based on arguments
    if args.trace:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Trace logging enabled")
    elif args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug logging enabled")
    
    # Load configuration
    try:
        config = load_config(args.config)
        logger.info(f"Configuration loaded from {args.config}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return 1
    
    # Execute in the appropriate mode
    if args.watch:
        watch_directory(config)
    elif args.input:
        success = process_single_file(args.input, config)
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
