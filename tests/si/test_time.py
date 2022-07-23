import pytest

from measured import Quantity, approximately
from measured.si import Day, Hour, Minute, Second


@pytest.mark.parametrize(
    "days, hours, minutes, seconds",
    [
        (0 * Day, 0 * Hour, 0 * Minute, 0 * Second),
        (1 / 86400 * Day, 1 / 3600 * Hour, 1 / 60 * Minute, 1 * Second),
        (1 / 1440 * Day, 1 / 60 * Hour, 1 * Minute, 60 * Second),
        (1 / 24 * Day, 1 * Hour, 60 * Minute, 3600 * Second),
        (1 * Day, 24 * Hour, 1440 * Minute, 86400 * Second),
    ],
)
def test_time_conversions(
    days: Quantity, hours: Quantity, minutes: Quantity, seconds: Quantity
) -> None:
    assert days == hours
    assert days == minutes
    assert days == seconds

    assert hours == approximately(days)
    assert hours == minutes
    assert hours == seconds

    assert minutes == approximately(days)
    assert minutes == hours
    assert minutes == seconds

    assert seconds == approximately(days)
    assert seconds == hours
    assert seconds == minutes
