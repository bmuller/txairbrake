#!/usr/bin/env python
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

setup(
    name="txairbrake",
    version="0.1",
    description="txairbrake reports exceptions in Twisted code to an airbrake server",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/txairbrake",
    packages=["txairbrake"],
    requires=["twisted.words.xish", "twisted.web.client"]
)
