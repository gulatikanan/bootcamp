"""
Start a Thread

Instructions:
Complete the exercise according to the requirements.
"""

import threading

# Function to run in a separate thread
def print_numbers():
    for i in range(5):
        print(i)

# Create and start a thread
thread = threading.Thread(target=print_numbers)
thread.start()

# Wait for the thread to finish
thread.join()
