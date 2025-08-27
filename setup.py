#!/usr/bin/env python3
"""
Setup script for Pace Calculator
"""

from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pace-calculator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A beautiful, feature-rich pace calculator for runners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pace-calculator",
    py_modules=["pacecalc"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pacecalc=pacecalc:main",
        ],
    },
    keywords="running, pace, calculator, fitness, sports",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pace-calculator/issues",
        "Source": "https://github.com/yourusername/pace-calculator",
    },
)
