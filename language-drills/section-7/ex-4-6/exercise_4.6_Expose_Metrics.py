"""
Expose Metrics

Instructions:
Complete the exercise according to the requirements.
"""

metrics = {
    "requests": 0,
    "errors": 0,
    "total_time": 0.0
}

def serve_request():
    import time
    start = time.time()
    metrics["requests"] += 1
    try:
        time.sleep(0.2)
    except Exception:
        metrics["errors"] += 1
    metrics["total_time"] += (time.time() - start)

serve_request()
serve_request()
print("Metrics:", metrics)
