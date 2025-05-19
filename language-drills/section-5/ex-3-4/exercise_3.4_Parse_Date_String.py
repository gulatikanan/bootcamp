"""
Parse Date String

Instructions:
Complete the exercise according to the requirements.
"""

from datetime import datetime

# Parse a date string into a datetime object
date_str = "2024-01-01"
parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
print("Parsed Date:", parsed_date)
