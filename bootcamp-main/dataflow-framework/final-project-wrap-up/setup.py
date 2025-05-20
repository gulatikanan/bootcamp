from setuptools import setup, find_packages

setup(
    name="file-processing-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.21.1",
        "pydantic>=1.10.7",
        "watchdog>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "file-processor=main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A dynamic, observable, fault-tolerant file processing system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-processing-system",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
