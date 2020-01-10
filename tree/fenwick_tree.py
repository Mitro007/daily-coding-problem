from typing import Sequence, MutableSequence


# 149. Given a list of numbers L, implement a method sum(i, j) which returns the sum from the sublist L[i:j]
# (including i, excluding j).
#
# For example, given L = [1, 2, 3, 4, 5], sum(1, 3) should return sum([2, 3]), which is 5.
#
# You can assume that you can do some pre-processing. sum() should be optimized over the pre-processing step.
#
# ANSWER: Computing range sum each time is an O(n) operation. We can pre-process the array and store prefix sums in
# another array. Then range queries can be answered in O(1) time. However, if the original array changes, we need
# to update the prefix sum array, which is an O(n) time operation again. Instead, we will use a Fenwick tree, that
# provides O(log n) time operations updates and queries, and O(n) time construction.
#
# Each node i in the Fenwick tree stores the prefix sum [parent(i), i). So, node 1 stores the sum of the range [0, 0),
# node 8 stores the sum of [0, 7), node 10 stores the sum of [8, 9), and so on.
#
# Fenwick Tree range queries: https://www.youtube.com/watch?v=RgITNht_f4Q
# Fenwick Tree point updates: https://www.youtube.com/watch?v=B-BkW9ZpKKM
# Fenwick Tree construction: https://www.youtube.com/watch?v=BHPez138yX8
# Fenwick Tree or Binary Indexed Tree: https://www.youtube.com/watch?v=CWDQJGaN1gY
class FenwickTree:
    def __init__(self, nums: Sequence[int]):
        self._data: MutableSequence[int] = [0] * (len(nums) + 1)
        for i in range(1, len(self._data)):
            self._data[i] = nums[i - 1]
        for i in range(1, len(self._data)):
            j: int = FenwickTree._next(i)
            if 1 <= j < len(self._data):
                self._data[j] += self._data[i]

    def get(self, i: int) -> int:
        if 0 <= i < len(self._data) - 1:
            return self._data[i + 1]
        return None

    def add(self, i: int, val: int) -> None:
        j: int = i + 1
        if 1 <= j < len(self._data):
            self._data[j] += val
            self.add(FenwickTree._next(j) - 1, val)

    # range_sum(start, end) = range_sum(0, end) - range_sum(0, start - 1)
    # Note that we want to include start so exclude it from the 2nd term
    def range_sum(self, start: int, end: int) -> int:
        if end < start:
            return 0
        i: int = start + 1
        j: int = end + 1
        if i == j:
            return self._data[j]
        k: int = self._parent(j)
        return self._data[j] + self.range_sum(0, k - 1) - self.range_sum(0, start - 1)

    def __repr__(self) -> str:
        return str(self._data)

    @staticmethod
    def _next(i: int) -> int:
        """Return the index of the next node that is affected by an update to node i."""
        return i + FenwickTree._lsb(i)

    @staticmethod
    def _parent(i: int) -> int:
        """Return the index of the parent of node i."""
        return i - FenwickTree._lsb(i)

    # 1. If we subtract 1 from i, it will be subtracted from the right most set bit (say index j) and that bit will
    #    become 0. All bits to the right of j become 1, and all bits to the left of j stay the same.
    # 2. Then if we negate the result of step 1, the right most set bit will become 1.  All bits to the right of j
    #    become 0, and all bits to the left of j get flipped.
    # 3. Then if we bitwise and the result of step 2 with i, everything but the right most set bit is set to 0.
    @staticmethod
    def _lsb(i: int) -> int:
        return i & ~(i - 1)
