from str import functions as func
import pytest


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
