#!/usr/bin/env python

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nothoney',
    py_modules=['nothoney'],
    version='0.1.2',
    description='recursively iterate through a nested (n-deep) dictionary or JSON object/file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/vesche/nothoney',
    author='Austin Jackson',
    author_email='vesche@protonmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
