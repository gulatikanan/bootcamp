"""
Chained Partials

Instructions:
Complete the exercise according to the requirements.
"""

from functools import partial

# Base partial function for print
custom_print = partial(print, end='')

# Further customizations
custom_print_with_prefix = partial(custom_print, "Prefix: ")

# Test
custom_print_with_prefix("Hello, World!")  # Output: Prefix: Hello, World!
