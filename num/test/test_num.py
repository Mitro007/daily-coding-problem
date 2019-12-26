from num import functions as func
import pytest


class TestNum:
    def test_square_root(self):
        tolerance: float = 0.0001
        assert func.square_root(7, tolerance) == pytest.approx(2.6457, tolerance)
