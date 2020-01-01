from typing import MutableSequence, Tuple, Deque, Iterable, Counter
from collections import deque
import collections


# LeetCode 5.
# 46. Given a string, find the longest palindromic contiguous substring. If there are more than one with the maximum
# length, return any one.
#
# For example, the longest palindromic substring of "aabcdcb" is "bcdcb". The longest palindromic substring of
# "bananas" is "anana".
#
# ANSWER: Let dp[i][j] = true if s[i:j+1] is a palindrome. Since a palindrome is symmetric, dp[i][j] = true when
# dp[i + 1][j - 1] = true and s[i] = s[j].
# The base case is for palindromes of length 1, which are single letter strings.
#
# Time complexity: For a string of length n and a substring of length j, there are n - j + 1 possible substrings
# (see the inner for loop below). Since j could run from 2 through n, we have a series (n - 1 + n - 2 + ... + 1),
# which sums to n(n - 1) / 2. Thus, the runtime is quadratic. So is the space complexity, since we have a 2D array
# of size n^2.
#
# There a O(n) algorithm by Manacher. See https://github.com/asarkar/coding-interview/blob/master/src/main/scala/org \
# /asarkar/codinginterview/strings/package.scala
def longest_palindrome(s: str) -> str:
    if not s:
        return ""

    n: int = len(s)
    dp: MutableSequence[MutableSequence[bool]] = [[False] * n for _ in range(n)]
    longest: Tuple[int, int] = (-1, -1)

    for i in range(n):
        dp[i][i] = True
        longest = (i, i)

    for j in range(2, n + 1):
        for i in range(0, n - j + 1):
            k = i + j - 1
            dp[i][k] = s[i] == s[k] and (j == 2 or dp[i + 1][k - 1])
            if dp[i][k] and k - i + 1 > longest[1] - longest[0]:
                longest = (i, k)

    return s[longest[0]:longest[1] + 1]


# LeetCode 438.
# 111. Given a word W and a string S, find all starting indices in S which are anagrams of W.
#
# For example, given that W is "ab", and S is "abxaba", return 0, 3, and 4.
#
# ANSWER: We start with a sliding window of size len(w), that moves 1 step to the right at each iteration.
# The algorithm is as follows:
# 1. At the beginning of an iteration, we check if the current window contains an anagram of W using a temporary
# counter.
#  a. If yes, we add the start index of the window the the result.
#  b. If not, we slide the window, and adjust the temporary counter by decrementing the count for the outgoing
#     character, and incrementing the count for the incoming character.
# 2. If the end has not moved past the last index of S, go to step 1.
#
# Time complexity: Possibly O(n), since we make a single pass over S. However, I'm not sure about the time taken for
# comparing the Counters.
def anagrams(s: str, w: str) -> Iterable[int]:
    letter_map: Counter[str] = collections.Counter(w)
    result: MutableSequence[int] = []
    start: int = 0
    end: int = start + len(w) - 1
    tmp: Counter[str] = collections.Counter(s[start:end + 1])

    while end < len(s):
        if tmp == letter_map:
            result.append(start)

        tmp.update({s[start]: -1})
        if tmp[s[start]] == 0:
            del tmp[s[start]]
        start += 1
        end += 1
        if end < len(s):
            tmp.update({s[end]: 1})

    return result


# 114. Given a string and a set of delimiters, reverse the words in the string while maintaining the relative order of
# the delimiters. For example, given "hello/world:here", return "here/world:hello"
#
# Follow-up: Does your solution work for the following cases: "hello/world:here/", "hello//world:here"
def reverse_string_preserving_delimiters(s: str) -> str:
    word_stack: MutableSequence[str] = []
    delimiter_queue: Deque[str] = deque()
    word: MutableSequence[str] = []
    delimiter: MutableSequence[str] = []

    for ch in s:
        if ch.isalpha():
            if delimiter:
                delimiter_queue.append("".join(delimiter))
                delimiter.clear()
            word.append(ch)
        else:
            if word:
                word_stack.append("".join(word))
                word.clear()
            delimiter.append(ch)

    if word:
        word_stack.append("".join(word))
        word.clear()
    if delimiter:
        delimiter_queue.append("".join(delimiter))
        delimiter.clear()

    while len(word_stack) > 1:
        delim: str = delimiter_queue.popleft() if delimiter_queue else ""
        word_1: str = word_stack.pop()
        if word_stack:
            word_stack.append(f"{word_1}{delim}{word_stack.pop()}")
        else:
            word_stack.append(f"{word_1}{delim}")

    while word_stack and delimiter_queue:
        word_stack.append(f"{word_stack.pop()}{delimiter_queue.popleft()}")

    return word_stack.pop()
