"""
Setup Logger

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger with basic configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("This is an info log message!")
