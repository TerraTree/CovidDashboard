
from time_conversions import hhmm_to_seconds, minutes_to_seconds, hours_to_minutes


def test_hhmm_to_seconds():
    time = hhmm_to_seconds("1:11")
    assert time == 4260


def test_minutes_to_seconds():
    time = minutes_to_seconds(45)
    assert time == 2700


def test_hours_to_minutes():
    time = hours_to_minutes(3)
    assert time == 180
