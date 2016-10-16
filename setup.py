#!/usr/bin/env python
import ez_setup
import sys
import os
import imp
import tempfile
ez_setup.use_setuptools()

PROJECT = 'automata'

# Change docs/sphinx/conf.py too!
VERSION = '0.0.1'

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

    url='https://github.com/GeorgeArgyros/automata',
    download_url='https://github.com/GeorgeArgyros/automata/tarball/master',

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

def check_for_fst():
    try:
        print 'Checking for fst module:',
        imp.find_module('fst')
        print 'OK'
    except ImportError:
        print 'FAIL'
        try:
            print 'Checking for pywrapfst module:',
            imp.find_module('pywrapfst')
            print 'OK'
        except ImportError:
            print 'FAIL'
            print 'It is recommended to use openfst python bindings (either pyfst or pywrapfst)' \
                  ' for the DFA implementation. While this is not necessary, using openfst python' \
                  ' bindings will increase execution speed significally.'
            install = raw_input(
                ('* Install pywrapfst now? [y/n] ')
            )
            if install == 'y':
                current = os.getcwd()
                temp = tempfile.gettempdir()
                os.system('wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.5.3.tar.gz -P '+temp)
                if os.path.isfile(temp+'/openfst-1.5.3.tar.gz'):
                    os.system('cd '+temp+' && tar zxvf openfst-1.5.3.tar.gz')
                    os.system('cd '+temp+'/openfst-1.5.3 && ./configure --enable-python')
                    os.system('cd '+temp+'/openfst-1.5.3 && make')
                    os.system('cd '+temp+'/openfst-1.5.3 && sudo make install')
                    os.system('cd '+current)
                else:
                    sys.exit(('It was not possible to install'
                              'pywrapfst module. The application'
                              'will fallback to a python '
                              'implementation during execution'))
            else:
                sys.exit(('The application will fallback to a python '
                          'implementation during execution'))

check_for_fst()
