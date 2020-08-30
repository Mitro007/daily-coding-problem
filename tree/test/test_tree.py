import pytest

import tree.functions as func
from tree.binary_tree import BinaryTree


class TestTree:
    def test_num_unival(self):
        assert func.num_unival(BinaryTree.build_level_order([0, 1, 0, 1, 1, 1, 0])) == 5
        assert func.num_unival(BinaryTree.build_level_order([5, 1, 5, 5, 5, None, 5])) == 4

    def test_eval_bintree(self):
        assert func.eval_bintree(BinaryTree.build_level_order(["*", "+", "+", "3", "2", "4", "5"])) == 45

    def test_inorder_successor(self):
        ten = BinaryTree(10)
        fourteen = BinaryTree(14)
        twelve = BinaryTree(12, ten, fourteen)

        four = BinaryTree(4)
        eight = BinaryTree(8, four, twelve)

        twenty_two = BinaryTree(22)
        BinaryTree(20, eight, twenty_two)

        assert func.inorder_successor(eight) == 10
        assert func.inorder_successor(ten) == 12
        assert func.inorder_successor(fourteen) == 20

    def test_min_path_sum_1(self):
        negative_one = BinaryTree(-1)
        one = BinaryTree(1, negative_one)
        five_right = BinaryTree(5, None, one)
        two = BinaryTree(2)
        five_left = BinaryTree(5, None, two)
        ten = BinaryTree(10, five_left, five_right)

        assert func.min_path_sum(ten) == 15

    def test_min_path_sum_2(self):
        zero = BinaryTree(0)
        one = BinaryTree(1, zero)
        three = BinaryTree(3, one)
        eight = BinaryTree(8)
        ten = BinaryTree(10, eight)
        seven = BinaryTree(7, three, ten)

        assert func.min_path_sum(seven) == 11

    def test_max_path_sum(self):
        assert func.max_path_sum(BinaryTree.build_level_order([1, 2, 3])) == 6
        assert func.max_path_sum(BinaryTree.build_level_order([-10, 9, 20, None, None, 15, 7])) == 42
        assert func.max_path_sum(BinaryTree.build_level_order([-2, 6, None, 0, -6])) == 6
        assert func.max_path_sum(BinaryTree.build_level_order([-1, None, 9, -6, 3, None, None, None, -2])) == 12

    def test_prune_zeros(self):
        root = BinaryTree.build_level_order([0, 1, 0, None, None, 1, 0, 0, 0])
        assert list(func.prune_zeros(root)) == [1, 0, 1, 0]

        root = BinaryTree.build_level_order([1, None, 0, 0, 1])
        assert list(func.prune_zeros(root)) == [1, 0, 1]

        root = BinaryTree.build_level_order([1, 0, 1, 0, 0, 0, 1])
        assert list(func.prune_zeros(root)) == [1, 1, 1]

        root = BinaryTree.build_level_order([1, 1, 0, 1, 1, 0, 1, 0])
        assert list(func.prune_zeros(root)) == [1, 1, 1, 1, 0, 1]

    def test_longest_path(self):
        assert func.longest_path([
            ("a", "b", 3), ("a", "c", 5), ("a", "d", 8),
            ("d", "e", 2), ("d", "f", 4),
            ("e", "g", 1), ("e", "h", 1)
        ]) == 17

    @pytest.mark.parametrize("nodes", [
        [2, 4, 3, 8, 7, 5],
        [5, 17, 19, 18, 16, 70, 85, 60, 20]
    ])
    def test_from_postorder(self, nodes):
        assert (list(func.from_postorder(nodes))) == sorted(nodes)
        assert (list(func.from_postorder_2(nodes))) == sorted(nodes)

    def test_from_postorder_and_inorder(self):
        postorder = [9, 15, 7, 20, 3]
        inorder = [9, 3, 15, 20, 7]
        assert list(func.from_postorder_and_inorder(postorder, inorder)) == inorder
