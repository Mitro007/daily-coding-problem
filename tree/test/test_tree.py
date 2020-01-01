import tree.functions as func
from tree.binary_tree import BinaryTree


class TestTree:
    def test_num_unival(self):
        assert func.num_unival(BinaryTree.from_iterable([0, 1, 0, 1, 1, 1, 0])) == 5
        assert func.num_unival(BinaryTree.from_iterable([5, 1, 5, 5, 5, None, 5])) == 4

    def test_eval_bintree(self):
        assert func.eval_bintree(BinaryTree.from_iterable(["*", "+", "+", "3", "2", "4", "5"])) == 45

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
        assert func.max_path_sum(BinaryTree.from_iterable([1, 2, 3])) == 6
        assert func.max_path_sum(BinaryTree.from_iterable([-10, 9, 20, None, None, 15, 7])) == 42
        assert func.max_path_sum(BinaryTree.from_iterable([-2, 6, None, 0, -6])) == 6
        assert func.max_path_sum(BinaryTree.from_iterable([-1, None, 9, -6, 3, None, None, None, -2])) == 12
