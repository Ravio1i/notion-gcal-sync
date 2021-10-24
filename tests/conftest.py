from datetime import datetime

import pytest

from notion_gcal_sync.config import Config
from notion_gcal_sync.events.Event import Event
from notion_gcal_sync.utils import Time


@pytest.fixture(scope="module")
def notion_columns_fixture():
    return {
        "name": "Name",
        "date": "Date",
        "recurrent_event": "Recurrence",
        "tags": "Tags",
        "description": "Description",
        "location": "Location",
        "last_updated_time": "Last Updated",
        "last_synced_time": "Last Synced",
        "gcal_event_id": "GCal event Id",
        "gcal_event_url": "GCal event url",
        "gcal_calendar_name": "Calendar",
        "gcal_calendar_id": "GCal calendar Id",
        "read_only": "Read Only",
        "to_delete": "To Delete",
        "deleted": "Deleted",
    }


@pytest.fixture(scope="module")
def config_dict_fixture(notion_columns_fixture):
    return {
        "default_event_length": 60,
        "no_date_action": "skip",
        "gcal_calendars": {"Default": "dude@gmail.com", "Calendar2": "abc123@group.calendar.google.com"},
        "gcal_default_calendar_name": "Default",
        "notion_columns": notion_columns_fixture,
        "notion_database_url": "https://www.notion.so/*/***?v=***&p=",
        "notion_token": "SECRET",
        "timezone_diff": "+02:00",
        "timezone_name": "Europe/Berlin",
    }


@pytest.fixture(scope="module")
def time_fixture():
    return Time("Europe/Berlin", "+02:00")


@pytest.fixture(scope="module")
def config_fixture(notion_columns_fixture, time_fixture):
    return Config(
        default_event_length=60,
        no_date_action="skip",
        gcal_calendars={"Default": "dude@gmail.com", "Calendar2": "abc123@group.calendar.google.com"},
        gcal_default_calendar_name="Default",
        notion_database_url="https://www.notion.so/*/***?v=***&p=",
        notion_token="SECRET",
        notion_columns=notion_columns_fixture,
        time=time_fixture,
    )


@pytest.fixture(scope="module")
def event_fixture(config_fixture):
    return Event(
        name="name",
        description="description",
        location="Vatikan",
        gcal_event_id="abc123",
        gcal_calendar_name="Default",
        gcal_calendar_id="dude@gmail.com",
        time_start=datetime(2021, 8, 1, 12, 30),
        time_end=datetime(2021, 8, 1, 14, 30),
        recurrent_event="",
        time_last_updated=datetime(2021, 10, 1, 2, 30),
        time_last_synced="2021-10-12T07:47",
        notion_page_url="https://www.notion.so",
        gcal_page_url="calendar.google.com",
        read_only=False,
        cfg=config_fixture,
    )
