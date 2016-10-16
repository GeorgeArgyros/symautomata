"""This module contains the PDA implementation"""
# !/usr/bin/python
import imp
from pdadiff import PdaDiff
from alphabet import createalphabet

try:
    print 'Checking for pythonpda module:',
    imp.find_module('pythonpda')
    print 'OK'
    from pythonpda import PythonPDA

    class PDA(PythonPDA):
        """This is the structure for a PDA"""

        def shortest_string(self):
            """
            Uses BFS in order to find the shortest string
            Args:
                None
            Returns:
                str: The shortest string
            """
            ops = PdaDiff(None, None, self.alphabet)
            ops.mmc = self
            return ops.get_string()

        def diff(self, mmb):
            """
            Automata Diff operation
            """
            ops = PdaDiff(self, mmb, self.alphabet)
            mmc = ops.diff()
            return mmc

except ImportError:
    print 'FAIL'