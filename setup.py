"""
Setup script for building executable
"""

from setuptools import setup, find_packages

setup(
    name="VideoSplitter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PySide6==6.6.0",
    ],
    entry_points={
        "console_scripts": [
            "videosplitter=main:main",
        ],
    },
)
