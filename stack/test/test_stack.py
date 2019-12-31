import pytest

from stack import functions as func


class TestStack:
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
