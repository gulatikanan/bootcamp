"""
Use Logging Levels

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger with basic configuration
logging.basicConfig(
    level=logging.DEBUG,  # Ensure you can capture all levels
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger object
logger = logging.getLogger(__name__)

# Log messages at different levels
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
