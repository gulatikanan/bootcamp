"""
Log with Context

Instructions:
Complete the exercise according to the requirements.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_user(user_id):
    logger.info("Processing user_id=%s in function=%s", user_id, process_user.__name__)

process_user("U123")
