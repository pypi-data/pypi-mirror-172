#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-black-ng",
    author="Will Hughes",
    author_email="will@willhughes.name",
    maintainer="Will Hughes",
    maintainer_email="will@willhughes.name",
    license="MIT",
    url="https://github.com/insertjokehere/pytest-black-ng",
    description="A pytest plugin to enable format checking with black",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["pytest_black"],
    python_requires=">=3.5",
    install_requires=[
        "black>=22.1.0",
        "pytest>=7.0.0",
        "toml",
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["black = pytest_black"]},
)
