from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from notion_gcal_sync.utils import Time


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2017-10-25T19:00:00.000+02:00", False),
        ("2017-10-25T19:00:00.000", False),
        ("2017-10-25", True),
        (
            datetime(2017, 10, 25, 00, 00, tzinfo=timezone(timedelta(seconds=7200))),
            False,
        ),
        (None, None),
    ],
)
def test_is_date(test_input, expected):
    assert Time.is_date(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            datetime(2017, 10, 25, 13, 37, 10, 11, tzinfo=timezone(timedelta(seconds=7200))),
            "2017-10-25T13:37:10+02:00",
        ),
        (None, None),
    ],
)
def test_datetime_to_str(test_input, expected):
    assert Time.datetime_to_str(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (datetime(2017, 10, 25), "2017-10-25"),
        (
            datetime(2017, 10, 25, 13, 37, 10, 11, tzinfo=timezone(timedelta(seconds=7200))),
            "2017-10-25",
        ),
        (None, None),
    ],
)
def test_datetime_to_str_date(test_input, expected):
    assert Time.datetime_to_str_date(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (Time("Europe/Berlin", "+02:00"), timedelta(hours=2, minutes=0)),
        (Time("UTC", "+00:00"), timedelta(hours=0, minutes=0)),
        (Time("America/Los_Angeles", "-07:00"), timedelta(hours=-7, minutes=0)),
    ],
)
def test_time(test_input, expected):
    assert test_input.timezone_diff_delta == expected


@pytest.fixture()
def time():
    return Time("Europe/Berlin", "+02:00")


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (None, None),
        ("2017-10-25", datetime(2017, 10, 25)),
        (
            "2017-10-25T00:00",
            datetime(2017, 10, 25, 00, 00, tzinfo=timezone(timedelta(seconds=7200))),
        ),
        (
            "2017-10-25T10:10",
            datetime(2017, 10, 25, 10, 10, tzinfo=timezone(timedelta(seconds=7200))),
        ),
        (
            "2017-10-25T10:10+01:00",
            datetime(2017, 10, 25, 11, 10, tzinfo=timezone(timedelta(seconds=7200))),
        ),
        (
            "2017-10-25T10:10+03:00",
            datetime(2017, 10, 25, 9, 10, tzinfo=timezone(timedelta(seconds=7200))),
        ),
    ],
)
def test_str_to_datetime(time_fixture, test_input, expected):
    assert time_fixture.str_to_datetime(test_input) == expected


def test_utc_str_to_datetime():
    time = Time("UTC", "+00:00")
    assert time.str_to_datetime("2017-10-25T10:10+03:00") == datetime(2017, 10, 25, 7, 10, tzinfo=ZoneInfo("UTC"))


@pytest.mark.parametrize(
    "test_input, expected",
    [(datetime(2017, 10, 25), datetime(2017, 10, 25)), (None, None)],
)
def test_to_datetime(time_fixture, test_input, expected):
    assert time_fixture.to_datetime(test_input) == expected
