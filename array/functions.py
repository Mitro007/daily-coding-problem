import sys
from typing import Sequence, MutableSequence, TypeVar, List, Tuple

import stack.functions as stack

T = TypeVar("T")


def swap(seq: MutableSequence[T], i: int, j: int) -> None:
    if seq:
        assert 0 <= i < len(seq) and 0 <= j < len(seq)
        tmp = seq[i]
        seq[i] = seq[j]
        seq[j] = tmp


# LeetCode 189.
# 126. Write a function that rotates a list by k elements. For example, [1, 2, 3, 4, 5, 6] rotated by two becomes
# [3, 4, 5, 6, 1, 2]. Try solving this without creating a copy of the list.
# How many swap or move operations do you need?
#
# ANSWER: For a O(1) space solution, we need to rotate the list in place. Observe that when the list is reversed,
# and then the first k elements, and then the remaining n - k elements are reversed, we end up with a list rotated
# right by k positions.
#
# Example: [1, 2, 3, 4, 5], k = 3
# Reverse list: [5, 4, 3, 2, 1]
# Reverse k = 3 elements: [3, 4, 5, 2, 1]
# Reverse remaining n - k = 2 elements: [3, 4, 5, 1, 2]
#
# Every element is swapped at most 2 times, thus, total number of swaps required is 2n.
def rotate(nums: MutableSequence[T], k: int) -> None:
    # Convert negative rotation to a positive one, also scale k in case k >= n
    n: int = (k if k >= 0 else len(nums) + k) % len(nums)
    nums.reverse()
    for i in range(n // 2):
        j: int = n - i - 1
        swap(nums, i, j)

    for i in range((len(nums) - n) // 2):
        j: int = len(nums) - i - 1
        swap(nums, n + i, j)


# LeetCode 188.
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
    if not prices:
        return 0
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


# LeetCode 85.
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
    if not matrix:
        return 0
    histogram: MutableSequence[int] = [*matrix[0]]
    largest_area: int = stack.largest_area_in_hist(histogram)

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

# LeetCode 322.
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
def min_coins(coins: Sequence[int], amount: int) -> int:
    # https://docs.python.org/3/library/sys.html#sys.maxsize
    dp: MutableSequence[int] = [sys.maxsize] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for j in range(len(coins)):
            if i >= coins[j]:
                dp[i] = min(dp[i], dp[i - coins[j]] + 1)

    return dp[-1]


# 143. Given a pivot x, and a list lst, partition the list into three parts.
#
# The first part contains all elements in lst that are less than x
# The second part contains all elements in lst that are equal to x
# The third part contains all elements in lst that are larger than x
# Ordering within a part can be arbitrary.
#
# For example, given x = 10 and lst = [9, 12, 3, 5, 14, 10, 10], one partition may be [9, 3, 5, 10, 10, 12, 14].
def partition(coins: MutableSequence[T], pivot: T) -> Tuple[int, int]:
    n: int = len(coins)
    if n > 1:
        # 0 until lt are values less than pivot
        lt: int = 0
        # After gt until the end of the array are values greater than pivot
        gt: int = n - 1
        i: int = 0

        while i < gt:
            if coins[i] < pivot:
                swap(coins, lt, i)
                lt += 1  # Item at lt is now < pivot
                i += 1  # No longer unknown
            elif coins[i] > pivot:
                swap(coins, gt, i)
                gt -= 1  # Item at gt is now >pivot, we don't know about item at i
            else:
                i += 1  # Item at i == pivot, no longer unknown

        return lt, gt

# 144. Given an array of numbers and an index i, return the index of the nearest larger number of the number at index i,
# where distance is measured in array indices.
#
# For example, given [4, 1, 3, 5, 6] and index 0, you should return 3.
#
# If two distances to larger numbers are the equal, then return any one of them. If the array at i doesn't have a
# nearest larger integer, then return null.
#
# Follow-up: If you can preprocess the array, can you do this in constant time?
#
# ANSWER: Can solve in linear time by scanning both ways from i. If we preprocess the array to partition it around i,
# can solve in constant time (see question 143).
