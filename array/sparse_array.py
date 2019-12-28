from __future__ import annotations

import bisect
import sys
from abc import abstractmethod, ABC
from enum import Enum, auto
from typing import MutableSequence, Sequence, MutableMapping


class SparseArrayType(Enum):
    DICT_OF_KEYS = auto()
    LIST_OF_LIST = auto()


# 134. You have a large array with most of the elements as zero.
#
# Use a more space-efficient data structure, SparseArray, that implements the same interface:
#
# init(arr, size): initialize with the original large array and size.
# set(i, val): updates index at i with val.
# get(i): gets the value at index i.

class SparseArray(MutableSequence[int], ABC):
    def __delitem__(self, i: int) -> None:
        raise TypeError("Method not supported")

    def insert(self, index: int, o: int) -> None:
        raise TypeError("Method not supported")

    @abstractmethod
    def compression_percent(self) -> float: ...


# Advantages:
#
# Efficient access to individual items (O(1) on average)
# Good for write-heavy uses (O(1))

# Disadvantages:
#
# Slow iteration in index order (due to the random order of keys)
# Slow slicing
class DictionaryOfKeys(SparseArray):
    def __init__(self, arr: Sequence[int]):
        self._data: MutableMapping[int, int] = dict(kv for kv in enumerate(arr) if kv[1] > 0)
        self._len_arr = len(arr)
        self._sizeof_arr = sys.getsizeof(arr)

    def __getitem__(self, i: int) -> int:
        if i in self._data:
            return self._data[i]
        return 0

    def __setitem__(self, i: int, o: int) -> None:
        if o != 0:
            self._data[i] = o
        elif i in self._data:
            self._data.__delitem__(i)

    def __len__(self) -> int:
        return self._len_arr

    def compression_percent(self):
        return ((self._sizeof_arr - sys.getsizeof(self._data)) / self._sizeof_arr) * 100


# Advantages:
#
# Good for read-heavy uses. Efficient access to individual items (O(log n) worse case)
# Fast index-order iteration due to sorted indices
# Fast slicing

# Disadvantages:
#
# Not so good for write-heavy uses. __setitem__ can be O(n) for insertion and deletions
class ListOfList(SparseArray):
    def __init__(self, arr: Sequence[int]):
        self._len_arr = len(arr)
        self._sizeof_arr = sys.getsizeof(arr)
        # The following invariants hold for i in [0, len(_indices)):
        # arr[_indices[i]] != 0
        # _data[_indices[i]] == arr[_indices[i]]
        # len(_data) == len(_indices)

        # For better performance, use a deque and more specific insert/delete ops
        self._data: MutableSequence[int] = []
        self._indices: MutableSequence[int] = []

        for i, v in enumerate(arr):
            if v != 0:
                self._data.append(v)
                self._indices.append(i)

    def __getitem__(self, i: int) -> int:
        idx: int = bisect.bisect_left(self._indices, i)
        if idx < len(self._indices) and self._indices[idx] == i:
            return self._data[idx]
        return 0

    def __setitem__(self, i: int, o: int) -> None:
        idx: int = bisect.bisect_left(self._indices, i)
        if idx < len(self._indices) and self._indices[idx] == i:
            if o != 0:
                self._data[idx] = o
            else:
                self._indices.__delitem__(idx)
                self._data.__delitem__(idx)
        elif o != 0:
            self._indices.insert(idx, i)
            self._data.insert(idx, o)

        assert len(self._data) == len(self._indices), "Illegal state: data and indices must be of the same length"

    def __len__(self) -> int:
        return self._len_arr

    def compression_percent(self):
        return ((self._sizeof_arr - (sys.getsizeof(self._data) + sys.getsizeof(self._indices))) / self._sizeof_arr) * \
               100


def get_instance(array_type: SparseArrayType, array: Sequence[int]) -> SparseArray[int]:
    if array_type == SparseArrayType.DICT_OF_KEYS:
        return DictionaryOfKeys(array)
    else:
        return ListOfList(array)
