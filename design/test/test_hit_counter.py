from datetime import datetime

from design.hit_counter import HitCounter


class TestHitCounter:
    @staticmethod
    def _hour(start_date: datetime, hr: int) -> int:
        return int(start_date.replace(hour=hr).timestamp())

    def test_hit_counter(self):
        start_date: datetime = datetime.now()
        hc = HitCounter(start_date=start_date.date())

        for hr in range(24):
            hc.record(self._hour(start_date, hr))

        assert hc.total() == 24
        assert hc.range(self._hour(start_date, 0), self._hour(start_date, 23)) == 24

    def test_reset_bucket(self):
        start_date: datetime = datetime.now()
        hc = HitCounter(start_date=start_date.date(), num_buckets=2)

        for hr in range(5):
            hc.record(self._hour(start_date, hr))

        assert hc.total() == 5
        assert hc.range(self._hour(start_date, 0), self._hour(start_date, 4)) == 2
