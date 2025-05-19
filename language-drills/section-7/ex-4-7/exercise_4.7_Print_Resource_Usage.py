"""
Print Resource Usage

Instructions:
Complete the exercise according to the requirements.
"""
import psutil

mem = psutil.virtual_memory()
cpu = psutil.cpu_percent(interval=1)

print(f"Memory usage: {mem.percent}%")
print(f"CPU usage: {cpu}%")
