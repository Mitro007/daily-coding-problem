from array import functions as func
from typing import MutableSequence


class TestArray:
    def test_rotate(self):
        seq: MutableSequence[int] = list(range(1, 7))
        func.rotate(seq, 2)

        assert seq == [5, 6, 1, 2, 3, 4]

        seq = list(range(1, 7))
        func.rotate(seq, -2)

        assert seq == [3, 4, 5, 6, 1, 2]
