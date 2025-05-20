#!/bin/bash
# run.sh - Alternative to Makefile for systems without make

# Display help information
function show_help {
    echo "File Processing System"
    echo "Usage:"
    echo "  ./run.sh [command] [options]"
    echo ""
    echo "Available commands:"
    echo "  run             - Run the system in watch mode"
    echo "  run-watch       - Run the system in watch mode (same as run)"
    echo "  run-file FILE   - Process a single file"
    echo "  clean           - Remove all processed files and logs"
    echo "  build-docker    - Build Docker image"
    echo "  run-docker      - Run the system in Docker container"
    echo "  build-package   - Build Python package"
    echo "  publish-package - Publish package to PyPI"
    echo "  help            - Show this help message"
}

# Process commands
case "$1" in
    run|run-watch)
        python main.py --watch
        ;;
    run-file)
        if [ -z "$2" ]; then
            echo "Error: Please specify a file path"
            echo "Usage: ./run.sh run-file path/to/file.txt"
            exit 1
        fi
        python main.py --input "$2"
        ;;
    clean)
        rm -rf watch_dir/processed/*
        rm -rf watch_dir/underprocess/*
        rm -rf results/*
        find . -name "__pycache__" -type d -exec rm -rf {} +
        find . -name "*.pyc" -delete
        echo "Cleaned up processed files and logs"
        ;;
    build-docker)
        docker build -t file-processor:latest .
        ;;
    run-docker)
        docker run -p 8000:8000 -v "$(pwd)/watch_dir:/app/watch_dir" -v "$(pwd)/results:/app/results" file-processor:latest
        ;;
    build-package)
        python setup.py sdist bdist_wheel
        ;;
    publish-package)
        twine upload dist/*
        ;;
    help|*)
        show_help
        ;;
esac
