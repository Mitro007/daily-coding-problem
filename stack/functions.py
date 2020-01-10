from typing import Sequence, MutableSequence, Tuple, Iterable, List


# LeetCode 56.
# 77. Given a list of possibly overlapping intervals, return a new list of intervals where all overlapping intervals
# have been merged.
# The input list is not necessarily ordered in any way.
# For example, given [(1, 3), (5, 8), (4, 10), (20, 25)], you should return [(1, 3), (4, 10), (20, 25)].
#
# ANSWER: Sort intervals by end time and merge when current interval starts after the previous one and ends before the
# previous one, or current interval starts before the previous one.
#
# Time and space complexities: O(n), since we may put every interval at least once on the stack.
def merge_overlapping_intervals(intervals: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    sorted_intervals: List[Tuple[int, int]] = sorted(intervals, key=lambda x: x[1])
    stack: List[Tuple[int, int]] = []

    def should_merge() -> bool:
        return len(stack) >= 2 and ((stack[-2][0] <= stack[-1][0] <= stack[-2][1]) or (stack[-1][0] <= stack[-2][0]))

    def merge() -> None:
        a: Tuple[int, int] = stack.pop()
        b: Tuple[int, int] = stack.pop()
        stack.append((min(a[0], b[0]), a[1]))

    for x in sorted_intervals:
        while should_merge():
            merge()

        stack.append(x)

    while should_merge():
        merge()

    return stack


# 128. The Tower of Hanoi is a puzzle game with three rods and n disks, each a different size.
#
# All the disks start off on the first rod in a stack. They are ordered by size, with the largest disk on the bottom
# and the smallest one at the top.
#
# The goal of this puzzle is to move all the disks from the first rod to the last rod while following these rules:
#
# You can only move one disk at a time.
# A move consists of taking the uppermost disk from one of the stacks and placing it on top of another stack.
# You cannot place a larger disk on top of a smaller disk.
# Write a function that prints out all the steps necessary to complete the Tower of Hanoi. You should assume that
# the rods are numbered, with the first rod being 1, the second (auxiliary) rod being 2, and the last (goal) rod
# being 3.
#
# For example, with n = 3, we can do this in 7 moves:
#
# Move 1 to 3
# Move 1 to 2
# Move 3 to 2
# Move 1 to 3
# Move 2 to 1
# Move 2 to 3
# Move 1 to 3

# Find the largest rectangular area possible in a given histogram where the largest rectangle can be made of a number
# of contiguous bars. For simplicity, assume that all bars have same width and the width is 1 unit.
# For example, consider the following histogram with 7 bars of heights {6, 2, 5, 4, 5, 1, 6}. The largest possible
# rectangle possible is 12 (consisting of the bars 5, 4, 5).
def largest_area_in_hist(hist: Sequence[int]) -> int:
    if not hist:
        return 0

    # Each item j on the stack represents the end of the area at j. Where does that area start? After stack[j - 1],
    # (index stack[j - 1] + 1) because the previous area ends at stack[j - 1], or if the stack is empty, at index 0.
    # The following invariant hold for the stack:
    # For i, j in [0, len(stack)), i > j, hist[stack[i]] >= hist[stack[j]]
    stack: MutableSequence[int] = []
    largest_area: int = -1

    def current_area(i: int) -> int:
        area: int = -1
        while stack and hist[stack[-1]] > (hist[i] if i < len(hist) else -1):
            j: int = stack.pop()
            width: int = i - ((stack[-1] + 1) if stack else 0)
            area = max(area, width * hist[j])
        return area

    for i, v in enumerate(hist):
        if stack and hist[stack[-1]] > v:
            largest_area = max(largest_area, current_area(i))
        stack.append(i)

    return max(largest_area, current_area(len(hist)))


# LeetCode 678.
# You're given a string consisting solely of (, ), and *. * can represent either a (, ), or an empty string.
# Determine whether the parentheses are balanced.
#
# For example, (()* and (*) are balanced. )*( is not balanced.
#
# ANSWER: Time and space complexities: O(n), since each character is pushed and popped at most once.
def is_valid_parenthesis_str(s: str) -> bool:
    left_parens: MutableSequence[int] = []
    asterisks: MutableSequence[int] = []

    for i, ch in enumerate(s):
        if ch == "(":
            left_parens.append(i)
        elif ch == ")":
            if left_parens:
                left_parens.pop()
            # treat * as left paren
            elif asterisks:
                asterisks.pop()
            else:  # found unmatched right paren
                return False
        else:
            asterisks.append(i)

    while left_parens and asterisks:
        # treat * as right paren
        if left_parens[-1] < asterisks[-1]:
            left_parens.pop()
            asterisks.pop()
        else:  # found unmatched left paren
            break

    return not left_parens

# 154. Implement a stack API using only a heap. A stack implements the following methods:
#
# push(item), which adds an element to the stack
# pop(), which removes and returns the most recently added element (or throws an error if there is nothing on the stack)
# Recall that a heap has the following operations:
#
# push(item), which adds a new key to the heap
# pop(), which removes and returns the max value of the heap
#
# ANSWER: Maintain a monotonically increasing counter, and push (counter, value) to the heap. Increment counter.
