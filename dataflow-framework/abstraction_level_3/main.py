from cli import parse_args
from pipeline import load_pipeline
from core import process_file

def main():
    args = parse_args()
    processors = load_pipeline(args.config)
    process_file(args.input, processors)

if __name__ == "__main__":
    main()
