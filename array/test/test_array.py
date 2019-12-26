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

    def test_stock_1(self):
        assert func.stock_1([5, 2, 4, 0, 1], 2) == 3
        assert func.stock_1([310, 315, 275, 295, 260, 270, 290, 230, 255, 250], 2) == 55
