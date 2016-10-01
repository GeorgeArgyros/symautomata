"""This modules generates a string from a CFG"""


class CFGGenerator(object):
    """This class generates a string from a CFG"""
    grammar = None
    resolved = None
    bfs_queue = None
    maxstate = 0

    def __init__(self, cfgr=None, optimized=1, splitstring=0, maxstate=0):
        """
        Object initialization
        Args:
            cfgr (CNF): grammar for the random objects
            optimized (bool): mode of operation - if enabled not all
                            CNF rules are included (mitigate O(n^3))
            splitstring (bool): A boolean for enabling or disabling
                            the splitting of symbols using a space
            maxstate (int): The maxstate is used for generating in a
                            dynamic way the CNF rules that were not
                            included due to the optimization. As a
                            result, the algorithm generates these
                            rules only if required.
        Returns:
            None
        """
        self.grammar = None
        self.resolved = None
        self.bfs_queue = None
        self.maxstate = 0
        self.grammar = cfgr
        self.optimized = optimized
        self.splitstring = splitstring
        self.grammar.terminalrules()
        # Because of the optimization, there are some non
        # existing terminals on the generated list
        if self.optimized:
            self._clean_terminals()
        self.grammar.nonterminalrules()
        self.resolved = {}
        self.bfs_queue = []
        self.maxstate = maxstate

    def generate(self):
        """
        Generates a new random string from the start symbol
        Args:
            None
        Returns:
            str: The generated string
        """

        result = self._gen(self.optimized, self.splitstring)
        if self.splitstring and result is not None:
            result = result[1:]
        return result

    def _clean_terminals(self):
        """
        Because of the optimization, there are some non existing terminals
        on the generated list. Remove them by checking for terms in form Ax,x
        """
        new_terminals = []
        for term in self.grammar.Terminals:
            x_term = term.rfind('@')
            y_term = term.rfind('A')
            if y_term > x_term:
                x_term = y_term
            ids = term[x_term + 1:].split(',')
            if len(ids) < 2:
                """It'input_string a normal terminal, not a state"""
                new_terminals.append(term)
        self.grammar.Terminals = new_terminals

    def _check_self_to_empty(self, stateid):
        """
        Because of the optimization, the rule for empty states is missing
        A check takes place live
        Args:
            stateid (int): The state identifier
        Returns:
            bool: A true or false response
        """
        x_term = stateid.rfind('@')
        y_term = stateid.rfind('A')
        if y_term > x_term:
            x_term = y_term
        ids = stateid[x_term + 1:].split(',')
        if len(ids) < 2:
            return 0
        if ids[0] == ids[1]:
            #    print 'empty'
            return 1
        return 0

    def _check_intemediate(self, myntr, maxstate):
        """
        For each state Apq which is a known terminal, this function
        searches for rules Apr -> Apq Aqr and Arq -> Arp Apq where
        Aqr is also a known terminal or Arp is also a known terminal.
        It is mainly used as an optimization in order to avoid the O(n^3)
        for generating all the Apq -> Apr Arq rules during the PDA to CFG
        procedure.
        Args:
            myntr (str): The examined non terminal that was poped out
                        of the queue
            maxstate (int): The maxstate is used for generating in a
                            dynamic way the CNF rules that were not
                            included due to the optimization. As a
                            result, the algorithm generates these
                            rules only if required.
        Returns:
            bool: Returns true if the algorithm was applied
                at least one time
        """
        # print 'BFS Dictionary Update - Intermediate'
        x_term = myntr.rfind('@')
        y_term = myntr.rfind('A')
        if y_term > x_term:
            x_term = y_term
        ids = myntr[x_term + 1:].split(',')
        if len(ids) < 2:
            return 0
        i = ids[0]
        j = ids[1]
        r = 0
        find = 0
        while r < maxstate:
            if r != i and r != j:
                if 'A' + i + ',' + \
                        repr(r) not in self.resolved \
                        and 'A' + j + ',' + repr(r) in self.resolved:
                    self.resolved[
                        'A' + i + ',' + repr(r)] = self.resolved[myntr] \
                                                   + self.resolved['A' + j + ',' + repr(r)]
                    if self._checkfinal('A' + i + ',' + repr(r)):
                        return self.resolved['A' + i + ',' + repr(r)]
                    if 'A' + i + ',' + repr(r) not in self.bfs_queue:
                        self.bfs_queue.append('A' + i + ',' + repr(r))
                    find = 1
                if 'A' + repr(r) + ',' + j not in self.resolved and 'A' + \
                        repr(r) + ',' + i in self.resolved:
                    self.resolved[
                        'A' + repr(r) + ',' + j] = self.resolved['A' + repr(r) + ',' + i] \
                                                   + self.resolved[myntr]
                    if self._checkfinal('A' + repr(r) + ',' + j):
                        return self.resolved['A' + repr(r) + ',' + j]
                    if 'A' + repr(r) + ',' + j not in self.bfs_queue:
                        self.bfs_queue.append('A' + repr(r) + ',' + j)
                    find = 1
            r = r + 1
        if find == 1:
            return 1
        return 0

    def _check_self_replicate(self, myntr):
        """
        For each Rule B -> c where c is a known terminal, this function
        searches for B occurences in rules with the form A -> B and sets
        A -> c.
        """
        # print 'BFS Dictionary Update - Self Replicate'
        find = 0
        for nonterm in self.grammar.ntr:
            for i in self.grammar.ntr[nonterm]:
                if self.grammar.Rules[i][0] not in self.resolved and not isinstance(
                        self.grammar.Rules[i][1], (set, tuple)) \
                        and self.grammar.Rules[i][1] == myntr:
                    self.resolved[self.grammar.Rules[i][0]] = self.resolved[myntr]
                    if self._checkfinal(self.grammar.Rules[i][0]):
                        return self.resolved[self.grammar.Rules[i][0]]
                    if self.grammar.Rules[i][0] not in self.bfs_queue:
                        self.bfs_queue.append(self.grammar.Rules[i][0])
                    find = 1
        if find == 1:
            return 1
        return 0

    def _check_self_nonterminals(self, optimized):
        """
        For each Rule A -> BC where B and C are known terminals (B -> c1 and C -> c2),
        this function searches replaces A to the corresponding terminals A -> c1c2
        """
        # print 'BFS Dictionary Update - Self Non Terminals'
        find = 0
        for nt in self.grammar.ntr:
            for i in self.grammar.ntr[nt]:
                if (self.grammar.Rules[i][0] not in self.resolved\
                    or self.grammar.Rules[i][0] == 'S') \
                    and isinstance(self.grammar.Rules[i][1], (set, tuple)):
                    # All rules are in CNF form, so first check the A -> BC rules
                    part_a = None
                    if optimized and self._check_self_to_empty(
                            self.grammar.Rules[i][1][0]):
                        part_a = ''
                    elif self.grammar.Rules[i][1][0] in self.resolved:
                        part_a = self.resolved[self.grammar.Rules[i][1][0]]
                    part_b = None
                    if optimized and self._check_self_to_empty(
                            self.grammar.Rules[i][1][1]):
                        part_b = ''
                    elif self.grammar.Rules[i][1][1] in self.resolved:
                        part_b = self.resolved[self.grammar.Rules[i][1][1]]
                    if part_a is not None and part_b is not None:
                        self.resolved[self.grammar.Rules[i][0]] = part_a + part_b
                        # print 'Non Terminals Resolving
                        # '+self.g.Rules[i][0]+": "+
                        # self.Resolved[self.g.Rules[i][0]]
                        if self._checkfinal(self.grammar.Rules[i][0]):
                            return self.resolved[self.grammar.Rules[i][0]]
                        if self.grammar.Rules[i][0] not in self.bfs_queue:
                            self.bfs_queue.append(self.grammar.Rules[i][0])
                        find = 1

        if find == 1:
            return 1
        return 0

    def _checkfinal(self, nonterminal):
        if nonterminal == 'S':
            return 1
        return 0

    def _gen(self, optimized, splitstring):
        """Generates a new random object generated from the nonterminal
        Args:
            optimized (bool): mode of operation - if enabled not all
                            CNF rules are included (mitigate O(n^3))
            splitstring (bool): A boolean for enabling or disabling
        Returns:
            str: The generated string
        """
        # Define Dictionary that holds resolved rules
        # (only in form A -> terminals sequence)
        self.resolved = {}
        # First update Resolved dictionary by adding rules
        # that contain only terminals (resolved rules)
        for nt in self.grammar.ntr:
            for i in self.grammar.ntr[nt]:
                if self.grammar.Rules[i][0] not in self.resolved\
                        and not isinstance(self.grammar.Rules[i][1], (set, tuple)):
                    if self.grammar.Rules[i][1] != '@empty_set' \
                            and self.grammar.Rules[i][1] in self.grammar.Terminals:

                        if splitstring:
                            self.resolved[
                                self.grammar.Rules[i][0]] = self.grammar.Rules[i][1]
                        else:
                            if self.grammar.Rules[i][1] == '&':
                                self.resolved[self.grammar.Rules[i][0]] = ' '
                            else:
                                self.resolved[
                                    self.grammar.Rules[i][0]] = self.grammar.Rules[i][1]
                        # print 'ResolvingA '+self.g.Rules[i][0]+": "+
                        # self.g.Rules[i][1]
                        if self._checkfinal(self.grammar.Rules[i][0]):
                            return self.resolved[self.grammar.Rules[i][0]]
                        if self.grammar.Rules[i][0] not in self.bfs_queue:
                            self.bfs_queue.append(self.grammar.Rules[i][0])
                    if self.grammar.Rules[i][1] == '@empty_set':
                        self.resolved[self.grammar.Rules[i][0]] = ''
                        # print 'ResolvingB '+self.g.Rules[i][0]+": "
                        self.bfs_queue.append(self.grammar.Rules[i][0])
                    if optimized and self._check_self_to_empty(
                            self.grammar.Rules[i][1]):
                        self.resolved[self.grammar.Rules[i][0]] = ''
                        # print 'ResolvingC '+self.g.Rules[i][0]+": "
                        if self.grammar.Rules[i][0] not in self.bfs_queue:
                            self.bfs_queue.append(self.grammar.Rules[i][0])

        # Then try to use the rules from Resolved dictionary and check
        # if there is another rule that can be resolved.
        # This should be done in a while loop
        change = 1
        while change:
            change = 0
            if not change:
                ret = self._check_self_nonterminals(optimized)
                if ret == 1:
                    change = 1
                elif ret != 0:
                    return ret
            if not change:
                while not change and len(self.bfs_queue) > 0:
                    myntr = self.bfs_queue.pop()
                    ret = self._check_self_replicate(myntr)
                    if ret == 1:
                        change = 1
                    elif ret != 0:
                        return ret
                    if optimized and self._check_intemediate(
                            myntr, self.maxstate):
                        change = 1
                        break
