#!/usr/bin/env python3.8

# example of a setup.py file, never used this before
# https://github.com/bast/somepackage/blob/master/setup.py

from setuptools import setup
import os
import sys

TARGET = "spotutils"

_here = os.path.abspath(os.path.dirname(__file__))

if(sys.version_info[0] < 3):
  with open(os.path.join(_here, 'README.md')) as f:
    long_description = f.read()
else:
  with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = {}

with open(os.path.join(_here, TARGET, 'version.py')) as f:
    exec(f.read(), version)

setup(
    name = TARGET,
    version = version['__version__'],
    description = ('Command line tools to communicate with Spoitfy'),
    long_description = long_description,
    author = "Jared Dyreson",
    author_email = "jareddyreson@csu.fullerton.edu",
    url = "https://github.com/JaredDyreson/Spoterm",
    license = "GNU GPL-3.0",
    packages = [TARGET],
    dependency_links=['https://github.com/JaredDyreson/SpotifyPlaylist'],
    include_package_data = True
    classifiers = [
        'Programming Language :: Python :: 3.8'
    ]
)
