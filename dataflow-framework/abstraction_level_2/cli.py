# cli.py
import argparse
from main import run_pipeline

def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--config", required=True, help="YAML config file path")
    parser.add_argument("--output", help="Optional output file path")

    args = parser.parse_args()

    # Extract arguments as strings
    input_path = args.input
    config_path = args.config
    output_path = args.output

    run_pipeline(input_path=input_path, config_path=config_path, output_path=output_path)
