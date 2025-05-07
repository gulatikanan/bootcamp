"""
Format Dates

Instructions:
Complete the exercise according to the requirements.
"""

from datetime import datetime

# Format today's date as "YYYY-MM-DD"
formatted_date = datetime.now().strftime("%Y-%m-%d")
print("Formatted Date:", formatted_date)
