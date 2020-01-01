from dp import functions as func


class TestDP:
    def test_num_decodings(self):
        assert func.num_decodings("226") == 3
        assert func.num_decodings("12") == 2
        assert func.num_decodings("111") == 3
        assert func.num_decodings("0") == 0
        assert func.num_decodings("01") == 0
        assert func.num_decodings("10") == 1
        assert func.num_decodings("101") == 1
        assert func.num_decodings("100") == 0
        assert func.num_decodings("110") == 1
        assert func.num_decodings("001") == 0
        assert func.num_decodings(
            "4757562545844617494555774581341211511296816786586787755257741178599337186486723247528324612117156948"
        ) == 589824
