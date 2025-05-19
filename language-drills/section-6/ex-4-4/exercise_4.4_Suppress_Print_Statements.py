"""
Suppress Print Statements

Instructions:
Complete the exercise according to the requirements.
"""

import logging

# Setup logger
logging.basicConfig(
    level=logging.DEBUG,  # Ensure capturing of all levels
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Replacing print with logger
user = "Alice"
logger.info(f"Processing user: {user}")  # Instead of print("Processing user: Alice")
