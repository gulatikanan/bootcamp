import os
import time
import random
from pathlib import Path

def create_sample_files(base_dir: str, num_files: int = 5, lines_per_file: int = 100):
    """Create sample files for testing the folder monitor."""
    unprocessed_dir = Path(base_dir) / "unprocessed"
    unprocessed_dir.mkdir(parents=True, exist_ok=True)
    
    log_levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    components = ["API", "Database", "Auth", "Frontend", "Backend"]
    actions = ["started", "completed", "failed", "processing", "waiting"]
    
    for i in range(num_files):
        file_path = unprocessed_dir / f"sample_log_{i}.txt"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for j in range(lines_per_file):
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                level = random.choice(log_levels)
                component = random.choice(components)
                action = random.choice(actions)
                
                # Make some lines contain "important" or "error" for the filter
                if random.random() < 0.1:
                    message = f"IMPORTANT: This is an important message about {component}"
                elif random.random() < 0.1:
                    message = f"An error occurred in {component} while {action}"
                else:
                    message = f"{component} {action} successfully"
                
                # Add some pipe-delimited lines for the splitter
                if random.random() < 0.2:
                    line = f"{timestamp}|{level}|{component}|{message}\n"
                else:
                    line = f"{timestamp} [{level}] {component}: {message}\n"
                
                f.write(line)
        
        print(f"Created sample file: {file_path}")

def main():
    # Create a base directory for the folder monitor
    base_dir = "sample_data"
    
    # Create sample files
    create_sample_files(base_dir, num_files=5, lines_per_file=100)
    
    print(f"\nSample files created in {base_dir}/unprocessed")
    print("Run the following command to start processing:")
    print(f"python main.py --monitor {base_dir} --dashboard --trace")

if __name__ == "__main__":
    main()