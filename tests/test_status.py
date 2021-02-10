from datetime import datetime, timezone

import pytest

from website_monitor.status import Status


class TestStatus:
    """
    Test the Status dataclass.
    """
    def test_parsed_timestamp(self):
        status = Status('http://www.ya.ru', '2021-02-10T18:04:28.023922+00:00', 200, 0.358636, True)
        assert status.parsed_timestamp == datetime(2021, 2, 10, 18, 4, 28, 23922, tzinfo=timezone.utc)

    def test_parsed_timestamp_fail(self):
        status = Status('http://www.ya.ru', 'WRONG', 200, 0.358636, True)
        with pytest.raises(ValueError):
            status.parsed_timestamp
