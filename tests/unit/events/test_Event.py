from datetime import datetime

import pytest

from notion_gcal_sync.events.Event import Event


def test_empty_event():
    assert Event()


@pytest.mark.parametrize(
    "test_input, expected",
    [("False", False), (None, False), (True, True), ("True", True)],
)
def test_read_only(test_input, expected):
    event = Event(read_only=test_input)
    assert event.read_only == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [(3000 * "#", 2000 * "#"), ("hello", "hello"), (None, "")],
)
def test_description_too_long(test_input, expected):
    event = Event(description=test_input)
    assert event.description == expected


def test_default_event_length(config_fixture):
    event = Event(
        time_start=datetime(2021, 12, 10, 10, 30),
        time_end=datetime(2021, 12, 10, 10, 30),
        cfg=config_fixture,
    )
    assert event.time_end == "2021-12-10T11:30:00+01:00"


def test_dict_from_class(event_fixture):
    assert event_fixture.to_dict() == dict(
        name="name",
        description="description",
        location="Vatikan",
        gcal_event_id="abc123",
        gcal_calendar_name="Default",
        gcal_calendar_id="dude@gmail.com",
        time_start="2021-08-01T12:30:00+02:00",
        time_end="2021-08-01T14:30:00+02:00",
        recurrent_event="",
        time_last_updated="2021-10-01T02:30:00+02:00",
        time_last_synced="2021-10-12T07:47",
        notion_page_url="https://www.notion.so",
        gcal_page_url="calendar.google.com",
        read_only=False,
    )


@pytest.mark.parametrize(
    "test_calendar_id, test_calendar_name, expected",
    [
        ("dude@gmail.com", "Default", ("dude@gmail.com", "Default")),
        ("dude@gmail.com", "asdf", ("dude@gmail.com", "Default")),
        ("asdf", "Default", ("dude@gmail.com", "Default")),
        (None, None, ("dude@gmail.com", "Default")),
        ("something@gmail.com", "Google Calendar", ("skip", "skip")),
    ],
)
def test_set_calendar(event_fixture, test_calendar_id, test_calendar_name, expected):
    assert event_fixture.set_calendar(test_calendar_id, test_calendar_name) == expected


def test_different_calendar(config_fixture):
    event = Event(
        gcal_calendar_id="dude@gmail.com",
        gcal_calendar_name="Calendar2",
        cfg=config_fixture,
    )
    assert event.gcal_calendar_name == "Calendar2"
    assert event.gcal_calendar_id == "abc123@group.calendar.google.com"
