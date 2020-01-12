import functools
from typing import Iterator


# LeetCode 260.
# 140. Given an array of integers in which two elements appear exactly once and all other elements appear exactly,
# twice, find the two elements that appear only once.
#
# For example, given the array [2, 4, 6, 8, 10, 2, 6, 10], return 4 and 8. The order does not matter.
#
# Follow-up: Can you do this in linear time and constant space?
#
# ANSWER: One solution that immediately comes to mind is using a frequency map (Counter in Python). That'll take
# linear time and space. Can we do better?
# Recall that XOR of a number with itself produces zero, and XOR of a number with zero produces itself. Thus, if we
# iteratively XOR every number in the array with its next, then the final result will be the XOR of the two unique
# numbers.
#
# For example: Given [1, 2, 1, 3, 2, 5]
# ((((1 XOR 2 = 3) ^ 1 = 2) ^ 3 = 1) ^ 2 = 3) ^ 5 = 6
#
# Now, we somehow need to "unXOR" 6 into its constituents, 3 and 5. To do that, we observe that 3=0b11 and 5=0b101.
# The binary representations first differ at the rightmost 2nd bit, or index 1. Thus, if we partition the array such
# that all numbers that have the index 1 set (=1) are in one group, and the others in another, then the two numbers
# we are looking for will be separated. Now, if we XOR each group, then duplicate numbers will zero each other, and we
# will be left with only the unique numbers.
#
# We iterate over the original array twice, thus time complexity is O(n). We don't use any additional space, so space
# complexity is constant.

def unique_numbers(*nums: int) -> (int, int):
    xor: int = functools.reduce(lambda x, y: x ^ y, nums)
    xor_str: str = bin(xor)
    first_set_bit: int = next(i for i in range(len(xor_str)) if xor_str[len(xor_str) - i - 1] == "1")
    mask: int = 1 << first_set_bit

    return functools.reduce(lambda x, y: ((x[0] ^ y, x[1]) if (y & mask == mask) else (x[0], x[1] ^ y)), nums, (0, 0))


# 148. Gray code is a binary code where each successive value differ in only one bit, as well as when wrapping around.
# Gray code is common in hardware so that we don't see temporary spurious values during transitions.
#
# Given a number of bits n, generate a possible gray code for it.
#
# For example, for n = 2, one gray code would be [00, 01, 11, 10].
#
# For number of bits n, there are 2^n Gray codes, including zero. Thus, the maximum Gray code is 2^n - 1. Since,
# by definition, Gray codes differ only by 1 bit from their neighbors, the i-th Gray code is given by the XOR of the
# i-th and the (i - 1)th bits of the binary representation of i, where 0 <= i < 2^n.
#
# For the example above, n = 2, the corresponding Gray codes are 0 ^ 0 = 0, 1 ^ 0 = 1, 2 ^ 1 = 3 and, 3 ^ 1 = 2
# (i >> 2 is simply moving the bits to the right by a bit, which is equivalent to integer division by 2).
def gray_codes(n: int) -> Iterator[int]:
    for i in range(1 << n):
        yield i ^ (i >> 1)


# LeetCode 190.
# 161. Given a 32-bit integer, return the number with its bits reversed.
#
# For example, given the binary number 1111 0000 1111 0000 1111 0000 1111 0000,
# return 0000 1111 0000 1111 0000 1111 0000 1111.
#
# ANSWER: Since Python 3 can handle arbitrary-length integers, we first mask the input to 32 bits. We then convert to
# binary, reverse until the 0b prefix, and append zeros if necessary since bin(n) function doesn't return preceding
# zeros. We return after converting the binary string to int.
def reverse_bits(n: int) -> int:
    return int("{:0<32}".format(bin(n & ((1 << 32) - 1))[:1:-1]), 2)
