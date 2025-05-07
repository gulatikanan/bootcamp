"""
Use Name as Logger Name

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger with __name__
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)  # Using __name__ for identifying the module

# Log some messages
logger.info("This is an info message with the logger name as the module name.")
