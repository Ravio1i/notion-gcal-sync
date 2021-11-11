from datetime import datetime, timedelta, timezone, date
from zoneinfo import ZoneInfo

import pytest
import pendulum

from notion_gcal_sync.utils import Time


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2017-10-25T19:00:00.000+02:00", "2017-10-25T19:00:00.000+02:00"),
        ("2017-10-25T19:00:00Z", "2017-10-25T19:00:00+00:00"),
        ("2017-10-25", "2017-10-25"),
        (None, None),
    ],
)
def test_format_date(test_input, expected):
    assert Time.format_str(test_input) == expected


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
        ("Europe/Berlin", pendulum.timezone("Europe/Berlin")),
        ("UTC", pendulum.timezone("UTC")),
        ("America/Los_Angeles", pendulum.timezone("America/Los_Angeles")),
    ],
)
def test_time(test_input, expected):
    time = Time(test_input)
    assert time.timezone == expected


@pytest.fixture()
def time():
    return Time("Europe/Berlin")


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
def test_to_str(time, test_input, expected):
    assert time.to_str(test_input) == expected


def test_utc_to_datetime():
    time = Time("UTC")
    assert time.to_datetime("2017-10-25T10:10+03:00") == datetime(2017, 10, 25, 7, 10, tzinfo=ZoneInfo("UTC"))


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (None, None),
        (date(2017, 10, 25), date(2017, 10, 25)),
        (date(2017, 10, 25), date(2017, 10, 25)),
        (
            datetime(2017, 10, 25, 10, 10, 10, 10, tzinfo=timezone(timedelta(seconds=7200))),
            datetime(2017, 10, 25, 10, 10, tzinfo=timezone(timedelta(seconds=7200))),
        ),
        (
            "2017-10-25T00:00:00",
            datetime(2017, 10, 25, 00, 00, tzinfo=timezone(timedelta(seconds=7200))),
        ),
        (
            "2017-10-25T10:10",
            datetime(2017, 10, 25, 10, 10, tzinfo=timezone(timedelta(seconds=7200))),
        ),
        (
            "2021-10-29T10:10+02:00",
            datetime(2021, 10, 29, 10, 10, tzinfo=timezone(timedelta(seconds=7200))),
        ),
        (
            "2021-10-31T11:10+01:00",
            datetime(2021, 10, 31, 11, 10, tzinfo=timezone(timedelta(seconds=3600))),
        ),
        (
            "2017-10-25T10:10+03:00",
            datetime(2017, 10, 25, 10, 10, tzinfo=timezone(timedelta(seconds=10800))),
        ),
    ],
)
def test_to_datetime(time_fixture, test_input, expected):
    assert time_fixture.to_datetime(test_input) == expected
