#!/usr/bin/env python
import ez_setup
import sys
import os
import imp
import tempfile
ez_setup.use_setuptools()

PROJECT = 'symautomata'

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


installpywrapfst1 = """
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew doctor

sudo easy_install pip

brew install wget

brew install graphviz

cd ~
mkdir -p prefix
cd prefix
export PREFIX=$PWD
echo $PREFIX

mkdir -p openfst
cd openfst
wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.5.4.tar.gz
tar xzf openfst-1.5.4.tar.gz

rm -rf objdir
mkdir objdir
cd objdir
../openfst-1.5.4/configure --prefix=$PREFIX --enable-pdt --enable-bin --enable-ngram-fsts  --enable-python
make -j 4
make install

echo "export PREFIX=$(cd; pwd)/prefix" >> ~/.bashrc

echo 'export CPLUS_INCLUDE_PATH=$PREFIX/include:$CPLUS_INCLUDE_PATH
export LIBRARY_PATH=$PREFIX/lib:$LIBRARY_PATH
export LIBRARY_PATH=$PREFIX/lib/fst:$LIBRARY_PATH
export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$PREFIX/lib/fst:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$PREFIX/lib/fst:$PREFIX/lib:$DYLD_LIBRARY_PATH
export PATH=$PREFIX/bin:$PATH
export PYTHONPATH=$PREFIX/lib/python2.7/site-packages:$PYTHONPATH' >> ~/.bashrc

echo "source ~/.bashrc" >> ~/.bash_profile

echo $PREFIX

for f in `find $PREFIX/include/fst -type f | xargs grep isspace | cut -f 1 -d ':' | uniq`; do
  sed -i .bak 's/isspace/std::isspace/g' $f
done
pip install openfst
"""
installpywrapfst2="""
wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.5.4.tar.gz
tar zxvf openfst-1.5.4.tar.gz
cd openfst-1.5.4
./configure --enable-python
make
sudo make install
"""


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
                os.system(installpywrapfst2)
                try:
                    print 'Checking for pywrapfst module:',
                    imp.find_module('pywrapfst')
                    print 'OK'
                except ImportError:
                    print 'FAIL'
                    os.system(installpywrapfst1)
                    try:
                        print 'Checking again for pywrapfst module:',
                        imp.find_module('pywrapfst')
                    except ImportError:
                        print 'FAIL'
                        print 'The application will fallback to a python implementation during execution'
            else:
                print 'The application will fallback to a python implementation during execution'

check_for_fst()
