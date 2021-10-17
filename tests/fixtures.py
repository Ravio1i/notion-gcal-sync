from datetime import datetime

import pytest

from notion_gcal_sync.config import Config
from notion_gcal_sync.events.Event import Event
from notion_gcal_sync.utils import Time


@pytest.fixture()
def columns():
    """
    :return:
    """
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
    """
    :return:
    """
    return Time("Europe/Berlin", "+02:00")


@pytest.fixture()
def config(columns, time):
    """
    :param columns:
    :param time:
    :return:
    """
    return Config(60, "skip", "dude@gmail.com", "Default",
                  {"Default": "dude@gmail.com", "Calendar2": "abc123@group.calendar.google.com"},
                  "https://www.notion.so/bla", "SECRET", columns, time)


@pytest.fixture()
def event(config):
    """
    :param config:
    :return:
    """
    return Event(name="name", description="description", location="Vatikan", gcal_event_id="abc123",
                 gcal_calendar_name="Default", gcal_calendar_id="dude@gmail.com", time_start=datetime(2021, 8, 1, 12, 30),
                 time_end=datetime(2021, 8, 1, 14, 30), recurrent_event="", time_last_updated=datetime(2021, 10, 1, 2, 30),
                 time_last_synced="2021-10-12T07:47", notion_page_url="https://www.notion.so",
                 gcal_page_url="calendar.google.com", read_only=False, cfg=config)
