"""This module contains the DFA implementation"""
# !/usr/bin/python
import imp
try:
    print 'Checking for pywrapfst module:',
    imp.find_module('pywrapfst')
    print 'OK'
    from pywrapfstdfa import PywrapfstDFA, TropicalWeight

    class DFA(PywrapfstDFA):
        """The DFA class implemented using openFst library"""
        pass
except ImportError:
    print 'FAIL'
    print 'Pywrapfst module is not installed.'
    try:
        print 'Checking for pyfst module:',
        imp.find_module('fst')
        print 'OK'
        from fstdfa import FstDFA, TropicalWeight

        class DFA(FstDFA):
            """The DFA class implemented using openFst library"""
            pass

    except ImportError:
        print 'FAIL'
        print 'Fst module is not installed.'
        print 'Fallback to python implementation:',
        from pythondfa import PythonDFA, TropicalWeight

        class DFA(PythonDFA):
            """The DFA class implemented using python"""
            pass
