from fixtures import *


@pytest.mark.parametrize(
    "test_url, expected",
    [
        ("https://www.notion.so/subdomain/THE_ID?v=asdfasdf123&p=", "THE_ID"),
        ("https://www.notion.so/THE_ID?v=asdfasdf123&p=", "THE_ID"),
        ("https://www.notion.so/THE_ID?v=asdfasdf123", "THE_ID"),
        ("https://www.notion.so/THE_ID?v=", None),
        ("https://www.notion.so/THE_ID", None),
        ("https://www.notion.so/THE_ID&p=", None),
        ("http://www.notion.so/THE_ID?v=asdfasdf123&p=", None),
        (None, None)
    ],
)
def test_database_id(time, notion_columns, test_url, expected):
    config = Config(60, "skip", {"Default": "dude@gmail.com"}, "Default", test_url, "SECRET", notion_columns, time)
    assert config.notion_database_id == expected


def test_default_event_length(config):
    config.default_event_length = "123"
    assert config.default_event_length == 60


@pytest.mark.parametrize(
    "test_action, expected", [("skip", "skip"), ("today", "today"), ("something_else", "skip")],
)
def test_no_date_action(config, test_action, expected):
    config.no_date_action = test_action
    assert config.no_date_action == expected


@pytest.mark.parametrize(
    "test_calendar_id, expected",
    [
        ("dude@gmail.com", "Default"),
        ("abc123@group.calendar.google.com", "Calendar2"),
        ("error@group.calendar.google.com", None),
        (None, None),
    ],
)
def test_get_calendar_name(config, test_calendar_id, expected):
    assert config.get_calendar_name(test_calendar_id) == expected


def test_notion_invalid_columns(notion_columns):
    del notion_columns["name"]
    with pytest.raises(ValueError):
        Config(notion_columns=notion_columns)


@pytest.mark.parametrize(
    "test_calendar_name, expected",
    [
        ("Default", "dude@gmail.com"),
        ("Calendar2", "abc123@group.calendar.google.com"),
        ("error@group.calendar.google.com", None),
        (None, None),
    ],
)
def test_get_calendar_id(config, test_calendar_name, expected):
    assert config.get_calendar_id(test_calendar_name) == expected


@pytest.mark.parametrize(
    "test_calendar_id, expected",
    [
        ("dude@gmail.com", True),
        ("abc123@group.calendar.google.com", True),
        ("error@group.calendar.google.com", False),
        (None, False),
    ],
)
def test_is_valid_calendar_id(config, test_calendar_id, expected):
    assert config.is_valid_calendar_id(test_calendar_id) == expected


@pytest.mark.parametrize(
    "test_calendar_name, expected",
    [("Default", True), ("Calendar2", True), ("error@group.calendar.google.com", False), (None, False),],
)
def test_is_valid_calendar_name(config, test_calendar_name, expected):
    assert config.is_valid_calendar_name(test_calendar_name) == expected


def test_to_dict(config, config_dict):
    assert config.to_dict() == config_dict
