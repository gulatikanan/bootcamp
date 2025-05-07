"""
Conditional Logging

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Conditional logging based on debug flag
debug = True  # Flag to control logging

if debug:
    logger.debug("This is a debug message that only logs when 'debug' is True.")
