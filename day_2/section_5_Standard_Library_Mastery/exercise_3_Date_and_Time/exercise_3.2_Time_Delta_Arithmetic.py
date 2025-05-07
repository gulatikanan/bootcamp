"""
Time Delta Arithmetic

Instructions:
Complete the exercise according to the requirements.
"""

from datetime import datetime, timedelta

# Add 7 days to today's date
new_date = datetime.now() + timedelta(days=7)
print("Date after 7 days:", new_date)
