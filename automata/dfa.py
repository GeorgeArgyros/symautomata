"""This module contains the DFA implementation"""
# !/usr/bin/python
import imp
import copy
try:
    print 'Checking for pywrapfst module:',
    imp.find_module('pywrapfstp')
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
    try:
        print 'Checking for fst module:',
        imp.find_module('fstp')
        print 'OK'
        from fstdfa import FstDFA, TropicalWeight

        class DFA(FstDFA):
            """The DFA class implemented using openFst library"""
            pass

    except ImportError:
        print 'FAIL'
        print 'Fallback to python implementation: OK'
        from pythondfa import PythonDFA, TropicalWeight

        class DFA(PythonDFA):
            """The DFA class implemented using python"""

            def copy(self):
                mma = DFA()
                mma.states = copy.deepcopy(self.states)
                mma.alphabet = copy.deepcopy(self.alphabet)
                mma.isyms = copy.deepcopy(self.isyms)
                mma.osyms = copy.deepcopy(self.osyms)
                return mma
            pass
