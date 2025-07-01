#!/usr/bin/env python3
"""
Setup script for SPSR-LCP package
"""

from setuptools import setup, find_packages
import os
import sys

# Read the README file for long description
def read_file(filename):
    """Read a file and return its contents"""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt"""
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return [
            'tree-sitter>=0.20.0',
            'tree-sitter-languages>=1.7.0',
            'networkx>=2.8.0',
            'numpy>=1.21.0',
            'pandas>=1.4.0',
            'nltk>=3.7',
            'datasets>=2.0.0',
            'scipy>=1.8.0',
            'tqdm>=4.64.0',
            'pyyaml>=6.0',
            'rich>=12.0.0',
        ]

# Package metadata
__version__ = "1.0.0"
__author__ = "Research Team"

setup(
    name="spsr-lcp",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Structure-Aware Corpus Construction and User-Perception-Aligned Metrics for LLM Code Completion",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/SPSR-LCP/SPSR-LCP",
    project_urls={
        "Bug Reports": "https://github.com/SPSR-LCP/SPSR-LCP/issues",
        "Source": "https://github.com/SPSR-LCP/SPSR-LCP",
        "Documentation": "https://github.com/SPSR-LCP/SPSR-LCP/docs",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
            'pre-commit>=2.17.0',
        ],
        'docs': [
            'sphinx>=4.5.0',
            'sphinx-rtd-theme>=1.0.0',
            'myst-parser>=0.17.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'spsr-lcp=spsr_lcp.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        'code completion',
        'large language models',
        'evaluation metrics',
        'abstract syntax tree',
        'graph neural networks',
        'software engineering',
        'nlp',
        'machine learning'
    ],
) 