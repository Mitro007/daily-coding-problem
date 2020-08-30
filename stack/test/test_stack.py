import pytest
import collections
from stack import functions as func


class TestStack:
    def test_merge_overlapping_intervals(self):
        assert func.merge_overlapping_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]) == \
               [(1, 6), (8, 10), (15, 18)]
        assert func.merge_overlapping_intervals([(1, 4), (4, 5)]) == [(1, 5)]
        assert func.merge_overlapping_intervals([(1, 4), (0, 4)]) == [(0, 4)]
        assert func.merge_overlapping_intervals([(1, 4), (2, 3)]) == [(1, 4)]
        assert func.merge_overlapping_intervals([(2, 3), (4, 5), (6, 7), (8, 9), (1, 10)]) == [(1, 10)]
        assert func.merge_overlapping_intervals(
            [(0, 0), (1, 2), (5, 5), (2, 4), (3, 3), (5, 6), (5, 6), (4, 6), (0, 0), (1, 2), (0, 2), (4, 5)]
        ) == [(0, 6)]
        assert func.merge_overlapping_intervals(
            [(1, 1), (8, 10), (4, 6), (5, 8), (9, 11), (9, 11), (7, 7), (8, 12), (9, 10), (4, 6), (8, 12), (5, 9)]
        ) == [(1, 1), (4, 12)]
        assert func.merge_overlapping_intervals(
            [(3, 3), (1, 1), (0, 2), (2, 2), (1, 2), (1, 3), (1, 1), (3, 3), (2, 3), (4, 6)]
        ) == [(0, 3), (4, 6)]

    @pytest.mark.parametrize("hist, expected", [
        ([2, 3, 1, 4, 5, 4, 2], 12),
        ([6, 2, 5, 4, 5, 1, 6], 12),
        ([6, 5, 8, 6, 2], 20),
        ([1, 6, 4, 6], 12)
    ])
    def test_largest_area_in_hist(self, hist, expected):
        assert func.largest_area_in_hist(hist) == expected

    @pytest.mark.parametrize("s, valid", [
        ("", True),
        ("()", True),
        ("(*)", True),
        ("(*))", True),
        ("(*))", True),
        (")*(", False)
    ])
    def test_is_valid_parenthesis_str(self, s, valid):
        assert func.is_valid_parenthesis_str(s) == valid

    def test_eval_rpn(self):
        assert func.eval_rpn(["5", "3", "+"]) == 8
        assert func.eval_rpn(["2", "1", "+", "3", "*"]) == 9
        assert func.eval_rpn(["4", "13", "5", "/", "+"]) == 6
        assert func.eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
        assert func.eval_rpn([15, 7, 1, 1, '+', '-', '/', 3, '*', 2, 1, 1, '+', '+', '-']) == 5

    def test_interleave(self):
        assert all(x == y for x, y in zip(func.interleave(collections.deque(range(1, 6))), [1, 5, 2, 4, 3]))
        assert all(x == y for x, y in zip(func.interleave(collections.deque(range(1, 5))), [1, 4, 2, 3]))
