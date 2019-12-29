from collections import deque
from typing import Iterator, TypeVar, Generic, Deque

T = TypeVar("T")


# 139. Given an iterator with methods next() and hasNext(), create a wrapper iterator, PeekableInterface, which
# also implements peek(). peek shows the next element that would be returned on next().
#
# Here is the interface:
# class PeekableInterface(object):
#     def __init__(self, iterator):
#         pass
#
#     def peek(self):
#         pass
#
#     def next(self):
#         pass
#
#     def hasNext(self):
#         pass
#
# ANSWER: I took the liberty if slightly modifying the interface to make it more Pythonic.
class PeekableIterator(Generic[T], Iterator[T]):
    def __init__(self, iterator: Iterator[T]):
        self._iter: Iterator[T] = iterator
        self._elements: Deque[T] = deque()

    def peek(self) -> T:
        try:
            self._elements.append(next(self._iter))
        except StopIteration:
            return None
        else:
            return self._elements[-1]

    def __next__(self) -> T:
        if self._elements:
            return self._elements.popleft()
        return next(self._iter)
