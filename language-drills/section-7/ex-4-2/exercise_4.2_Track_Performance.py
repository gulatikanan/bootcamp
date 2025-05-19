"""
Track Performance

Instructions:
Complete the exercise according to the requirements.
"""
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def slow_function():
    start = time.time()
    time.sleep(1)
    end = time.time()
    logger.info("slow_function took %.2f seconds", end - start)

slow_function()
