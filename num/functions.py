import functools
import random
from typing import Sequence, Mapping


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


# 175. You are given a starting state start, a list of transition probabilities for a Markov chain, and a number of
# steps num_steps. Run the Markov chain starting from start for num_steps and compute the number of times we visited
# each state.
#
# For example, given the starting state a, number of steps 5000, and the following transition probabilities:
#
# [
#   ('a', 'a', 0.9),
#   ('a', 'b', 0.075),
#   ('a', 'c', 0.025),
#   ('b', 'a', 0.15),
#   ('b', 'b', 0.8),
#   ('b', 'c', 0.05),
#   ('c', 'a', 0.25),
#   ('c', 'b', 0.25),
#   ('c', 'c', 0.5)
# ]
# One instance of running this Markov chain might produce { 'a': 3012, 'b': 1656, 'c': 332 }.
#
# See https://www.datacamp.com/community/tutorials/markov-chains-python-tutorial
def markov(start: str, transitions: Mapping[str, Mapping[str, float]], steps: int) -> Mapping[str, int]:
    for state, tr in transitions.items():
        assert sum(tr.values()) == 1.0, "Transition probabilities from state: {state} don't add up to 1"

    freq = dict(map(lambda k: (k, 0), transitions.keys()))
    choice: Sequence[str] = [start]
    for i in range(steps):
        tr = transitions[choice[0]]
        # https://docs.python.org/dev/library/random.html#random.choices
        # Returns a list, for us, k = 1, so it's a singleton list
        choice = random.choices(population=list(tr.keys()), weights=list(tr.values()))
        freq[choice[0]] += 1

    return freq


# 184. Given n numbers, find the greatest common denominator between them.
# For example, given the numbers [42, 56, 14], return 14.
#
# ANSWER: We use Euclidean algorithm. https://en.wikipedia.org/wiki/Euclidean_algorithm
# Replace the larger of the two numbers by its remainder when divided by the smaller of the two. Stop when remainder
# is zero.
# Noting gcd(a, b, c) = gcd(a, gcd(b, c)), we simply reduce the array using the gcd of two numbers.
#
# Time complexity for gcd of two numbers: 5 * O(k), where k is the number of digits in the smaller number = O(k)
# Time complexity for gcd of all numbers: O(nk), where k is the average number of digits.
def gcd(nums: Sequence[int]) -> int:
    def gcd(a: int, b: int) -> int:
        if a == 0:
            return b
        larger = max(a, b)
        smaller = min(a, b)
        return gcd(larger % smaller, smaller)

    return functools.reduce(gcd, nums, 0)
