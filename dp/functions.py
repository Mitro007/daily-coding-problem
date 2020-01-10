import math
from typing import MutableSequence, Sequence, Tuple, Iterable


# LeetCode 91.
# Given the mapping a = 1, b = 2, ... z = 26, and an encoded message, count the number of ways it can be decoded.
# For example, the message '111' would give 3, since it could be decoded as 'aaa', 'ka', and 'ak'.
# You can assume that the messages are decodable. For example, '001' is not allowed.
# Time complexity: O(n).


def num_decodings(msg: str) -> int:
    dp = [0] * (len(msg) + 1)  # dp[i] = Num decodings for message[:i]
    dp[0] = 1  # Only one way to decode an empty message, which is an empty string
    dp[1] = 1 if '1' <= msg[0] <= '9' else 0

    for i in range(2, len(dp)):
        if '1' <= msg[i - 1] <= '9':
            dp[i] += dp[i - 1]

        if '10' <= msg[i - 2:i] <= '26':
            dp[i] += dp[i - 2]

    return dp[-1]


# LeetCode 279.
# 156. Given a positive integer n, find the smallest number of squared integers which sum to n.
#
# For example, given n = 13, return 2 since 13 = 32 + 22 = 9 + 4.
#
# Given n = 27, return 3 since 27 = 32 + 32 + 32 = 9 + 9 + 9.
def perfect_sq(n: int) -> int:
    # dp[i] is the smallest number of squared integers which sum to i
    def loop(i: int, dp: MutableSequence[int]) -> int:
        if i == 0:
            return 0
        if dp[i] > 0:
            return dp[i]

        x: int = int(math.sqrt(i))
        dp[i] = min([1 + loop(i - j * j, dp) for j in range(1, x + 1)])
        return dp[i]

    return loop(n, [0] * (n + 1))


# LeetCode 62.
# 158. You are given an N by M matrix of 0s and 1s. Starting from the top left corner, how many ways are there to
# reach the bottom right corner?
#
# You can only move right and down. 0 represents an empty space while 1 represents a wall you cannot walk through.
#
# For example, given the following matrix:
#
# [[0, 0, 1],
#  [0, 0, 1],
#  [1, 0, 0]]
# Return two, as there are only two ways to get to the bottom right:
#
# Right, down, down, right
# Down, right, down, right
# The top left corner and bottom right corner will always be 0.
#
# ANSWER: Let dp[i][j] be the number of ways to reach cell matrix[i][j].
#  a. dp[0][0] = 1
#  b. dp[i][j] = 0 if matrix[i][j] == 1
#  c. Otherwise, dp[i][j] is the sum of the number of ways to reach its neighbors
#
# Time and space complexities: Since we have to look at each cell in the worst case, O(mn).
def num_ways(matrix: Sequence[Sequence[int]]) -> int:
    m: int = len(matrix)
    n: int = len(matrix[0])

    def neighbors(r: int, c: int) -> Iterable[Tuple[int, int]]:
        return filter(
            lambda xy: 0 <= xy[0] < m and 0 <= xy[1] < n and matrix[xy[0]][xy[1]] == 0,
            [(r, c - 1), (r - 1, c)]
        )

    dp: MutableSequence[MutableSequence[int]] = [([0] * n) for _ in range(m)]
    dp[0][0] = 1

    def loop(r: int, c: int) -> int:
        if dp[r][c] > 0:
            return dp[r][c]
        dp[r][c] = sum(map(lambda xy: loop(xy[0], xy[1]), neighbors(r, c)))
        return dp[r][c]

    return loop(m - 1, n - 1)
