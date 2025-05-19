"""
Format Output

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger with a custom format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Includes timestamp and log level
)
logger = logging.getLogger(__name__)

# Log messages with formatted output
logger.debug("This is a debug message.")
logger.info("This is an info message.")
