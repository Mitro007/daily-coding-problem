from typing import MutableSequence

import pytest

from array import functions as func


class TestArray:
    def test_rotate(self):
        seq: MutableSequence[int] = list(range(1, 7))
        func.rotate(seq, 2)

        assert seq == [5, 6, 1, 2, 3, 4]

        seq = list(range(1, 7))
        func.rotate(seq, -2)

        assert seq == [3, 4, 5, 6, 1, 2]

        seq = list(range(1, 8))
        func.rotate(seq, 3)

        assert seq == [5, 6, 7, 1, 2, 3, 4]

        seq = [-1]
        func.rotate(seq, 2)

        assert seq == [-1]

    @pytest.mark.parametrize("prices, k, expected", [
        ([5, 2, 4, 0, 1], 2, 3),
        ([310, 315, 275, 295, 260, 270, 290, 230, 255, 250], 2, 55)
    ])
    def test_stock_1(self, prices, k, expected):
        assert func.stock_1(prices, k) == expected

    def test_largest_rect(self):
        matrix = [
            [1, 0, 0, 0],
            [1, 0, 1, 1],
            [1, 0, 1, 1],
            [0, 1, 0, 0]
        ]

        assert func.largest_rect(matrix) == 4

        matrix = [
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 0, 0]
        ]

        assert func.largest_rect(matrix) == 8

        matrix = [[1, 1]]

        assert func.largest_rect(matrix) == 2

    @pytest.mark.parametrize("coins, amt, expected", [
        ([1, 5, 10, 25], 16, 3),
        ([5, 10, 25], 30, 2),
        ([1, 5, 6, 9], 11, 2)
    ])
    def test_min_coins(self, coins, amt, expected):
        assert func.min_coins(coins, amt) == expected

    @pytest.mark.parametrize("arr, pivot", [
        ([9, 12, 3, 5, 14, 10, 10], 10),
        (["P", "A", "B", "X", "W", "P", "P", "V", "P", "D", "P", "C", "Y", "Z"], "P")
    ])
    def test_partition(self, arr, pivot):
        lt, gt = func.partition(arr, pivot)
        assert all(i < pivot for i in arr[:lt])
        assert all(i == pivot for i in arr[lt:gt + 1])
        assert all(i > pivot for i in arr[gt + 1:])
