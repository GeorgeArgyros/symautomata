# -*- coding: utf-8 -*-
"""**Context Free Grammars Manipulation.**

Basic context-free grammars manipulation for building uniform random generetors

.. *Authors:* Rogério Reis & Nelma Moreira

.. *This is part of FAdo project* http://fado.dcc.fc.up.pt

.. *Copyright:* 1999-2014 Rogério Reis & Nelma Moreira {rvr,nam}@dcc.fc.up.pt


.. This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License as published
   by the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
   for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   675 Mass Ave, Cambridge, MA 02139, USA."""

# __package__ = "FAdo"

import re
import string
from types import StringType


class CFGgrammarError():
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return "Error in rule %s" % self.rule


class CFGrammar(object):
    """ Class for context-free grammars

     :var Rules: grammar rules
     :var Terminals: terminals symbols
     :var Nonterminals: nonterminals symbols
     :var str Start: start symbol
     :var ntr: dictionary of rules for each nonterminal"""

    def __init__(self, gram):
        """Initialization

            :param gram: is a list for productions; each production is a tuple (LeftHandside, RightHandside) with
                LeftHandside nonterminal, RightHandside list of symbols, First production is for start symbol

        """
        self.Rules = gram
        self.Nonterminals = {r[0] for r in self.Rules}
        self.Terminals = set()
        for r in self.Rules:
            if type(r[1]) is StringType:
                if r[1] not in self.Nonterminals:
                    self.Terminals.add(r[1])
            else:
                for s in r[1]:
                    if s not in self.Nonterminals:
                        self.Terminals.add(s)
        self.Start = self.Rules[0][0]
        self.Nullable = {}
        self.tr = {}
        self.ntr = {}
        for i in xrange(len(self.Rules)):
            if self.Rules[i][0] not in self.ntr:
                self.ntr[self.Rules[i][0]] = {i}
            else:
                self.ntr[self.Rules[i][0]].add(i)

    def __str__(self):
        """Grammar rules

        :return: a string representing the grammar rules"""
        s = ""
        for n in xrange(len(self.Rules)):
            lhs = self.Rules[n][0]
            rhs = self.Rules[n][1]
            if type(rhs) is not StringType and len(rhs) > 1:
                rhs = string.join(rhs)
            s += "{0:s} | {1:s} -> {2:s} \n".format(n, lhs, rhs)
        return "Grammar Rules:\n\n%s" % s

    def maketerminals(self):
        """Extracts C{terminals} from the rules. Nonterminals must already exist"""
        self.Terminals = set()
        for r in self.Rules:
            if type(r[1]) is StringType:
                if r[1] not in self.Nonterminals:
                    self.Terminals.add(r[1])
            else:
                for s in r[1]:
                    if s not in self.Nonterminals:
                        self.Terminals.add(s)

    def makenonterminals(self):
        """Extracts C{nonterminals}  from grammar rules."""
        for r in self.Rules:
            self.Nonterminals.add(r[0])

    def terminalrules(self):
        self.tr = {}
        for a in self.Terminals:
            for i in xrange(len(self.Rules)):
                if self.Rules[i][1] == a:
                    if a not in self.tr:
                        self.tr[a] = {i}
                    else:
                        self.tr[a].add(i)

    def nonterminalrules(self):
        self.ntr = {}
        for i in xrange(len(self.Rules)):
            if self.Rules[i][0] not in self.ntr:
                self.ntr[self.Rules[i][0]] = {i}
            else:
                self.ntr[self.Rules[i][0]].add(i)

    def NULLABLE(self):
        """Determines which nonterminals X ->* [] """
        self.Nullable = {}
        for s in self.Terminals:
            self.Nullable[s] = 0
        for s in self.Nonterminals:
            self.Nullable[s] = 0
            if s in self.ntr:
                for i in self.ntr[s]:
                    if not self.Rules[i][1]:
                        self.Nullable[s] = 1
                        break
        k = 1
        while k == 1:
            k = 0
            for r in self.Rules:
                e = 0
                for i in r[1]:
                    if not self.Nullable[i]:
                        e = 1
                        break
                if e == 0 and not self.Nullable[r[0]]:
                    self.Nullable[r[0]] = 1
                    k = 1


class CNF(CFGrammar):
    """No useless nonterminals or epsilon rules are ALLOWED... Given a CFG grammar description generates one in CNF
      Then its possible to random generate words of a given size. Before some pre-calculations are nedded."""

    def __init__(self, gram, mark="A@"):
        # super(CNF, self).__init__(gram)
        CFGrammar.__init__(self, gram)
        self.mark = mark
        self.newnt = 0
        self.nttr = {}
        self.unitary = self.get_unitary()
        self.Chomsky()

    def get_unitary(self):
        return set([r for r in self.Rules if
                    (type(r[1]) is StringType and
                     r[1] in self.Nonterminals) or
                    (len(r[1]) == 1 and r[1][0] in self.Nonterminals)])

    def elim_unitary(self):
        """Elimination of unitary rules """
        f = 1
        while f:
            f = 0
            self.unitary = self.get_unitary()

            for u in self.unitary:
                if type(u[1]) is StringType:
                    ui = u[1]
                else:
                    ui = u[1][0]
                if ui in self.ntr:
                    for i in self.ntr[ui]:
                        if (u[0], self.Rules[i][1]) not in self.Rules:
                            f = 1
                            self.Rules.append((u[0], self.Rules[i][1]))
                            self.ntr[u[0]].add(len(self.Rules) - 1)

        for u in self.unitary:
            self.Rules.remove(u)

    def get_ntr_tr(self, a):
        nta = self.mark + a
        self.Nonterminals.add(nta)
        self.Rules.append((nta, a))
        return nta

    def iter_rule(self, lhs, rhs, i):
        if type(rhs) is not StringType and len(rhs) == 2:
            self.Rules[i] = (lhs, rhs)
            return
        nta = self.mark + "_" + str(self.newnt)
        self.Nonterminals.add(nta)
        self.newnt += 1
        self.Rules.append((lhs, (rhs[0], nta)))
        self.iter_rule(nta, rhs[1:], i)

    def Chomsky(self):
        """ Transform to CNF """
        self.elim_unitary()
        self.nttr = {}
        # terminal a is replaced by A@_a in all rules > 2
        for a in self.Terminals:
            for i in xrange(len(self.Rules)):
                if type(self.Rules[i][1]) is not StringType and len(self.Rules[i][1]) >= 2 and a in self.Rules[i][1]:
                    if a not in self.nttr:
                        self.nttr[a] = self.get_ntr_tr(a)
                    rr = list(self.Rules[i][1])
                    for k in xrange(len(rr)):
                        if rr[k] == a:
                            rr[k] = self.nttr[a]
                    self.Rules[i] = (self.Rules[i][0], tuple(rr))
        n = len(self.Rules)
        for i in xrange(n):
            if type(self.Rules[i][1]) is not StringType and len(self.Rules[i][1]) > 2:
                self.iter_rule(self.Rules[i][0], self.Rules[i][1], i)


def gRules(rules_list, rulesym=":", rhssep=None, rulesep='|'):
    """Transforms a list of rules into  a grammar description.

      :param rules_list: is a list of rule where rule is a string  of the form: Word rulesym Word1 ... Word2 or  Word
          rulesym []
      :param rulesym: LHS and RHS rule separator
      :param rhssep: RHS values separator (None for white chars)
      :return: a grammar description """
    gr = []
    sep = re.compile(rulesym)
    # rsep = re.compile(rulesep)
    for r in rules_list:
        if type(r) is StringType:
            rule = r
        else:
            rule = r[0]
        m = sep.search(rule)
        if not m:
            continue
        else:
            if m.start() == 0:
                raise CFGgrammarError(rule)
            else:
                lhs = rule[0:m.start()].strip()
            if m.end() == len(rule):
                raise CFGgrammarError(rule)
            else:
                rest = string.strip(rule[m.end():])
                if rest == "[]":
                    rhs = []
                else:
                    multi = string.split(rest, rulesep)
                    rhs = []
                    for i in multi:
                        l = string.split(i, rhssep)
                        if len(l) > 1:
                            l = tuple(string.split(i, rhssep))
                        else:
                            l = l[0]
                        gr.append((lhs, l))
    return gr
