"""
File Logging

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger to log to a file
logging.basicConfig(
    filename='app.log',  # Log output file
    level=logging.DEBUG,  # Log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log some messages
logger.info("Application started.")
logger.warning("Low disk space warning.")
