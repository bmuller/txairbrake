#!/usr/bin/env python
from setuptools import setup, find_packages

from txairbrake import version

setup(
    name="txairbrake",
    version=version,
    description="txairbrake reports exceptions in Twisted code to an airbrake server",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/txairbrake",
    packages=find_packages(),
    requires=["twisted.words.xish", "twisted.web.client"]
)
