from graph import functions as func


class TestGraph:
    def test_path_in_maze(self):
        assert func.path_in_maze([
            [False] * 4,
            [True, True, False, True],
            [False] * 4,
            [False] * 4,
        ], (3, 0), (0, 0)) == 7

        assert func.path_in_maze([
            [False, False, True, False, False],
            [False] * 5,
            [False, False, False, True, False],
            [True, True, False, True, True],
            [False] * 5,
        ], (0, 4), (4, 4)) == 8

    def test_has_word(self):
        board = [
            ['A', 'B', 'C', 'E'],
            ['S', 'F', 'C', 'S'],
            ['A', 'D', 'E', 'E']
        ]
        assert func.has_word(board, "ABCCED")
        assert func.has_word(board, "SEE")
        assert not func.has_word(board, "ABCB")

        board = [
            ["A", "B", "C", "E"],
            ["S", "F", "E", "S"],
            ["A", "D", "E", "E"]
        ]
        assert func.has_word(board, "ABCESEEEFS")

    def test_sorted_courses(self):
        assert func.sorted_courses({'CSC300': ['CSC100', 'CSC200'], 'CSC200': ['CSC100'], 'CSC100': []}) == \
               ['CSC100', 'CSC200', 'CSC300']
        assert func.sorted_courses({'CSC200': ['CSC100'], 'CSC100': ['CSC200']}) is None
