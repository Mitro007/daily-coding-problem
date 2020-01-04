from collections import deque, defaultdict
from enum import Enum, auto
from typing import Sequence, Tuple, Set, Iterable, Deque, Dict, MutableSequence, DefaultDict


# 23. You are given an M by N matrix consisting of booleans that represents a board. Each True boolean represents a
# wall. Each False boolean represents a tile you can walk on.
#
# Given this matrix, a start coordinate, and an end coordinate, return the minimum number of steps required to reach
# the end coordinate from the start. If there is no possible path, then return null. You can move up, left, down, and
# right. You cannot move through walls. You cannot wrap around the edges of the board.
#
# For example, given the following board:
#
# [[f, f, f, f],
#  [t, t, f, t],
#  [f, f, f, f],
#  [f, f, f, f]]
# and start = (3, 0) (bottom left) and end = (0, 0) (top left), the minimum number of steps required to reach the end
# is 7, since we would need to go through (1, 2) because there is a wall everywhere else on the second row.
#
# ANSWER: We run BFS, because if the destination is nearby, DFS would waste time exploring the depths.
# Time and space complexities: O(mn). Complete traversal of maze will be done in the worst case (although I can't
# imagine a maze where we will need to visit all cells).
def path_in_maze(board: Sequence[Sequence[bool]], start: Tuple[int, int], dest: Tuple[int, int]) -> int:
    m: int = len(board)
    n: int = len(board[0])

    def neighbors(row: int, col: int) -> Iterable[Tuple[int, int]]:
        return [xy for xy in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                if 0 <= xy[0] < m and 0 <= xy[1] < n and not board[xy[0]][xy[1]]
                ]

    visited: Set[Tuple[int, int]] = set()
    queue: Deque[Tuple[Tuple[int, int], Tuple[int, int]]] = deque()
    queue.append((start, None))
    parent: Dict[Tuple[int, int], Tuple[int, int]] = dict()

    while queue:
        cell, prev = queue.popleft()
        if cell in visited:
            continue
        visited.add(cell)
        parent[cell] = prev

        if cell == dest:
            break

        for neighbor in filter(lambda xy: xy not in visited, neighbors(cell[0], cell[1])):
            queue.append((neighbor, cell))

    cell: Tuple[int, int] = dest
    path: Deque[Tuple[int, int]] = deque()

    while cell in parent:
        path.appendleft(cell)
        cell = parent[cell]

    print(f"The shortest path from {start} to {dest} is: {path}")
    return len(path) - 1  # We want the number of edges


# LeetCode 207.
# 92. We're given a hashmap with a key courseId and value a list of courseIds, which represents that the prerequisite
# of courseId is courseIds. Return a sorted ordering of courses such that we can finish all courses.
#
# Return null if there is no such ordering.
#
# For example, given {'CSC300': ['CSC100', 'CSC200'], 'CSC200': ['CSC100'], 'CSC100': []},
# should return ['CSC100', 'CSC200', 'CSC300'].
#
# ANSWER: Topological sort. We launch DFS from each vertex, and if we encounter another vertex that has unexplored
# neighbors, there's a cycle in the graph. Otherwise, we mark the vertex as visited and put it on a stack.
#
# Time and space complexities: O(|V|), since each vertex is visited once.
def sorted_courses(prerequisites: Dict[str, Sequence[str]]) -> Sequence[str]:
    class VertexState(Enum):
        NOT_VISITED = auto()
        VISITED = auto()
        VISITING = auto()

    stack: MutableSequence[str] = []
    visited: DefaultDict[str, VertexState] = defaultdict(lambda: VertexState.NOT_VISITED)

    def has_loop(course: str) -> bool:
        state: VertexState = visited[course]

        if state == VertexState.VISITING:
            return True
        elif state == VertexState.VISITED:
            return False
        else:
            visited[course] = VertexState.VISITING
            if course in prerequisites and prerequisites[course]:
                if any(has_loop(x) for x in prerequisites[course]):
                    return True
            stack.append(course)
            visited[course] = VertexState.VISITED

        return False

    return None if any(has_loop(course) for course in set(prerequisites.keys())) else stack


# LeetCode 79.
# 98. Given a 2D board of characters and a word, find if the word exists in the grid.
#
# The word can be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those
# horizontally or vertically neighboring. The same letter cell may not be used more than once.
#
# For example, given the following board:
#
# [
#   ['A','B','C','E'],
#   ['S','F','C','S'],
#   ['A','D','E','E']
# ]
# exists(board, "ABCCED") returns true, exists(board, "SEE") returns true, exists(board, "ABCB") returns false.
#
# ANSWER: We launch a DFS from each cell looking for the next letter in the word in one of the neighbors.
# If we get stuck, we backtrack until we found an unvisited neighbor.
#
# Time Complexity: The complexity is O(mn * 4^s) where m is the no. of rows and n is the no. of columns and s is
# the length of the input string. When we start searching from a character we have 4 choices of neighbors for the
# first character and subsequent characters have only 3 or fewer than 3 choices but we can take it as 4 (permissible
# sloppiness in upper bound). This sloppiness would be acceptable for large matrices. So for each character we have 4
# choices. Total no. of characters are s where s is the length of the input string. So one invocation of search
# function O(4^s) time. In the worst case the search is invoked for mn times. So an upper bound would be O(mn * 4^s).
def has_word(board: Sequence[Sequence[str]], word: str) -> bool:
    m: int = len(board)
    n: int = len(board[0])

    def neighbors(row: int, col: int, i: int) -> Iterable[Tuple[int, int]]:
        return [xy for xy in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                if 0 <= xy[0] < m and 0 <= xy[1] < n and i < len(word) and board[xy[0]][xy[1]] == word[i]]

    def search(cell: Tuple[int, int], i: int, visited: Set[Tuple[int, int]]) -> bool:
        if cell not in visited:
            visited.add(cell)

            # any returns False on empty iterables
            if i < len(word) - 1 and \
                    not any(search(neighbor, i + 1, visited) for neighbor in neighbors(cell[0], cell[1], i + 1)):
                visited.remove(cell)
                return False

        return len(visited) >= len(word)

    for row in range(m):
        for col in range(n):
            if board[row][col] == word[0] and search((row, col), 0, set()):
                return True

    return False
