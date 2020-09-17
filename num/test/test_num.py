import pytest

from num import functions as func


class TestNum:
    def test_square_root(self):
        tolerance: float = 0.0001
        assert func.square_root(7, tolerance) == pytest.approx(2.6457, tolerance)

    def test_markov(self):
        freq = func.markov("a", {
            "a": {"a": 0.9, "b": 0.075, "c": 0.025},
            "b": {"a": 0.15, "b": 0.8, "c": 0.05},
            "c": {"a": 0.25, "b": 0.25, "c": 0.50}
        }, 100)
        assert sum(freq.values()) == 100

    def test_gcd(self):
        assert func.gcd([1]) == 1
        assert func.gcd([1071, 462]) == 21
        assert func.gcd([42, 56, 14]) == 14
