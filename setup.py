#!/usr/bin/env python

# Require setuptools. See http://pypi.python.org/pypi/setuptools for
# installation instructions, or run the ez_setup script found at
# http://peak.telecommunity.com/dist/ez_setup.py
from setuptools import setup, find_packages

setup(
    name = "instatrace",
    version = "1.0.0",
    author = "Peter Teichman",
    author_email = "peter@teichman.org",
    url = "http://wiki.github.com/pteichman/instatrace/",
    description = "Software statistics recorder/display",
    packages = ["instatrace"],
    test_suite = "tests",
    install_requires = ["argparse>=1.1"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    entry_points = {
        "console_scripts" : [
            "instatrace = instatrace.control:main"
        ]
    }
)
