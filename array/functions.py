import itertools
import sys
from typing import Sequence, MutableSequence, TypeVar, List, Tuple, Dict, Iterable, Set, MutableMapping

import stack.functions as stack

T = TypeVar("T")


def swap(seq: MutableSequence[T], i: int, j: int) -> None:
    if seq:
        assert 0 <= i < len(seq) and 0 <= j < len(seq)
        tmp = seq[i]
        seq[i] = seq[j]
        seq[j] = tmp


# LeetCode 1
# 1. Given a list of numbers, return whether any two sums to k. For example, given [10, 15, 3, 7] and k of 17, return
# true since 10 + 7 is 17.
#
# Bonus: Can you do this in one pass?
def two_sum(nums: Sequence[int], k: int) -> Tuple[int, int]:
    num_map: Dict[int, int] = {kv[1]: kv[0] for kv in enumerate(nums)}

    return next(
        ((kv[0], num_map[k - kv[1]]) for kv in enumerate(nums) if k - kv[1] in num_map and kv[0] != num_map[k - kv[1]]),
        None
    )


# LeetCode 41.
# 4. Given an array of integers, find the first missing positive integer in linear time and constant space.
# In other words, find the lowest positive integer that does not exist in the array. The array can contain duplicates
# and negative numbers as well.
#
# For example, the input [3, 4, -1, 1] should give 2. The input [1, 2, 0] should give 3.
#
# You can modify the input array in-place.
#
# ANSWER:
# 1. We divide the array into 2 parts such that the first part consists of only non-negative numbers. Say we have
# the starting index as 0 and the ending index as lo (inclusive).
# 2. We traverse the array from index 0 to lo. We take the absolute value of the element at that index - say the
# value is x.
#  a. If x > lo + 1 or x == 0, we do nothing.
#  b. Otherwise, we make the sign of the element at index x - 1 negative. We subtract 1 because we want to map
#     positive numbers to array indices, and indices start from 0.
# 3. Finally, we traverse the array once more from index 0 to lo. In case we encounter a positive element at some
# index, we output index + 1. This is the answer. However, if we do not encounter any positive element, it means that
# integers 1 to lo occur in the array. We output lo + 1.
def missing_int(nums: MutableSequence[int]) -> int:
    # If empty array or doesn't have 1, return 1
    if not next((x for x in nums if x == 1), 0):
        return 1

    lo: int = 0
    hi: int = len(nums) - 1
    i: int = 0
    pivot: int = 1

    while i <= hi:
        if nums[i] < pivot:
            swap(nums, i, hi)
            hi -= 1
        elif nums[i] > pivot:
            swap(nums, i, lo)
            i += 1
            lo += 1
        else:
            i += 1

    x = 0
    while x <= hi:  # hi is the index of the last positive number
        y: int = abs(nums[x])
        if 0 < y <= lo + 1 and nums[y - 1] > 0:  # Don't flip sign if already negative
            nums[y - 1] *= -1
        x += 1

    return next((i for i, v in enumerate(nums[:hi + 1]) if v >= 0), x) + 1


# 44. We can determine how "out of order" an array A is by counting the number of inversions it has. Two elements
# A[i] and A[j] form an inversion if A[i] > A[j] but i < j. That is, a smaller element appears after a larger element.
#
# Given an array, count the number of inversions it has. Do this faster than O(N^2) time.
#
# You may assume each element in the array is distinct.
#
# For example, a sorted list has zero inversions. The array [2, 4, 1, 3, 5] has three inversions:
# (2, 1), (4, 1), and (4, 3). The array [5, 4, 3, 2, 1] has ten inversions: every distinct pair forms an inversion.
#
# ANSWER: We merge sort the array and count inversions during the merge process. If for i in [0, len(left)) and
# j in [0, len(right)), left(i) > right(j), then all elements after index i are also greater than right(j) and
# count in the inversions.
#
# Time complexity: O(n log n). Space complexity: O(n), since two arrays of same length as the input are created.
def count_inversions(nums: Sequence[int]) -> int:
    nums_copy: List[int] = [i for i in nums]
    tmp: List[int] = [0] * len(nums)

    def merge(lo: int, mid: int, hi: int) -> int:
        i: int = lo
        j: int = mid
        k: int = 0
        counter: int = 0

        while i < mid and j < hi:
            if nums_copy[i] > nums_copy[j]:
                counter += (mid - i)
                tmp[k] = nums_copy[j]
                j += 1
            else:
                tmp[k] = nums_copy[i]
                i += 1
            k += 1

        while i < mid:
            tmp[k] = nums_copy[i]
            i += 1
            k += 1

        while j < hi:
            tmp[k] = nums_copy[j]
            j += 1
            k += 1

        for x in range(k):
            nums_copy[lo + x] = tmp[x]

        return counter

    def merge_sort(lo: int, hi: int) -> int:
        if hi - lo <= 1:
            return 0
        mid: int = lo + (hi - lo) // 2

        x: int = merge_sort(lo, mid)
        y: int = merge_sort(mid, hi)

        return merge(lo, mid, hi) + x + y

    return merge_sort(0, len(nums))


# LeetCode 53.
# 49. Given an array of numbers, find the maximum sum of any contiguous subarray of the array.
#
# For example, given the array [34, -50, 42, 14, -5, 86], the maximum sum would be 137, since we would take elements
# 42, 14, -5, and 86.
#
# Given the array [-5, -1, -8, -9], the maximum sum would be 0, since we would not take any elements.
#
# Do this in O(N) time.
#
# ANSWER: We use Kadane's algorithm that takes advantage of the optimal substructure of the problem.
#
# Given array A, let M[i] be the maximum sum of the subarray ending at index i. M[i+1] could be obtained by extending
# the M[i] with A[i+1]. Another possibility is that M[i] is a very small value (perhaps many of the elements are
# negative integers), and we are better off just taking A[i+1] by itself.
# Thus, the recurrence relation is:
#
# M[i] = max{ M[i - 1] + A[i], A[i] }, ∀ i = 1 to n - 1
#      = 0 if i = 0.
#
# Basically, we are trying to figure out if to start a new streak, or continue the current one.
# If the array contains only negative numbers, the maximum sum would be zero, since we would not take any elements.
#
# However, since each value of M[i] is only computed once, because this algorithm doesn't exhibit overlapping
# subproblems (recomputing the same values over and over). Thus, it may not strictly be called dynamic programming.
#
def max_subarray_sum(nums: Sequence[int]) -> int:
    running_sum = -sys.maxsize + 1
    max_sum = 0

    for i in nums:
        # If running_sum is negative, we are better off taking just the current number
        running_sum = max(0, running_sum) + i
        max_sum = max(max_sum, running_sum)

    return max_sum


# LeetCode 33.
# 58. An sorted array of integers was rotated an unknown number of times.
#
# Given such an array, find the index of the element in the array in faster than linear time. If the element doesn't
# exist in the array, return null.
#
# For example, given the array [13, 18, 25, 2, 8, 10] and the element 8, return 4 (the index of 8 in the array).
#
# You can assume all the integers in the array are unique.
#
# ANSWER: In the rotated array, the largest element is potentially not at the end. Observe that all the elements after
# the max element are sorted. Thus, if we take the middle element, and compare it to the end elements, we can tell
# which side the max element is on relative to the middle element. All the elements on the other side of middle that
# max is NOT on are sorted. We check if the target element falls on the sorted side, and if yes, we binary search
# there. Else we search on the non-sorted side (the side containing max).
#
# Time complexity: O(log n)
def search_in_rotated_sorted_array(nums: Sequence[int], target: int) -> int:
    lo: int = 0
    hi: int = len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid

        if nums[lo] <= nums[mid] >= nums[hi]:  # max is in [mid, hi]
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # max is in [lo, mid)
            if nums[hi] >= target > nums[mid]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1


# LeetCode 128.
# 99. Given an unsorted array of integers, find the length of the longest consecutive elements sequence.
#
# For example, given [100, 4, 200, 1, 3, 2], the longest consecutive element sequence is [1, 2, 3, 4].
# Return its length: 4.
#
# Your algorithm should run in O(n) complexity.
# Time Complexity: O(n), although because number is removed after it's seen once.
def longest_consecutive_seq(nums: Sequence[int]) -> int:
    best: int = 0
    x: Set[int] = set(nums)

    for i in nums:
        if i not in x:
            continue
        counter: int = 1
        j: int = 1
        while i + j in x:
            counter += 1
            x.remove(i + j)
            j += 1
        j = 1
        while i - j in x:
            counter += 1
            x.remove(i - j)
            j += 1
        x.remove(i)

        best = max(best, counter)
        if not x:
            break

    return best


# 102. Given a list of integers and a number K, return which contiguous elements of the list sum to K.
#
# For example, if the list is [1, 2, 3, 4, 5] and K is 9, then it should return [2, 3, 4].
#
# ANSWER: We simply grow the current window until its sum exceeds k. Then we reduce from the left until the sum drops
# below k.
# Time complexity: O(n), since each element may be seen twice, first in the outer loop, and later in the inner loop.
# The worst case is when the last element equals k and the rest sum to less than k.
def subarray_sum(nums: Sequence[int], k: int) -> Iterable[int]:
    start: int = 0
    i: int = 0
    total: int = 0

    while total != k and i < len(nums):
        current: int = nums[i]
        total += current
        i += 1

        while total > k:
            total -= nums[start]
            start += 1

    return nums[start:i]


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

# LeetCode 969.
# 147. Given a list, sort it using this method: reverse(lst, i, j), which reverses lst from i to j.
#
# ANSWER: This is known as Pancake sorting. At each iteration, we find the index of the maximum element among the
# unsorted elements. Let's say this index is i. We then reverse [0, i], and then reverse [i, j], where j is the
# index where nums[i] would be after the array is completely sorted. Clearly, j starts from the last index of the
# array, and gets decremented by 1 at each iteration.
#
# Time complexity: Finding the max index is an O(n) operation. Since reverse does n/2 swaps, and we do 2 reversals,
# there are O(n) swaps. Thus, we do O(n) work at each operation, and O(n^2) work for the whole algorithm.
def pancake_sort(nums: MutableSequence[int]) -> None:
    def reverse(i: int, j: int) -> None:
        x: int = (j - i + 1) // 2
        lo: int = i
        hi: int = j

        for y in range(x):
            a: int = nums[lo + y]
            b: int = nums[hi - y]
            tmp: int = a
            nums[lo + y] = b
            nums[hi - y] = tmp
            lo += 1
            hi -= 1

    def index_of_max(x: int) -> int:
        """Return the index of the maximum element until the index x."""
        return max(map(lambda y: (y, nums[y]), range(x + 1)), key=lambda z: z[1])[0]

    for i in range(len(nums)):
        # After the current iteration, nums[j] is going to contain the element that would be at index j if nums
        # were sorted
        j = len(nums) - 1 - i
        hi = index_of_max(j)
        if hi != j:
            reverse(0, hi)
            reverse(0, j)


# LeetCode 733.
# 151. Given a 2-D matrix representing an image, a location of a pixel in the screen and a color C, replace the color
# of the given pixel and all adjacent same colored pixels with C.
#
# For example, given the following matrix, and location pixel of (2, 2), and 'G' for green:
#
# B B W
# W W W
# W W W
# B B B
# Becomes
#
# B B G
# G G G
# G G G
# B B B

# LeetCode 287.
# 164. You are given an array of length n + 1 whose elements belong to the set {1, 2, ..., n}. By the pigeonhole
# principle, there must be a duplicate. Find it in linear time and space.
def find_dup(nums: Sequence[int]) -> int:
    nums_cp: Set[int] = set(nums)

    for i in nums:
        if i not in nums_cp:
            return i
        nums_cp.remove(i)

    return None


# LeetCode 315.
# 165. Given an array of integers, return a new array where each element in the new array is the number of smaller
# elements to the right of that element in the original input array.
#
# For example, given the array [3, 4, 9, 6, 1], return [1, 1, 2, 1, 0], since:
#
# There is 1 smaller element to the right of 3
# There is 1 smaller element to the right of 4
# There are 2 smaller elements to the right of 9
# There is 1 smaller element to the right of 6
# There are no smaller elements to the right of 1
#
# ANSWER: We can solve this problem trivially in O(n^2) time by counting the smaller numbers to the right of each
# number. Can we do better?
# Observe that if we traverse two sorted subsequences from the end, if the current number in the left array is greater
# than the current one in the right array, the number in the left array has len(right) smaller elements to its right in
# the original array. If the right array is empty, all the numbers in it were no smaller than the current number in the
# left array.
# This is essentially the merge step in merge sort, except instead of building the merged array by appending
# non-decreasing numbers, we build it by prepending non-increasing numbers to the left.
#
# Time complexity: O(n log(n)). We create a bunch of intermediate arrays, but this can be eliminated by passing around
# an array of equal length as the original unsorted array.
def count_smaller(nums: Sequence[int]) -> Sequence[int]:
    count: MutableSequence[int] = [0] * len(nums)

    def sort(xs: List[Tuple[int, int]]) -> None:
        mid: int = len(xs) // 2
        if mid < 1:
            return

        left: List[Tuple[int, int]] = xs[:mid]
        sort(left)
        right: List[Tuple[int, int]] = xs[mid:]
        sort(right)

        for i in reversed(range(len(xs))):
            if left and ((right and left[-1][1] > right[-1][1]) or not right):
                count[left[-1][0]] += len(right)
                xs[i] = left.pop()
            else:
                xs[i] = right.pop()

    sort(list(enumerate(nums)))
    return count


# 166. Implement a 2D iterator class. It will be initialized with an array of arrays, and should implement the following
# methods:
#
# next(): returns the next element in the array of arrays. If there are no more elements, raise an exception.
# has_next(): returns whether or not the iterator still has elements left.
# For example, given the input [[1, 2], [3], [], [4, 5, 6]], calling next() repeatedly should output 1, 2, 3, 4, 5, 6.
#
# Do not use flatten or otherwise clone the arrays. Some of the arrays can be empty.

# LeetCode 48.
# 168. Given an N by N matrix, rotate it by 90 degrees clockwise.
#
# For example, given the following matrix:
#
# [[1, 2, 3],
#  [4, 5, 6],
#  [7, 8, 9]]
# you should return:
#
# [[7, 4, 1],
#  [8, 5, 2],
#  [9, 6, 3]]
# Follow-up: What if you couldn't use any extra space?
#
# ANSWER: Imagine the matrix like an onion with multiple layers. Observe that the number of layers is simply n // 2.
# The rotation happens layer by layer. At each iteration, we swap 4 elements from the current layer.
def rotate_matrix(matrix: MutableSequence[MutableSequence[int]]) -> None:
    n: int = len(matrix)
    layers: int = n // 2

    for layer in range(layers):
        for shift in range(layer, n - layer - 1):
            top_left: int = matrix[layer][shift]
            top_right: int = matrix[shift][n - layer - 1]
            bottom_left: int = matrix[n - shift - 1][layer]
            bottom_right: int = matrix[n - layer - 1][n - shift - 1]

            matrix[layer][shift] = bottom_left
            matrix[shift][n - layer - 1] = top_left
            matrix[n - layer - 1][n - shift - 1] = top_right
            matrix[n - shift - 1][layer] = bottom_right


# Consider a big party where a log register for each guest's entry and exit times is maintained. Find the time at which
# there are maximum guests in the party. Note that entries in register are not in any order.

# For example:
# [(1, 4), (2, 5), (9, 12), (5, 9), (5, 12)]
# First guest arrives at 1 and leaves at 4,
# second guest arrives at 2 and leaves at 5, and so on.
# There are maximum 3 guests at time 5.
#
# ANSWER: The problem boils down to the maximum overlap of the following line segments, where the beginning of a line
# segment indicates the entry time of a guest, and the end indicates their exit. We can see that three lines overlap
# at 5, and as well as 9. We will return the first answer.
# To do this, we convert the register into a list of entry and exit events, and mark an entry by 1, and an exit by -1.
# Then we sort the events based on the times, and if the times are equal, we put an entry before an exit. For the
# example above, we get [(1, 1), (2, 1), (4, -1), (5, 1), (5, 1), (5, -1), (9, 1), (9, -1), (12, -1), (12, -1). Then
# we simply traverse this list adding up the 1's and -1's, keeping track of the maximum value at all times.
#         ------------------
#         ---------
#                 ----------
#   -------
# -------
# 1 2 3 4 5 6 7 8 9 10 11 12
#
# Time complexity:
# Conversion of the register to list of entry and exit events: O(n).
# Sorting of the events: O(n log(n)).
# Overall, O(n log(n)).
#
# A variation of the problem is as follows:
# 171. You are given a list of data entries that represent entries and exits of groups of people into a building.
# An entry looks like this:
#
# {"timestamp": 1526579928, count: 3, "type": "enter"}
#
# This means 3 people entered the building. An exit looks like this:
#
# {"timestamp": 1526580382, count: 2, "type": "exit"}
#
# This means that 2 people exited the building. timestamp is in Unix time.
#
# Find the busiest period in the building, that is, the time with the most people in the building. Return it as a pair
# of (start, end) timestamps. You can assume the building always starts off and ends up empty, i.e. with 0 people
# inside.
def max_guests(register: Sequence[Tuple[int, int]]) -> Tuple[int, int]:
    time = num_guests = max_num_guests = 0

    events = map(lambda x: [(x[0], 1), (x[1], -1)], register)
    for t, c in sorted(itertools.chain.from_iterable(events), key=lambda x: (x[0], -x[1])):
        num_guests += c
        if num_guests > max_num_guests:
            time = t
            max_num_guests = num_guests

    return time, max_num_guests


# LeetCode 223/836.
# 185. Given two rectangles on a 2D graph, return the area of their intersection. If the rectangles don't intersect,
# return 0.
#
# For example, given the following rectangles:
#
# {
#     "top_left": (1, 4),
#     "dimensions": (3, 3) # width, height
# }
# and
#
# {
#     "top_left": (0, 5),
#     "dimensions": (4, 3) # width, height
# }
# return 6.
#
# ANSWER: Refer to the diagram "test/rectangles.jpg" for some examples.
# Every rectangle has two unique x coordinates, and two unique y coordinates. In order for the rectangles to
# intersect, at least one x coordinate of a rectangle must be within the x coordinates of the other one (both x
# coordinates of the first may be within the x coordinates of the other one if the first one is completely contained
# in the second one). Thus, if all the x coordinates are sorted, the middle two give us the x-range of the intersection.
# Same argument applies to y coordinates.
# Note that if the rectangles don't intersect but have sides that touch, the intersecting range is zero.
def area_of_overlap(r1: Tuple[Tuple[int, int], Tuple[int, int]], r2: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    # r1 bottom left
    r1x1, r1y1 = r1[0]
    # r1 top right
    r1x2, r1y2 = r1x1 + r1[1][0], r1y1 + r1[1][1]
    # r2 bottom left
    r2x1, r2y1 = r2[0]
    # r2 top right
    r2x2, r2y2 = r2x1 + r2[1][0], r2y1 + r2[1][1]

    x: Sequence[Tuple[int, str]] = sorted([(r1x1, "r1"), (r1x2, "r1"), (r2x1, "r2"), (r2x2, "r2")])
    y: Sequence[Tuple[int, str]] = sorted([(r1y1, "r1"), (r1y2, "r1"), (r2y1, "r2"), (r2y2, "r2")])
    if x[0][1] == x[1][1] or x[2][1] == x[3][1] or y[0][1] == y[1][1] or y[2][1] == y[3][1]:
        return 0
    return (x[2][0] - x[1][0]) * (y[2][0] - y[1][0])


# LeetCode 3.
# 189. Given an array of elements, return the length of the longest subarray where all its elements are distinct.
#
# For example, given the array [5, 1, 3, 5, 2, 3, 4, 1], return 5 as the longest subarray of distinct elements is
# [5, 2, 3, 4, 1].
#
# ANSWER: We solve this by using a sliding window that contains only distinct numbers. At each iteration, we extend
# the window on the right; if the current element is one that is already present in the window, we move the left
# boundary past the duplicate element. The longest distinct subarray is the longest of all the subarrays we see.
#
# Time complexity: O(n), since all the operations at each iteration are constant time.
def longest_distinct_subarray(nums: Sequence[int]) -> int:
    start: int = 0
    max_window_length: int = -1
    uniq: MutableMapping[int, int] = dict()

    for end in range(len(nums)):
        current = nums[end]
        if current in uniq and start <= uniq[current]:
            start = uniq[current] + 1
        uniq[current] = end
        running_window_length = end - start + 1
        max_window_length = max(max_window_length, running_window_length)

    return max_window_length


# LeetCode 918.
# 190. Given a circular array, compute its maximum subarray sum in O(n) time. A subarray can be empty, and in this
# case the sum is 0.
#
# For example, given [8, -1, 3, 4], return 15 as we choose the numbers 3, 4, and 8 where the 8 is obtained from
# wrapping around.
#
# Given [-4, 5, 1, 0], return 6 as we choose the numbers 5 and 1.
#
# ANSWER: For an array A of length N, there are two cases of the maximum subarray:
#   1. The maximum subarray lies between 0 <= i < N
#   2. The maximum subarray wraps around, so part of it k < i < N, and the rest 0 <= j <= k, for some k.
#
#   In the second case, if the total sum of A is S, and the maximum subarray sum is S1, then the sum of the subarray
#   between k and i is given by S2 = S - S1. Or, S1 = S - S2. Since S is fixed, S1 is maximized if S2 is minimized.
#
#   Thus, we find the maximum subarray sum for case 1, and the minimum subarray sum for case 2, using Kadane's
#   algorithm. The result is given by the maximum of the case 1 sum and S - S2.
#
# Time complexity O(N).
def max_sum_circular_arr(nums: Sequence[int]) -> int:
    greatest: int = -sys.maxsize + 1
    smallest: int = sys.maxsize
    # Running sums
    x = y = total = 0

    for i in nums:
        x += i
        greatest = max(greatest, x)
        # If running_sum is negative, we are better off taking just the next number
        x = max(x, 0)

        y += i
        smallest = min(smallest, y)
        # If running_sum is positive, we are better off taking just the next number
        y = min(y, 0)

        total += i

    # If all numbers are negative, return the greatest one
    return greatest if greatest < 0 else max(greatest, total - smallest)
