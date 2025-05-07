"""
Trace Function Calls

Instructions:
Complete the exercise according to the requirements.
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def trace(func):
    def wrapper(*args, **kwargs):
        logger.info("Calling function: %s | args=%s kwargs=%s", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.info("Function %s returned: %s", func.__name__, result)
        return result
    return wrapper

@trace
def multiply(x, y):
    return x * y

multiply(3, 4)
