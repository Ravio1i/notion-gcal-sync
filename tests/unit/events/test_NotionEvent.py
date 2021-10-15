from datetime import datetime, timezone, timedelta

import pytest

from events.NotionEvent import NotionEvent
from utils import Time


def test_get_name():
    column = "Name"
    properties = {
        "Name": {
            "title": [{
                "text": {
                    "content": "Title"
                }
            }]
        }
    }
    assert NotionEvent.get_name(properties, column) == "Title"


def test_get_name_invalid():
    column = "Name"
    properties = {}
    assert NotionEvent.get_name(properties, column) is None


def test_get_last_edited_time():
    column = "Last Edited Time"
    time = Time(timezone_name="Europe/Berlin", timezone_diff="+02:00")
    properties = {
        column: {
            "last_edited_time": "2021-10-01T11:37:00.000Z"
        }
    }
    expected = datetime(2021, 10, 1, 13, 37, tzinfo=timezone(timedelta(seconds=7200)))
    assert NotionEvent.get_last_edited_time(properties, column, time) == expected


@pytest.mark.parametrize(
    "test_start, test_end, expected",
    [("2021-10-01T11:37:00.000Z", None, ("2021-10-01T11:37:00.000Z", "2021-10-01T11:37:00.000Z")),
     ("2021-10-01T11:37:00.000Z", "2021-10-01T13:37:00.000Z", ("2021-10-01T11:37:00.000Z", "2021-10-01T13:37:00.000Z")),
     ("2021-10-01", None, ("2021-10-01", "2021-10-01"))])
def test_get_time(test_start, test_end, expected):
    column = "Date"
    properties = {
        column: {
            "date": {
                "start": test_start,
                "end": test_end
            }
        }
    }
    assert NotionEvent.get_time(properties, column) == expected


def test_get_time_invalid():
    column = "Date"
    properties = {}
    assert NotionEvent.get_time(properties, column) == (None, None)


def test_get_text():
    column = "Description"
    properties = {
        column: {
            "rich_text": [{
                "text": {
                    "content": "This is a text"
                }
            }]
        }
    }
    assert NotionEvent.get_text(properties, column) == "This is a text"


def test_get_text_invalid():
    column = "Description"
    properties = {}
    assert NotionEvent.get_text(properties, column) == ""


def test_get_url():
    column = "Url"
    properties = {
        column: {
            "url": "https://google.com"
        }
    }
    assert NotionEvent.get_url(properties, column) == "https://google.com"


def test_get_select():
    column = "Select"
    properties = {
        column: {
            "select": {
                "name": "Selection1"
            }
        }
    }
    assert NotionEvent.get_select(properties, column) == "Selection1"


def test_get_select_invalid():
    column = "Select"
    properties = {}
    assert NotionEvent.get_select(properties, column) == ""


def test_get_multiselect():
    column = "MultiSelect"
    properties = {
        column: {
            "multi_select": [{
                "name": "Selection1"
            }, {
                "name": "Selection2"
            }]
        }
    }
    assert NotionEvent.get_multiselect(properties, column) == ["Selection1", "Selection2"]


def test_get_multiselect_invalid():
    column = "MultiSelect"
    properties = {}
    assert NotionEvent.get_multiselect(properties, column) == []


@pytest.mark.parametrize("test_input, expected", [(False, False), (True, True)])
def test_get_checkbox(test_input, expected):
    column = "Checkbox"
    properties = {
        column: {
            "checkbox": test_input
        }
    }
    assert NotionEvent.get_checkbox(properties, column) == expected


def test_get_checkbox_invalid():
    column = "Checkbox"
    properties = {}
    assert not NotionEvent.get_checkbox(properties, column)

# def test_body():
    # NotionEvent("Name", "Test", "Heaven", "event_id", "calendar_name", "calendar_id", datetime(2021, 2, 1),
    #     datetime(2021, 2, 2), "",
    #             datetime(2021, 1, 1, 13, 37), "NSYNC", "https://notion.so", "https://google.com", "notion_id", False, )
    # test_body = {
    #     "properties": {
    #         self.cfg.col_name: {
    #             "title": [{
    #                 "text": {
    #                     "content": self.name
    #                 }
    #             }]
    #         },
    #         self.cfg.col_date: {
    #             "date": {
    #                 "start": time_start,
    #                 "end": time_end
    #             }
    #         },
    #         self.cfg.col_recurrent_event: {
    #             "rich_text": [{
    #                 "text": {
    #                     "content": self.recurrent_event
    #                 }
    #             }]
    #         },
    #         self.cfg.col_description: {
    #             "rich_text": [{
    #                 "text": {
    #                     "content": self.description
    #                 }
    #             }]
    #         },
    #         self.cfg.col_gcal_calendar_id: {
    #             "select": {
    #                 "name": self.gcal_calendar_id
    #             }
    #         },
    #         self.cfg.col_gcal_calendar_name: {
    #             "select": {
    #                 "name": self.gcal_calendar_name
    #             }
    #         },
    #         self.cfg.col_location: {
    #             "rich_text": [{
    #                 "text": {
    #                     "content": self.location
    #                 }
    #             }]
    #         },
    #         self.cfg.col_gcal_event_id: {
    #             "rich_text": [{
    #                 "text": {
    #                     "content": self.gcal_event_id
    #                 }
    #             }]
    #         },
    #         self.cfg.col_last_synced_time: {
    #             "rich_text": [{
    #                 "text": {
    #                     "content": self.cfg.time.now(),
    #                 }
    #             }]
    #         },
    #         self.cfg.col_gcal_event_url: {
    #             "url": self.gcal_page_url
    #         },
    #         self.cfg.col_read_only: {
    #             "checkbox": bool(self.read_only)
    #         }
    #     },
    # }
