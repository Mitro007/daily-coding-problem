import math
from typing import TypeVar

from .linked_list import LinkedList

T = TypeVar("T")


# LeetCode 206.
# 73. Given the head of a singly linked list, reverse it in-place.
# Example:
#
# Input: 1 -> 2 -> 3 -> 4 -> 5 -> NULL
# Output: 5 -> 4 -> 3 -> 2 -> 1 -> NULL
def reverse(ll: LinkedList[T]) -> LinkedList[T]:
    node: LinkedList[T] = ll
    prev: LinkedList[T] = None

    while node:
        nxt: LinkedList[T] = node.next
        node.next = prev
        prev = node
        node = nxt

    return prev


# LeetCode 160.
# Given two singly linked lists that intersect at some point, find the intersecting node. The lists are non-cyclical.
# For example, given A = 3 -> 7 -> 8 -> 10 and B = 99 -> 1 -> 8 -> 10, return the node with value 8.
# In this example, assume nodes with the same value are the exact same node objects.
# Do this in O(M + N) time (where M and N are the lengths of the lists) and constant space.
def intersection(l1: LinkedList[T], l2: LinkedList[T]) -> LinkedList[T]:
    counter_1: int = 0
    counter_2: int = 0
    node_1: LinkedList[T] = l1
    node_2: LinkedList[T] = l2

    while node_1:
        counter_1 += 1
        node_1 = node_1.next

    while node_2:
        counter_2 += 1
        node_2 = node_2.next

    node_1 = l1
    node_2 = l2

    if counter_1 > counter_2:
        for i in range(counter_1 - counter_2):
            node_1 = node_1.next
    else:
        for i in range(counter_2 - counter_1):
            node_2 = node_2.next

    while node_1 is not node_2:
        node_1 = node_1.next
        node_2 = node_2.next

    return node_1


# LeetCode 2.
# 127. Let's represent an integer in a linked list format by having each node represent a digit in the number.
# The nodes make up the number in reversed order.
#
# For example, the following linked list:
# 1 -> 2 -> 3 -> 4 -> 5
#
# is the number 54321.
#
# Given two linked lists in this format, return their sum in the same linked list format.
#
# For example, given
# 9 -> 9
# 5 -> 2
#
# return 124 (99 + 25) as:
# 4 -> 2 -> 1
def sum(l1: LinkedList[int], l2: LinkedList[int]) -> LinkedList[int]:
    # short circuit
    if not l1:
        return l2
    if not l2:
        return l1

    result: LinkedList[int] = None
    head: LinkedList[int] = None
    carry: int = 0
    ptr1: LinkedList[int] = l1
    ptr2: LinkedList[int] = l2

    while ptr1 or ptr2:
        s: int = carry

        for p in filter(None, [ptr1, ptr2]):
            s += p.val
            if p is ptr1:
                ptr1 = ptr1.next
            if p is ptr2:
                ptr2 = ptr2.next

        x: LinkedList[int] = LinkedList(s % 10)

        if not result:
            result = x
            head = x
        else:
            result.next = x
            result = result.next

        carry = math.floor(s / 10)

    if carry > 0:
        result.next = LinkedList(carry)

    return head


# LeetCode 138.
# 131. Given the head to a singly linked list, where each node also has a ???random??? pointer that points to anywhere in
# the linked list, deep clone the list.

# LeetCode 24.
# 145. Given the head of a singly linked list, swap every two nodes and return its head.
#
# For example, given 1 -> 2 -> 3 -> 4, return 2 -> 1 -> 4 -> 3.
def swap_pairs(head: LinkedList[T]) -> LinkedList[T]:
    new_head: LinkedList[T] = None
    prev: LinkedList[T] = None
    node: LinkedList[T] = head

    while node:
        if node.next:
            tmp: LinkedList[T] = node.next
            if not new_head:
                new_head = tmp
            else:
                prev.next = tmp
            node.next = tmp.next
            tmp.next = node
            prev = node
        node = node.next

    return new_head if new_head else head


# LeetCode 148.
# 169. Given a linked list, sort it in O(n log n) time and constant space.
#
# For example, the linked list 4 -> 1 -> -3 -> 99 should become -3 -> 1 -> 4 -> 99.
#
# Time Complexity: We iterate the lists of size n, n/2, ..., at each step to find the middle element. We also merge
# two sorted lists of same size, which is O(n). Using the Master theorem, T(n) <= a.T(n/b) + O(n^d), a=b=2, d=1.
# This is the case a = b^d, which gives the answer T(n) <= O(n^d log n)=O(n log n).
def sort(linked_list: LinkedList[int]) -> LinkedList[int]:
    # Return n // 2 element
    def middle(head: LinkedList[int]) -> LinkedList[int]:
        if not head or not head.next:
            return head
        slow = head
        fast = head.next

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow

    def merge(head1: LinkedList[int], head2: LinkedList[int]) -> LinkedList[int]:
        p1 = head1
        p2 = head2
        prev = head = None

        while p1 and p2:
            smaller = p1 if p1.val < p2.val else p2
            if not head:
                head = smaller
            if prev:
                prev.next = smaller
            prev = smaller

            if smaller == p1:
                p1 = p1.next
            else:
                p2 = p2.next

        if prev:
            prev.next = p1 or p2
        else:
            head = p1 or p2

        return head

    def merge_sort(head: LinkedList[int]) -> LinkedList[int]:
        if head and head.next:
            mid = middle(head)
            next_to_mid = mid.next
            # Makes it easier to stop
            mid.next = None

            return merge(merge_sort(head), merge_sort(next_to_mid))
        else:
            return head

    return merge_sort(linked_list)


# LeetCode 61.
# 177. Given a linked list and a positive integer k, rotate the list to the right by k places.
# For example, given the linked list 7 -> 7 -> 3 -> 5 and k = 2, it should become 3 -> 5 -> 7 -> 7.
# Given the linked list 1 -> 2 -> 3 -> 4 -> 5 and k = 3, it should become 3 -> 4 -> 5 -> 1 -> 2.
#
# Time complexity: O(n).
def rotate_right(head: LinkedList[int], k: int) -> LinkedList[int]:
    length: int = 0
    node: LinkedList[int] = head

    while node:
        node = node.next
        length += 1

    if length <= 1:
        return head

    n = k % length

    if n == 0:
        return head

    node = head
    for _ in range(length - n - 1):
        node = node.next

    new_head = node.next
    node.next = None
    node = new_head
    while node and node.next:
        node = node.next
    if node:
        node.next = head

    return new_head
