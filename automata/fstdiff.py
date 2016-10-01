"""This module performs the diff operation between two
pyfst automata and returns the shortest string"""

from sys import argv
from operator import attrgetter
from dfa import TropicalWeight
from alphabet import createalphabet
from dfa import DFA
from flex2fst import Flexparser

class FstDiff:
    """This class performs the diff operation between two
    pyfst automata and returns the shortest string"""

    def __init__(self, input_fst_a, input_fst_b, alphabet=None):
        """
        Initialization function
        Args:
            input_fst_a (DFA): The first input DFA
            input_fst_b (DFA): The SECOND input DFA
            alphabet (list): The used Alphabet
        Returns:
            None
        """
        self.mma = DFA()
        self.mma.init_from_acceptor(input_fst_a)
        self.mmb = DFA()
        self.mmb.init_from_acceptor(input_fst_b)
        if alphabet is None:
            alphabet = createalphabet()
        self.alphabet = alphabet

    def _bfs(self, graph, start):
        """
        Finds the shortest string using BFS
        Args:
            graph (DFA): The DFA states
            start (DFA state): The DFA initial state
        Returns:
            str: The shortest string
        """
        # maintain a queue of paths
        queue = []
        visited = []
        # maintain a queue of nodes
        # push the first path into the queue
        queue.append([['', start]])
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            # get the last node from the path
            node = path[-1][1]
            if node.stateid not in visited:
                visited.append(node.stateid)
                # path found
                if node.final != TropicalWeight(float('inf')):
                    return "".join([mnode[0] for mnode in path])
                # enumerate all adjacent nodes, construct a new path and push
                # it into the queue
                for arc in node.arcs:
                    char = graph.isyms.find(arc.ilabel)
                    next_state = graph[arc.nextstate]
                    # print next_state.stateid
                    if next_state.stateid not in visited:
                        new_path = list(path)
                        new_path.append([char, next_state])
                        queue.append(new_path)

    def get_string(self, mma):
        """
        Uses BFS in order to find the shortest string
        Args:
            mma (DFA): The DFA states
        Returns:
            str: The BFS result
        """
        initialstates = sorted(
            mma.states,
            key=attrgetter('initial'),
            reverse=True)
        if len(initialstates) > 0:
            return self._bfs(mma, initialstates[0])
        else:
            return None

    def diff(self):
        """
        Automata Diff operation
        """
        self.mma.minimize()
        self.mmb.complement(self.alphabet)
        self.mmb.minimize()
        mmc = self.mma & self.mmb
        mmd = DFA()
        mmd.init_from_acceptor(mmc)
        mmd.minimize()
        return mmd


def main():
    """
    Testing function for DFA Diff Operation
    """
    if len(argv) < 2:
        print 'Usage: '
        print '         Get A String              %s fst_fileA fst_fileB' % argv[0]
        return

    flex_a = Flexparser()
    mma = flex_a.yyparse(argv[1])
    mma.minimize()

    flex_b = Flexparser()
    mmb = flex_b.yyparse(argv[2])
    mmb.minimize()

    ops = FstDiff(mma, mmb)
    mmc = ops.diff()

    string = ops.get_string(mmc)
    print string


if __name__ == '__main__':
    main()
