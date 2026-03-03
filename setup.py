from setuptools import setup, find_packages

setup(
    name="traceloop",
    version="0.1.0",
    description="A lightweight local AI agent execution recorder and replayer.",
    author="Rishab",
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
)
