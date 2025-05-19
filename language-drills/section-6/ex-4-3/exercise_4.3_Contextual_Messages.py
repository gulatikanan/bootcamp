"""
Contextual Messages

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger
logging.basicConfig(
    level=logging.DEBUG,  # Capture all levels from DEBUG and above
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Contextual logging
user_name = "John Doe"
user_age = 30
logger.debug(f"User: {user_name}, Age: {user_age} - This is a debug message with user info.")
logger.info(f"User: {user_name} has logged in at age {user_age}.")
