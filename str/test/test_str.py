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
