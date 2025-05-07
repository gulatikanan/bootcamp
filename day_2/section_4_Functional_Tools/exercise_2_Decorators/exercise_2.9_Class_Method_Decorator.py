"""
Class Method Decorator

Instructions:
Complete the exercise according to the requirements.
"""

def validate_args(func):
    def wrapper(self, *args, **kwargs):
        if not args:
            raise ValueError("Arguments cannot be empty")
        return func(self, *args, **kwargs)
    return wrapper

class MyClass:
    @validate_args
    def set_name(self, name):
        self.name = name

# Example usage
obj = MyClass()
obj.set_name("Alice")  # Works fine
obj.set_name()  # Raises ValueError
