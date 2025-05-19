import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Dynamic Text Processor")
    parser.add_argument("--input", required=True, help="Input text file path")
    parser.add_argument("--config", required=True, help="YAML config defining pipeline")
    return parser.parse_args()
