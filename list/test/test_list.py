import pytest

from list import functions as func
from list.linked_list import LinkedList


class TestList:
    def test_reverse(self):
        ll = LinkedList.from_iterable(range(1, 6))
        assert list(func.reverse(ll)) == list(range(5, 0, -1))

    def test_intersection(self):
        common = LinkedList.from_iterable([8, 10])
        l1 = LinkedList.from_iterable([3, 7])
        l2 = LinkedList.from_iterable([99, 1])
        l1.next.next = common
        l2.next.next = common

        assert func.intersection(l1, l2).val == 8

        l3 = LinkedList(1)
        l3.next = common
        assert func.intersection(l1, l3).val == 8

    def test_sum(self):
        l1 = LinkedList.from_iterable([9, 9])
        l2 = LinkedList.from_iterable([5, 2])

        assert list(func.sum(l1, l2)) == [4, 2, 1]

        l1 = LinkedList.from_iterable([1, 2, 1])
        l2 = LinkedList.from_iterable([5])

        assert list(func.sum(l1, l2)) == [6, 2, 1]

        assert func.sum(l1, None) is l1
        assert func.sum(None, l2) is l2

    def test_swap_pairs(self):
        ll = LinkedList.from_iterable(range(1, 5))
        assert list(func.swap_pairs(ll)) == [2, 1, 4, 3]
        assert list(func.swap_pairs(LinkedList(1))) == [1]

    @pytest.mark.parametrize("itr", [
        [4, 1, -3, 99],
        [4, 2, 1, 3],
        [-1, 0, 3, 4, 5]
    ])
    def test_sort(self, itr):
        ll = LinkedList.from_iterable(itr)
        assert list(func.sort(ll)) == sorted(itr)

    @pytest.mark.parametrize("before, after, k", [
        ([1, 2, 3, 4, 5], [4, 5, 1, 2, 3], 2),
        ([0, 1, 2], [2, 0, 1], 4),
        ([7, 7, 3, 5], [3, 5, 7, 7], 2),
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
        ([1], [1], 0),
        ([1, 2], [1, 2], 0)
    ])
    def test_rotate_right(self, before, after, k):
        assert list(func.rotate_right(LinkedList.from_iterable(before), k)) == after
