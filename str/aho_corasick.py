from __future__ import annotations

import collections
from typing import Sequence, MutableMapping, MutableSequence


# Let there be a set of strings with the total length m (sum of all lengths). The Aho-Corasick algorithm constructs a
# data structure similar to a trie with some additional links, and then constructs a finite state machine (automaton)
# in O(mk) time, where k is the size of the used alphabet.
#
# See https://www.youtube.com/watch?v=OFKxWFew_L0
class AhoCorasickAutomaton:
    def find(self, word: str) -> Node:  # noqa: F821
        node = self.root
        for ch in word:
            if ch not in node.children:
                return None
            node = node.children[ch]

        return node

    class Node:
        def __init__(self):
            self.parent: AhoCorasickAutomaton.Node = None
            self.word: str = None
            self.ch: str = None
            self.failure: AhoCorasickAutomaton.Node = None
            self.output: AhoCorasickAutomaton.Node = None
            self.children: MutableMapping[str, AhoCorasickAutomaton.Node] = {}
            self.val: MutableSequence[int] = []

        def add(self, word: str, i: int):
            node = self
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = AhoCorasickAutomaton.Node()
                node.children[ch].parent = node
                node = node.children[ch]
                node.ch = ch
            node.word = word
            node.val.append(i)

        # Failure link points to the node that is the longest proper suffix that exists in the tree. It may or may not
        # point to a word node.
        # Example:
        #   "abc"'s proper suffixes are "bc", "c", and "". If patterns "bc" and "c" both exist in the tree, the
        #   failure link from node 'c' of "abc' would point to the node 'c' of "bc".
        # Algorithm:
        #   Follow w's failing edge to node x.
        #   If node xa exists, wa has a failing edge to xa. Otherwise, follow x's failing edge and repeat.
        #   If we need to follow all the way back to the root, then wa's failing edge points to the root.
        def add_failure(self, root: AhoCorasickAutomaton.Node):
            if self is root:
                return
            elif self.parent is root:
                self.failure = root
            else:
                x = self.parent.failure
                while not self.failure:
                    if self.ch in x.children:
                        self.failure = x.children[self.ch]
                    elif x is root:
                        self.failure = x
                    else:
                        x = x.failure

        # Output link points to the word node found by following the failure links.
        def add_output(self, root: AhoCorasickAutomaton.Node):
            if self is root:
                return
            assert self.failure, "Cannot add output link when suffix link is undefined"
            self.output = self.failure if self.failure.word else self.failure.output

        def __repr__(self):
            return f"{self.ch}"

    def __init__(self, words: Sequence[str]):
        self.root = AhoCorasickAutomaton.Node()

        for i, w in enumerate(words):
            self.root.add(w, i)

        # Observation 1: Failing edges point from longer strings to shorter strings.
        # Observation 2: If we precompute failing edges for nodes in ascending order of string length, all of the
        # information needed for the above approach will be available at the time we need it.
        #
        # Enter BFS.
        queue = collections.deque()
        visited = set()
        queue.append(self.root)
        visited.add(self.root)
        num_nodes_in_level = 1
        num_nodes_in_next_level = 0

        while queue:
            node = queue.popleft()
            node.add_failure(self.root)
            node.add_output(self.root)

            for child in node.children.values():
                if child not in visited:
                    queue.append(child)
                    visited.add(child)
                    num_nodes_in_next_level += 1

            num_nodes_in_level -= 1
            if not num_nodes_in_level:
                num_nodes_in_level = num_nodes_in_next_level
                num_nodes_in_next_level = 0
