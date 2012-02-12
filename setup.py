#!/usr/bin/env python
""" setup.py for multimethods-py
"""

from distutils.core import setup

setup(
    name         = 'multimethods',
    version      = '0.2',
    description  = 'Clojure-style multimethods for Python',
    author       = 'Daniel Werner',
    url          = 'http://github.com/macro/multimethods',
    py_modules   = ['multimethods'],
    entry_points = {},
)
