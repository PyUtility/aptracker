#!/usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools import find_packages

sys.path.append(
    os.path.join(os.path.dirname(__file__))
)

import aptracker

setup(
    name = "aptracker",
    version = aptracker.__version__,
    description = "Advanced Project Tracker and Manager Application",
    long_description = open("README.md", "r").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/PyUtility/aptracker",
    packages = find_packages(
        exclude = ["tests*", "examples*"]
    ),
    install_requires = [
        "SQLAlchemy>=2.0"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires = ">=3.12"
)
