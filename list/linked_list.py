from __future__ import annotations

from typing import TypeVar, Generic, Iterable

T = TypeVar("T")


class LinkedListIterator(Generic[T]):
    def __init__(self, ll: LinkedList[T]):
        self.node = ll

    def __next__(self):
        if self.node:
            val = self.node.val
            self.node = self.node.next
            return val
        raise StopIteration()


class LinkedList(Generic[T]):
    def __init__(self, val: T):
        self.val = val
        self.next = None

    def __iter__(self):
        return LinkedListIterator(self)

    def __repr__(self):
        return f"{self.val}"

    @classmethod
    def from_iterable(cls, itr: Iterable[T]) -> LinkedList[T]:
        result: LinkedList[T] = None
        head: LinkedList[T] = None

        for i in itr:
            if not result:
                result = cls(i)
                head = result
            else:
                result.next = cls(i)
                result = result.next

        return head
