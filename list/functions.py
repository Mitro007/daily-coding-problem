import math
from typing import TypeVar

from .linked_list import LinkedList

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

T = TypeVar("T")


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
# 131. Given the head to a singly linked list, where each node also has a “random” pointer that points to anywhere in
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
