#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "instatrace",
    version = "1.0",
    author = "Peter Teichman",
    author_email = "peter@teichman.org",
    url = "http://wiki.github.com/pteichman/instatrace/",
    description = "Software statistics recorder/display",
    packages = ["instatrace"],
    test_suite = "tests.suite",
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
