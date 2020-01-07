from tree.fenwick_tree import FenwickTree


class TestFenwickTree:
    def test_init(self):
        ft = FenwickTree([3, 4, -2, 7, 3, 11, 5, -8, -9, 2, 4, -8])
        assert ft.get(0) == 3
        assert ft.get(1) == 7
        assert ft.get(2) == -2
        assert ft.get(3) == 12
        assert ft.get(4) == 3
        assert ft.get(5) == 14
        assert ft.get(6) == 5
        assert ft.get(7) == 23
        assert ft.get(8) == -9
        assert ft.get(9) == -7
        assert ft.get(10) == 4
        assert ft.get(11) == -11

    def test_add(self):
        ft = FenwickTree([3, 4, -2, 7, 3, 11, 5, -8, -9, 2, 4, -8])
        ft.add(5, 3)
        assert ft.get(5) == 17
        assert ft.get(7) == 26

    def test_range_sum(self):
        ft = FenwickTree([3, 4, -2, 7, 3, 11, 5, -8, -9, 2, 4, -8])
        assert ft.range_sum(0, 6) == ft.get(6) + ft.get(5) + ft.get(3)
        assert ft.range_sum(3, 7) == 18
