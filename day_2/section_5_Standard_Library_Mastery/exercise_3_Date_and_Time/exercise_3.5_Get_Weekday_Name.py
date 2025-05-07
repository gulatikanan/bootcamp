"""
Get Weekday Name

Instructions:
Complete the exercise according to the requirements.
"""

import calendar
from datetime import datetime

# Get the weekday name
date = datetime.now()
weekday_name = calendar.day_name[date.weekday()]
print("Weekday Name:", weekday_name)
