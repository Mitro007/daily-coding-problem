from typing import DefaultDict, List
from collections import defaultdict
import bisect
import functools


# 97. Write a map implementation with a get function that lets you retrieve the value of a key at a particular time.
#
# It should contain the following methods:
#     set(key, value, time): # sets key to value for t = time.
#     get(key, time): # gets the key at t = time.
#
# The map should work like this. If we set a key at a particular time, it will maintain that value forever or until
# it gets set at a later time. In other words, when we get a key at a time, it should return the value that was set
# for that key set at the most recent time.
#
# Consider the following examples:
#
# d.set(1, 1, 0) # set key 1 to value 1 at time 0
# d.set(1, 2, 2) # set key 1 to value 2 at time 2
# d.get(1, 1) # get key 1 at time 1 should be 1
# d.get(1, 3) # get key 1 at time 3 should be 2
#
# d.set(1, 1, 5) # set key 1 to value 1 at time 5
# d.get(1, 0) # get key 1 at time 0 should be null
# d.get(1, 10) # get key 1 at time 10 should be 1
#
# d.set(1, 1, 0) # set key 1 to value 1 at time 0
# d.set(1, 2, 0) # set key 1 to value 2 at time 0
# d.get(1, 0) # get key 1 at time 0 should be 2
#
# ANSWER: We keep a map of key to a list of (time, value) sorted by time. For each set/get call, we do a binary search
# on the values to find the element corresponding to the given time. Since bisect_left doesn't indicate whether the
# value was found or not, we check if the element at the returned index matches the given time. If not, this is the
# insertion point for the given time, and the getter/setter proceeds accordingly.
#
# Time complexity: O(log n) for each get/set call, where n is the number of values for that key.
@functools.total_ordering
class MapValue:
    def __init__(self, time: int, value: int = 0):
        self.time = time
        self.value = value

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time


class TimedMap:
    def __init__(self):
        self._data: DefaultDict[int, List[MapValue]] = defaultdict(list)

    def set(self, key: int, value: int, time: int) -> None:
        new_val: MapValue = MapValue(time, value)
        i: int = bisect.bisect_left(self._data[key], new_val)
        if i < len(self._data[key]):
            if self._data[key][i].time == time:
                self._data[key][i] = new_val
            else:
                self._data[key].insert(i, new_val)
        else:
            self._data[key].append(new_val)

    def get(self, key: int, time: int) -> int:
        i: int = bisect.bisect_left(self._data[key], MapValue(time))
        if i < len(self._data[key]) and self._data[key][i].time == time:
            return self._data[key][i].value
        if i > 0:
            return self._data[key][i - 1].value
        return None

    def __repr__(self):
        return f"{self._data}"
