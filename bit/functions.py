import functools


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

def unique_numbers(*arr: int) -> (int, int):
    xor: int = functools.reduce(lambda x, y: x ^ y, arr)
    xor_str: str = bin(xor)
    first_set_bit: int = next(i for i in range(len(xor_str)) if xor_str[len(xor_str) - i - 1] == "1")
    mask: int = 1 << first_set_bit

    return functools.reduce(lambda x, y: ((x[0] ^ y, x[1]) if (y & mask == mask) else (x[0], x[1] ^ y)), arr, (0, 0))
