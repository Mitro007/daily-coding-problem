# LeetCode 91.
# Given the mapping a = 1, b = 2, ... z = 26, and an encoded message, count the number of ways it can be decoded.
# For example, the message '111' would give 3, since it could be decoded as 'aaa', 'ka', and 'ak'.
# You can assume that the messages are decodable. For example, '001' is not allowed.
# Time complexity: O(n).


def num_decodings(msg: str) -> int:
    dp = [0] * (len(msg) + 1)  # dp[i] = Num decodings for message[:i]
    dp[0] = 1  # Only one way to decode an empty message, which is an empty string
    dp[1] = 1 if '1' <= msg[0] <= '9' else 0

    for i in range(2, len(dp)):
        if '1' <= msg[i - 1] <= '9':
            dp[i] += dp[i - 1]

        if '10' <= msg[i - 2:i] <= '26':
            dp[i] += dp[i - 2]

    return dp[-1]
