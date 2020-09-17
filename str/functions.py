import collections
import heapq
import string
import sys
from typing import MutableSequence, Tuple, Deque, Iterable, Counter, Sequence, MutableMapping, Mapping, Set, List

from .aho_corasick import AhoCorasickAutomaton
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


# LeetCode 30.
# 172. Given a string 's' and a list of words 'words', where each word is the same length, find all starting indices of
# substrings in 's' that is a concatenation of every word in 'words' exactly once.
#
# For example, given s = "dogcatcatcodecatdog" and words = ["cat", "dog"], return [0, 13], since "dogcat" starts at
# index 0 and "catdog" starts at index 13.
#
# Given s = "barfoobazbitbyte" and words = ["dog", "cat"], return [] since there are no substrings composed of "dog"
# and "cat" in s.
def substr_indices(s: str, words: Sequence[str]) -> Sequence[int]:
    indices = []
    if not words:
        return indices
    m = len(words[0])
    n = m * len(words)

    for start in range(len(s)):
        end = start + n
        if end > len(s):
            break
        uniq = collections.Counter(words)
        for i in range(start, end, m):
            token = s[i:i + m]
            uniq[token] -= 1
            if uniq[token] >= 0:  # Counter returns zero for missing keys
                if uniq[token] == 0:
                    del uniq[token]
                if not uniq:
                    indices.append(start)
            else:
                break

    return indices


# Alternative solution to #172 using an Aho-Corasick automaton and a sliding window.
def substr_indices_2(s: str, words: Sequence[str]) -> Sequence[int]:
    indices: MutableSequence[int] = []
    n: int = len(words)
    m: int = len(words[0]) if n > 0 else 0
    if not words or m * n > len(s):
        return indices

    # Create Aho-Corasick automaton, and for each word, store the indices at which it appears in 'words'
    ac = AhoCorasickAutomaton(words)

    # f[i] = x if s[i:i + m] = words[x]
    #      = -1 otherwise
    # In other words, for each i, f[i] is the index of the word in words that starts at s[i].
    f: MutableSequence[int] = [-1] * len(s)
    node: AhoCorasickAutomaton.Node = ac.root
    i = 0
    freq: MutableMapping[str, int] = collections.defaultdict(int)
    while i < len(s) and node:
        if s[i] in node.children:
            node = node.children[s[i]]
            i += 1
        elif node.failure:
            node = node.failure
        else:
            node = ac.root
            i += 1

        if node.word:
            f[i - m] = node.val[0]
            freq[words[node.val[0]]] = len(node.val)

    # Divide 'f' into subarrays, where each subarray is of the form: {f[i], f[i + m], f[i + 2m], ...}.
    # Each subarray must contain at least n items. Since f[i] represents a match (or not) for a string of length m,
    # we don't need to check the (m - 1) indices between each f[i] in the subarray. What we are looking for is a
    # contiguous sequence of length n that is some permutation of numbers from 0 to n, that, in turn, represents
    # some permutation of the words in 'words'.

    # Indices to the words we have seen so far; when its size is equal to n, a match has been found. By checking its
    # size, we can determine in constant time if a match has been found without having to scan the 'seen' dict
    queue: Deque[int] = collections.deque()
    # seen[i] = number of times we have seen f[i]
    seen: MutableMapping[int, int] = collections.defaultdict(int)
    for i in range(len(f) - n * m + 1):
        # Start new window
        seen.clear()
        queue.clear()
        for j in range((len(f) - i) // m):
            k: int = i + j * m

            if f[k] != -1:
                # We have seen the words[f[k]] before
                while queue and seen[f[k]] >= freq[words[f[k]]]:
                    x = queue.popleft()
                    seen[x] -= 1

                queue.append(f[k])
                seen[f[k]] += 1

                if len(queue) == n:
                    indices.append(k - (n - 1) * m)
            else:
                # Invalidate window, start new
                seen.clear()
                queue.clear()
            # Never check same index twice; this guards against the degenerate case where each pattern is of length 1
            f[k] = -1

    return indices


# LeetCode 205.
# 176. Determine whether there exists a one-to-one character mapping from one string s1 to another s2.
# For example, given s1 = abc and s2 = bcd, return true since we can map a to b, b to c, and c to d.
# Given s1 = foo and s2 = bar, return false since the o cannot map to two characters.
def is_isomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    c1: Mapping[str, Set[int]] = collections.defaultdict(set)
    c2: Mapping[str, Set[int]] = collections.defaultdict(set)

    for i in range(len(s)):
        c1[s[i]].add(i)
        c2[t[i]].add(i)

    return len(c1) == len(c2) and all(c1[k1] == c2[k2] for k1, k2 in zip(c1.keys(), c2.keys()))


# LeetCode 131.
# Given a string s, partition s such that every substring of the partition is a palindrome.
# Return all possible palindrome partitioning of s.
#
# Example:
#
# Input: "aab"
# Output:
# [
#   ["aa","b"],
#   ["a","a","b"]
# ]
def palindrome_substr(s: str) -> MutableSequence[MutableSequence[str]]:
    seen = {}

    def helper(s1: str) -> List[List[str]]:
        # return solution if stored
        if s1 in seen:
            return seen[s1]

        out = []

        for i in range(1, len(s1) + 1):
            part = s1[:i]

            # if substring is a palindrome, recurse
            if part == part[::-1]:
                # get palindrome partitions for rest of string
                rest = helper(s1[i:])
                # populate output array with palindrome partitions
                for r in rest:
                    # list concatenation
                    out.append([part] + r)
                if not rest:
                    out.append([part])

        # store subproblem solution
        seen[s1] = out

        return out

    return helper(s)


# LeetCode 132.
# 181. Given a string, split it into as few strings as possible such that each string is a palindrome.
#
# For example, given the input string racecarannakayak, return ["racecar", "anna", "kayak"].
#
# Given the input string abc, return ["a", "b", "c"].
#
# ANSWER: We first find all palindromes in string s. This forms a graph where the vertices are the start indices, and
# the edges are the length of the palindromes. Then we run BFS on this graph, visiting the neighbor first that has the
# longest palindrome. We make this greedy choice based on the common sense that we will need fewer cuts if we can cover
# more ground by following a longer edge.
#
# Alternative solution:
# If s1 is a palindrome, no cuts are necessary; else we cut at each index, and calculate the min of all using
# dynamic programming. The problem exhibits the following characteristics:
#   Overlapping subproblems: Either or both of the left or right substrings could have been seen before.
#   Optimal substructure: Num cuts is one more than the sum of the min num of cuts of the left and the right
#   substrings. For example, consider string "aabc" cut into "aa" and "bc". Since "aa" is a palindrome, its
#   min num of cuts is zero; "bc" can further be cut into "b" and "c", each of which are palindromes. Thus,
#   min num of cuts for "bc" is one, and hence, min num of cuts for "aabc" is 0 + 1 + 1 = 2.
#
# Time complexity:
#   Note that for 1 <= i <= n, there are n - i - 1 possible substrings.
#   Thus, finding all palindromes takes n - 1 + n - 2 + ... + 1 time, which is O(n^2).
#   BFS takes O(n) time in the worst case when all characters are distinct. Each heap operation takes O(log n) time.
#   Overall time complexity: O(n^2) + O(n log n) = O(n^2).
def palindrome_substr_min_cut(s: str) -> int:
    graph: MutableMapping[int, MutableSequence[int]] = dict()
    palindromes: Set[Tuple[int, int]] = set()
    n = len(s)
    for i in range(n):
        graph[i] = [i + 1]
        palindromes.add((i, i + 1))

    def is_palindrome(start: int, end: int) -> bool:
        return s[start] == s[end] and (end - start == 1 or (start + 1, end) in palindromes)  # noqa: F821

    # Find all palindromes of length i, 2 <= i <= n
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length - 1

            if is_palindrome(start, end):
                graph[start].append(end + 1)
                palindromes.add((start, end + 1))

    del palindromes

    queue: List[Tuple[int, int, int, int]] = [(0, graph[0][-1], 0, -1)]
    seen: Set[int] = set()
    parents: MutableMapping[int, int] = dict()

    while queue:
        x = heapq.heappop(queue)
        depth, i, parent = x[0], -x[2], x[3]
        seen.add(i)
        parents[i] = parent
        if i == n:
            break

        unseen_neighbors = filter(lambda k: k not in seen, graph[i])
        for j in unseen_neighbors:
            k = graph[j][-1] if j in graph else j
            heapq.heappush(queue, (depth + 1, -k, -j, i))

    tokens: Deque[str] = collections.deque()
    i: int = n

    while i > 0:
        tokens.appendleft(s[parents[i]:i])
        i = parents[i]

    return len(tokens) - 1
