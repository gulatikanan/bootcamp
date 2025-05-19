"""
Ensure Cleanup

Instructions:
Complete the exercise according to the requirements.
"""
class SafeContext:
    def __enter__(self):
        print("Entered safe context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exited safe context (cleanup)")
        if exc_type:
            print("Handled exception:", exc_type.__name__)
        return True  # Suppress the exception

with SafeContext():
    print("Doing something risky...")
    raise ValueError("Something went wrong")

