from __future__ import annotations

import collections
from typing import TypeVar, Generic, Iterable, Sequence, List, Deque

T = TypeVar("T")


class BinaryTreeIterator(Generic[T]):
    def __init__(self, bin_tree: BinaryTree[T]):
        self.tree: BinaryTree[T] = bin_tree
        self._stack: List[BinaryTree[T]] = []

        node: BinaryTree[T] = bin_tree

        while node:
            self._stack.append(node)
            node = node.left

    def __next__(self):
        if self._stack:
            node: BinaryTree[T] = self._stack.pop()
            val: T = node.val
            node = node.right
            while node:
                self._stack.append(node)
                node = node.left
            return val

        raise StopIteration()


class BinaryTree(Generic[T], Iterable[T]):
    def __init__(self, val: T, left: BinaryTree[T] = None, right: BinaryTree[T] = None):
        self.val: T = val
        self.left: BinaryTree[T] = left
        self.right: BinaryTree[T] = right
        self.parent: BinaryTree[T] = None
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    def __iter__(self):
        '''Returns an inorder iterator'''
        return BinaryTreeIterator(self)

    def __repr__(self):
        return f"{self.val}"

    @classmethod
    def build_level_order(cls, seq: Sequence[T]) -> BinaryTree[T]:
        """ Builds a binary tree in level-order fashion.

            Parameters
            ----------
            seq: Sequence[T]
                The sequence of node values.

            Returns
            -------
            BinaryTree[T]
                The binary tree that was built.
            """
        if not seq:
            return None
        queue: Deque[BinaryTree[T]] = collections.deque()
        root: BinaryTree[T] = BinaryTree(seq[0])
        queue.append(root)
        left: bool = True
        parent: BinaryTree[T] = None

        for i in range(1, len(seq)):
            if left:
                assert queue, "No parent found"
                parent = queue.popleft()
                if seq[i] is not None:
                    parent.left = BinaryTree(seq[i])
                    queue.append(parent.left)
            elif seq[i] is not None:
                parent.right = BinaryTree(seq[i])
                queue.append(parent.right)
            left = not left

        return root

    @classmethod
    def bst_from_iterable(cls, seq: Sequence[T]) -> BinaryTree[T]:
        values: Sequence[T] = sorted(seq)

        def _build_bst(lo: int, hi: int) -> BinaryTree[T]:
            if lo > hi:
                return None

            mid: int = lo + (hi - lo) // 2
            left = _build_bst(lo, mid - 1)
            right = _build_bst(mid + 1, hi)

            return cls(values[mid], left, right)

        return _build_bst(0, len(values) - 1)
