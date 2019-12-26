from list.linked_list import LinkedList


class TestLinkedList:
    def test_linked_list(self):
        ll = LinkedList.from_iterable(range(5))
        assert list(ll) == list(range(5))
