import unittest

import networkx as nx

from graph.bellman_ford import BellmanFord


class TestBellmanFord(unittest.TestCase):
    def test_bellman_ford(self):
        g = nx.DiGraph()
        g.add_weighted_edges_from([
            (0, 1, 4),
            (0, 2, 2),
            (1, 3, 4),
            (2, 1, -1),
            (2, 4, 2),
            (4, 3, 2)
        ])
        bf = BellmanFord(g, 0)
        assert bf.negative_cycle is None
        assert bf._pred is not None
        assert bf.dist == [0, 1, 2, 5, 4]
        assert list(bf.shortest_path(1)) == [0, 2, 1]
        assert list(bf.shortest_path(3)) == [0, 2, 1, 3]

        g = nx.DiGraph()
        # contains negative-weight cycle and zero-weight cycle
        g.add_weighted_edges_from([
            (0, 1, 3.0),
            (1, 2, -3.430337482745286),
            (2, 3, 0),
            (3, 4, - 2),
            (4, 5, - 5),
            (5, 0, 0),
            (3, 6, - 4),
            (6, 7, - 5),
            (7, 3, 9)
        ])

        bf = BellmanFord(g, 2)
        assert bf.negative_cycle is not None
        assert list(bf.negative_cycle) == [0, 1, 2, 3, 4, 5, 0]
        assert bf.dist is None
        assert bf._pred is None
        self.assertRaises(AssertionError, bf.shortest_path, 1)
