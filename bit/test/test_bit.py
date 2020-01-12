from bit import functions as func


class TestBit:
    def test_unique_numbers(self):
        uniq = func.unique_numbers(1, 2, 1, 3, 2, 5)
        assert uniq == (3, 5) or uniq == (5, 3)

    def test_gray_codes(self):
        assert list(func.gray_codes(2)) == [0, 1, 3, 2]

    def test_reverse_bits(self):
        assert func.reverse_bits(43261596) == 964176192
        assert func.reverse_bits(4294967293) == 3221225471
