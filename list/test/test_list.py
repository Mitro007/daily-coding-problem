from list import functions as func
from list.linked_list import LinkedList


class TestList:
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
