import random
from typing import Sequence


# LeetCode 69.
# 129. Given a real number n, find the square root of n. For example, given n = 9, return 3.


def square_root(n: int, tolerance: float) -> float:
    assert n >= 0, "n must be positive"
    prev_guess: float = 0.0
    new_guess: float = n / 2

    while abs(new_guess - prev_guess) > tolerance:
        prev_guess = new_guess
        new_guess = 0.5 * (prev_guess + n / prev_guess)

    return new_guess


# 152. You are given n numbers as well as n probabilities that sum up to 1. Write a function to generate one of the
# numbers with its corresponding probability.
#
# For example, given the numbers [1, 2, 3, 4] and probabilities [0.1, 0.5, 0.2, 0.2], your function should return
# 1 10% of the time, 2 50% of the time, and 3 and 4 20% of the time.
#
# You can generate random numbers between 0 and 1 uniformly.
#
# ANSWER: There is a library function random.choices for doing exactly what this question asks for, but if using that
# isn't allowed, we could simply replicate each number in accordance with it's probability, and then pick one from
# the resultant list.
def choose_with_probability(nums: Sequence[int], probabilities: Sequence[float]) -> int:
    return random.choice([j for i in range(len(nums)) for j in [i] * int(10 * probabilities[i])])
