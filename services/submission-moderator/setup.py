#!/usr/bin/python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from submission_moderator import __doc__, __version__

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="submission-moderator",
    version=__version__,
    description=__doc__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/datascience-bot/submission-moderator",
    author="vogt4nick",
    author_email="vogt4nick@gmail.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    zip_safe=True,
    test_suite="tests",
    tests_require="pytest",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
