import pytest

from str import functions as func


class TestString:
    @pytest.mark.parametrize("s, palindrome", [
        ("cbbd", "bb"),
        ("aabcdcb", "bcdcb"),
        ("bananas", "anana"),
        ("", ""),
        ("a", "a"),
        ("aaaa", "aaaa"),
        ("ababababa", "ababababa"),
        ("aaabaaaa", "aaabaaa"),
        ("ccc", "ccc"),
        ("babad", "aba")
    ])
    def test_longest_palindrome(self, s, palindrome):
        assert func.longest_palindrome(s) == palindrome

    def test_reverse_string_preserving_delimiters(self):
        assert func.reverse_string_preserving_delimiters("hello/world:here") == "here/world:hello"
        assert func.reverse_string_preserving_delimiters("hello/world:here/") == "here/world:hello/"
        assert func.reverse_string_preserving_delimiters("hello//world:here") == "here//world:hello"

    def test_anagrams(self):
        assert func.anagrams("abxaba", "ab") == [0, 3, 4]
        assert func.anagrams("cbaebabacd", "abc") == [0, 6]
        assert func.anagrams("abab", "ab") == [0, 1, 2]
        assert func.anagrams("baa", "aa") == [1]
        assert func.anagrams("", "a") == []

    def test_smallest_dist(self):
        assert func.smallest_dist("dog cat hello cat dog dog hello cat world", ("hello", "world")) == 1

    def test_can_be_made_palindrome(self):
        assert func.can_be_made_palindrome("carrace")
        assert not func.can_be_made_palindrome("daily")

    def test_first_recurring_ch(self):
        assert func.first_recurring_ch("acbbac") == "b"
        assert func.first_recurring_ch("abcdef") is None

    def test_shortest_unique_prefix(self):
        assert func.shortest_unique_prefix(["dog", "cat", "apple", "apricot", "fish"]) == ["d", "c", "app", "apr", "f"]
        assert func.shortest_unique_prefix(["zebra", "dog", "duck", "dove"]) == ["z", "dog", "du", "dov"]

    def test_palindrome_pairs(self):
        assert func.palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"]) == [(0, 1), (1, 0), (3, 2), (2, 4)]
        assert func.palindrome_pairs(["bat", "tab", "cat"]) == [(0, 1), (1, 0)]
        assert func.palindrome_pairs(["code", "edoc", "da", "d"]) == [(0, 1), (1, 0), (2, 3)]
        assert func.palindrome_pairs(["a", ""]) == [(0, 1), (1, 0)]
        assert func.palindrome_pairs(["a", "b", "c", "ab", "ac", "aa"]) == [(1, 3), (3, 0), (2, 4), (4, 0), (0, 5),
                                                                            (5, 0)]

    def test_ladder_length(self):
        assert func.ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
        assert func.ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
        assert func.ladder_length("hot", "dog", ["hot", "dog"]) == 0
        assert func.ladder_length("hit", "cog", ["hot", "dot", "tog", "cog"]) == 0
        assert func.ladder_length("a", "c", ["a", "b", "c"]) == 2

    @pytest.mark.parametrize("s, words, indices", [
        ("dogcatcatcodecatdog", ["cat", "dog"], [0, 13]),
        ("barfoothefoobarman", ["foo", "bar"], [0, 9]),
        ("wordgoodgoodgoodbestword", ["word", "good", "best", "word"], []),
        ("barfoobazbitbyte", ["dog", "cat"], []),
        ("barfoofoobarthefoobarman", ["bar", "foo", "the"], [6, 9, 12]),
        ("aaa", ["a", "a"], [0, 1]),
        ("aaa", ["aa", "aa"], []),
        ("", [], []),
        ("aaaaaa", ["aaa", "aaa"], [0]),
        ("aaaaaaaa", ["aa", "aa", "aa"], [0, 1, 2]),
        ("abaababbaba", ["ba", "ab", "ab"], [1, 3]),
        ("cbaacacbaa", ["cb", "aa"], [0, 6]),
        ("aaabbbc", ["a", "a", "b", "b", "c"], [])
    ])
    def test_substr_indices(self, s, words, indices):
        assert set(func.substr_indices(s, words)) == set(indices)
        assert set(func.substr_indices_2(s, words)) == set(indices)

    def test_is_isomorphic(self):
        assert func.is_isomorphic("egg", "add")
        assert not func.is_isomorphic("foo", "bar")
        assert func.is_isomorphic("paper", "title")
        assert func.is_isomorphic("abc", "bcd")
        assert not func.is_isomorphic("aba", "baa")
