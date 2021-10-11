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
    return Config(60, "skip", "dude@gmail.com", "Default", {"Default": "dude@gmail.com"}, "https://www.notion.so/bla",
                  "SECRET", columns, time)


@pytest.mark.parametrize(
    "test_url, expected",
    [("https://www.notion.so/subdomain/THE_ID?v=asdfasdf123&p=", "THE_ID"),
     ("https://www.notion.so/bla", None),
     ("https://www.notion.so/bla?v=", None),
     ("https://www.notion.so/bla?v=", None)])
def test_database_id(time, columns, test_url, expected):
    config = Config(60, "skip", "dude@gmail.com", "Default", {"Default": "dude@gmail.com"}, test_url,
                    "SECRET", columns, time)

    assert config.database_id == expected


def test_config(config):
    config.notion_url
    assert config.database_id == "THISISTHEID"


def test_get_calendar_name():
    assert False


def test_is_valid_calendar_name():
    assert False


def test_is_valid_calendar_id():
    assert False
