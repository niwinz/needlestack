#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys


#INSTALL_REQUIRES = [
#    "jinja2 >=2.5",
#    "django >=1.4",
#]
#
#if sys.version_info < (2, 7):
#    INSTALL_REQUIRES.append('importlib')

setup(
    name = "needlestack",
    version = "0.1",
    description = "Modular search for Django"
    long_description = "",
    keywords = "django, search, elasticsearch, whoosh, solr",
    author = "Andrey Antukh",
    author_email = "niwi@niwi.be",
    url = "https://github.com/niwibe/needlestack",
    license = "BSD",
    packages = [
        # TODO
    ],

    # install_requires = INSTALL_REQUIRES,

    classifiers = [
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
