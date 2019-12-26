from typing import Sequence, MutableSequence, TypeVar, List

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
def stock_1(prices: Sequence[int], k: int) -> int:
    # profit[i][j] is the maximum profit that could be made on day i by making up to j transactions
    # GOTCHA: [[v] * col] * row references the same list in all rows!
    profits: List[List[int]] = [[0] * (k + 1) for _ in range(len(prices))]

    def profit(selling_day: int, buying_day: int, num_txn: int) -> int:
        return prices[selling_day] - prices[buying_day] + profits[buying_day][num_txn - 1]

    for day in range(1, len(prices)):
        for num_txn in range(1, k + 1):
            best_buying_day: int = max(range(day), key=lambda d: profit(day, d, num_txn))
            profit_if_do_nothing: int = profits[day - 1][num_txn]
            profit_if_sell: int = profit(day, best_buying_day, num_txn)
            profits[day][num_txn] = max(profit_if_do_nothing, profit_if_sell)

    return profits[-1][-1]
