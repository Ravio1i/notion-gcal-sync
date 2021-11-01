import pytest

from events.GCalEvent import GCalEvent


@pytest.mark.parametrize(
    "test_url, expected",
    [
        ({"htmlLink": "https://www.google.com/calendar/event?eid=***"}, "https://www.google.com/calendar/event?eid=***"),
        (
            {"htmlLink": "https://www.google.com/calendar/event?eid=***&ctz=Europe/Berlin"},
            "https://www.google.com/calendar/event?eid=***",
        ),
        ({}, ""),
    ],
)
def test_get_gcal_page_url(test_url, expected):
    assert GCalEvent.get_gcal_page_url(test_url) == expected
