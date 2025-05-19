"""
Write Small Functions

Instructions:
Complete the exercise according to the requirements.
"""

def process_data(data):
    cleaned_data = [d.strip() for d in data]
    filtered_data = [d for d in cleaned_data if len(d) > 3]
    final_data = [d.upper() for d in filtered_data]
    return final_data

def clean_data(data):
    return [d.strip() for d in data]

def filter_data(data):
    return [d for d in data if len(d) > 3]

def process_data(data):
    cleaned_data = clean_data(data)
    filtered_data = filter_data(cleaned_data)
    final_data = [d.upper() for d in filtered_data]
    return final_data
