from heap import functions as func


class TestHeap:
    def test_k_closest_points(self):
        assert func.k_closest_points([(1, 3), (-2, 2)], 1) == [(-2, 2)]
        closest = set(func.k_closest_points([(3, 3), (5, -1), (-2, 4)], 2))
        assert (-2, 4) in closest
        assert (3, 3) in closest
