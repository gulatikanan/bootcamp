"""
Thread Locking

Instructions:
Complete the exercise according to the requirements.
"""
import threading

# Shared variable
counter = 0

# Lock to protect the shared variable
lock = threading.Lock()

# Function to increment the counter
def increment():
    global counter
    with lock:  # Ensure only one thread can increment at a time
        for _ in range(10000):
            counter += 1

# Start two threads
threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads:
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("Final Counter:", counter)
