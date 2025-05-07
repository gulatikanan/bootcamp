"""
Use Environment Flag for Verbose Mode

Instructions:
Complete the exercise according to the requirements.
"""
import os
import logging

# Check environment variable for DEBUG mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

logger.debug("This is a debug message - only shows if DEBUG=True")
logger.info("This is an info message")

