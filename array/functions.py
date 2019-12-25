from typing import MutableSequence, TypeVar

T = TypeVar("T")


def swap(seq: MutableSequence[T], i: int, j: int) -> None:
    if seq:
        assert 0 <= i < len(seq) and 0 <= j < len(seq)
        tmp = seq[i]
        seq[i] = seq[j]
        seq[j] = tmp

# This problem was asked by Facebook.
#
# Write a function that rotates a list by k elements. For example, [1, 2, 3, 4, 5, 6] rotated by two becomes
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
