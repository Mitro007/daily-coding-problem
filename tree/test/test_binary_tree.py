import random

from tree.binary_tree import BinaryTree


class TestBinaryTree:
    def test_binary_tree_iterator(self):
        twenty_two = BinaryTree(22)
        thirty_five = BinaryTree(35)
        thirty = BinaryTree(30, twenty_two, thirty_five)
        five = BinaryTree(5)
        ten = BinaryTree(10, five, thirty)

        assert list(ten) == [5, 10, 22, 30, 35]

    def test_bst_from_iterable(self):
        lst = [5, 10, 22, 30, 35]
        random.shuffle(lst)

        assert list(BinaryTree.bst_from_iterable(lst)) == [5, 10, 22, 30, 35]

    def test_from_iterable(self):
        assert list(BinaryTree.from_iterable([1, 2, 3])) == [2, 1, 3]
        assert list(BinaryTree.from_iterable([-10, 9, 20, None, None, 15, 7])) == [9, -10, 15, 20, 7]
        assert list(BinaryTree.from_iterable([-1, None, 9, -6, 3, None, None, None, -2])) == [-1, -6, 9, 3, -2]
