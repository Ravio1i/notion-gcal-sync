import pytest

from Config import Config
from utils.Time import Time


@pytest.fixture()
def columns():
    return {
        "name": "Name",
        "date": 'Date',
        "recurrent_event": 'Recurrence',
        "tags": 'Tags',
        "description": 'Description',
        "location": 'Location',
        "last_updated_time": 'Last Updated',
        "last_synced_time": 'Last Synced',
        "gcal_event_id": 'GCal event Id',
        "gcal_event_url": 'GCal event url',
        "gcal_calendar_name": 'Calendar',
        "gcal_calendar_id": 'GCal calendar Id',
        "read_only": 'Read Only',
        "to_delete": 'Delete?',
        "deleted": 'Deleted'
    }


@pytest.fixture()
def time():
    return Time("Europe/Berlin", "+02:00")


@pytest.fixture()
def config(columns, time):
    return Config(60, "skip", "dude@gmail.com", "Default", {"Default": "dude@gmail.com", "Calender2": "abc123@group.calendar.google.com"},
                  "https://www.notion.so/bla", "SECRET", columns, time)


@pytest.mark.parametrize(
    "test_url, expected",
    [("https://www.notion.so/subdomain/THE_ID?v=asdfasdf123&p=", "THE_ID"),
     ("https://www.notion.so/THE_ID?v=asdfasdf123&p=", "THE_ID"),
     ("https://www.notion.so/bla", None),
     ("https://www.notion.so/bla?v=", None)])
def test_database_id(time, columns, test_url, expected):
    config = Config(60, "skip", "dude@gmail.com", "Default", {"Default": "dude@gmail.com"}, test_url,
                    "SECRET", columns, time)

    assert config.database_id == expected


def test_default_event_length(config):
    config.default_event_length = "123"
    assert config.default_event_length == 60


@pytest.mark.parametrize(
    "test_action, expected",
    [("skip", "skip"), ("today", "today"), ("something_else", "skip")])
def test_no_date_action(config, test_action, expected):
    config.no_date_action = test_action
    assert config.no_date_action == expected


@pytest.mark.parametrize(
    "test_calendar_id, expected",
    [("dude@gmail.com", "Default"), ("abc123@group.calendar.google.com", "Calender2"),
     ("error@group.calendar.google.com", None), (None, None)])
def test_get_calendar_name(config, test_calendar_id, expected):
    assert config.get_calendar_name(test_calendar_id) == expected


@pytest.mark.parametrize(
    "test_calendar_name, expected",
    [("Default", "dude@gmail.com"), ("Calender2", "abc123@group.calendar.google.com"),
     ("error@group.calendar.google.com", None), (None, None)])
def test_get_calendar_idd(config, test_calendar_name, expected):
    assert config.get_calendar_id(test_calendar_name) == expected


@pytest.mark.parametrize(
    "test_calendar_id, expected",
    [("dude@gmail.com", True), ("abc123@group.calendar.google.com", True),
     ("error@group.calendar.google.com", False), (None, False)])
def test_is_valid_calendar_id(config, test_calendar_id, expected):
    assert config.is_valid_calendar_id(test_calendar_id) == expected


@pytest.mark.parametrize(
    "test_calendar_name, expected",
    [("Default", True), ("Calender2", True),
     ("error@group.calendar.google.com", False), (None, False)])
def test_is_valid_calendar_name(config, test_calendar_name, expected):
    assert config.is_valid_calendar_name(test_calendar_name) == expected

