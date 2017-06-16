#!/usr/bin/env python
import ez_setup
import sys
import os
import imp
import tempfile
ez_setup.use_setuptools()

PROJECT = 'symautomata'

# Change docs/sphinx/conf.py too!
VERSION = '0.0.10'

from setuptools import setup, find_packages

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Automata classes',
    long_description=long_description,

    author='George Argyros, Ioannis Stais',
    author_email='ioannis.stais@gmail.com',

    url='https://github.com/GeorgeArgyros/symautomata',
    download_url='https://github.com/GeorgeArgyros/symautomata/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],
    scripts=[],
    provides=[],
    install_requires=['FAdo', 'python-dateutil'],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)


