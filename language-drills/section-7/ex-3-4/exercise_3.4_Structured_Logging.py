"""
Structured Logging

Instructions:
Complete the exercise according to the requirements.
"""

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def sample_function():
    logger.debug("Entering sample_function")
    result = sum(range(5))
    logger.debug("Exiting sample_function with result: %s", result)
    return result

sample_function()
