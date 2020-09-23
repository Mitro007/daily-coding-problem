import math
from typing import MutableSequence, Sequence, Tuple, Iterable, Set


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


def _subset_sum(nums: Sequence[int], k: int) -> Sequence[Sequence[bool]]:
    """Helper method to solve the subset sum problem using dynamic programming.
    The problem has optimal substructure because if a number at index i is included to make sum j,
    there exists a subset of i - 1 numbers the sum of which is j - nums[i].

    The overlapping subproblems property is easy to see; consider nums = [1, 2, 3]. If k = 1, for any i in [0, 3),
    we can find a subset such that the sum is 1. Thus, d[i][1] would be true for all i in this case.

    This is a variation of the 0/1 Knapsack problem where the profits and weights are equal to the numbers.
    """
    n = len(nums)
    # dp[i][j] = True if sum j can be formed by taking some or all of the numbers from the first i numbers
    dp: MutableSequence[MutableSequence[bool]] = [[False for _ in range(k + 1)] for _ in range(n)]

    # Zero sum can be formed by taking no numbers regardless of i
    for i in range(n):
        dp[i][0] = True
    # If there is just one number, and it's not greater than j, it's included to make a sum equal to the number
    for j in range(1, k + 1):
        dp[0][j] = nums[0] == j

    for i in range(1, n):
        for j in range(1, k + 1):
            # The i-th number is included if:
            #   It is less than or equal to the sum j, and
            #   Sum j - nums[i] can be formed by taking some or all of the first i - 1 numbers
            # Else the i-th number is excluded
            dp[i][j] = dp[i - 1][j] or (nums[i] <= j and dp[i - 1][j - nums[i]])

    return dp


def _subset(dp: Sequence[Sequence[bool]], nums: Sequence[int], j: int) -> Set[int]:
    """Return the indices corresponding to the numbers that form a subset such that the sum is equal to j."""
    subset: Set[int] = set()
    k = j
    i = len(dp) - 1

    while k > 0:
        if dp[i][k] and dp[i - 1][k - nums[i]]:
            subset.add(i)
            k -= nums[i]
        i -= 1

    return subset


# LeetCode 416.
#
# ANSWER: There exists two subsets whose sums are equal if:
#  The total sum is even, and
#  There exists a subset of the numbers such that its sum is half of the total sum.
#
# Time complexity: O(nk), where k = sum(nums) // 2, arising from the nested for loops.
def equal_subset_sum(nums: Sequence[int]) -> Set[int]:
    s = sum(nums)
    if s % 2 != 0:
        return None
    k = s // 2
    dp = _subset_sum(nums, k)

    if not dp[-1][-1]:
        return None

    return _subset(dp, nums, k)


# 186. Given an array of positive integers, divide the array into two subsets such that the difference between the sum
# of the subsets is as small as possible.
#
# For example, given [5, 10, 15, 20, 25], return the sets {10, 25} and {5, 15, 20}, which has a difference of 5, which
# is the smallest possible difference.
#
# ANSWER: Note that the smallest possible difference between two subsets is zero. Thus, we proceed similar to the
# equal subset sum problem, except that in the end, we start backtracking from the greatest sum that could be made,
# instead of starting from k = sum // 2. In other words, we check if sum k could be made out of a subset, then we
# check if sum k - 1 could be made, so on and so forth. Note that the other subset may have a greater sum, but by
# maximizing the sum for this subset, we minimize the difference between the two sums.
def min_subset_sum(nums: Sequence[int]) -> Set[int]:
    s = sum(nums)
    k = s // 2
    dp = _subset_sum(nums, k)

    j = next(x for x in range(k, -1, -1) if dp[-1][x])

    return _subset(dp, nums, j)
