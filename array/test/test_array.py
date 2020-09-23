from typing import MutableSequence

import pytest

from array import functions as func


class TestArray:
    def test_missing_int(self):
        assert func.missing_int([1, 2, 1, 0]) == 3
        assert func.missing_int([3, 4, -1, 1]) == 2
        assert func.missing_int([7, 8, 9, 11, 12]) == 1
        assert func.missing_int([1]) == 2
        assert func.missing_int([]) == 1
        assert func.missing_int([0]) == 1
        assert func.missing_int([2, 1]) == 3
        assert func.missing_int([-1, -2, -3]) == 1
        assert func.missing_int([1, 1]) == 2
        assert func.missing_int([1000, -1]) == 1
        assert func.missing_int([-10, -3, -100, -1000, -239, 1]) == 2
        assert func.missing_int([1, 1]) == 2

    def test_subarray_sum(self):
        assert list(func.subarray_sum(range(1, 6), 9)) == list(range(2, 5))
        assert list(func.subarray_sum([1, 2, 3, 4, 5], 0)) == []
        assert list(func.subarray_sum([1, 2, 3, 4, 5], 1)) == [1]
        assert list(func.subarray_sum([1, 2, 3, 4, 5], 5)) == [2, 3]
        assert list(func.subarray_sum([5, 4, 3, 4, 5], 12)) == [5, 4, 3]
        assert list(func.subarray_sum([5, 4, 3, 4, 5], 11)) == [4, 3, 4]
        assert list(func.subarray_sum([1, 2, 3, 4, 5], 9)) == [2, 3, 4]
        assert list(func.subarray_sum([1, 2, 3, 4, 5], 3)) == [1, 2]

    def test_longest_consecutive_seq(self):
        assert func.longest_consecutive_seq([100, 4, 200, 1, 3, 2]) == 4
        assert func.longest_consecutive_seq([]) == 0
        assert func.longest_consecutive_seq([1, 0, -1]) == 3
        assert func.longest_consecutive_seq([9, 1, -3, 2, 4, 8, 3, -1, 6, -2, -4, 7]) == 4

    @pytest.mark.parametrize("nums, total", [
        ([34, -50, 42, 14, -5, 86], 137),
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([8, -19, 5, -4, 20], 21),
        ([-1, -2, -3], 0)
    ])
    def test_max_subarray_sum(self, nums, total):
        assert func.max_subarray_sum(nums) == total

    def test_count_inversions(self):
        assert func.count_inversions([2, 4, 1, 3, 5]) == 3
        assert func.count_inversions([5, 4, 3, 2, 1]) == 10
        assert func.count_inversions([1, 2, 3, 4, 5]) == 0

    @pytest.mark.parametrize("nums", [
        [4, 5, 6, 7, 0, 1, 2],
        [13, 18, 25, 2, 8, 10],
        [3, 1],
        [5, 1, 3],
        [4, 5, 6, 7, 8, 1, 2, 3]
    ])
    def test_search_in_rotated_sorted_array(self, nums):
        for i, v in enumerate(nums):
            assert func.search_in_rotated_sorted_array(nums, v) == i

    def test_two_sum(self):
        assert func.two_sum([2, 7, 11, 15], 9) == (0, 1)
        assert func.two_sum([3, 2, 4], 6) == (1, 2)
        assert func.two_sum([3, 3], 6) == (0, 1)

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

    def test_pancake_sort(self):
        arr = [3, 2, 4, 1]
        func.pancake_sort(arr)
        assert arr == list(range(1, 5))

        arr = list(reversed(range(1, 10)))
        func.pancake_sort(arr)
        assert arr == list(range(1, 10))

    def test_find_dup(self):
        assert func.find_dup([1, 3, 4, 2, 2]) == 2
        assert func.find_dup([3, 1, 3, 4, 2]) == 3
        assert func.find_dup([2] * 5) == 2

    def test_count_smaller(self):
        assert func.count_smaller([3, 4, 9, 6, 1]) == [1, 1, 2, 1, 0]
        assert func.count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]

    def test_rotate_matrix(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        func.rotate_matrix(matrix)
        assert matrix == [
            [7, 4, 1],
            [8, 5, 2],
            [9, 6, 3]
        ]
        matrix = [
            [5, 1, 9, 11],
            [2, 4, 8, 10],
            [13, 3, 6, 7],
            [15, 14, 12, 16]
        ]
        func.rotate_matrix(matrix)
        assert matrix == [
            [15, 13, 2, 5],
            [14, 3, 4, 1],
            [12, 6, 8, 9],
            [16, 7, 10, 11]
        ]

    def test_max_guests(self):
        assert func.max_guests([(1, 4), (2, 5), (9, 12), (5, 9), (5, 12)]) == (5, 3)

    def test_area_of_overlap(self):
        assert func.area_of_overlap(((1, 4), (3, 3)), ((0, 5), (4, 3))) == 6
        assert func.area_of_overlap(((0, 0), (2, 2)), ((1, 1), (2, 2))) == 1
        assert func.area_of_overlap(((0, 0), (3, 2)), ((1, 0), (1, 1))) == 1
        assert func.area_of_overlap(((0, 0), (1, 1)), ((1, 0), (1, 1))) == 0
        assert func.area_of_overlap(((4, 0), (2, 6)), ((-5, -3), (9, 5))) == 0

    def test_longest_distinct_subarray(self):
        assert func.longest_distinct_subarray([5, 1, 3, 5, 2, 3, 4, 1]) == 5

    def test_max_sum_circular_arr(self):
        assert func.max_sum_circular_arr([1, -2, 3, -2]) == 3
        assert func.max_sum_circular_arr([5, -3, 5]) == 10
        assert func.max_sum_circular_arr([3, -1, 2, -1]) == 4
        assert func.max_sum_circular_arr([3, -2, 2, -3]) == 3
        assert func.max_sum_circular_arr([-2, -3, -1]) == -1
        assert func.max_sum_circular_arr([-5, 3, 5]) == 8
        assert func.max_sum_circular_arr([8, 1, -5, -1, 9, -6]) == 12
        assert func.max_sum_circular_arr([-5, 4, -6]) == 4
