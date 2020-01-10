# LeetCode 169.
# 155. Given a list of elements, find the majority element, which appears more than half the time
# (> floor(len(lst) / 2.0)).
#
# You can assume that such element exists.
#
# For example, given [1, 2, 1, 1, 3, 4, 0], return 1.
#
# We could solve this trivially with a collections.Counter.most_common(1), or if that's not allowed, by manually
# populating a dictionary and keeping track of the max count.
