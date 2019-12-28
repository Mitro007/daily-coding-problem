import tree.functions as func
from tree.binary_tree import BinaryTree


class TestTree:
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
