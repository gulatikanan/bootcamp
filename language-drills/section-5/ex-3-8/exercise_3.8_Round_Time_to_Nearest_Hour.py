"""
Round Time to Nearest Hour

Instructions:
Complete the exercise according to the requirements.
"""

from datetime import datetime, timedelta

# Round current time to the nearest hour
now = datetime.now()
rounded_time = now.replace(minute=0, second=0, microsecond=0)
if now.minute >= 30:
    rounded_time += timedelta(hours=1)

print("Rounded Time:", rounded_time)
