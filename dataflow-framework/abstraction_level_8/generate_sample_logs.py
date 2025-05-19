import os
import time
import random
from pathlib import Path

def create_sample_log_file(output_dir: str, file_index: int, lines: int = 100):
    """Create a sample log file with random log entries."""
    log_levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    components = ["API", "Database", "Auth", "Frontend", "Backend"]
    actions = ["started", "completed", "failed", "processing", "waiting"]
    
    file_path = Path(output_dir) / f"sample_log_{file_index}.txt"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for _ in range(lines):
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
    
    return file_path

def main():
    # Create the directory structure
    base_dir = "watch_dir"
    unprocessed_dir = os.path.join(base_dir, "unprocessed")
    
    # Create directories if they don't exist
    os.makedirs(unprocessed_dir, exist_ok=True)
    
    # Create sample log files
    num_files = 5
    for i in range(num_files):
        file_path = create_sample_log_file(unprocessed_dir, i)
        print(f"Created sample log file: {file_path}")
    
    print(f"\nCreated {num_files} sample log files in {unprocessed_dir}")
    print("Run the following command to start processing:")
    print(f"python main.py --monitor {base_dir} --trace --dashboard")

if __name__ == "__main__":
    main()