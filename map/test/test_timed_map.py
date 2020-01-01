from map.timed_map import TimedMap


class TestTimedMap:
    def test_timed_map(self):
        tm = TimedMap()
        tm.set(1, 1, 0)  # set key 1 to value 1 at time 0
        tm.set(1, 2, 2)  # set key 1 to value 2 at time 2
        assert tm.get(1, 1) == 1  # get key 1 at time 1 should be 1
        assert tm.get(1, 3) == 2  # get key 1 at time 3 should be 2

        tm = TimedMap()
        tm.set(1, 1, 5)  # set key 1 to value 1 at time 5
        assert tm.get(1, 0) is None  # get key 1 at time 0 should be null
        assert tm.get(1, 10) == 1  # get key 1 at time 10 should be 1

        tm = TimedMap()
        tm.set(1, 1, 0)  # set key 1 to value 1 at time 0
        tm.set(1, 2, 0)  # set key 1 to value 2 at time 0
        assert tm.get(1, 0) == 2  # get key 1 at time 0 should be 2
