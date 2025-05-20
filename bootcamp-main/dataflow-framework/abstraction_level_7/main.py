# import argparse
# import time
# import sys
# from pathlib import Path
# from typing import List, Dict, Any, Optional

# from metrics.metrics_store import MetricsStore
# from processors.simple import adapt_simple_processor, observable_processor
# from processors.stateful import LineCounter, LineJoiner, LineSplitter, FilterProcessor
# from pipeline.pipeline import ObservablePipeline
# from dashboard.server import Dashboard
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
#         with open(file_path, 'r', encoding='utf-8') as f:
#             lines = f.readlines()
        
#         results = list(pipeline.process(iter(lines)))
        
#         if output_path:
#             with open(output_path, 'w', encoding='utf-8') as f:
#                 for line in results:
#                     f.write(line + '\n')
#         else:
#             for line in results:
#                 print(line)
    
#     except Exception as e:
#         print(f"Error processing file: {str(e)}")
#         sys.exit(1)

# def main():
#     parser = argparse.ArgumentParser(description="Stream Processing System with Observability")
#     parser.add_argument("--file", help="Process a single file")
#     parser.add_argument("--output", help="Output file for processed results")
#     parser.add_argument("--config", help="Path to configuration file")
#     parser.add_argument("--trace", action="store_true", help="Enable tracing")
#     parser.add_argument("--dashboard", action="store_true", help="Start the web dashboard")
#     parser.add_argument("--dashboard-port", type=int, default=8000, help="Dashboard port")
    
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
#     if args.dashboard:
#         dashboard = Dashboard(port=args.dashboard_port)
#         dashboard.start()
#         print(f"Dashboard started at http://localhost:{args.dashboard_port}")
    
#     # Process a file if specified
#     if args.file:
#         process_file(args.file, pipeline, args.output)
#     else:
#         # If no file is specified and dashboard is running, keep the main thread alive
#         if args.dashboard:
#             try:
#                 print("Press Ctrl+C to exit")
#                 while True:
#                     time.sleep(1)
#             except KeyboardInterrupt:
#                 print("Shutting down...")
#         else:
#             parser.print_help()

# if __name__ == "__main__":
#     main()

import argparse
import time
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from metrics.metrics_store import MetricsStore
from processors.simple import adapt_simple_processor, observable_processor
from processors.stateful import LineCounter, LineJoiner, LineSplitter, FilterProcessor
from pipeline.pipeline import ObservablePipeline
from dashboard.server import Dashboard
from config.config_loader import load_config, create_pipeline_from_config

def create_sample_pipeline() -> ObservablePipeline:
    """Create a sample pipeline with various processors."""
    pipeline = ObservablePipeline()
    
    # Add processors
    pipeline.add_processor(LineCounter(processor_id="counter"))
    
    # Add a simple processor using the adapter
    @observable_processor
    def uppercase(line: str) -> str:
        return line.upper()
    
    pipeline.add_processor(uppercase(processor_id="uppercase"))
    
    # Add a filter processor
    def is_important(line: str) -> bool:
        return "important" in line.lower() or "error" in line.lower()
    
    pipeline.add_processor(FilterProcessor(is_important, processor_id="important_filter"))
    
    # Add a line splitter
    pipeline.add_processor(LineSplitter(delimiter="|", processor_id="splitter"))
    
    return pipeline

def process_file(file_path: str, pipeline: ObservablePipeline, output_path: Optional[str] = None) -> None:
    """Process a single file through the pipeline."""
    try:
        print(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Read {len(lines)} lines from file")
        results = list(pipeline.process(iter(lines)))
        print(f"Processed {len(results)} lines")
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                for line in results:
                    f.write(line + '\n')
            print(f"Results written to {output_path}")
        else:
            for line in results:
                print(line)
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Stream Processing System with Observability")
    parser.add_argument("--file", help="Process a single file")
    parser.add_argument("--output", help="Output file for processed results")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--trace", action="store_true", help="Enable tracing")
    parser.add_argument("--dashboard", action="store_true", help="Start the web dashboard")
    parser.add_argument("--dashboard-port", type=int, default=8000, help="Dashboard port")
    
    args = parser.parse_args()
    
    # Create pipeline
    if args.config:
        config = load_config(args.config)
        pipeline = create_pipeline_from_config(config)
    else:
        pipeline = create_sample_pipeline()
    
    # Configure tracing
    metrics_store = MetricsStore()
    metrics_store.set_tracing_enabled(args.trace)
    
    # Start dashboard if requested
    dashboard = None
    if args.dashboard:
        dashboard = Dashboard(port=args.dashboard_port)
        dashboard.start()
        print(f"Dashboard started at http://localhost:{args.dashboard_port}")
        # Give the dashboard time to start
        time.sleep(1)
    
    # Process a file if specified
    if args.file:
        process_file(args.file, pipeline, args.output)
        
        # If dashboard is running, keep the main thread alive
        if args.dashboard:
            print("\nProcessing complete. Dashboard is still running.")
            print("Visit http://localhost:8000 to view metrics and traces.")
            print("Press Ctrl+C to exit")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Shutting down...")
    else:
        # If no file is specified and dashboard is running, keep the main thread alive
        if args.dashboard:
            # Generate some sample data for the dashboard
            print("No input file specified. Generating sample data for dashboard...")
            sample_lines = [
                "INFO: This is a sample log line",
                "ERROR: This is an error message",
                "WARNING: This is a warning",
                "INFO|This is a pipe-delimited line"
            ]
            pipeline.process(iter(sample_lines))
            
            print("\nDashboard is running with sample data.")
            print("Visit http://localhost:8000 to view metrics and traces.")
            print("Press Ctrl+C to exit")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Shutting down...")
        else:
            parser.print_help()

if __name__ == "__main__":
    main()