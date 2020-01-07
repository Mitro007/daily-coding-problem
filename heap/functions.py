import heapq
from typing import Sequence, Tuple, MutableSequence


# LeetCode 973.
# 150. Given a list of points, a central point, and an integer k, find the nearest k points from the central point.
#
# For example, given the list of points [(0, 0), (5, 4), (3, 1)], the central point (1, 2), and k = 2,
# return [(0, 0), (3, 1)].
def k_closest_points(points: Sequence[Tuple[int, int]], k: int, center: Tuple[int, int] = (0, 0)) -> \
        Sequence[Tuple[int, int]]:
    def dist_sq(p: Tuple[int, int]) -> float:
        return (p[0] - center[0]) ^ 2 + (p[1] - center[1]) ^ 2

    pairs: MutableSequence[Tuple[float, Tuple[int, int]]] = [(dist_sq(p), p) for p in points]
    heapq.heapify(pairs)
    return [heapq.heappop(pairs)[1] for _ in range(k)]
