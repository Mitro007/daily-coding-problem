from __future__ import annotations

from typing import MutableMapping


class ShortestPrefixTrie:
    def __init__(self):
        self.children: MutableMapping[str, ShortestPrefixTrie] = dict()
        self.prefix: bool = False

    def insert(self, word: str) -> None:
        node: ShortestPrefixTrie = self

        for ch in word:
            node = node._insert(ch)

    def _insert(self, ch: str) -> ShortestPrefixTrie:
        if ch not in self.children:
            self.children[ch] = ShortestPrefixTrie()
            self.children[ch].prefix = True
        else:
            self.children[ch].prefix = False

        return self.children[ch]

    def shortest_prefix(self, word: str) -> str:
        node: ShortestPrefixTrie = self
        for i, ch in enumerate(word):
            if node.children[ch].prefix:
                return word[:i + 1]
            else:
                node = node.children[ch]

    def __repr__(self):
        return str(self.children.keys())
