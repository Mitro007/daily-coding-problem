import sys
from typing import TypeVar

from tree.binary_tree import BinaryTree

T = TypeVar("T")


# 133. Given a node in a binary search tree, return the next bigger element, also known as the inorder successor.
# You can assume each node has a parent pointer.
# ANSWER:
# if node has a right tree, smallest node there
# else if it is a left child, parent node
# else first larger parent node
def inorder_successor(node: BinaryTree[T]) -> T:
    def _smallest(root: BinaryTree[T]) -> BinaryTree[T]:
        y: BinaryTree[T] = root

        while y.left:
            y = y.left

        return y

    if node.right:
        return _smallest(node.right).val
    elif node is node.parent.left:
        return node.parent.val

    x: BinaryTree[T] = node
    while x is x.parent.right:
        x = x.parent

    return x.parent.val


# 135. Given a binary tree, find a minimum path sum from root to a leaf.
#
# For example, the minimum path in this tree is [10, 5, 1, -1], which has sum 15.
# +---+10+---+
# |          |
# 5+---+     5+----+
#      |           |
#      2     +----+1
#            |
#            |
#            -1
def min_path_sum(root: BinaryTree[int]) -> int:
    def _min_sum(node: BinaryTree[int], best: int, sum_so_far: int) -> int:
        if node is None:
            return best

        if node.left is None and node.right is None:
            return min(sum_so_far + node.val, best)

        min_left: int = _min_sum(node.left, best, sum_so_far + node.val)
        min_right: int = _min_sum(node.right, min(min_left, best), sum_so_far + node.val)

        return min(min_left, min_right)

    if root is None:
        return 0
    return _min_sum(root, sys.maxsize, 0)
