import collections
import string
import sys
from typing import MutableSequence, Tuple, Deque, Iterable, Counter, Sequence, MutableMapping, Mapping, Set

from .shortest_prefix_trie import ShortestPrefixTrie


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
# ANSWER: One solution is start with a sliding window of size len(w), that moves 1 step to the right at each iteration.
# The algorithm is as follows:
# 1. At the beginning of an iteration, we check if the current window contains an anagram of W using a temporary
# counter.
#  a. If yes, we add the start index of the window the the result.
#  b. If not, we slide the window, and adjust the temporary counter by decrementing the count for the outgoing
#     character, and incrementing the count for the incoming character.
# 2. If the end has not moved past the last index of S, go to step 1.
#
# Time complexity: If m = len(W) and n = len(W), O(mn), since we make a single pass over S, and only add the unique
# letters from W to the dictionaries. Space complexity: O(W).
#
# Can we do better?
#
# The problem with the above algorithm is the Counter comparison that happens at every iteration. Instead, let's
# keep track of the letters remaining to complete the anagram in a Counter. When all the counts are zero, we've
# found an anagram within the current sliding window of size |W|.
# To keep track of when all the counts are zero, without having to check every entry in the Counter, we maintain a
# distance from the goal state (anagram found). When the distance is zero, we've found an anagram. We begin with a
# distance of |W|, obviously, since we haven't seen any letters yet.

# For every new letter seen at an iteration, if it's present in Counter, we decrement the value by 1 (1 fewer letter
# remains to be seen). If the value becomes negative, we have seen too many of this letter, and we increment the
# distance by 1; otherwise we decrement the distance, indicating we had previously seen fewer of this character, and
# are now moving closer to the goal state.
# For every letter going out of the sliding window, if it's present in Counter, we increment the value by 1 (1 more
# letter remains to be seen). If the value becomes positive, we need more of this letter, and we increment the
# distance by 1; otherwise we decrement the distance, indicating we had previously seen more of this character,
# and are now moving closer to the goal state.
#
# With this improvement, checking whether the current window contains an anagram becomes O(1), and the overall algorithm
# O(n).
def anagrams(s: str, w: str) -> Iterable[int]:
    remains_to_be_seen: Counter[str] = collections.Counter(w)
    result: MutableSequence[int] = []
    dist: int = len(w)

    for i in range(len(s)):
        if s[i] in remains_to_be_seen:
            remains_to_be_seen[s[i]] -= 1
            dist += 1 if remains_to_be_seen[s[i]] < 0 else -1
        j: int = i - len(w)
        if j >= 0 and s[j] in remains_to_be_seen:
            remains_to_be_seen[s[j]] += 1
            dist += 1 if remains_to_be_seen[s[j]] > 0 else -1

        if dist == 0:
            result.append(j + 1)

    return result


# 114. Given a string and a set of delimiters, reverse the words in the string while maintaining the relative order of
# the delimiters. For example, given "hello/world:here", return "here/world:hello"
#
# Follow-up: Does your solution work for the following cases: "hello/world:here/", "hello//world:here"
def reverse_string_preserving_delimiters(s: str) -> str:
    word_stack: MutableSequence[str] = []
    delimiter_queue: Deque[str] = collections.deque()
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


# 153. Find an efficient algorithm to find the smallest distance (measured in number of words) between any two given
# words in a string.
#
# For example, given words "hello", and "world" and a text content of "dog cat hello cat dog dog hello cat world",
# return 1 because there's only one word "cat" in between the two words.
#
# ANSWER: Time complexity: O(n).
def smallest_dist(text: str, words: Tuple[str, str]) -> int:
    i = j = -1
    smallest: int = sys.maxsize

    for x, w in enumerate(text.split()):
        if w == words[0]:
            i = x
        elif w == words[1]:
            j = x

        if i >= 0 and j >= 0:
            smallest = min(smallest, abs(i - j))

    return smallest - 1


# 157. Given a string, determine whether any permutation of it is a palindrome.
#
# For example, carrace should return true, since it can be rearranged to form racecar, which is a palindrome. daily
# should return false, since there's no rearrangement that can form a palindrome.
def can_be_made_palindrome(s: str) -> bool:
    counter: Counter[str] = collections.Counter(s)
    num_odd: int = sum(v % 2 != 0 for v in counter.values())

    return num_odd == len(s) % 2


# 159. Given a string, return the first recurring character in it, or null if there is no recurring character.
#
# For example, given the string "acbbac", return "b". Given the string "abcdef", return null.
def first_recurring_ch(s: str) -> str:
    ch_freq: MutableMapping[str, int] = dict()
    x: Tuple[int, int] = (len(s), -1)

    for i, ch in enumerate(s):
        if ch in ch_freq:
            last_idx: int = ch_freq[ch]
            if i - last_idx < x[0]:
                x = (i - last_idx, last_idx)
        else:
            ch_freq[ch] = i

    return s[x[1]] if x[1] >= 0 else None


# 162. Given a list of words, return the shortest unique prefix of each word. For example, given the list:
#
# dog
# cat
# apple
# apricot
# fish
# Return the list:
#
# d
# c
# app
# apr
# f
#
# ANSWER: We build a Trie that remembers at each node whether or not it's part of a common prefix of the words along
# that branch. For example, if the word "apple" is inserted, every node along that branch has prefix=False.
# However, if we then insert "apricot", nodes "a" and "p" have prefix=True, indicating both words have a common
# prefix "ap".
# With this, finding unique prefix for a word is simply looking for the first node with prefix=False.
# We assume that one word isn't a prefix of another, in which case, we won't have a unique prefix for that word.
#
# To build the Trie, we must insert every character in every word. If average word length is n, and there are m words,
# building the Trie takes O(mn) time and space.
# In the worst case, all words match up to the penultimate character and finding a common prefix takes O(m * (n - 1))
# time, or O(mn) time.
def shortest_unique_prefix(words: Sequence[str]) -> Sequence[str]:
    trie: ShortestPrefixTrie = ShortestPrefixTrie()

    for w in words:
        trie.insert(w)

    return [trie.shortest_prefix(w) for w in words]


# LeetCode 336.
# 167. Given a list of words, find all pairs of unique indices such that the concatenation of the two words is a
# palindrome.
#
# For example, given the list ["code", "edoc", "da", "d"], return [(0, 1), (1, 0), (2, 3)].
#
# ANSWER: For any two words s1s2 and s3, they can be combined to create a palindrome if:
#  1. s1 is a palindrome and s3 is the reverse of s2. The palindrome would be s2s1s3.
#  2. s2 is a palindrome and s3 is the reverse of s1. The palindrome would be s1s2s3.
#
# If there are n words of average length k, we go over each character in each word, so time complexity is O(nk).
def palindrome_pairs(words: Sequence[str]) -> Iterable[Tuple[int, int]]:
    uniq: Mapping[str, int] = {s: i for i, s in enumerate(words)}
    pairs: MutableSequence[Tuple[int, int]] = []

    for s, i in uniq.items():
        for j in range(len(s)):
            left: str = s[:j]
            rev_left: str = left[::-1]
            right: str = s[j:]
            rev_right: str = right[::-1]

            if left == rev_left and rev_right in uniq.keys() and i != uniq[rev_right]:
                # left is a palindrome, and reverse of right exists; prepending the reverse of right makes a palindrome
                if left:
                    pairs.append((uniq[rev_right], i))
                # left is empty, and reverse of right exists; appending the reverse of right makes a palindrome
                else:
                    pairs.append((i, uniq[rev_right]))
            if right == rev_right and rev_left in uniq.keys() and i != uniq[rev_left]:
                # right is a palindrome, and reverse of left exists; appending the reverse of left makes a palindrome
                pairs.append((i, uniq[rev_left]))
                # left is empty, and exists among the words, any palindrome can be combined with it
                if not left:
                    pairs.append((uniq[rev_left], i))

    return pairs


# LeetCode 127.
# 170. Given a start word, an end word, and a dictionary of valid words, find the shortest transformation sequence
# from start to end such that only one letter is changed at each step of the sequence, and each transformed word
# exists in the dictionary. If there is no possible transformation, return null. Each word in the dictionary have
# the same length as start and end and is lowercase.
#
# For example, given start = "dog", end = "cat", and dictionary = {"dot", "dop", "dat", "cat"},
# return ["dog", "dot", "dat", "cat"].
#
# Given start = "dog", end = "cat", and dictionary = {"dot", "tod", "dat", "dar"}, return null as there is no
# possible transformation from dog to cat.
#
# ANSWER: We build an implicit unweighted directed graph where an edge exists from w1 -> w2 if a single letter
# transformation exists from w1 to w2. Then we run a BFS from the start word looking for the end word.
# Time complexity: To find the edges for a node, we loop n * 26 times, which for small n, it practically constant.
# BFS takes O(V+E) time, where V is the number of words, and E is the number of edges.
def ladder_length(start: str, end: str, words: Sequence[str]) -> int:
    uniq_words = dict((w, i) for i, w in enumerate(words))

    # assuming all letters are lowercase alphabetic characters
    def one_apart(word: str) -> Set[int]:
        ret = set()
        for i in range(len(end)):
            for c in string.ascii_lowercase:
                w = word[:i] + c + word[i + 1:]
                if w != word and w in uniq_words:
                    ret.add(uniq_words[w])
        return ret

    end_idx = -1 if end not in uniq_words else uniq_words[end]
    if end_idx == -1:
        return 0

    # https://www.youtube.com/watch?v=KiCBXu4P-2Y
    def bfs(s: int) -> Tuple[bool, int]:
        visited: Set[int] = set()
        queue: Deque[int] = collections.deque()
        # Start word to s is one move already
        move_count = 1
        nodes_in_next_layer = 0
        nodes_left_in_layer = 1
        found = False

        queue.append(s)
        visited.add(s)

        while queue:
            x = queue.popleft()
            if x == end_idx:
                found = True
                break

            for y in one_apart(words[x]) - visited:
                nodes_in_next_layer += 1
                queue.append(y)
                visited.add(y)

            nodes_left_in_layer -= 1
            if nodes_left_in_layer == 0:
                nodes_left_in_layer = nodes_in_next_layer
                nodes_in_next_layer = 0
                move_count += 1

        return found, move_count

    moves = sys.maxsize
    for x in one_apart(start):
        y = bfs(x)
        if y[0]:
            moves = min(moves, y[1])
    return moves + 1 if moves < sys.maxsize else 0
