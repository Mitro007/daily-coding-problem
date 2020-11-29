import collections
import math
from typing import Iterable

import networkx as nx


class BellmanFord:
    """
    Computes shortest paths from a given source vertex to all of the other vertices in a weighted digraph,
    or detects a negative-weight cycle.

    Attributes
    ----------
    dist: Sequence
        shortest path distances of each vertex from the source or None if there exists a negative-weight cycle.
    negative_cycle: Iterable
        The vertices that make up the negative-weight cycle or None.

    Methods
    -------
    shortest_path(v: int)
        Returns the shortest path from source to the vertex v.
    """

    def __init__(self, g: nx.DiGraph, s: int):
        """
        Parameters
        ----------
        g: networkx.DiGraph
            Weighted digraph.
        s: int
            Source vertex.
        """
        n = g.number_of_nodes()
        # dist[i][v] = distance of node v from s using at most i edges
        dist = [[0] * n for _ in range(n + 1)]
        for v in list(g):
            if s != v:
                dist[s][v] = math.inf
        self._pred = [None] * n
        stable = True

        for i in range(1, n + 1):
            stable = True
            for v in list(g):
                u, _, w = min(
                    # g.in_edges(v, data=True)  -> (u, v, {'weight': 3.0})
                    g.in_edges(v, data=True),
                    key=lambda x: dist[i - 1][x[0]] + x[2]["weight"],
                    default=(None, v, {"weight": math.inf})
                )
                d = dist[i - 1][u] + w["weight"] if u is not None else w["weight"]
                if d < dist[i - 1][v]:
                    self._pred[v] = u
                    dist[i][v] = d
                    stable = False
                    if i == n:
                        break
                else:
                    dist[i][v] = dist[i - 1][v]

            if stable:
                break

        if not stable:
            self.dist = None
            self.negative_cycle = collections.deque()
            visited = set()
            u = v
            while u not in visited:
                visited.add(u)
                self.negative_cycle.appendleft(u)
                u = self._pred[u]
            self.negative_cycle.appendleft(v)
            self._pred = None
        else:
            self.dist = list(map(lambda v: dist[i - 1][v], list(g)))
            self.negative_cycle = None

    def shortest_path(self, v: int) -> Iterable[int]:
        """ Returns the shortest path from source to the vertex v.

        Parameters
        ----------
        v: int
            The vertex for which the shortest path is to be calculated.

        Returns
        -------
        Iterable[int]
            Vertices that are on the shortest path.

        Raises
        ------
        AssertionError
            If v isn't a vertex in the graph.
        AssertionError
            If there exists a negative-weight cycle.
        """

        assert not self.negative_cycle, "Negative-weight cycle"
        assert v < len(self.dist), f"Unknown vertex: {v}"
        path = collections.deque()
        u = v
        while u is not None:
            path.appendleft(u)
            u = self._pred[u]

        return path
