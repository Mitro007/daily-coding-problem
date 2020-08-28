from typing import Mapping, Any


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

# 173. Write a function to flatten a nested dictionary. Namespace the keys with a period.
#
# For example, given the following dictionary:
#
# {
#     "key": 3,
#     "foo": {
#         "a": 5,
#         "bar": {
#             "baz": 8
#         }
#     }
# }
# it should become:
#
# {
#     "key": 3,
#     "foo.a": 5,
#     "foo.bar.baz": 8
# }
# You can assume keys do not contain dots in them, i.e. no clobbering will occur.
#
# See https://stackoverflow.com/questions/39817081/typing-any-vs-object
def flatten_dict(nested_dict: Mapping[str, Any]) -> Mapping[str, int]:
    def flatten(prefix: str, v: Any) -> Mapping[str, int]:
        if isinstance(v, int):
            return {prefix: v}
        d = {}
        for k, v in v.items():
            # See https://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/
            d = {**d, **flatten(f"{prefix}.{k}" if prefix else k, v)}

        return d

    return flatten("", nested_dict)
