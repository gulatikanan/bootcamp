"""
Deque for Stack and Queue

Instructions:
Complete the exercise according to the requirements.
"""

import collections

# Simulate a stack (LIFO)
stack = collections.deque()
stack.append(1)
stack.append(2)
stack.append(3)

# Pop from stack (last-in, first-out)
print(stack.pop())  # Outputs: 3

# Simulate a queue (FIFO)
queue = collections.deque()
queue.append(1)
queue.append(2)
queue.append(3)

# Pop from queue (first-in, first-out)
print(queue.popleft())  # Outputs: 1
