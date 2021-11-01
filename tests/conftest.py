from datetime import datetime, date

import pytest
import pytz

from notion_gcal_sync.config import Config
from notion_gcal_sync.events.Event import Event
from notion_gcal_sync.utils import Time


@pytest.fixture(scope="module")
def notion_columns_fixture():
    return {
        "name": "Name",
        "date": "Date",
        "tags": "Tags",
        "description": "Description",
        "location": "Location",
        "last_updated_time": "Last Updated",
        "last_synced_time": "Last Synced",
        "gcal_event_id": "GCal event Id",
        "recurrent_event": "GCal Recurrence",
        "gcal_event_url": "GCal event url",
        "gcal_calendar_name": "Calendar",
        "gcal_calendar_id": "GCal calendar Id",
        "to_delete": "To Delete",
        "deleted": "Deleted",
        "read_only": "Read Only",
    }


@pytest.fixture(scope="module")
def config_dict_fixture(notion_columns_fixture):
    return {
        "default_event_length": 60,
        "no_date_action": "skip",
        "gcal_calendars": {"Default": "dude@gmail.com", "Calendar2": "abc123@group.calendar.google.com"},
        "gcal_default_calendar_name": "Default",
        "notion_columns": notion_columns_fixture,
        "notion_database_url": "https://www.notion.so/***?v=***&p=",
        "notion_token": "SECRET",
        "timezone_name": "Europe/Berlin",
    }


@pytest.fixture(scope="module")
def time_fixture():
    return Time("Europe/Berlin")


@pytest.fixture(scope="module")
def config_fixture(notion_columns_fixture, time_fixture):
    return Config(
        default_event_length=60,
        no_date_action="skip",
        gcal_calendars={"Default": "dude@gmail.com", "Calendar2": "abc123@group.calendar.google.com"},
        gcal_default_calendar_name="Default",
        notion_database_url="https://www.notion.so/***?v=***&p=",
        notion_token="SECRET",
        notion_columns=notion_columns_fixture,
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


@pytest.fixture(scope="module")
def events_dict(config_fixture):
    return [
        {
            "name": "test_time",
            "description": "",
            "location": "",
            "gcal_event_id": "abcdefg1234",
            "gcal_calendar_id": "gsuite.integration.test@gmail.com",
            "gcal_calendar_name": "Default",
            "time_start": datetime(2021, 11, 1, 7, 0, tzinfo=pytz.timezone("Europe/Berlin")),
            "time_end": datetime(2021, 11, 1, 8, 0, tzinfo=pytz.timezone("Europe/Berlin")),
            "recurrent_event": "",
            "time_last_updated": datetime(2021, 11, 1, 14, 2, tzinfo=pytz.timezone("Europe/Berlin")),
            "time_last_synced": "2021-11-01T13:59",
            "notion_page_url": "https://www.notion.so/test_time-123",
            "gcal_page_url": "https://www.google.com/calendar/event?eid=test_time-123",
            "read_only": False,
            "to_delete": False,
            "notion_id": "123-abc",
        },
        {
            "name": "test_all_day",
            "description": "",
            "location": "",
            "gcal_event_id": "xyz1234",
            "gcal_calendar_id": "gsuite.integration.test@gmail.com",
            "gcal_calendar_name": "Default",
            "time_start": date(2021, 11, 1),
            "time_end": date(2021, 11, 1),
            "recurrent_event": "",
            "time_last_updated": datetime(2021, 11, 1, 14, 2, tzinfo=pytz.timezone("Europe/Berlin")),
            "time_last_synced": "2021-11-01T13:59",
            "notion_page_url": "https://www.notion.so/test_all_day",
            "gcal_page_url": "https://www.google.com/calendar/event?eid=test_all_day-123",
            "read_only": False,
            "to_delete": False,
            "notion_id": "789-def",
        },
        {
            "name": "test_to_delete",
            "description": "",
            "location": "",
            "gcal_event_id": "bla1",
            "gcal_calendar_id": "gsuite.integration.test@gmail.com",
            "gcal_calendar_name": "Default",
            "time_start": date(2021, 11, 1),
            "time_end": date(2021, 11, 1),
            "recurrent_event": "",
            "time_last_updated": datetime(2021, 11, 1, 14, 2, tzinfo=pytz.timezone("Europe/Berlin")),
            "time_last_synced": "2021-11-01T13:59",
            "notion_page_url": "https://www.notion.so/test_to_delete",
            "gcal_page_url": "https://www.google.com/calendar/event?eid=test_to_delete",
            "read_only": False,
            "to_delete": False,
            "notion_id": "789-def",
        },
    ]
