"""This module contains the DFA implementation"""
# !/usr/bin/python
import imp
import copy
try:
    print 'Checking for pywrapfst module:',
    imp.find_module('pywrapfst')
    print 'OK'
    from pywrapfstdfa import PywrapfstDFA, TropicalWeight

    class DFA(PywrapfstDFA):
        """The DFA class implemented using openFst library"""
        def copy(self):
            mma = DFA()
            mma.automaton =self.automaton.copy()
            mma.alphabet = copy.deepcopy(self.alphabet)
            mma.isyms = copy.deepcopy(self.isyms)
            mma.osyms = copy.deepcopy(self.osyms)
            return mma

        pass
except ImportError:
    print 'FAIL'
    print 'Pywrapfst module is not installed. Fallback to python implementation:',
    try:
        print 'Checking for fst module:',
        imp.find_module('fsta')
        print 'OK'
        from fstdfa import FstDFA, TropicalWeight

        class DFA(FstDFA):
            """The DFA class implemented using openFst library"""
            pass

    except ImportError:
        print 'FAIL'
        print 'Fst module is not installed. Fallback to python implementation:',
        from pythondfa import PythonDFA, TropicalWeight

        class DFA(PythonDFA):
            """The DFA class implemented using python"""
            pass
