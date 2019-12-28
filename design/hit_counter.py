from datetime import datetime, date
from typing import List


# 132. Design and implement a HitCounter class that keeps track of requests (or hits).
# It should support the following operations:
#
# record(timestamp): records a hit that happened at timestamp
# total(): returns the total number of hits recorded
# range(lower, upper): returns the number of hits that occurred between timestamps lower and upper (inclusive)
# Follow-up: What if our system has limited memory?
#
# ANSWER: We map each timestamp to an hourly bucket. To work with limited memory, we reuse a bucket by resetting it
# if a later timestamp maps to it. However, we don't decrement the total number of hits; thus, only the range is
# affected by the reset.

class HitCounter:
    def __init__(
            self,
            *,
            start_date: date = date.today(),
            num_buckets: int = 24
    ):
        assert start_date <= date.today(), "Start date can't be in the future"
        assert num_buckets > 0, "Number of buckets must be positive"

        self.start_date = start_date
        self.num_buckets = num_buckets
        self._buckets: List[int] = [0] * num_buckets
        self._total = 0

    def _bucket_idx(self, ts: int) -> int:
        num_sec: int = (datetime.fromtimestamp(ts) - datetime.fromisoformat(str(self.start_date))).seconds
        return num_sec // 3600

    def record(self, ts: int) -> None:
        i: int = self._bucket_idx(ts)
        if i >= self.num_buckets:
            i %= self.num_buckets
            self._buckets[i] = 0
            print(f"Reset bucket: {i}")

        self._buckets[i] += 1
        self._total += 1

    def total(self) -> int:
        return self._total

    def range(self, lower_ts: int, upper_ts: int) -> int:
        start_idx: int = self._bucket_idx(lower_ts)
        end_idx: int = self._bucket_idx(upper_ts)

        return sum(self._buckets[start_idx: end_idx + 1])
