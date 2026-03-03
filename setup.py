from setuptools import setup, find_packages
import os

# Read the README for the PyPI description page
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="traceloop-local",
    version="0.1.0",
    description="A lightweight local AI agent execution recorder and replayer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rishab",
    author_email="kumarjharishab@gmail.com",
    url="https://github.com/Rishab87/traceloop",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask>=3.0.0",
        "click>=8.0.0",
        "rich>=13.0.0"
    ],
    entry_points={
        "console_scripts": [
            "traceloop=traceloop.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
