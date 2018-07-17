#!/usr/bin/env python3
from dynpaper import dynpaper
import os
import sys

from setuptools import setup, find_packages
# Dynamically calculate the version based on django.VERSION.
version = dynpaper.get_version()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='Dynpaper',
        version=version,
        url='https://www.github.com/oddproton/dynpaper',
        author='Stelios Tymvios',
        author_email='stelios.tymvios@icloud.com',
        description=('A dynamic wallpaper setter inspired by MacOS Mojave'),
        license='BSD 3-Clause "New" or "Revised" License',
        scripts=['bin/dynpaper']
    )
