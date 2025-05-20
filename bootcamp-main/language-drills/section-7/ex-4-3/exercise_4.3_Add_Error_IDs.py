"""
Add Error IDs

Instructions:
Complete the exercise according to the requirements.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def risky_operation():
    try:
        # Simulate an error
        raise ValueError("Simulated error")
    except ValueError as e:
        logger.error("[ERR1001] ValueError occurred: %s", e)

risky_operation()
