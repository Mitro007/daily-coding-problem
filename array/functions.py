import sys
from typing import Sequence, MutableSequence, TypeVar, List

import stack.functions as stack

T = TypeVar("T")


def swap(seq: MutableSequence[T], i: int, j: int) -> None:
    if seq:
        assert 0 <= i < len(seq) and 0 <= j < len(seq)
        tmp = seq[i]
        seq[i] = seq[j]
        seq[j] = tmp


# 126. Write a function that rotates a list by k elements. For example, [1, 2, 3, 4, 5, 6] rotated by two becomes
# [3, 4, 5, 6, 1, 2]. Try solving this without creating a copy of the list.
# How many swap or move operations do you need?
#
# ANSWER: Consider the following example for n = 2:
# After swapping indices 0 and 2: [3, 2, 1, 4, 5, 6]
# But now the element at index 0, 3, should finally be at index 4. We swap again.
# After swapping indices 0 and 4: [5, 2, 1, 4, 3, 6]
# Now the element at index 0, 5, is where it should be. We move on to the next index, 1.
# After swapping indices 1 and 3: [5, 4, 1, 2, 3, 6]
# But now the element at index 1, 4, should finally be at index 5. We swap again.
# After swapping indices 1 and 5: [5, 6, 1, 2, 3, 4]
# Now the element at index 1, 6, is where it should be.
#
# Thus, we observe that we need to swap the elements at indices 0 through n - 1, each n times. Overall, we do n^2 swaps.


def rotate(seq: MutableSequence[T], n: int) -> None:
    def _target(k: int) -> int:
        return (k + n) % len(seq)

    for current in range(abs(n)):
        target: int = _target(current)

        while current != target:
            swap(seq, current, target)
            target = _target(target)


# 130. Given an array of numbers representing the stock prices of a company in chronological order and an integer k,
# return the maximum profit you can make from k buys and sells. You must buy the stock before you can sell it,
# and you must sell the stock before you can buy it again.
#
# For example, given k = 2 and the array [5, 2, 4, 0, 1], you should return 3.

# ANSWER: Assuming stocks can't be sold and purchased on the same day, on any day, there are two options:
# 1. Make no transactions; the max profit on that day is the same as the previous day
# 2. Sell; the max profit on that day is the difference of prices between that day and a previous day when the
# stock was purchased, plus the max profit made until the buying day with one less transaction
#
# If there are n prices, the time complexity is O(n^2 * k). We can improve the time complexity by eliminating the
# inner loop for determining the profit on sale if we store the profit for buying up to day - 2. Then the profit
# for buying up to day - 1 can be calculated in constant time.
#
# Space complexity is O(nk). This can be improved too by observing that we only need the last two rows and one
# column to calculate to profit for today (provided profit for buying up to day - 2 is stored).
def stock_1(prices: Sequence[int], k: int) -> int:
    # profit[i][j] is the maximum profit that could be made on day i by making up to j transactions
    # GOTCHA: [[v] * col] * row references the same list in all rows!
    profits: List[List[int]] = [[0] * (k + 1) for _ in range(len(prices))]

    for day in range(1, len(prices)):
        for num_txn in range(1, k + 1):
            profit_if_sell: int = max(
                map(
                    lambda buying_day: prices[day] - prices[buying_day] + profits[buying_day][num_txn - 1],
                    range(day)
                )
            )
            profit_if_do_nothing: int = profits[day - 1][num_txn]
            profits[day][num_txn] = max(profit_if_do_nothing, profit_if_sell)

    return profits[-1][-1]


# 136. Given an N by M matrix consisting only of 1's and 0's, find the largest rectangle containing only 1's and
# return its area.
#
# For example, given the following matrix:
#
# [[1, 0, 0, 0],
#  [1, 0, 1, 1],
#  [1, 0, 1, 1],
#  [0, 1, 0, 0]]
#
# Return 4.
#
# ANSWER: For each row, we build a histogram with the bars corresponding to all 1's in a column. Then we employ
# the subroutine to find the largest rectangular area in a histogram.
# For example, the histogram for row 2 (index 1) will have a single bar of length 2 at column 0.
# out of all the areas for all the rows, we return the maximum one.
def largest_rect(matrix: Sequence[Sequence[int]]) -> int:
    histogram: MutableSequence[int] = [*matrix[0]]
    largest_area: int = max(*histogram)

    for row in range(1, len(matrix)):
        for col in range(len(matrix[0])):
            histogram[col] = (histogram[col] + 1) if matrix[row][col] == 1 else 0

        largest_area = max(largest_area, stack.largest_area_in_hist(histogram))

    return largest_area


# 137. Implement a bit array.
#
# A bit array is a space efficient array that holds a value of 1 or 0 at each index.
#
# init(size): initialize the array with size
# set(i, val): updates index at i with val where val is either 1 or 0.
# get(i): gets the value at index i.
#
# ANSWER: Same as question 134, sparse array.

# 138. Find the minimum number of coins required to make n cents.
#
# You can use standard American denominations, that is, 1¢, 5¢, 10¢, and 25¢.
#
# For example, given n = 16, return 3 since we can make it with a 10¢, a 5¢, and a 1¢.
#
# ANSWER: Let dp[n] be the min number of coins required to make n cents. We can't make any amount with coins that
# are larger, so we only consider cases where amount > coin. Therefore, dp[i] = dp[n - coin] + 1, where 1 is for
# using a coin. We find the min of this expression for all coins.
#
# Time complexity: O(coins * amt)
def min_coins(coins: Sequence[int], amt: int) -> int:
    # https://docs.python.org/3/library/sys.html#sys.maxsize
    dp: MutableSequence[int] = [sys.maxsize] * (amt + 1)
    dp[0] = 0

    for i in range(1, amt + 1):
        for j in range(len(coins)):
            if i >= coins[j]:
                dp[i] = min(dp[i], dp[i - coins[j]] + 1)

    return dp[-1]
