"""
Setup script for Real-time Audio Analysis Pipeline
"""
from setuptools import setup, find_packages

setup(
    name="realtime-audio-analyzer",
    version="1.0.0",
    description="Production-grade real-time audio analysis and visualization tool",
    author="Audio Analysis Pipeline",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "sounddevice>=0.4.6",
        "numpy>=1.21.0", 
        "matplotlib>=3.5.0",
        "scipy>=1.7.0",
        "librosa>=0.9.0",
        "soundfile>=0.10.0"
    ],
    entry_points={
        "console_scripts": [
            "audio-analyzer=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)